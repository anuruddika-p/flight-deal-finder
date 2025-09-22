from twilio.base.exceptions import TwilioException
from twilio.rest import Client
import os
import logging
from dotenv import load_dotenv

#configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("flight_deals.log")
    ]
)

#load .env file
load_dotenv()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        # sender and receiver whatsapp numbers
        self.FROM = os.getenv("FROM")
        self.TO = os.getenv("TO")


    def send_message(self, flight_dict):
        """This function is used to send whatsaoo messages
        arg : flight_dict(dict) - dictionary includes origin, destination, departure time and dare, price
        output - send whatsapp messages with the passed data"""
        account_sid = self.twilio_sid
        auth_token = self.auth_token
        try:
            client = Client(account_sid, auth_token)
            if not flight_dict:
                logging.error("No data in flight_dict")
                return []
            for item in flight_dict:
                origin = item["origin"]
                destination = item["destination"]
                (date, time) = item["departure_date"].split("T")
                price = item["price"]
                message = client.messages.create(
                    from_= self.FROM,
                    body = f"✈️ 🚨Flight Alert \n You hava a cheap flight from {origin} to {destination} on {date} at {time} for USD {price}",
                    to=self.TO
                )
                logging.info(message.status)
        except TwilioException as ex:
            logging.error(f"Error at sending message {str(ex)}")
