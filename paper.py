# arxiv_mcp_server.py
import arxiv
from python_a2a.mcp import FastMCP, text_response
from typing import List, Dict, Any
from datetime import datetime
import json

# Initialize MCP server
mcp_server = FastMCP(
    name="ArXiv Research Tools",
    description="Tools for searching ArXiv papers on Agentic AI security topics"
)

# TODO: Define your paper data structure as a Python dataclass or dict
# Hint: Include the fields you decided on above
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

    def to_dict(self) -> Dict[str, Any]:
            return {
                'title': self.title,
                'year': self.year,
                'conference': self.conference,
                'abstract': self.abstract,
                'authors': self.authors,
                'url': self.url,
                'pdf_url': self.pdf_url,
                'categories': self.categories,
                'tags': self.tags,
                'keywords': self.keywords
            }

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

    base_terms = ["red team", "adversarial attack", "agent security", "agentic ai", "agentic ai security", "agentic ai red team", "agentic ai adversarial attack"]

    search_query = " OR ".join([f'"{term}"' for term in base_terms])
    if query:
        search_query += f" AND ({query})"

    try:
        # TODO: Use arxiv.Search to query papers
        # Hint: search = arxiv.Search(query=search_query, max_results=max_results)
        search = arxiv.Search(query=search_query, max_results=max_results)

        papers = []
        # TODO: Process search results and convert to Paper objects
        # Hint: Loop through search.results() and extract relevant fields
        for result in search.results():
            paper = Paper(
                title=result.title,
                year=result.published.year,
                conference=result.journal_ref,
                abstract=result.summary,
                authors=result.authors,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                categories=result.categories,
                tags=result.tags,
                keywords=result.keywords
            )
        return text_response(json.dumps([paper.to_dict() for paper in papers], indent=2))

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
    # TODO: Implement this - similar to search_redteam_papers
    # But with defense-focused terms like "safety", "alignment", "robustness"
    base_terms = ["safety", "alignment", 'agentic ai defense',"Agentic AI Security","robustness", "agentic ai", "agentic ai safety", "agentic ai alignment", "agentic ai robustness"]

    search_query = " OR ".join([f'"{term}"' for term in base_terms])
    if query:
        search_query += f" AND ({query})"

    try:
        search = arxiv.Search(query=search_query, max_results=max_results)
        papers = []
        for result in search.results():
            paper = Paper(
                title=result.title,
                year=result.published.year,
                conference=result.journal_ref,
                abstract=result.summary,
                authors=result.authors,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                categories=result.categories,
                tags=result.tags,
                keywords=result.keywords
            )
            papers.append(paper)
        return text_response(json.dumps([paper.to_dict() for paper in papers], indent=2))

    except Exception as e:
        return text_response(f"Error searching ArXiv: {str(e)}")

# TODO: Add a tool for searching benchmark papers
# @mcp_server.tool(name="search_benchmark_papers", ...)
@mcp_server.tool(name="search_benchmark_papers", description="Search ArXiv for benchmark papers on Agentic AI")
def search_benchmark_papers(query: str = "", max_results: int = 10):
    """
    Search for benchmark papers related to Agentic AI
    """
    base_terms = ["Agentic AI benchmark", "Agentic AI benchmarking", "Agentic AI evaluation", "Agentic AI evaluation metrics", "Agentic AI evaluation methods",
                "Agentic AI evaluation datasets", "Agentic AI evaluation frameworks", "Agentic AI evaluation tools", "Agentic AI evaluation benchmarks",
                "Agentic AI evaluation tools", "Agentic AI evaluation benchmarks", "Agentic AI evaluation datasets",
                "Agentic AI evaluation frameworks", "Agentic AI evaluation tools", "Agentic AI evaluation benchmarks",
                "Agentic AI evaluation datasets", "Agentic AI evaluation frameworks", "Agentic AI evaluation tools",]

    search_query = " OR ".join([f'"{term}"' for term in base_terms])
    if query:
        search_query += f" AND ({query})"

    try:
        search = arxiv.Search(query=search_query, max_results=max_results)

        papers = []
        for result in search.results():
            paper = Paper(
                title=result.title,
                year=result.published.year,
                conference=result.journal_ref,
                abstract=result.summary,
                authors=result.authors,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                categories=result.categories,
                tags=result.tags,
                keywords=result.keywords
            )
            papers.append(paper)
        return text_response(json.dumps([paper.to_dict() for paper in papers], indent=2))

    except Exception as e:
        return text_response(f"Error searching ArXiv: {str(e)}")

if __name__ == "__main__":
    print("Starting ArXiv MCP Server...")
    print("Available tools:")
    print("- search_redteam_papers")
    print("- search_defense_papers")
    print("- search_benchmark_papers")
    # Run the server
    mcp_server.run(host="0.0.0.0", port=5001)