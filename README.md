# 📊 CryptoPulse Dashboard

CryptoPulse Dashboard is a Python-based terminal dashboard that pulls real-time cryptocurrency data from the CoinGecko API and visualizes it using `pandas` and `matplotlib`.

It is designed as a lightweight project for learning API integration, data transformation, and basic analytics — perfect for freelance and portfolio use.

---

## 🚀 Features

- Pulls data from [CoinGecko API](https://www.coingecko.com/en/api)
- Supports top cryptocurrencies by market cap
- Displays:
  - Current price
  - 24h change %
  - Market cap
  - Volume
- Saves data to CSV for further analysis
- Data visualization with simple matplotlib charts

---

## 🛠️ Tech Stack

- `Python 3.10+`
- `requests`
- `pandas`
- `matplotlib`
- `json`

---

## 📦 Installation

```bash
git clone https://github.com/backsterlite/CryptoPulse-dashboard.git
cd CryptoPulse-dashboard
pip install -r requirements.txt
```

---

## ▶️ Usage
```
python main.py
```
You can adjust the list of tracked cryptocurrencies and the output format directly in the script.

---

## 📁 Output Example
A sample CSV file will be created:
```
symbol,price_usd,24h_change,market_cap,volume
BTC,63800.34,+1.25%,1.23T,32.5B
ETH,3240.56,-0.55%,387B,16.4B
...
```

---

## 📈 Visualization
The script generates basic line/bar plots using matplotlib to help you track trends visually.


---

## 📌 Notes
- This project is for educational and portfolio purposes.
- CoinGecko's free API has rate limits — avoid too frequent calls.

---

## 📬 Contact
Feel free to reach out if you'd like to extend this project, integrate it into a Telegram bot, or visualize it on a web dashboard!