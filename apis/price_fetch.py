# price_fetcher.py
"""
Since ByMykel's API doesn't include prices, we'll need to either:
1. Use Steam Community Market API (free but rate-limited)
2. Scrape from CSGOFloat, CSGOStash, or similar sites
3. Use your static dataset for predictions

For now, we'll use Steam Community Market API
"""

import requests
import time
from urllib.parse import quote


class SteamMarketPriceFetcher:
    """
    Fetch current prices from Steam Community Market
    FREE but rate-limited - use sparingly!
    """

    def __init__(self):
        self.base_url = "https://steamcommunity.com/market/priceoverview/"
        self.app_id = 730  # CS2 App ID
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 2  # Seconds between requests (be nice to Steam)

    def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def get_price(self, market_hash_name, currency=1):
        """
        Get current price from Steam Market

        Args:
            market_hash_name: Full item name (e.g., "AK-47 | Redline (Field-Tested)")
            currency: Currency code (1=USD, 3=EUR, etc.)

        Returns:
            dict with price info or None
        """
        self._rate_limit()

        params = {
            "appid": self.app_id,
            "currency": currency,
            "market_hash_name": market_hash_name,
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get("success"):
                    return {
                        "market_hash_name": market_hash_name,
                        "lowest_price": self._parse_price(data.get("lowest_price")),
                        "median_price": self._parse_price(data.get("median_price")),
                        "volume": data.get("volume"),
                        "success": True,
                    }

            return {
                "market_hash_name": market_hash_name,
                "success": False,
                "error": f"HTTP {response.status_code}",
            }

        except Exception as e:
            print(f"Error fetching price: {e}")
            return {
                "market_hash_name": market_hash_name,
                "success": False,
                "error": str(e),
            }

    def _parse_price(self, price_string):
        """
        Parse Steam price string to float

        Args:
            price_string: e.g., "$12.34" or "€10,50"

        Returns:
            float price or None
        """
        if not price_string:
            return None

        try:
            # Remove currency symbols and convert
            cleaned = price_string.replace("$", "").replace("€", "").replace("£", "")
            cleaned = cleaned.replace(",", ".")  # Handle European format
            cleaned = cleaned.strip()
            return float(cleaned)
        except ValueError:
            return None


# Example usage
if __name__ == "__main__":
    fetcher = SteamMarketPriceFetcher()

    # Test with a common skin
    price_data = fetcher.get_price("AK-47 | Redline (Field-Tested)")

    if price_data and price_data.get("success"):
        print(f"Item: {price_data['market_hash_name']}")
        print(f"Lowest Price: ${price_data['lowest_price']:.2f}")
        print(f"Median Price: ${price_data['median_price']:.2f}")
        print(f"Volume: {price_data['volume']}")
    else:
        print(f"Failed to fetch price: {price_data.get('error')}")
