import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import cross_val_score, KFold

CLEAN_CSV = "extracted_data.csv"


def getCasesFromCSV():
    df = pd.read_csv(CLEAN_CSV)

    allCaseNames = []

    for row in df.iterrows():

        if row[1]["Case"] not in allCaseNames:
            allCaseNames.append(row[1]["Case"])

    allCaseNames = sorted(allCaseNames)
    return allCaseNames


def convertUserInputToFeatures(weapon, case, rarity, wear, isStatTrak):
    df = pd.read_csv(CLEAN_CSV)

    allWeapons = df["Weapon"].unique()
    weaponEncode = {}
    for i, curWeapon in enumerate(allWeapons):
        weaponEncode[curWeapon] = i

    allCases = df["Case"].unique()
    caseEncode = {}
    for i, curCase in enumerate(allCases):
        caseEncode[curCase] = i

    wears = {
        "Factory New (FN)": 0,
        "Minimal Wear (MW)": 1,
        "Field-Tested (FT)": 2,
        "Well-Worn (WW)": 3,
        "Battle-Scared (BS)": 4,
    }

    rarities = {
        "Mil-Spec (Blue)": 1,
        "Restricted (Purple)": 2,
        "Classified (Pink)": 3,
        "Covert (Red)": 4,
        "Contraband (Yellow)": 5,
    }

    statTrak = {"Yes": 1, "No": 0}

    weaponID = weaponEncode[weapon]
    caseID = caseEncode[case]
    rarityID = rarities[rarity]
    wearID = wears[wear]
    statTrakID = statTrak[isStatTrak]

    return [weaponID, caseID, rarityID, wearID, statTrakID]


def getFeaturesAsMatrix():
    df = pd.read_csv(CLEAN_CSV)
    examples = []

    WANTED_FEATURES = ["Weapon_ID", "Case_ID", "Rarity", "Wear_ID", "StatTrak"]

    for _, row in df.iterrows():
        curFeatures = []

        for col in WANTED_FEATURES:
            curFeatures.append(row[col])

        examples.append(curFeatures)

    return examples


def getValuesAsArray():
    df = pd.read_csv(CLEAN_CSV)
    values = []

    for _, row in df.iterrows():
        values.append(row["Price"])

    return values


def getMAE(y_predicted, y_test):
    total = 0

    for i in range(len(y_predicted)):
        total += abs(y_predicted[i] - y_test[i])

    total = total / len(y_predicted)
    return total


def getRMSE(y_predicted, y_test):

    sds = 0
    for i in range(len(y_predicted)):
        sds += (y_predicted[i] - y_test[i]) ** 2

    sds = sds / len(y_predicted)
    sds = sds**0.5
    return sds


def getMAPE(y_predicted, y_test):
    return mean_absolute_percentage_error(y_test, y_predicted)


def getcrossvalidation(x, y, split, model):

    folds = KFold(n_splits=split, shuffle=True)
    score = cross_val_score(model, x, y, cv=folds)
    return score.mean()
