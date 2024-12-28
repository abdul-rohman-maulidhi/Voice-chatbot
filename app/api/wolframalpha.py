import requests

class WolframalphaApi:
    
    def __init__(self):
        self.wolfram_app_id = "2W5T47-QG4EQPYKP6"
        self.wolfram_url = "http://api.wolframalpha.com/v1/result"
        
    def search_wolframalpha(self, query: str):
        try:
            query = query.lower().replace("wolfram", "").strip()
            if not query:
                return "Please specify what you want to search on Wolfram Alpha."

            params = {
                "i": query,  # Query parameter
                "appid": self.wolfram_app_id,  # API key
            }
            response = requests.get(self.wolfram_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            if response.status_code == 200:
                return f"Wolfram Alpha result: {response.text}"
            else:
                return "Wolfram Alpha couldn't process your request."
        except requests.exceptions.RequestException as e:
            return f"An error occurred while connecting to Wolfram Alpha: {e}"