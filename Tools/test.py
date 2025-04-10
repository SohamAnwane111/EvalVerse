import requests
from bs4 import BeautifulSoup

SERPER_API_KEY = ""

def web_summary(query, num_results=2, max_summary_len=3):
    """
    Perform web search and extract clean, focused technical summaries.

    Args:
        query (str): Search query.
        num_results (int): Number of search results to scrape.
        max_summary_len (int): Max paragraphs to return from best result.

    Returns:
        str: Ranked summary from scraped data.
    """
    try:
        # Search via Serper
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={"q": query}
        )
        response.raise_for_status()
        results = response.json().get("organic", [])[:num_results]
        
        final_output = []

        for result in results:
            url = result.get("link")
            if not url:
                continue
            
            page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")

            # Remove fluff
            for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
                tag.decompose()

            paragraphs = [p.get_text().strip() for p in soup.find_all("p")]
            paragraphs = [p for p in paragraphs if 50 < len(p) < 500]

            # Relevance scoring
            q_words = query.lower().split()
            scored = sorted(paragraphs, key=lambda p: sum(word in p.lower() for word in q_words), reverse=True)

            top_summary = "\n".join(scored[:max_summary_len])
            final_output.append(f"🔗 {url}\n📌 Summary:\n{top_summary}")

        return "\n\n".join(final_output) if final_output else "❌ No relevant content found."

    except Exception as e:
        return f"❌ Error: {e}"


if __name__ == "__main__":
    query = "how does react work with sql database"
    print(web_summary(query, num_results=1, max_summary_len=3))