import numpy as np
import pandas as pd

# from sklearn.model_selection import train_test_split

DATA = "Skins_Price.csv"
OUTPUT = "extracted_data.csv"


df = pd.read_csv(DATA)


# Encoding the rarity levels to numerical values
def encode_rarity(rarity):
    rarities = rarity.str.split().str[0]
    return rarities.replace(
        {"Mil-Spec": 1, "Restricted": 2, "Classified": 3, "Covert": 4, "Contraband": 5}
    )

df["Rarity"] = encode_rarity(df["Rarity"])

# encode cases
allCases = df["Case"].unique()
caseEncode = {}

for i, case in enumerate(allCases):
    caseEncode[case] = i

df['Case_ID'] = df["Case"].map(caseEncode)


# Encoding the weapon types to numerical values
weapon_encoder = {w: i for i, w in enumerate(df["Weapon"].unique())}
df["Weapon_ID"] = df["Weapon"].map(weapon_encoder)

price_cols = {
    "StatTrak Factory New": ("FN", 1),
    "StatTrak Minimal Wear": ("MW", 1),
    "StatTrak Field-Tested": ("FT", 1),
    "StatTrak Well-Worn": ("WW", 1),
    "StatTrak Battle-Scarred": ("BS", 1),
    "Factory New": ("FN", 0),
    "Minimal Wear": ("MW", 0),
    "Field-Tested": ("FT", 0),
    "Well-Worn": ("WW", 0),
    "Battle-Scarred": ("BS", 0),
}

wear_order = {"FN": 0, "MW": 1, "FT": 2, "WW": 3, "BS": 4}

records = []
for _, row in df.iterrows():
    base = {
        "Weapon": row["Weapon"],
        "Weapon_ID": row["Weapon_ID"],
        "Skin": row["Case"],
        "Case": row["Case_1"],
        "Case_ID": row["Case_ID"],
        "Rarity": row["Rarity"],
        "Min_Wear": row["Min Wear"],
        "Max_Wear": row["Max Wear"],
    }
    for col, (wear_label, is_stattrak) in price_cols.items():
        raw = str(row[col]).strip()
        if raw == "Not Possible" or raw == "nan":
            continue
        try:
            price = float(raw.replace("$", "").replace(",", ""))
        except ValueError:
            continue
        records.append(
            {
                **base,
                "Wear": wear_label,
                "Wear_ID": wear_order[wear_label],
                "StatTrak": is_stattrak,
                "Price": price,
            }
        )

result = pd.DataFrame(records)

result = result[
    [
        "Weapon",
        "Weapon_ID",
        "Skin",
        "Case",
        "Case_ID",
        "Rarity",
        "Min_Wear",
        "Max_Wear",
        "Wear",
        "Wear_ID",
        "StatTrak",
        "Price",
    ]
]
result.to_csv(OUTPUT, index=False)
