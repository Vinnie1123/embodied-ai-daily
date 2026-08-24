import arxiv
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import os
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
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
    
    def fetch_arxiv_papers(self, days_back=1) -> List[Dict]:
        """抓取 arXiv 最近的论文"""
        papers = []
        
        # 计算日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # 搜索 cs.RO (Robotics) 和 cs.AI 分类
        categories = ["cs.RO", "cs.AI", "cs.CV", "cs.LG"]
        
        for category in categories:
            search = arxiv.Search(
                query=f"cat:{category}",
                max_results=50,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for result in search.results():
                # 检查是否在日期范围内
                if result.published.replace(tzinfo=None) < start_date:
                    continue
                
                # 检查是否包含关键词
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
        
        # 去重并按发布时间排序
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
        """使用 LLM 生成简短摘要"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个技术摘要助手。用 1-2 句话（中文）概括论文/项目的核心贡献和创新点。语言简洁、专业。"
                    },
                    {
                        "role": "user",
                        "content": f"标题：{title}\n\n内容：{content[:1000]}"
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "摘要生成失败"
    
    def fetch_all(self) -> Dict:
        """获取所有内容"""
        print("Fetching arXiv papers...")
        papers = self.fetch_arxiv_papers()
        
        print("Fetching GitHub trending...")
        repos = self.fetch_github_trending()
        
        # 为论文生成摘要
        print("Generating summaries for papers...")
        for paper in papers[:10]:  # 只为前 10 篇生成摘要，节省 API 调用
            paper["ai_summary"] = self.generate_summary(
                paper["title"],
                paper["summary"]
            )
        
        # 为 GitHub 项目生成摘要
        print("Generating summaries for repos...")
        for repo in repos[:10]:
            repo["ai_summary"] = self.generate_summary(
                repo["name"],
                repo["description"]
            )
        
        return {
            "papers": papers,
            "repos": repos,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

if __name__ == "__main__":
    fetcher = ContentFetcher()
    data = fetcher.fetch_all()
    
    print(f"\n找到 {len(data['papers'])} 篇相关论文")
    print(f"找到 {len(data['repos'])} 个相关项目")
