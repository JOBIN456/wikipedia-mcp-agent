import requests


HEADERS = {
    "User-Agent": "WikipediaMCPAgent/1.0 (pythonpopit@gmail.com)"
}


def search_wikipedia(query: str):

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

    return response.json()


def get_wikipedia_page(title: str):

    url = f"https://en.wikipedia.org/w/rest.php/v1/page/{title}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    response.raise_for_status()
    
    return response.json()


# Test search
results = search_wikipedia("Virat Kohli")

for page in results["pages"]:
    print("Title:", page["title"])
    print("Description:", page.get("description"))
    print("Key:", page["key"])
    print("-" * 50)