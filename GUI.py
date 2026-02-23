import tkinter as tk
from tkinter import ttk


class GUIWindow(): 

    # Use GUIWindow.getSelectedValues() to get an array of the user entered values in this order [Wear, Rarity, WeaponType, isStattrak]
    # Use GUIWindow.setPredictedValue(newPredictedValue) to set the GUI to display the new precited value

    def __init__(self):
        self.root = tk.Tk()
        self.windowStyling()
        self.setupInputFields()
        self.setupOutputFields()

    def windowStyling(self): 
        self.root.title("CS2 Skin Price Predictor")
        self.root.configure(background="gray15") 
        self.root.minsize(1200, 800)
        self.root.maxsize(1200, 800)
    
    def setupInputFields(self):
        self.selectedWear = tk.StringVar()
        self.selectWearBox = ttk.Combobox(self.root, textvariable=self.selectedWear, state="readonly") 
        self.selectWearBox["values"] = ["Factory New (FN)", "Minimal Wear (MW)", "Field-Tested (FT)", "Well-Worn (WW)", "Battle-Scared (BS)"]
        self.selectWearBox.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.selectedRarity = tk.StringVar()
        self.selectRarityBox = ttk.Combobox(self.root, textvariable=self.selectedRarity, state="readonly")
        self.selectRarityBox["values"] = ["Consumer Grade (White)", "Industrial Grade (light blue)", "Mil-Spec (blue)", "Restricted (Purple)", "Classified (Pink)", "Covert (Red)", "Contraband (Yellow)"]
        self.selectRarityBox.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.selectedWeaponType = tk.StringVar()
        self.selectWeaponTypeBox = ttk.Combobox(self.root, textvariable=self.selectedWeaponType, state="readonly")
        self.selectWeaponTypeBox["values"] = ["---PISTOLS---", "CZ75-Auto", "Desert Eagle", "Dual Berettas", "Five-SeveN", "Glock-18", "P200", "P250", "R8 Revolver", "Tec-9", "USP-S", 
                                              "---RIFLES---", "AK-47", "AUG", "AWP", "FAMAS", "G3SG1", "Galil AR", "M4A1-S", "M4A4", "SCAR-20", "SG 553", "SSG 08", 
                                              "---SMGs---", "MAC-10", "MP5-SD", "MP7", "MP9", "PP-Bizon", "P90", "UMP-45",
                                              "---HEAVY---", "MAG-7", "Nova", "Sawed-Off", "XM1014", "M249", "Negev", 
                                              "---KNIVES---", "Bayonet", "Bowie Knife", "Butterfly Knife", "Classic Knife", "Falchion Knife", "Flip Knife", "Gut Knife", "Huntsman Knife", "Karambit", "Kukri Knife", "M9 Bayonet", "Navaja Knife", "Nomad Knife", "Paracord Knife", "Shadow Daggers", "Skeleton Knife", "Stiletto Knife", "Survival Knife", "Talon Knife", "Ursus Knife"]
        self.selectWeaponTypeBox.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.selectedStatTrak = tk.StringVar()
        self.selectStatTrakBox = ttk.Combobox(self.root, textvariable=self.selectedStatTrak, state="readonly")
        self.selectStatTrakBox["values"] = ["Yes", "No"]
        self.selectStatTrakBox.grid(row=3, column=0, padx=10, pady=10, sticky="w")


        # replace self.printselected with actual function that sends that to the predictor later
        self.button = tk.Button(self.root, text="Submit", command=self.printselected)
        self.button.grid(row=4, column=0, pady=10)
    
    def setupOutputFields(self): 
        self.predictedValue = tk.DoubleVar()
        self.outputLabel = tk.Label(self.root, text="Predicted Value: ")
        self.outputLabel.grid(row=5, column=0, padx=10, pady=50, sticky="w")
        self.outputBox = tk.Label(self.root, textvariable=self.predictedValue, relief="sunken", width=15)
        self.outputBox.grid(row=5, column=1, padx=1, pady=10, sticky="w")



    def setPredictedValue(self, newPredictedValue): 
        self.predictedValue.set(newPredictedValue)  

    def getSelectedValues(self): 
        selectedValues = [self.selectedWear.get(), self.selectedRarity.get(), self.selectedWeaponType.get(), self.selectedStatTrak.get()]
        return selectedValues

    def run(self):
        self.root.mainloop(); 
    
    # demo function currently, remove and replace with real ai functionality hwne done
    def printselected(self):
        self.setPredictedValue(0.67) 
        print(self.getSelectedValues())
        return 
