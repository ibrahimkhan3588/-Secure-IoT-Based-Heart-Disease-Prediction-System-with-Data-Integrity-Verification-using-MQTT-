# Secure IoT Healthcare System (MQTT + AI)

This project is a simple IoT-based healthcare system for heart disease prediction using a machine learning model and MQTT communication. It allows users to enter structured medical data through a GUI, send it over MQTT, and receive predictions along with data integrity verification.

The system works by taking patient inputs (such as age, blood pressure, cholesterol, etc.), generating a hash of the data, and transmitting it using MQTT. At the receiver side, the system checks whether the data is authentic or tampered by comparing hashes and then performs heart disease prediction using a trained ML model.

Key features include a user-friendly GUI, real-time MQTT communication, AI-based prediction, and hash-based data integrity checking. The system can also simulate an attack where data is modified during transmission, and the receiver detects it as "Not Authentic Data".

Main files in the project include:
- MQTT_Client_GUI.py (main application)
- Heart_predictor.py (ML prediction logic)
- attacker.py (attack simulation)
- rf_classifier.pkl (trained model)
- scaler.pkl (data scaler)

To run the project:
1. Start the MQTT broker using: mosquitto -v
2. Run the GUI using: python MQTT_Client_GUI.py
3. (Optional) Run attacker using: python attacker.py

The output shows both the prediction (Heart Disease / No Heart Disease) and the data status (Authentic / Not Authentic).

Author: Ibrahim Khan
