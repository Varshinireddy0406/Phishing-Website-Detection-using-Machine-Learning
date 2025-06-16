# importing required libraries
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import os

# suppress warnings
warnings.filterwarnings('ignore')

# import your custom feature extractor
from feature import FeatureExtraction

# load the trained model from pickle
file_path = os.path.join(os.path.dirname(__file__), "pickle", "model.pkl")
with open(file_path, "rb") as file:
    gbc = pickle.load(file)

# create the Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # extract features from the entered URL
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30) 

        # make prediction
        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

        prediction = "It is {:.2f}% safe to go.".format(y_pro_non_phishing * 100)

        return render_template('index.html', 
                               xx=round(y_pro_non_phishing * 100, 2),
                               url=url,
                               prediction=prediction,
                               result="Safe" if y_pred == 1 else "Unsafe")

    return render_template("index.html", xx=-1)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
