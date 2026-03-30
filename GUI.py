import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from helpers import getCasesFromCSV
from helpers import convertUserInputToFeatures


class GUIWindow(): 

    # Use GUIWindow.getSelectedValues() to get an array of the user entered values in this order [Wear, Rarity, WeaponType, isStattrak, Case]
    # Use GUIWindow.setOutputValues(newPredictedValue, realValue) to set the GUI to display the new precited value
    # idk how to get the real value to display 

    def __init__(self, model, metrics):
        self.root = tk.Tk()
        self.allCases = getCasesFromCSV()
        self.model = model
        self.metrics = metrics
        self.windowStyling()
        self.setupInputFields()
        self.setupOutputFields()
        self.setupMetrics()


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
        self.selectRarityBox["values"] = ["Mil-Spec (Blue)", "Restricted (Purple)", "Classified (Pink)", "Covert (Red)", "Contraband (Yellow)"]
        self.selectRarityBox.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.selectedWeaponType = tk.StringVar()
        self.selectWeaponTypeBox = ttk.Combobox(self.root, textvariable=self.selectedWeaponType, state="readonly")
        self.selectWeaponTypeBox["values"] = ["---PISTOLS---", "CZ75-Auto", "Desert Eagle", "Dual Berettas", "Five-SeveN", "Glock-18", "P2000", "P250", "R8 Revolver", "Tec-9", "USP-S", 
                                              "---RIFLES---", "AK-47", "AUG", "AWP", "FAMAS", "G3SG1", "Galil AR", "M4A1-S", "M4A4", "SCAR-20", "SG 553", "SSG 08", 
                                              "---SMGs---", "MAC-10", "MP5-SD", "MP7", "MP9", "PP-Bizon", "P90", "UMP-45",
                                              "---HEAVY---", "MAG-7", "Nova", "Sawed-Off", "XM1014", "M249", "Negev", 
                                              "---KNIVES---", "Bayonet", "Bowie Knife", "Butterfly Knife", "Classic Knife", "Falchion Knife", "Flip Knife", "Gut Knife", "Huntsman Knife", "Karambit", "Kukri Knife", "M10 Bayonet", "Navaja Knife", "Nomad Knife", "Paracord Knife", "Shadow Daggers", "Skeleton Knife", "Stiletto Knife", "Survival Knife", "Talon Knife", "Ursus Knife"]
        self.selectWeaponTypeBox.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.selectedStatTrak = tk.StringVar()
        self.selectStatTrakBox = ttk.Combobox(self.root, textvariable=self.selectedStatTrak, state="readonly")
        self.selectStatTrakBox["values"] = ["Yes", "No"]
        self.selectStatTrakBox.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.selectedCase = tk.StringVar()
        self.selectCaseEntry = tk.Entry(self.root, textvariable=self.selectedCase)
        self.selectCaseEntry.grid(row = 4, column=0, padx=10, pady=10, sticky="w")

        self.button = tk.Button(self.root, text="Submit", command=self.runPrediction)
        self.button.grid(row=5, column=0, pady=10)
    
    def setupOutputFields(self): 
        self.predictedValue = tk.DoubleVar()
        self.outputLabel = tk.Label(self.root, text="Predicted Value: ")
        self.outputLabel.grid(row=6, column=0, padx=10, pady=50, sticky="w")
        self.outputBox = tk.Label(self.root, textvariable=self.predictedValue, relief="sunken", width=15)
        self.outputBox.grid(row=6, column=1, padx=1, pady=10, sticky="w")

        # self.realValue = tk.DoubleVar()
        # self.outputLabelRealValue = tk.Label(self.root, text="Real Value: ")
        # self.outputLabelRealValue.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        # self.outputBoxRealValue = tk.Label(self.root, textvariable=self.realValue, relief="sunken", width=15)  
        # self.outputBoxRealValue.grid(row=7, column=1, padx=1, pady=10, sticky="w")

    def setupMetrics(self): 
        tk.Label(self.root, text="MODEL METRICS").grid(row=0, column=10, padx=10, pady=10, sticky="w")
        tk.Label(self.root, text=f"MAE: {self.metrics['MAE']}", background="gray15", foreground="white").grid(row=1, column=10, padx=10, sticky="w")
        tk.Label(self.root, text=f"RMSE: {self.metrics['RMSE']}", background="gray15", foreground="white").grid(row=2, column=10, padx=10, sticky="w")
        tk.Label(self.root, text=f"MAPE: {self.metrics['MAPE']}", background="gray15", foreground="white").grid(row=3, column=10, padx=10, sticky="w")
        tk.Label(self.root, text=f"R2: {self.metrics['CROSSVAL']}", background="gray15", foreground="white").grid(row=4, column=10, padx=10, sticky="w")



    def setOutputValues(self, newPredictedValue, newRealValue): 
        self.predictedValue.set(newPredictedValue)  
        # self.realValue.set(newRealValue)

    def getSelectedValues(self): 
        if self.selectedCase.get() not in self.allCases: 
            mbox.showerror("Entered Case Does Not Exist", "Please enter a valid case")
            return

        selectedValues = [self.selectedWeaponType.get(), self.selectedCase.get(), self.selectedRarity.get(), self.selectedWear.get(), self.selectedStatTrak.get()]
        return selectedValues

    def run(self):
        self.root.mainloop(); 
    

    def runPrediction(self): 
        selected = self.getSelectedValues() 
        if selected == None: 
            return 
        
        converted = convertUserInputToFeatures(selected[0], selected[1], selected[2], selected[3], selected[4])
        prediction = self.model.predict([converted])
        self.setOutputValues(round(prediction[0], 2), 0)