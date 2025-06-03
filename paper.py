# Fixed version of your ArXiv MCP server
import arxiv
from python_a2a.mcp import FastMCP, text_response
from typing import List, Dict, Any
from datetime import datetime
import json

# Init MCP server
mcp_server = FastMCP(
    name="ArXiv Research Tools",
    description="Tools for searching ArXiv papers on Agentic AI security topics"
)

class Paper:
    def __init__(self, title: str, year: int, conference: str = None, **kwargs):
        self.title = title
        self.year = year
        self.conference = conference
        self.abstract = kwargs.get('abstract', '')
        self.authors = kwargs.get('authors', [])
        self.url = kwargs.get('url', '')
        self.pdf_url = kwargs.get('pdf_url', '')
        self.categories = kwargs.get('categories', [])
        self.tags = kwargs.get('tags', [])
        self.keywords = kwargs.get('keywords', [])
        self.arxiv_id = kwargs.get('arxiv_id', '')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'year': self.year,
            'conference': self.conference,
            'abstract': self.abstract,
            'authors': [str(author) for author in self.authors],
            'url': self.url,
            'pdf_url': self.pdf_url,
            'categories': self.categories,
            'tags': self.tags,
            'keywords': self.keywords,
            'arxiv_id': self.arxiv_id
        }

def extract_paper_from_result(result) -> Paper:
    """Helper function to extract Paper object from ArXiv result"""
    return Paper(
        title=result.title.strip(),
        year=result.published.year,
        conference=result.journal_ref if result.journal_ref else "ArXiv Preprint",
        abstract=result.summary.strip(),
        authors=[str(author) for author in result.authors],
        url=result.entry_id,
        pdf_url=result.pdf_url,
        categories=result.categories,
        tags=["red-team"],
        keywords=[],
        arxiv_id=result.entry_id.split('/')[-1]
    )

@mcp_server.tool(
    name="search_redteam_papers",
    description="Search ArXiv for red-teaming papers on Agentic AI"
)
def search_redteam_papers(query: str = "", max_results: int = 10):
    """
    Search for red-teaming papers related to Agentic AI
    Args:
        query: Additional search terms (optional)
        max_results: Maximum number of papers to return
    """
    base_terms = [
        "red team", "adversarial attack", "agent security",
        "agentic ai security", "adversarial agents",
        "agent vulnerability", "llm attack"
    ]

    search_query = " OR ".join([f'"{term}"' for term in base_terms])
    if query:
        search_query += f" AND ({query})"

    try:
        search = arxiv.Search(query=search_query, max_results=max_results)
        papers = []

        for result in search.results():
            paper = extract_paper_from_result(result)
            paper.tags = ["red-team"]
            papers.append(paper)

        # Convert papers to dicts and return as JSON string
        paper_dicts = [paper.to_dict() for paper in papers]
        return text_response(json.dumps(paper_dicts))

    except Exception as e:
        return text_response(f"Error searching ArXiv: {str(e)}")

@mcp_server.tool(
    name="search_defense_papers",
    description="Search ArXiv for defense/safety papers on Agentic AI"
)
def search_defense_papers(query: str = "", max_results: int = 10):
    """
    Search for defense and safety papers related to Agentic AI
    """
    base_terms = [
        "ai safety", "agent alignment", "agentic ai defense",
        "agent robustness", "llm safety", "agent security defense",
        "ai alignment", "safe agents"
    ]

    search_query = " OR ".join([f'"{term}"' for term in base_terms])
    if query:
        search_query += f" AND ({query})"

    try:
        search = arxiv.Search(query=search_query, max_results=max_results)
        papers = []

        for result in search.results():
            paper = extract_paper_from_result(result)
            paper.tags = ["defense"]
            papers.append(paper)

        # Convert papers to dicts and return as JSON string
        paper_dicts = [paper.to_dict() for paper in papers]
        return text_response(json.dumps(paper_dicts))

    except Exception as e:
        return text_response(f"Error searching ArXiv: {str(e)}")

@mcp_server.tool(
    name="search_benchmark_papers",
    description="Search ArXiv for benchmark papers on Agentic AI"
)
def search_benchmark_papers(query: str = "", max_results: int = 10):
    """
    Search for benchmark papers related to Agentic AI
    """
    base_terms = [
        "agentic ai benchmark", "agent evaluation", "llm benchmark",
        "agent performance metrics", "ai agent testing",
        "multi-agent evaluation", "agent capability assessment"
    ]

    search_query = " OR ".join([f'"{term}"' for term in base_terms])
    if query:
        search_query += f" AND ({query})"

    try:
        search = arxiv.Search(query=search_query, max_results=max_results)
        papers = []

        for result in search.results():
            paper = extract_paper_from_result(result)
            paper.tags = ["benchmark"]
            papers.append(paper)

        # Convert papers to dicts and return as JSON string
        paper_dicts = [paper.to_dict() for paper in papers]
        return text_response(json.dumps(paper_dicts))

    except Exception as e:
        return text_response(f"Error searching ArXiv: {str(e)}")

if __name__ == "__main__":
    print("Starting ArXiv MCP Server...")
    print("Available tools:")
    print("- search_redteam_papers")
    print("- search_defense_papers")
    print("- search_benchmark_papers")

    #Server run
    mcp_server.run(host="0.0.0.0", port=5001)