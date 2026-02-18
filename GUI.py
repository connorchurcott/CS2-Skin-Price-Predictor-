import tkinter as tk
from tkinter import ttk


class GUIWindow(): 

    # Use GUIWindow.getSelectedValues() to get an array of the user entered values in this order [Wear, Rarity, WeaponType, isStattrak]

    def __init__(self):
        self.root = tk.Tk()
        self.windowStyling()
        self.setupInputFields()

    def windowStyling(self): 
        self.root.title("CS2 Skin Price Predictor")
        self.root.configure(background="gray15") 
        self.root.minsize(1200, 800)
        self.root.maxsize(1200, 800)
    
    def setupInputFields(self):
        self.selectedWear = tk.StringVar()
        self.selectWearBox = ttk.Combobox(self.root, textvariable=self.selectedWear, state="readonly") 
        self.selectWearBox["values"] = ["Factory New (FN)", "Minimal Wear (MW)", "Field-Tested (FT)", "Well-Worn (WW)", "Battle-Scared (BS)"]
        self.selectWearBox.pack(pady=10)

        self.selectedRarity = tk.StringVar()
        self.selectRarityBox = ttk.Combobox(self.root, textvariable=self.selectedRarity, state="readonly")
        self.selectRarityBox["values"] = ["Consumer Grade (White)", "Industrial Grade (light blue)", "Mil-Spec (blue)", "Restricted (Purple)", "Classified (Pink)", "Covert (Red)", "Contraband (Yellow)"]
        self.selectRarityBox.pack(pady=10)

        self.selectedWeaponType = tk.StringVar()
        self.selectWeaponTypeBox = ttk.Combobox(self.root, textvariable=self.selectedWeaponType, state="readonly")
        self.selectWeaponTypeBox["values"] = ["---PISTOLS---", "CZ75-Auto", "Desert Eagle", "Dual Berettas", "Five-SeveN", "Glock-18", "P200", "P250", "R8 Revolver", "Tec-9", "USP-S", 
                                              "---RIFLES---", "AK-47", "AUG", "AWP", "FAMAS", "G3SG1", "Galil AR", "M4A1-S", "M4A4", "SCAR-20", "SG 553", "SSG 08", 
                                              "---SMGs---", "MAC-10", "MP5-SD", "MP7", "MP9", "PP-Bizon", "P90", "UMP-45",
                                              "---HEAVY---", "MAG-7", "Nova", "Sawed-Off", "XM1014", "M249", "Negev", 
                                              "---KNIVES---", "Bayonet", "Bowie Knife", "Butterfly Knife", "Classic Knife", "Falchion Knife", "Flip Knife", "Gut Knife", "Huntsman Knife", "Karambit", "Kukri Knife", "M9 Bayonet", "Navaja Knife", "Nomad Knife", "Paracord Knife", "Shadow Daggers", "Skeleton Knife", "Stiletto Knife", "Survival Knife", "Talon Knife", "Ursus Knife"]
        self.selectWeaponTypeBox.pack(pady=10)

        self.selectedStatTrak = tk.StringVar()
        self.selectStatTrakBox = ttk.Combobox(self.root, textvariable=self.selectedStatTrak, state="readonly")
        self.selectStatTrakBox["values"] = ["Yes", "No"]
        self.selectStatTrakBox.pack(pady=10)

        self.button = tk.Button(self.root, text="print selection", command=self.printselected)
        self.button.pack(); 


    def getSelectedValues(self): 
        selectedValues = [self.selectedWear.get(), self.selectedRarity.get(), self.selectedWeaponType.get(), self.selectedStatTrak.get()]
        return selectedValues

    def run(self):
        self.root.mainloop(); 
    



    
    def printselected(self):
        print(self.getSelectedValues())
        return 




def main():
    window = GUIWindow()
    window.run()
    return 


if __name__ == "__main__":
    main() 