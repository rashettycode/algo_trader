import gdown
import os

def download_file_from_google_drive(file_id, output_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    gdown.download(url, output_path, quiet=False)

# Ensure the output directory exists
output_dir = "data/processed/"
os.makedirs(output_dir, exist_ok=True)

# URLs from Google Drive
file_urls = {
    "trained_model.pkl": "1AjKObh897ynJ0P0HrAFl00cI-C_Mt9vs",
    "random_forest_model_with_indicators.pkl": "19usam8SrQsFLobAVRIRfy9jERohlRCjm",
    "simple_random_forest_model.pkl": "19hx0pPnqcayHc1pYu58y1Ml2-lgoe_Po",
    "best_ensemble_model.pkl": "1G7Qi2jBKTX76acSZkEKF-ov5ToLPPsyd",
    "best_random_forest_model.pkl": "1W93C7rBnQYmj7sgpzV0setAnDHswrx6a"
}

# Download each file
for file_name, file_id in file_urls.items():
    output_path = os.path.join(output_dir, file_name)
    download_file_from_google_drive(file_id, output_path)
