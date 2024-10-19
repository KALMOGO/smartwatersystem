import pandas as pd
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def get_last_30_data(self, start_datetime):
        """
        Cette methode permet d'obtenir les 30 valeurs précédentes de notre 
        jeu de donnée en fonction de la date fournie par l'utilisateur
        """
        start_datetime = pd.to_datetime(start_datetime, format='%m/%d/%Y %H:%M')
        if start_datetime in self.data.index:
            start_index = self.data.index.get_loc(start_datetime)
            if start_index >= 30:
                selected_data = self.data.iloc[start_index-30:start_index]
            else:
                selected_data = self.data.iloc[:start_index]
            end_time = selected_data.tail(1).index
        else:
            selected_data = self.data.tail(30)
            end_time = self.data.tail(1).index
        return selected_data, end_time
    
    @staticmethod
    def thirty_minute_intervals(start_datetime, end_datetime):
        """
        Cette fonction permet de retourner la liste des temps en la date debut de la prédiction et 
        la date de fin
        """
        start_time = datetime.strptime(start_datetime[0].strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_datetime, '%m/%d/%Y %H:%M')
        intervals = []
        delta = timedelta(minutes=30)
        current_time = start_time

        while current_time <= end_time:
            intervals.append(current_time)
            current_time += delta

        return intervals
    
    def scale_data(self, data):
        """
        Cette methode permet de normaliser les données
        """
        scaled_data = self.scaler.fit_transform(data)
        return scaled_data
    
class TemperaturePredictor:
    """
        Modèle de prédiction de la qualité de l'eau
    """
    
    def __init__(self, model_path, data_processor):
        self.model = load_model(model_path)
        self.data_processor = data_processor
    
    def make_predictions(self, data, intervals):
        """
        Effectue la prédiction des paramètres
        """
        predictions = []
        num_hours = len(intervals)
        window_size = 30

        scaled_data = self.data_processor.scale_data(data)
        last_sequence = scaled_data[-window_size:].reshape((1, window_size, 1))

        # Predict the temperature for the next hour
        for i in range(num_hours):
            next_temp_scaled = self.model.predict(last_sequence, verbose=0)
            next_temp = self.data_processor.scaler.inverse_transform(next_temp_scaled)
            predictions.append({"temperature": next_temp[0][0], "datetime": intervals[i].strftime('%d/%m/%Y %H:%M')})

            # Update the last_sequence with the predicted value
            next_temp_scaled_reshaped = next_temp_scaled.reshape((1, 1, 1))
            new_input = np.append(last_sequence[:, 1:, :], next_temp_scaled_reshaped, axis=1)
            last_sequence = new_input
        return predictions


def mainParamsPrediction(start_datetime=None, end_datetime=None):
    # Convert datetime objects to the required string format
    start_datetime_str = start_datetime.strftime('%m/%d/%Y %H:%M')
    end_datetime_str   = end_datetime.strftime('%m/%d/%Y %H:%M')

    data_path ="saveModels\processed_temperature.csv"
    # Data processing
    data_processor = DataProcessor(data_path)
    selected_data, date_end = data_processor.get_last_30_data(start_datetime_str)

    # Time intervals generation
    intervals = DataProcessor.thirty_minute_intervals(date_end, end_datetime_str)

    # Model prediction
    model_path = "saveModels\\temperature_prediction_model.h5"
    temperature_predictor = TemperaturePredictor(model_path, data_processor)
    predictions = temperature_predictor.make_predictions(selected_data, intervals)

    return predictions
