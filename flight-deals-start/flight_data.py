import requests
import os
import logging
from dotenv import load_dotenv

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler("flight_deals.log")]
)

#this method is called to load .env file
load_dotenv()

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        #Amadeus endpoint, API keys
        self.amadeus_secret_key = os.getenv("AMADEUS_SECRET_KEY")
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_endpoint = "https://test.api.amadeus.com/v1/"

    def get_token(self):
        """ This function is used to get authorization token from Amadeus website,
        return :
            amadeus_token(str)"""
        #Amadeus endpoint, parameters and header to request a token
        auth_url = f"{self.amadeus_endpoint}security/oauth2/token"
        get_token_parameters = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_api_key,
            "client_secret": self.amadeus_secret_key
        }
        get_token_header = {
            "content-type": "application/x-www-form-urlencoded"
        }
        try:
            access_token_data = requests.post(url=auth_url,data=get_token_parameters,headers=get_token_header)
            access_token_data.raise_for_status()
            access_token = access_token_data.json()["access_token"]
            logging.info("Successfully fetched Amadeus token")
            return access_token
        except (requests.RequestException, ValueError, KeyError) as ex:
            logging.error(f"Error fetching token - {str(ex)}")
            return []

    def get_city_code(self, amadeus_token, city_list):
        """This function is used to get city codes for the cities listed in Flight Deals Google sheet.
        Args :  Amadeous_token(str)
                city_list(list) - list of cities.
        returns :
                city_code_list(list)"""
        #Amadeus endpoint, header and parameters to get city codes for particular city
        get_city_code_url = f"{self.amadeus_endpoint}/reference-data/locations/cities"
        get_city_code_header = {
            "authorization": f"Bearer {amadeus_token}"
        }
        try:
            city_code_list = []
            if not city_list:
                logging.error("No data in city_list")
                return []
            for city in city_list:
                if "city" not in city or "id" not in city:
                    logging.error(f"Missing city or id in {city}")
                get_city_code_parameters = {
                    "keyword": city["city"].upper(),
                    "max" : 1
                }
                city_code = requests.get(url=get_city_code_url,params=get_city_code_parameters,headers=get_city_code_header)
                city_code.raise_for_status()
                city_codes = city_code.json()
                if not city_codes.get("data"):
                    logging.error(f"No city code found for {city['city']}")
                city_code_dict = [{
                    "city_code" : city_codes["data"][0]["iataCode"],
                    "id" : city["id"]
                }]
                city_code_list.extend(city_code_dict)
                logging.info(f"Successfully fetched city code for {city['city']}")
            return city_code_list
        except (requests.RequestException, KeyError, ValueError) as ex:
            logging.error(f"Error fetching city codes- {str(ex)}")
            return []
