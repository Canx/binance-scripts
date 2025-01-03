import httpx
from datetime import datetime
import urllib.parse

# URL del nuevo endpoint con más artículos
url = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1&pageNo=1&pageSize=50&catalogId=161"

async def fetch_articles():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("data", {}).get("catalogs", [])[0].get("articles", [])
            else:
                print("Error en la respuesta de la API:", data.get("message"))
        else:
            print(f"Error al acceder a la API: {response.status_code}")
    return []

def parse_articles(articles):
    parsed = []
    for article in articles:
        title = article.get("title", "No Title")
        release_date = article.get("releaseDate", 0)
        formatted_date = datetime.fromtimestamp(release_date / 1000).strftime('%Y-%m-%d %H:%M:%S')
        parsed.append({"title": title, "release_date": formatted_date, "code": article.get("code")})
    return parsed

def generate_article_url(base_url, article):
    # Base URL fija
    base_url = "https://www.binance.com/en/support/announcement/"

    # Formatear el título reemplazando espacios por guiones y codificando caracteres especiales
    formatted_title = article["title"].replace(" ", "-").lower()
    formatted_title = urllib.parse.quote_plus(formatted_title).replace("+", "-")

    # Construir la URL final con el título formateado y el código
    article_url = f"{base_url}{formatted_title}-{article['code']}"
    return article_url

async def main():
    print("Fetching articles...")
    articles = await fetch_articles()
    parsed_articles = parse_articles(articles)

    if parsed_articles:
        print("\nLatest Articles:")
        for article in parsed_articles:
            url = generate_article_url("https://www.binance.com/en/support/announcement/", article)
            print(f"- {article['title']} (Release Date: {article['release_date']})")
            print(f"  URL: {url}")
    else:
        print("No articles found.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
