✈️ Flight Deals Automation

An automation tool that finds the cheapest flight deals using the Amadeus API and sends personalized alerts via WhatsApp (Twilio API).
It also integrates with Google Sheets (Sheety API) to manage destinations and price thresholds.

📌 Features

✅ Fetches city codes for destinations from Google Sheets

✅ Searches for cheap flights (within a 2-month window) using Amadeus API

✅ Updates Google Sheet with city codes automatically

✅ Sends WhatsApp notifications for the best deals using Twilio

✅ Detailed logging for debugging and monitoring

🛠️ Tech Stack

Python 3.11+

APIs: Amadeus (Flight Offers), Sheety, Twilio WhatsApp

Libraries:

requests (API calls)

python-dotenv (environment variables)

logging (monitoring & debugging)

dateutil (date handling)

📂 Project Structure
FlightDeals/
│── data_manager.py          # Google Sheets integration
│── flight_data.py           # Get Amadeus API token + city codes
│── flight_search.py         # Search for flight offers
│── notification_manager.py  # Send WhatsApp alerts via Twilio
│── main.py                  # Main runner script
│── .env                     # API keys and config (ignored in Git)
│── flight_deals.log         # Log file
│── README.md

⚙️ Setup & Installation
1. Clone repository
git clone git@github.com-work:anuruddika-p/flight-deals-automation.git
cd flight-deals-automation

2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Create .env file in root folder:
# Amadeus API
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_SECRET_KEY=your_amadeus_secret

# Sheety API
SHEETY_URL=your_google_sheety_url

# Twilio API
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth
FROM=whatsapp:+14155238886     # Twilio sandbox number
TO=whatsapp:+94XXXXXXXXX       # Your WhatsApp number

# Other configs
ORIGIN=CMB
ADULTS=1
CURRENCY_CODE=USD
MAX_OFFERS=5

5. Run the project
python main.py

📊 Example Output
2025-09-22 09:00:23 - INFO - Successfully fetched Amadeus token
2025-09-22 09:00:24 - INFO - Successfully fetched city code for Paris
2025-09-22 09:00:25 - INFO - Successfully fetched flight data for CDG
2025-09-22 09:00:26 - INFO - ✈️ Flight Alert: Cheap flight from CMB → CDG on 2025-11-20 at 07:00 for USD 420

🔒 Security

API keys are stored securely in .env (never commit this file to GitHub).

Added .gitignore to protect sensitive credentials.

🌟 Future Improvements

Add email notifications in addition to WhatsApp

Support for multiple origins

Store booking history in a database (SQLite/PostgreSQL)

👤 Author

Anuruddika Punchihewage

👋 Contact
Email: anuruddika.codes@gmail.com · LinkedIn: linkedin.com/in/anuruddika-p-883372385

GitHub: anuruddika-p

LinkedIn: (Add your LinkedIn link here for recruiters)
