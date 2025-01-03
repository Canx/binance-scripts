import httpx

tags_to_filter = ["Monitoring"]  # Specify desired tags

def get_products_by_tags(tags):
    """
    Fetch Binance products filtered by the specified tags.

    Args:
        tags (list): A list of tags to filter the products.

    Returns:
        list: A list of products matching the specified tags.
    """
    url = "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1"
    }
    try:
        with httpx.Client(headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

            if "data" not in data:
                print("The response does not contain the 'data' field.")
                return []

            filtered_products = [
                product for product in data["data"]
                if any(tag in product.get("tags", []) for tag in tags)
            ]

            return filtered_products
    except httpx.RequestError as e:
        print(f"Error connecting to Binance API: {e}")
        return []

# Script execution
def main():
    products = get_products_by_tags(tags_to_filter)

    if products:
        print(f"Found {len(products)} products matching the tags {tags_to_filter}:")
        for product in products:
            print(f"Symbol: {product['s']}, Name: {product['an']}, Tags: {product['tags']}")
    else:
        print("No products found matching the specified tags.")

if __name__ == "__main__":
    main()
