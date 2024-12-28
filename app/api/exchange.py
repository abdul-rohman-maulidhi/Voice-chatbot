import requests

class ExchangeApi:
    def __init__(self):
        self.exchange_api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        
    def get_exchange_rate(self, query: str):
        try:
            words = query.lower().split()
            print(f"Debug: Parsed words: {words}")  # Debug parsing input
            
            if len(words) >= 4:
                target_currency = words[-1].upper()
                
                # Fetch data from API
                response = requests.get(self.exchange_api_url)
                data = response.json()
                
                # Check if the target currency exists in the rates
                if target_currency in data["rates"]:
                    rate = data["rates"][target_currency]
                    return f"The exchange rate from USD to {target_currency} is {rate:.2f}."
                else:
                    return f"The target currency '{target_currency}' is not valid. Please try another currency."
            else:
                return "Please provide a query like 'Exchange rate to EUR'."
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching exchange rates: {e}"