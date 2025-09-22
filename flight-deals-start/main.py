#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import logging
#importing all the classes
from flight_data import FlightData
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

#configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("flight_deals.log")
    ]
)

def update_city_codes(amadeus_token):
    """This function will get city name list from Google sheet and
    fine relevant city code's and then update the Google sheet with the city codes."""
    #read excel sheet data
    if not amadeus_token:
        logging.error("No valid Amadius token")
        return
    city_name_list = data_manager_class.read_city_name()
    #request city codes for the relevant city names
    city_code_list = flight_data_class.get_city_code(amadeus_token, city_name_list)
    #update Google sheet
    data_manager_class.write_city_codes(city_code_list)

def send_cheap_flights_by_whatsapp(amadeus_token):
    sheet_data = data_manager_class.read_data()
    flight_data_dict = flight_search_class.search_cheap_flight(amadeus_token,sheet_data)
    notification_manager_class.send_message(flight_data_dict)

def main():
    """Main function to run the Flight Deal Finder."""
    global flight_data_class, data_manager_class, flight_search_class, notification_manager_class
    flight_data_class = FlightData()
    data_manager_class = DataManager()
    flight_search_class = FlightSearch()
    notification_manager_class = NotificationManager()
    amadeus_token = flight_data_class.get_token()
    update_city_codes(amadeus_token)
    send_cheap_flights_by_whatsapp(amadeus_token)

if __name__ == "__main__":
    main()




