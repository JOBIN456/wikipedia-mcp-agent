from fastmcp import FastMCP
import requests

mcp = FastMCP("Wikipedia Server")

HEADERS = {
    "User-Agent": "WikipediaMCPAgent/1.0 (pythonpopit@gmail.com)"
}

@mcp.tool
def search_wikipedia(query: str):
    """Search Wikipedia for a topic."""

    url = "https://en.wikipedia.org/w/rest.php/v1/search/page"

    params = {
        "q": query,
        "limit": 5
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for page in data.get("pages", []):
        results.append({
            "title": page.get("title"),
            "description": page.get("description")
        })

    return results



@mcp.tool
def get_wikipedia_page(title: str):
    """Get the content of a Wikipedia page."""

    url = f"https://en.wikipedia.org/w/rest.php/v1/page/{title}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    response.raise_for_status()


    data = response.json()

    return data.get("source", "")[:1000]


if __name__ == "__main__":
    mcp.run(transport="stdio")