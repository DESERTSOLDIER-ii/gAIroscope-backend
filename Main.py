from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {"User-Agent": "Mozilla/5.0"}

# Function to scrape VIX (from Cboe or Investing.com)
def scrape_vix():
    url = "https://www.investing.com/indices/volatility-s-p-500"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        vix_value = soup.find("div", {"class": "instrument-price_last"}).text.strip()
        return vix_value
    return "Error fetching VIX"

# Function to scrape NASDAQ (from Yahoo Finance)
def scrape_nasdaq():
    url = "https://finance.yahoo.com/quote/%5EIXIC/"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        nasdaq_value = soup.find("fin-streamer", {"data-field": "regularMarketPrice"}).text.strip()
        return nasdaq_value
    return "Error fetching NASDAQ"

# Function to scrape US30 (from IG or LiteFinance)
def scrape_us30():
    url = "https://www.litefinance.com/trading/dow-jones/"  # Example source
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        us30_value = soup.find("div", {"class": "current-price"}).text.strip()
        return us30_value
    return "Error fetching US30"

# Function to scrape Gold/USD (from Bloomberg)
def scrape_gold():
    url = "https://www.bloomberg.com/quote/XAUUSD:CUR"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        gold_value = soup.find("span", {"class": "priceText__1853e8a5"}).text.strip()
        return gold_value
    return "Error fetching Gold/USD"

# API routes
@app.route("/data", methods=["GET"])
def get_data():
    data = {
        "VIX Index": scrape_vix(),
        "NASDAQ": scrape_nasdaq(),
        "US30": scrape_us30(),
        "Gold/USD": scrape_gold()
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
