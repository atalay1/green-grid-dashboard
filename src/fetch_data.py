import requests
import json
import sys

def fetch_data():
    """
    Fetches the last 48 hours of DeclarationProduction data
    for DK1 and DK2 price areas.
    """
    
    # The API endpoint for the dataset
    base_url = "https://api.energidataservice.dk/dataset/DeclarationProduction"
    
    # Define the parameters for the API call
    params = {
        'start': 'now-P2D',  # 'P2D' is a duration of 2 days (48 hours)
        'filter': json.dumps({"PriceArea": ["DK1", "DK2"]}),
        'sort': 'HourUTC ASC' # Get data in chronological order
    }
    
    print("Fetching data from Energi Data Service...")
    
    try:
        # Make the GET request
        response = requests.get(base_url, params=params)
        
        # Raise an error if the request was unsuccessful
        response.raise_for_status()
        
        print(f"Success: {response.status_code}")
        
        # Parse the JSON response
        data = response.json()
        
        # Define the output file name
        output_file = './data/raw_data.json'
        
        # Save the data to a JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        record_count = len(data.get('records', []))
        print(f"Successfully fetched {record_count} records.")
        print(f"Data saved to {output_file}")
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    # Make sure you are in the 'green-grid-dashboard' environment
    print(f"Running with Python version: {sys.version.split()[0]}")
    fetch_data()