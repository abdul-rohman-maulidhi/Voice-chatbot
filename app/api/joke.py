import requests

class JokeApi:
    def __init__(self):
        self.__joke_api_url = "https://v2.jokeapi.dev/joke/Any"
    
    def get_joke(self):
        # Mengambil lelucon dari Joke API
        url = self.__joke_api_url
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception untuk error HTTP
            joke = response.json()
            if joke["type"] == "single":
                return joke["joke"]
            elif joke["type"] == "twopart":
                return f"{joke['setup']} ... {joke['delivery']}"
        except requests.exceptions.RequestException as e:
            return f"Sorry, I couldn't fetch a joke right now. Error: {e}"