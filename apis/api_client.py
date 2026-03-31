# api_client.py (COMPLETELY REWRITTEN for ByMykel/CSGO-API)
import requests
import pandas as pd
from datetime import datetime
import time


class CSGOAPIClient:
    def __init__(self, language="en"):
        """
        Initialize the API client
        """
        self.base_url = (
            "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api"
        )
        self.language = language
        self.cache = {}

    def _fetch_json(self, endpoint):
        """Fetch JSON data from the API with caching"""
        cache_key = f"{self.language}_{endpoint}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.base_url}/{self.language}/{endpoint}.json"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            self.cache[cache_key] = data
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def get_all_skins(self):
        """
        Get all skins (grouped by skin, includes all wears)

        Returns:
            List of skin objects
        """
        return self._fetch_json("skins")

    def get_all_skins_not_grouped(self):
        """
        Get all skins not grouped (each wear/stattrak combination is separate)
        This is the most useful for price lookups!

        Returns:
            DataFrame with individual skin variations
        """
        data = self._fetch_json("skins_not_grouped")

        if data:
            records = []
            for item in data:
                records.append(
                    {
                        "id": item.get("id"),
                        "skin_id": item.get("skin_id"),
                        "name": item.get("name"),
                        "market_hash_name": item.get("market_hash_name"),
                        "weapon": item.get("weapon", {}).get("name"),
                        "weapon_id": item.get("weapon", {}).get("weapon_id"),
                        "category": item.get("category", {}).get("name"),
                        "pattern": item.get("pattern", {}).get("name"),
                        "wear": item.get("wear", {}).get("name"),
                        "rarity": item.get("rarity", {}).get("name"),
                        "rarity_color": item.get("rarity", {}).get("color"),
                        "stattrak": item.get("stattrak", False),
                        "souvenir": item.get("souvenir", False),
                        "min_float": item.get("min_float"),
                        "max_float": item.get("max_float"),
                        "paint_index": item.get("paint_index"),
                        "image": item.get("image"),
                    }
                )

            return pd.DataFrame(records)

        return None

    def search_skin_by_attributes(
        self, weapon=None, pattern=None, wear=None, stattrak=False
    ):
        """
        Search for a specific skin by attributes

        Args:
            weapon: Weapon name (e.g., "AK-47")
            pattern: Skin pattern (e.g., "Redline")
            wear: Wear condition (e.g., "Factory New", "Field-Tested")
            stattrak: Boolean

        Returns:
            DataFrame row or None
        """
        df = self.get_all_skins_not_grouped()

        if df is None or df.empty:
            return None

        # Filter by each attribute if provided
        if weapon:
            df = df[df["weapon"] == weapon]

        if pattern:
            df = df[df["pattern"] == pattern]

        if wear:
            df = df[df["wear"] == wear]

        df = df[df["stattrak"] == stattrak]

        if df.empty:
            return None

        return df.iloc[0].to_dict() if len(df) > 0 else None

    def get_market_hash_name(self, weapon, pattern, wear, stattrak=False):
        """
        Get the proper market_hash_name for a skin

        Args:
            weapon: e.g., "AK-47"
            pattern: e.g., "Redline"
            wear: e.g., "Field-Tested"
            stattrak: Boolean

        Returns:
            market_hash_name string or None
        """
        skin = self.search_skin_by_attributes(weapon, pattern, wear, stattrak)

        if skin:
            return skin.get("market_hash_name")

        return None

    def get_all_crates(self):
        """Get all cases/crates"""
        return self._fetch_json("crates")

    def get_all_collections(self):
        """Get all collections"""
        return self._fetch_json("collections")

    def get_all_stickers(self):
        """Get all stickers"""
        return self._fetch_json("stickers")

    def get_weapons_list(self):
        """
        Get list of all unique weapon names

        Returns:
            List of weapon names
        """
        df = self.get_all_skins_not_grouped()

        if df is not None:
            return sorted(df["weapon"].dropna().unique().tolist())

        return []

    def get_patterns_for_weapon(self, weapon):
        """
        Get all skin patterns available for a specific weapon

        Args:
            weapon: Weapon name (e.g., "AK-47")

        Returns:
            List of pattern names
        """
        df = self.get_all_skins_not_grouped()

        if df is not None:
            filtered = df[df["weapon"] == weapon]
            return sorted(filtered["pattern"].dropna().unique().tolist())

        return []

    def get_wear_conditions(self):
        """
        Get all possible wear conditions

        Returns:
            List of wear conditions
        """
        return [
            "Factory New",
            "Minimal Wear",
            "Field-Tested",
            "Well-Worn",
            "Battle-Scarred",
        ]

    def get_rarity_levels(self):
        """
        Get all rarity levels

        Returns:
            List of rarity names
        """
        df = self.get_all_skins_not_grouped()

        if df is not None:
            return sorted(df["rarity"].dropna().unique().tolist())

        return []


if __name__ == "__main__":
    api = CSGOAPIClient(language="en")

    # Get all skins
    skins_df = api.get_all_skins_not_grouped()
    print(f"Total skins: {len(skins_df)}")
    print("\nFirst few skins:")
    print(skins_df.head())

    # Search for specific skin
    skin = api.search_skin_by_attributes(
        weapon="AK-47", pattern="Redline", wear="Field-Tested", stattrak=False
    )

    if skin:
        print(f"\nFound skin:")
        print(f"Name: {skin['name']}")
        print(f"Market Hash Name: {skin['market_hash_name']}")
        print(f"Rarity: {skin['rarity']}")

    # Get all weapons
    weapons = api.get_weapons_list()
    print(f"\nTotal weapons: {len(weapons)}")
    print(f"Sample weapons: {weapons[:10]}")

    # Get patterns for AK-47
    ak_patterns = api.get_patterns_for_weapon("AK-47")
    print(f"\nAK-47 patterns: {len(ak_patterns)}")
    print(f"Sample patterns: {ak_patterns[:10]}")
