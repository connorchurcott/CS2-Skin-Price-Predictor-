# **Counter Strike 2 Item Price Predictor**

This project utilizes a supervised regression model (Gradient Boosting Regression) to predict the price of a CS2 weapon skin. The skin is specified by the user through 5 features (Weapon Type, 
Rarity, Wear, Case, isStatTrak). The model is trained on 5664 data points, which originate from this Kaggle set and some clever data cleaning methods. 

Kaggle Dataset: https://www.kaggle.com/datasets/corymusial/cs2-skins-database?resource=download 


# **How To Run**

PREREQUISITES: Must have Python 3.x and Git installed. 

First, we must download this repo and download the nessecary library dependencies. 

1. Clone this repo locally: git clone https://github.com/connorchurcott/CS2-Skin-Price-Predictor-.git
2. Change to this repo's folder: cd CS2-Skin-Price-Predictor
3. Setup Virtual Environment: python -m venv venv
4. Start venv: venv/Scripts/activate    **NOTE: this command will be different for OS's other than Windows**
5. Install libraries in venv: pip install -r requirements.txt

Now we have everything we need to run the project

1. Train the model on the dataset: python model.py    **NOTE: if this is sucessful you will see two .joblib files be created in the local file**
2. Run the GUI: python main.py

If everything went correctly, you will now see the GUI pop up. 

# **Usage**

On the right side you see the trained model's metrics. These should be static and will only change if you retrain the model. 
On the left hand side you will see the feature input fields. This is where you input the features of the skin you want to predict the price of. The case field is the only field where the input 
is user typed. If you input a case that does not exist you will see an error message pop up. You must enter a case that already exists. Once you input all the feature fields correctly you can hit
the "Submit" button the predicted value will appear. 

To predict a new skin value, just replace the input features and press the "Submit" button again. 

# **Team**

This project was created with the work of 4 people: Connor, Duc, Jose, and Amr. 
