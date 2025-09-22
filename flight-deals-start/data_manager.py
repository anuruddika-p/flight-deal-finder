import requests
import os
import logging
from dotenv import load_dotenv

#configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("flight_deals.log")
    ]
)

#this method is called to load .env file
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_url = os.getenv("SHEETY_URL")

    def read_city_name(self):
        """This function is used to read city names mentioned in the Google sheet and returns a list of city names.
            returns:
                city_names(list) - list of dictionaries with 'id' and 'city' """
        data = self.read_data()
        if not data or "prices" not in data:
            logging.error("No valid data or 'prices' key missing in Google Sheet")
            return []
        city_list = [
            {"id" : city["id"],
             "city" : city["city"]}
            for city in data["prices"] if "id" in city and "city" in city]
        logging.info(f"Read {len(city_list)} cities from Google Sheet")
        return city_list

    def write_city_codes(self, city_code_list):
        """This function is used to update the Flight Deal Google sheet with the city codes
        args : city_code_list(list) - list of city codes
        returns : empty list for consistency"""
        try:
            if not city_code_list:
                logging.error("No data in city code list")
                return []
            for city_code in city_code_list:
                if "id" not in city_code or "city_code" not in city_code:
                    logging.error("Missing 'id' or 'city_code' in ")
                row_id = int(city_code["id"])
                sheet_update_url = f"{self.sheety_url}/{row_id}"
                body = {"price": {"iataCode": city_code["city_code"],}}
                response = requests.put(url=sheet_update_url, json=body)
                response.raise_for_status()
                logging.info(f"Updated row {row_id} with city code {city_code}")
            return []
        except (requests.RequestException, ValueError, KeyError) as ex:
            logging.error(f"Error updating city codes: {str(ex)}")
            return []

    def read_data(self):
        """This function is used to read the data in the Flight Data Google sheet and
        return a dictionary include all the data in Google sheet.
        return : sheet_data(dict)"""
        try:
            response = requests.get(url=self.sheety_url)
            response.raise_for_status()
            sheet_data = response.json()
            logging.info("Successfully fetch Google Sheet data")
            return sheet_data
        except (requests.RequestException, ValueError, KeyError) as ex:
            logging.error(f"Error fetching sheet data {str(ex)}")
            return []



