import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class WeatherPredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the GUI layout and style
        self.setWindowTitle("Weather Prediction System")
        self.setGeometry(200, 200, 500, 400)
        self.setStyleSheet("background-color: #f5f5f5; font-family: Arial;")

        layout = QVBoxLayout()

        # Instructions and input fields for the user
        self.date_label = QLabel("Enter the prediction date (YYYY-MM-DD):")
        layout.addWidget(self.date_label)
        self.date_input = QLineEdit()
        layout.addWidget(self.date_input)

        # Button to load data and predict
        self.load_predict_button = QPushButton("Load Data and Predict", self)
        self.load_predict_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;")
        self.load_predict_button.clicked.connect(self.load_and_predict)
        layout.addWidget(self.load_predict_button)

        # Label to display results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_csv_files(self):
        # Load HADC and LADC data from the "data/raw/" folder
        hadc_file = "data/raw/HADC/location_1.csv"
        ladc_file = "data/raw/LADC/location_1.csv"
        location_file = "data/raw/LADC/__locations__.csv"

        if os.path.exists(hadc_file):
            self.hadc_data = pd.read_csv(hadc_file)
            print("HADC data loaded.")
        else:
            self.result_label.setText("HADC file not found.")
        
        if os.path.exists(ladc_file):
            self.ladc_data = pd.read_csv(ladc_file)
            print("LADC data loaded.")
        else:
            self.result_label.setText("LADC file not found.")

        if os.path.exists(location_file):
            self.location_data = pd.read_csv(location_file)
            print("Location data loaded.")
        else:
            self.result_label.setText("Location data file not found.")

    def train_model(self, data, target_column):
        # Features: Temp, Humi, AQI
        X = data[['Temp', 'Humi', 'AIQ']]
        y = data[target_column]  # Target to predict

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Linear Regression model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        return model

    def load_and_predict(self):
        # Load all CSV files automatically
        self.load_csv_files()

        # If data is loaded correctly, perform predictions
        if hasattr(self, 'hadc_data') and hasattr(self, 'ladc_data'):
            # Concatenate HADC and LADC data for simplicity
            combined_data = pd.concat([self.hadc_data[['Temp', 'Humi', 'AIQ']], self.ladc_data[['Temp', 'Humi', 'AIQ']]])

            # Train models for Temp, Humi, AQI
            temp_model = self.train_model(combined_data, 'Temp')
            humi_model = self.train_model(combined_data, 'Humi')
            aqi_model = self.train_model(combined_data, 'AIQ')

            # Latest data for predictions
            latest_data = combined_data.tail(1)[['Temp', 'Humi', 'AIQ']]

            # Predict future weather conditions
            predicted_temp = temp_model.predict(latest_data)[0]
            predicted_humi = humi_model.predict(latest_data)[0]
            predicted_aqi = aqi_model.predict(latest_data)[0]

            # Display predictions
            date = self.date_input.text()
            self.result_label.setText(
                f"Predicted for {date}:\n"
                f"Temperature: {predicted_temp:.2f}°C\n"
                f"Humidity: {predicted_humi:.2f}%\n"
                f"AQI: {predicted_aqi:.2f}"
            )
        else:
            self.result_label.setText("Failed to load data for prediction.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherPredictionApp()
    window.show()
    sys.exit(app.exec_())
