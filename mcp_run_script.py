# test_arxiv_mcp.py
import requests
import json

def test_mcp_server():
    # Test red-team search
    response = requests.post(
        "http://localhost:5001/tools/search_redteam_papers",
        json={"query": "", "max_results": 3}
    )

    if response.status_code == 200:
        response_data = json.loads(response.text)
        paper_content = response_data['content'][0]['text']
        papers = json.loads(paper_content)
        print(f"Found {len(papers)} red-team papers")
        for paper in papers:
            print(f"- {paper['title']} ({paper['year']})")
            print(f"  Authors: {', '.join(paper['authors'])}")
            print(f"  URL: {paper['url']}")
            print()

if __name__ == "__main__":
    test_mcp_server()