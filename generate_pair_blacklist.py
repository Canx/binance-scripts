import httpx
import json
import argparse
import re
from binance_product_filter import get_products_by_tags

def load_blacklist(file_path):
    """
    Load the current blacklist from a file, removing any comments.

    Args:
        file_path (str): Path to the blacklist file.

    Returns:
        dict: The current blacklist structure.
    """
    try:
        with open(file_path, "r") as file:
            content = file.read()
            # Remove comments starting with //
            content = re.sub(r"//.*", "", content)
            return json.loads(content)
    except FileNotFoundError:
        return {"exchange": {"pair_blacklist": []}}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {file_path}: {e}")
        return {"exchange": {"pair_blacklist": []}}

def generate_pair_blacklist(tag, current_blacklist_path, output_file_path=None):
    """
    Generate a new JSON file with the Freqtrade pair_blacklist structure, 
    extending the current blacklist with coins filtered by the specified tag.

    Args:
        tag (str): The tag to filter coins by.
        current_blacklist_path (str): Path to the current blacklist JSON file.
        output_file_path (str): Path to save the new pair_blacklist JSON file. Defaults to `blacklist_<tag>.json`.
    """
    # Load the current blacklist
    current_blacklist = load_blacklist(current_blacklist_path)
    current_pairs = list(current_blacklist.get("exchange", {}).get("pair_blacklist", []))

    # Get new pairs based on the tag
    products = get_products_by_tags([tag])
    new_pairs = [product['s'] for product in products if product['s'] not in current_pairs]

    # Add new pairs to the end of the list
    updated_pairs = current_pairs + new_pairs

    # Create the updated blacklist structure
    updated_blacklist = {
        "exchange": {
            "pair_blacklist": updated_pairs
        }
    }

    # Determine output file path
    if output_file_path is None:
        output_file_path = f"blacklist_{tag}.json"

    # Save the updated blacklist
    try:
        with open(output_file_path, "w") as file:
            json.dump(updated_blacklist, file, indent=4)
        print(f"Updated pair blacklist saved to {output_file_path}")
    except IOError as e:
        print(f"Error saving updated pair blacklist: {e}")

# Script execution
def main():
    parser = argparse.ArgumentParser(description="Generate a Freqtrade pair blacklist based on a specified tag.")
    parser.add_argument("tag", type=str, help="The tag to filter coins by.")
    parser.add_argument("--current", type=str, default="current_blacklist.json", help="Path to the current blacklist JSON file.")
    parser.add_argument("--output", type=str, help="Path to save the new pair_blacklist JSON file. Defaults to `blacklist_<tag>.json`.")

    args = parser.parse_args()

    generate_pair_blacklist(args.tag, args.current, args.output)

if __name__ == "__main__":
    main()