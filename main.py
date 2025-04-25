import requests
import argparse
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASIC_URL = "https://api.coingecko.com/api/v3/"


headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
}

def parse_arguments():
    """
    Parse the arguments from the command line.
    """
    parser = argparse.ArgumentParser(
        description="""
        This script is used to parse the data from the CoinGecko API and save it to the CSV file or
        draw a dashboard for the data.
        """
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create parser for the "list" command
    list_parser = subparsers.add_parser("list", help="Show list of cryptocurrencies to possible parse.")
    list_parser.add_argument(
        "--update",
        "-u",
        action="store_true",
        help="Update the list of cryptocurrencies"
    )
    # Create parser for the "coin" command
    coin_parser = subparsers.add_parser("track", help="Track a specific cryptocurrency.")
    coin_parser.add_argument(
        "coin", 
        type=str, 
        nargs="+", 
        help="Name of the cryptocurrency to parse. for example: bitcoin, ethereum, solana"
    )
    coin_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default="data/crypto_data.csv",
        help="Path to the output CSV file"
    )
  
    
    
    return parser.parse_args()

def check_connection():
    """
    Check if the connection to the CoinGecko API is working.
    """
    response = requests.get(f"{BASIC_URL}/ping")
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("gecko_says") == "(V3) To the Moon!":
            return True
        else:
            return False
    else:
        return False

def get_list_of_coins(with_update: bool = False):
    """
    Get list of coins from the CoinGecko API and save it to the JSON file.
    If the file exists, it will be updated with the new data.
    If the file does not exist, it will be created.
    Args:
        with_update (bool, optional): If True, the list of coins will be updated. Defaults to False.

    Returns:
        Dict: List of coins
    """
    
    if with_update:
        response = requests.get(f"{BASIC_URL}/coins/list", headers=headers)
        response.raise_for_status()
        if not Path("data").exists():
            Path("data").mkdir(parents=True, exist_ok=True)
        
        with open("data/list_of_coins.json", "w") as f:
            json.dump(response.json(), f, indent=4)

        print(f"List of coins updated and saved to {Path('data/list_of_coins.json')}")
    else:
        if Path("data/list_of_coins.json").exists():
            with open("data/list_of_coins.json", "r") as f:
                data = json.load(f)
                prepared_data  = [f"[name->{coin['name']} ID->{coin['id']}] | " for coin in data]
                grouped_data = ["".join(prepared_data[i:i+4]) for i in range(0, len(prepared_data), 4)]
                return "\n".join(grouped_data)
        else:
            return []



def get_coin_data(coin_names: list[str]) -> list[dict]:
    """
    Get coin data from the CoinGecko API.

    Args:
        coin_names (list[str]): List of coin names

    Returns:
        Dict: Coin data
    """
    response = requests.get(
        f"{BASIC_URL}/simple/price",
        headers=headers,
        params={"ids": ",".join(coin_names), "vs_currencies": "usd", "include_last_updated_at": "true"})
    response.raise_for_status()
    data = response.json()
    result = []
    for coin in data:
        result.append({
            "name": coin,
            "usd": data[coin]["usd"],
            "date": datetime.fromtimestamp(data[coin]["last_updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
        })
    return result

def prepare_coin_data(coin_data: list[dict]):
    """
    Prepare coin data for the dashboard.

    Args:
        coin_data (dict): Coin data

    Returns:
        Dict: Prepared coin data
    """
    df = pd.DataFrame([{"name": coin["name"], "price": coin["usd"], "date": coin["date"]} for coin in coin_data])
    return df

def save_coin_data(coin_data: pd.DataFrame, output_path: Path = Path("data/crypto_data.csv")):
    """
    Save coin data to the CSV file.

    Args:
        coin_data (dict): Coin data
        output_path (Path): Path to the output CSV file
    """
    coin_data.to_csv(output_path, index=False)











if __name__ == "__main__":
    args = parse_arguments()
    if check_connection():
        if args.command == "list":
            print(get_list_of_coins(with_update=args.update))
        if args.command == "track":
            coin_data = get_coin_data(args.coin)
            coin_data_df = prepare_coin_data(coin_data)
            filepath = Path(args.output) if args.output else None
            save_coin_data(coin_data_df, filepath)
    else:
        print("Connection to the CoinGecko API is not working.")