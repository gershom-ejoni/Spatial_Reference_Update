from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
from arcgis.env import active_gis
from arcgis.geometry import project
# from arcgis.features.manage_data import manage_data
import arcpy

# Connect to the GIS (Enterprise Geodatabase)
gis = GIS("https://winchester162.maps.arcgis.com/", "lvelez65", "Erme1917!")

# Set the workspace to your SQL Server geodatabase (feature dataset)
# Replace with your connection file or feature dataset path
arcpy.env.workspace = r"C:\Coding_Projects\SpatialReferenceUpdate\connections\SQLServer-gis-501sql2016-WinchesterCT(gis).sde"

# Get the list of feature classes within the feature dataset
feature_dataset = "WL_Winchester.SDE.INTERNAL_WGS1984"
feature_classes = arcpy.ListFeatureClasses(feature_dataset=feature_dataset)

# Define the new spatial reference you want to project into (for example, EPSG 4326 for WGS 84)
new_spatial_ref = arcpy.SpatialReference(4326)  # Change this to your desired spatial reference

# Loop through each feature class in the feature dataset and project them
for fc in feature_classes:
    print(f"Projecting {fc} to new spatial reference...")

    # Define output feature class name (you can modify this as needed)
    output_fc = f"{fc}_projected"

    # Project the feature class
    arcpy.Project_management(fc, output_fc, new_spatial_ref)

print("Projection update completed for all feature classes.")
