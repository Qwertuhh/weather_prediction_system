import numpy as np

class WindEngine:
    def __init__(self):
        pass
    @staticmethod
    def calculate_wind_direction(temperature):
        if temperature < 20:
            return 270
        elif temperature < 30:
            return 0
        else:
            return 90

    def calculate_wind_vector(self, lat, lon, temperature):
        """Return vector components for the wind direction."""
        wind_direction = self.calculate_wind_direction(temperature)
        arrow_length = 0.005
        end_lat = lat + arrow_length * np.sin(np.radians(wind_direction))
        end_lon = lon + arrow_length * np.cos(np.radians(wind_direction))
        return end_lat, end_lon
