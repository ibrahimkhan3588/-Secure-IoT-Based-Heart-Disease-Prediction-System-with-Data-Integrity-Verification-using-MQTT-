import pickle
import numpy as np
import os
import sys

# Fix path when running as EXE
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

model_path = os.path.join(base_path, "rf_classifier.pkl")
scaler_path = os.path.join(base_path, "scaler.pkl")

# Load trained model
model = pickle.load(open(model_path, "rb"))

# Load scaler
scaler = pickle.load(open(scaler_path, "rb"))


def predict_heart(male, age, currentSmoker, cigsPerDay, BPMeds,
                  prevalentStroke, prevalentHyp, diabetes,
                  totChol, sysBP, diaBP, BMI, heartRate, glucose):

    # Encode yes/no values
    male = 1 if male.lower() == "male" else 0
    currentSmoker = 1 if currentSmoker.lower() == "yes" else 0
    BPMeds = 1 if BPMeds.lower() == "yes" else 0
    prevalentStroke = 1 if prevalentStroke.lower() == "yes" else 0
    prevalentHyp = 1 if prevalentHyp.lower() == "yes" else 0
    diabetes = 1 if diabetes.lower() == "yes" else 0

    features = np.array([[male, age, currentSmoker, cigsPerDay, BPMeds,
                          prevalentStroke, prevalentHyp, diabetes,
                          totChol, sysBP, diaBP, BMI, heartRate, glucose]])

    scaled = scaler.transform(features)

    result = model.predict(scaled)

    if result[0] == 1:
        return "Heart Disease"
    else:
        return "No Heart Disease"