import json
from difflib import get_close_matches
import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import wolframalpha
from abc import ABC, abstractmethod
from fuzzywuzzy import fuzz  # Untuk pencocokan fuzzy
from fuzzywuzzy import process

# Abstract Class sebagai interface dasar chatbot
class ChatbotBase(ABC):
    @abstractmethod
    def listen(self):
        pass
    
    @abstractmethod
    def respond(self, text: str):
        pass
    
    @abstractmethod
    def talk(self, response: str):
        pass


# Class untuk TTS dan Speech Recognition
class SpeechHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "I couldn't understand that."
        except sr.RequestError:
            return "Speech Recognition service is down."

    def talk(self, response: str):
        print(f"Chatbot: {response}")
        self.engine.say(response)
        self.engine.runAndWait()


# Class utama Chatbot, menggunakan inheritance dari ChatbotBase
class Chatbot(ChatbotBase):
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.wolfram_app_id = "2W5T47-QG4EQPYKP6"  # API Wolfram
        self.wolfram_url = "http://api.wolframalpha.com/v1/result"  # Endpoint Instant Calculator API
        self.intents = self.load_intents("intents.json")
        self.threshold = 60
        
    def load_intents(self, filepath):
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {filepath} not found.")
            return {"intents": []}
        
    def match_intent(self, user_input):
        user_input = user_input.lower()
        best_match = None
        highest_score = 0
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Calculate similarity score
                similarity_score = fuzz.partial_ratio(user_input, pattern.lower())
                if similarity_score > self.threshold and similarity_score > highest_score:
                    highest_score = similarity_score
                    best_match = intent
        
        return best_match
        
    def listen(self):
        return self.speech_handler.listen()
    
    def generate_response(self, intent):
        return intent['responses'][0]  # Return the first response as default

    def respond(self, text: str):
        matched_intent = self.match_intent(text)
        
        if matched_intent:
            return self.generate_response(matched_intent)
        elif "wikipedia" in text.lower():
            return self.search_wikipedia(text)
        elif "wolfram" in text.lower():
            return self.search_wolframalpha(text)
        else:
            return "I can answer basic queries, fetch information from Wikipedia, or use Wolfram Alpha."

    def search_wikipedia(self, query: str):
        try:
            query = query.lower().replace("wikipedia", "").strip()
            if not query:
                return "Please specify what you want to search on Wikipedia."
            summary = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"There are multiple results for your query: {e.options[:5]}"
        except wikipedia.exceptions.PageError:
            return "I couldn't find anything on Wikipedia for your query."
        except Exception:
            return "An error occurred while searching Wikipedia."
    
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
        

    def talk(self, response: str):
        self.speech_handler.talk(response)


# Polimorfisme: Menambahkan fitur berbeda melalui inheritance
class AdvancedChatbot(Chatbot):
    def respond(self, text: str):
        response = super().respond(text)
        if "your name" in text.lower():
            return "I'm your intelligent assistant!"
        elif "thank you" in text.lower():
            return "You're welcome!"
        else:
            return response


# Program Utama
if __name__ == "__main__":
    chatbot = AdvancedChatbot()
    print("Chatbot is ready to assist you. Say something!")
    
    while True:
        try:
            user_input = chatbot.listen()
            print(f"You: {user_input}")
            if "exit" in user_input.lower():
                chatbot.talk("Goodbye!")
                break
            response = chatbot.respond(user_input)
            chatbot.talk(response)
        except KeyboardInterrupt:
            print("\nChatbot terminated.")
            break
