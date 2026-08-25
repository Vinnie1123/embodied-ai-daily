import arxiv
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import os
import time
from openai import OpenAI

# 关键词配置
KEYWORDS = [
    "embodied",
    "world model",
    "robot manipulation",
    "llm robot",
    "sim2real",
    "edge deployment",
    "quantization",
    "ros",
    "vision-language model",
    "visual language"
]

class ContentFetcher:
    def __init__(self):
        self.base_url = os.getenv("OPENAI_BASE_URL") or "https://api.deepseek.com/v1"
        default_model = "deepseek-chat" if "deepseek.com" in self.base_url else "gpt-4o-mini"
        self.model = os.getenv("OPENAI_MODEL") or default_model
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=self.base_url
        )
        self.arxiv_client = arxiv.Client(
            page_size=20,
            delay_seconds=3,
            num_retries=1
        )
    
    def fetch_arxiv_papers(self, days_back=1) -> List[Dict]:
        """抓取 arXiv 最近的论文，遇到限流时降级而不中断整次任务。"""
        papers = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        categories = ["cs.RO", "cs.AI", "cs.CV", "cs.LG"]

        for category in categories:
            search = arxiv.Search(
                query=f"cat:{category}",
                max_results=20,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            try:
                for result in self.arxiv_client.results(search):
                    if result.published.replace(tzinfo=None) < start_date:
                        continue

                    text = f"{result.title} {result.summary}".lower()
                    matched_keywords = [kw for kw in KEYWORDS if kw.lower() in text]

                    if matched_keywords:
                        papers.append({
                            "title": result.title,
                            "authors": [author.name for author in result.authors][:3],
                            "summary": result.summary[:500],
                            "url": result.entry_id,
                            "published": result.published.strftime("%Y-%m-%d"),
                            "keywords": matched_keywords,
                            "category": category
                        })
            except Exception as e:
                print(f"Warning: arXiv {category} fetch failed: {e}")
            finally:
                time.sleep(3)

        unique_papers = {p["url"]: p for p in papers}.values()
        return sorted(unique_papers, key=lambda x: x["published"], reverse=True)
    
    def fetch_github_trending(self) -> List[Dict]:
        """抓取 GitHub Trending 项目"""
        repos = []
        
        try:
            # 使用 GitHub Trending API
            topics = ["robotics", "embodied-ai", "llm", "computer-vision"]
            
            for topic in topics:
                url = f"https://api.github.com/search/repositories"
                params = {
                    "q": f"topic:{topic} created:>={(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 10
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get("items", []):
                        # 检查关键词
                        text = f"{item['name']} {item['description'] or ''}".lower()
                        matched_keywords = [kw for kw in KEYWORDS if kw.lower() in text]
                        
                        if matched_keywords or topic in ["robotics", "embodied-ai"]:
                            repos.append({
                                "name": item["name"],
                                "full_name": item["full_name"],
                                "description": item["description"] or "No description",
                                "url": item["html_url"],
                                "stars": item["stargazers_count"],
                                "language": item["language"] or "Unknown",
                                "keywords": matched_keywords
                            })
        
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
        
        # 去重并按 stars 排序
        unique_repos = {r["url"]: r for r in repos}.values()
        return sorted(unique_repos, key=lambda x: x["stars"], reverse=True)[:15]
    
    def generate_summary(self, title: str, content: str) -> str:
        """生成能帮助读者理解和判断价值的中文技术解读。"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "你是具身智能研究员和工程师。请用中文写一段 180-260 字的技术解读，"
                            "严格包含四部分：解决的问题、核心方法、主要价值、对具身智能实践的启发。"
                            "不要复述标题，不要编造论文中没有的信息，语言具体、易懂。"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"标题：{title}\n\n原始内容：{content[:1800]}"
                    }
                ],
                max_tokens=420,
                temperature=0.25
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary with model {self.model}: {e}")
            return "原始内容可供参考，但 AI 解读暂时生成失败。"

    def generate_overview(self, selected: List[Dict]) -> str:
        """根据精选内容生成当天的趋势总览。"""
        digest = "\n".join(
            f"- {item.get('title', item.get('full_name', item.get('name', '')))}: "
            f"{item.get('summary', item.get('description', ''))[:500]}"
            for item in selected
        )
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是具身智能领域编辑。用中文写 3-5 句话总结今天精选资讯的共同趋势、技术重点和读者应该关注的方向，必须基于给定内容，不要泛泛而谈。"
                    },
                    {"role": "user", "content": digest}
                ],
                max_tokens=300,
                temperature=0.25
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating overview with model {self.model}: {e}")
            return "今天的精选内容覆盖具身智能、机器人学习与相关工程工具，建议优先阅读标记为重点推荐的条目。"

    def rank_items(self, papers: List[Dict], repos: List[Dict]) -> List[Dict]:
        """按相关性和实用价值合并筛选每日精选内容。"""
        for paper in papers:
            paper["content_type"] = "论文"
            paper["score"] = len(paper.get("keywords", [])) * 10 + (5 if paper["category"] == "cs.RO" else 0)
        for repo in repos:
            repo["content_type"] = "项目"
            repo["score"] = len(repo.get("keywords", [])) * 10 + min(repo.get("stars", 0) / 1000, 10)

        combined = papers + repos
        combined.sort(key=lambda item: (item["score"], item.get("published", ""), item.get("stars", 0)), reverse=True)
        return combined[:10]

    def fetch_all(self) -> Dict:
        """获取并生成每日十条精选内容。"""
        print("Fetching arXiv papers...")
        papers = self.fetch_arxiv_papers()

        print("Fetching GitHub trending...")
        repos = self.fetch_github_trending()

        selected = self.rank_items(papers, repos)
        selected_papers = [item for item in selected if item["content_type"] == "论文"]
        selected_repos = [item for item in selected if item["content_type"] == "项目"]

        print(f"Selected {len(selected)} high-value items")
        print("Generating detailed summaries...")
        for item in selected:
            item["ai_summary"] = self.generate_summary(
                item.get("title", item.get("name", "")),
                item.get("summary", item.get("description", ""))
            )

        print("Generating daily overview...")
        overview = self.generate_overview(selected)
        for index, item in enumerate(selected[:3]):
            item["is_recommended"] = True
            item["recommendation_reason"] = "优先推荐：与今日主题高度相关，且兼具研究价值或实践参考价值。"

        return {
            "papers": selected_papers,
            "repos": selected_repos,
            "selected": selected,
            "overview": overview,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

if __name__ == "__main__":
    fetcher = ContentFetcher()
    data = fetcher.fetch_all()
    
    print(f"\n找到 {len(data['papers'])} 篇相关论文")
    print(f"找到 {len(data['repos'])} 个相关项目")
