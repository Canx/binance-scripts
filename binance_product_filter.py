import httpx
import argparse

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
    
def get_all_tags():
    """
    Fetch all unique tags from Binance products.

    Returns:
        set: A set of unique tags.
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
                return set()

            # Extract unique tags
            tags = set()
            for product in data["data"]:
                tags.update(product.get("tags", []))

            return tags
    except httpx.RequestError as e:
        print(f"Error connecting to Binance API: {e}")
        return set()


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

def get_all_tags():
    """
    Fetch all unique tags from Binance products.

    Returns:
        set: A set of unique tags.
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
                return set()

            # Extract unique tags
            tags = set()
            for product in data["data"]:
                tags.update(product.get("tags", []))

            return tags
    except httpx.RequestError as e:
        print(f"Error connecting to Binance API: {e}")
        return set()

def main():
    parser = argparse.ArgumentParser(description="Binance Product Utility")
    parser.add_argument("--list-tags", action="store_true", help="List all available tags from Binance.")
    parser.add_argument("--filter", type=str, help="Filter products by a specific tag.")

    args = parser.parse_args()

    if args.list_tags:
        tags = get_all_tags()
        if tags:
            print("Available tags:")
            for tag in sorted(tags):
                print(tag)
        else:
            print("No tags found.")

    elif args.filter:
        tag = args.filter
        products = get_products_by_tags([tag])
        if products:
            print(f"Found {len(products)} products matching the tag '{tag}':")
            for product in products:
                print(f"Symbol: {product['s']}, Name: {product['an']}, Tags: {product['tags']}")
        else:
            print(f"No products found matching the tag '{tag}'.")
    else:
        print("No action specified. Use --help for available options.")

if __name__ == "__main__":
    main()
