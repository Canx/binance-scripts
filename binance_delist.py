from playwright.async_api import async_playwright
from datetime import datetime
import urllib.parse
import asyncio
import aiohttp
import re

# URL del nuevo endpoint con más artículos
url = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1&pageNo=1&pageSize=50&catalogId=161"


def detect_delist_tokens(content, title):
    """
    Detecta si un artículo trata sobre un delist de spot y extrae los tokens sin duplicados.
    Verifica que no mencione "margin" en el título.

    Args:
        content (str): El contenido completo del artículo.
        title (str): El título del artículo.

    Returns:
        dict: Diccionario con información sobre si es un delist de spot y los tokens detectados.
    """
    # Detectar si el título menciona "margin"
    is_margin_mentioned = "margin" in title.lower()

    # Detectar si el artículo menciona "spot"
    is_spot_delist = "spot" in content.lower() and not is_margin_mentioned
    
    # Buscar líneas que contengan pares de tokens (e.g., NOT/BNB, RDNT/BTC)
    token_pattern = r"\b[A-Z0-9]+/[A-Z0-9]+\b"
    tokens = re.findall(token_pattern, content)

    # Eliminar duplicados convirtiendo a un conjunto y luego a una lista
    unique_tokens = list(set(tokens))

    return {
        "is_spot_delist": is_spot_delist,
        "tokens": unique_tokens
    }

async def fetch_articles():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("success"):
                    return data.get("data", {}).get("catalogs", [])[0].get("articles", [])
                else:
                    print("Error en la respuesta de la API:", data.get("message"))
            else:
                print(f"Error al acceder a la API: {response.status}")
    return []

async def fetch_article_content_from_url(article_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Cambiar a True para ejecución en segundo plano
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            accept_downloads=False,
            ignore_https_errors=False,
            java_script_enabled=True,
        )
        page = await context.new_page()
        try:
            #print(f"Accediendo a la URL del artículo: {article_url}")  # Depuración
            await page.goto(article_url, wait_until="domcontentloaded", timeout=60000)  # Asegurar que la página carga completamente
            await asyncio.sleep(5)  # Esperar un poco para contenido dinámico
            
            # Guardar el HTML completo para inspección
            html_content = await page.content()
            #with open("debug_page.html", "w", encoding="utf-8") as file:
            #    file.write(html_content)
            #print("HTML completo guardado en 'debug_page.html'. Verifica la estructura.")

            # Extraer el título del elemento <h1>
            h1_element = await page.query_selector("h1")
            title = await h1_element.text_content() if h1_element else "No Title Found"

            # Extraer el contenido del artículo desde el <div id="support_article">
            content_element = await page.query_selector("#support_article")
            content = await content_element.inner_text() if content_element else "No Content Found"

            return title.strip(), content.strip()
        except Exception as e:
            print(f"Error al cargar la página: {e}")
        finally:
            #print("Cerrando el navegador automáticamente después de inspeccionar.")
            #await asyncio.sleep(5)  # Esperar unos segundos antes de cerrar el navegador
            await browser.close()

    return "No Title Found", "No Content Found"


def extract_text_from_body(body_content):
    text = ""
    for node in body_content.get("child", []):
        if node.get("node") == "element" and node.get("tag") in ["p", "li"]:
            text += extract_text_from_body(node) + "\n"
        elif node.get("node") == "text":
            text += node.get("text", "")
    return text.strip()

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
            print(f"Procesando artículo: {article['title']}")
            
            # Obtener el contenido del artículo
            title, content = await fetch_article_content_from_url(url)
            delist_info = detect_delist_tokens(content, title)

            # Mostrar resultados
            #print(f"- Título: {title}")
            #print(f"- Fecha de publicación: {article['release_date']}")
            #print(f"- URL: {url}")
            #print(f"- Contenido detectado: {'Delist de Spot detectado' if delist_info['is_spot_delist'] else 'No es un Delist de Spot'}")
            if delist_info['tokens']:
                print(f"  Tokens detectados: {', '.join(delist_info['tokens'])}")
            else:
                print("  No se detectaron tokens relacionados.\n")
    else:
        print("No articles found.")


if __name__ == "__main__":
    asyncio.run(main())


