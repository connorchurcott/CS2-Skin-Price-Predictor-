import joblib
from GUI import GUIWindow


def main(): 
    model = joblib.load("model.joblib")
    metrics = joblib.load("metrics.joblib")
    window = GUIWindow(model, metrics)
    window.run()

main()




