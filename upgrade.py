from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
from arcgis.env import active_gis
from arcgis.geometry import project
# from arcgis.features.manage_data import manage_data
import arcpy
import logging
import os

# Configure logging
log_file = "db_projection_log.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def setup_logging():
    logging.info("Starting the script...")

    # Check if log file exists
    if os.path.exists(log_file):
        logging.info(f"Logging to file: {log_file}")
    else:
        logging.warning(f"Log file not created at expected path: {log_file}")


def connect_to_database(sde_path):
    try:
        logging.info(f"Setting workspace to: {sde_path}")
        arcpy.env.workspace = sde_path

        # Verify the connection
        if arcpy.Exists(sde_path):
            logging.info("Successfully connected to the geodatabase.")
        else:
            logging.error("Failed to connect to the geodatabase. Check the connection file.")
            return False
    except Exception as e:
        logging.error(f"Error connecting to the database: {str(e)}")
        return False

    return True


def retrieve_feature_classes(feature_dataset):
    try:
        # List all feature classes within the feature dataset
        logging.info(f"Retrieving feature classes from feature dataset: {feature_dataset}")
        feature_classes = arcpy.ListFeatureClasses(feature_dataset=feature_dataset)

        if feature_classes:
            logging.info(f"Found {len(feature_classes)} feature classes in the dataset.")
        else:
            logging.warning(f"No feature classes found in the dataset: {feature_dataset}")

        return feature_classes

    except Exception as e:
        logging.error(f"Error retrieving feature classes: {str(e)}")
        return []


def project_feature_classes(feature_classes, new_spatial_ref):
    for fc in feature_classes:
        try:
            logging.info(f"Projecting feature class: {fc}")
            output_fc = f"{fc}_projected"
            arcpy.Project_management(fc, output_fc, new_spatial_ref)
            logging.info(f"Successfully projected {fc} to {output_fc}")
        except Exception as e:
            logging.error(f"Error projecting feature class {fc}: {str(e)}")


def main():
    setup_logging()

    # Path to your .sde connection file
    sde_path = r"C:\Coding_Projects\SpatialReferenceUpdate\connections\SQLServer-gis-501sql2016-WinchesterCT(gis).sde"

    # Name of the feature dataset you are working with
    feature_dataset = "WL_Winchester.SDE.INTERNAL_WGS1984"

    # Define the new spatial reference (e.g., WGS 84 - EPSG: 4326)
    new_spatial_ref = arcpy.SpatialReference(4326)

    # Connect to the database
    if connect_to_database(sde_path):
        # Retrieve feature classes within the feature dataset
        feature_classes = retrieve_feature_classes(feature_dataset)

        # If feature classes are retrieved, proceed to project them
        if feature_classes:
            project_feature_classes(feature_classes, new_spatial_ref)
        else:
            logging.warning("No feature classes to project.")
    else:
        logging.error("Database connection failed. Exiting script.")

    logging.info("Script completed.")


# Run the main function
if __name__ == "__main__":
    main()