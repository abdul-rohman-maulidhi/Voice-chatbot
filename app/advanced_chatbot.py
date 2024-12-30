from app.chatbot import Chatbot
from app.browser.open_browser import OpenBrowser
from app.api.wikipedia import WikipediaApi
from app.api.wolframalpha import WolframalphaApi
from app.api.exchange import ExchangeApi
from app.api.joke import JokeApi
from app.api.trivia import TriviaApi
from app.api.weather import WeatherApi

class AdvancedChatbot(Chatbot): 
    def __init__(self):
        super().__init__()
        self.open_browser = OpenBrowser()
        self.wikipedia_api = WikipediaApi()
        self.wolframalpha_api = WolframalphaApi()
        self.exchange_api = ExchangeApi()
        self.joke_api = JokeApi()
        self.trivia_api = TriviaApi()
        self.weather_api = WeatherApi()
         
    def respond(self, text: str):
        response = super().respond(text)
        
        if self.trivia_api.current_trivia_answer:  
            return self.trivia_api.verify_trivia_answer(text)  # Call verify_trivia_answer correctly
        
        if "your name" in text.lower():
            return "I'm your intelligent assistant!"
        elif "open browser" in text.lower() or "browser" in text.lower():
            return self.open_browser.handle_open_browser(text)
        elif "wikipedia" in text.lower() or "wiki" in text.lower():
            return self.wikipedia_api.search_wikipedia(text)
        elif "wolfram" in text.lower() or "solve" in text.lower() or "calculate" in text.lower():
            return self.wolframalpha_api.search_wolframalpha(text)
        elif "exchange rate to" in text.lower() or "exchange" in text.lower():
            return self.exchange_api.get_exchange_rate(text)
        elif "joke" in text.lower() or "funny" in text.lower():
            return self.joke_api.get_joke()
        elif "trivia" in text.lower() or "quiz" in text.lower():
            return self.trivia_api.fetch_trivia()
        elif "weather" in text.lower() or "weather in" in text.lower():
            return self.weather_api.get_weather(text)
        else:
            return response