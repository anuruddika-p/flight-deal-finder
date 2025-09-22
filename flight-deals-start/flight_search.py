import os

import requests
import logging
import datetime as dt
from dateutil.relativedelta import relativedelta

#configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("flight_deals.log")
    ]
)

#data to search flights


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.amadeus_endpoint = "https://test.api.amadeus.com/v2/"
        #get today date using datetime module in Python
        self.today_date = dt.datetime.today().date()
        #departure date is set to 2 months period from today date
        self.departure_date = self.today_date + relativedelta(months=2)
        self.origin = os.getenv("ORIGIN")
        self.adults = os.getenv("ADULTS")
        self.currency_code = os.getenv("CURRENCY_CODE")
        self.max_offers = os.getenv("MAX_OFFERS")

    def search_cheap_flight(self, amadeus_token, flight_details):
        """This function is used to search the flight offers with departure date 2 months from today,
        destinations from the Google sheet,prices below specified thresholds,
         and return a list of dictionary with origin, destination, departure_date, price.

         Args : Amadeus_token(str) : Amadeus API token
                flight_details(dict) - google sheet data
        returns:
            list : list of dictionaries with flight details (origin, destination, departure time and date,price)
            or empty list if no result
        """
        url_flight_search = f"{self.amadeus_endpoint}shopping/flight-offers"
        flight_search_header = {
            "authorization": f"Bearer {amadeus_token}"
        }
        if not flight_details or "prices" not in flight_details:
            logging.error("invalid or missing flight details data")
            return []
        all_flights = []
        for location in flight_details["prices"]:
            if not all(key in location for key in ["iataCode", "lowestPrice"]):
                logging.error(f"Invalid data for destination {location.get('iataCode', 'unknown')}")
                continue
            flight_search_parameters = {
                        "originLocationCode": self.origin,
                        "destinationLocationCode": location["iataCode"],
                        "departureDate": self.departure_date,
                        "adults" : self.adults,
                        "currencyCode" : self.currency_code,
                        "maxPrice" : location["lowestPrice"],
                        "max" : self.max_offers,
                }

            try:
                response = requests.get(url=url_flight_search,
                                        headers=flight_search_header,
                                        params=flight_search_parameters)
                response.raise_for_status()
                flight_data = response.json()
                if not flight_data.get("data"):
                    logging.error(f"No flights found for {location['iataCode']}")
                flight_dict = [
                    {
                        "origin": self.origin,
                        "departure_date" : flight["itineraries"][0]["segments"][0]["departure"]["at"],
                        "destination": location["iataCode"],
                        "price": flight["price"]["grandTotal"]
                    }
                    for flight in flight_data["data"]
                ]
                all_flights.extend(flight_dict)
                logging.info(f"Successfully fetched flight data for {location['iataCode']}")
            except (requests.RequestException, KeyError, ValueError) as ex:
                logging.error(f"Error fetching data {location['iataCode']} : {str(ex)}")
                return []
        return all_flights
