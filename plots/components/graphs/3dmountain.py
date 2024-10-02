import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MountainMapVisualizer:
    def __init__(self, ladc_file, hadc_file):
        self.ladc_file = ladc_file
        self.hadc_file = hadc_file
        self.ladc_data = None
        self.hadc_data = None
        self.grid_x = None
        self.grid_y = None
        self.grid_z = None

    def load_data(self):
        """Load data from LADC and HADC CSV files."""
        try:
            self.ladc_data = pd.read_csv(self.ladc_file)
            self.hadc_data = pd.read_csv(self.hadc_file)
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def prepare_data(self):
        """Prepare data for 3D plotting."""
        # Combine LADC and HADC data for the grid
        all_data = pd.concat([self.ladc_data, self.hadc_data], ignore_index=True)
        
        # Creating a grid for plotting
        x = all_data['longitude']
        y = all_data['latitude']
        z = all_data['Temp'].fillna(0)  # Handle NaN temperatures

        # Create a grid for X, Y
        self.grid_x, self.grid_y = np.meshgrid(np.unique(x), np.unique(y))

        # Create a grid for Z (temperature)
        self.grid_z = np.zeros_like(self.grid_x)

        for i in range(len(x)):
            xi = np.where(np.unique(x) == x[i])[0][0]
            yi = np.where(np.unique(y) == y[i])[0][0]
            self.grid_z[yi, xi] = z[i]

    def plot_mountain(self):
        """Plot a 3D mountain map."""
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot the surface
        ax.plot_surface(self.grid_x, self.grid_y, self.grid_z, cmap='viridis')

        # Add labels
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Temperature (°C)')
        ax.set_title('3D Mountain Map of Temperature')

        plt.show()

def create_mountain_map(ladc_file, hadc_file):
    """Create and display the 3D mountain map."""
    mountain_visualizer = MountainMapVisualizer(ladc_file, hadc_file)
    mountain_visualizer.load_data()
    mountain_visualizer.prepare_data()
    mountain_visualizer.plot_mountain()

if __name__ == "__main__":
    ladc_path = 'data/raw/LADC/__locations__.csv'
    hadc_path = 'data/raw/HADC/Location_1.csv'
    create_mountain_map(ladc_path, hadc_path)
