import json
import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import random
import webbrowser
from abc import ABC, abstractmethod
from fuzzywuzzy import fuzz

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
        
        self.exchange_api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        
        self.joke_api_url = "https://v2.jokeapi.dev/joke/Any"
        
        self.intents = self.load_intents("./app/intents.json")
        self.threshold = 50
        
        self.current_trivia_answer = None
        self.trivia_api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
        
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
        if intent["tag"] == "help":
            return "\n".join(intent["responses"])  # Gabungkan semua respons
        else:
            return random.choice(intent["responses"])  # Pilih satu respons secara acak # Return the first response as default

    def respond(self, text: str):
        if self.current_trivia_answer:  # Check if a trivia question is active
            return self.verify_trivia_answer(text)
        
        matched_intent = self.match_intent(text)
        
        if matched_intent:
            return self.generate_response(matched_intent)
        elif "open browser" in text.lower():
            return self.handle_open_browser(text)
        elif "wikipedia" in text.lower() or "wiki" in text.lower():
            return self.search_wikipedia(text)
        elif "wolfram" in text.lower() or "solve" in text.lower() or "calculate" in text.lower():
            return self.search_wolframalpha(text)
        elif "exchange rate to" in text.lower():
            return self.get_exchange_rate(text)
        elif "joke" in text.lower() or "funny" in text.lower():
            return self.get_joke()
        elif "trivia" in text.lower() or "quiz" in text.lower():
            return self.fetch_trivia()
        else:
            return "Use \"help\" to see more information"
        
    def handle_open_browser(self, text: str):
        """
        Handles requests to open popular websites in the browser.
        """
        if "youtube" in text.lower():
            return self.open_website("https://www.youtube.com", "YouTube")
        elif "maps" in text.lower():
            return self.open_website("https://www.google.com/maps", "Google Maps")
        elif "classroom" in text.lower():
            return self.open_website("https://classroom.google.com", "Google Classroom")
        else:
            return "I couldn't find the specified site. Please say 'open browser YouTube', 'open browser Maps', or 'open browser Classroom'."
        
    def open_website(self, url, site_name):
        """
        Open a website in the default web browser.
        """
        try:
            webbrowser.open(url)
            return f"Opening {site_name} in your browser..."
        except Exception as e:
            return f"Sorry, I couldn't open {site_name}. Error: {e}"

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
        
    def get_joke(self):
        # Mengambil lelucon dari Joke API
        url = self.joke_api_url
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
        
    def fetch_trivia(self):
        """
        Fetch a random trivia question using Open Trivia DB API.
        """
        url = self.trivia_api_url
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            trivia_data = response.json()

            if trivia_data["response_code"] == 0:
                question = trivia_data["results"][0]
                question_text = question["question"]
                options = question["incorrect_answers"] + [question["correct_answer"]]
                random.shuffle(options)

                # Save the correct answer for verification
                self.current_trivia_answer = question["correct_answer"]

                trivia_response = f"Here's a trivia question: {question_text} "
                trivia_response += " Options: " + ", ".join(options)
                return trivia_response
            else:
                return "I couldn't fetch a trivia question at the moment. Try again later."
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching trivia: {e}"

    def verify_trivia_answer(self, user_input):
        """
        Verifies if the user's answer matches the correct trivia answer.
        """
        if fuzz.ratio(user_input.lower(), self.current_trivia_answer.lower()) > 80:
            response = "Correct! Well done!"
        else:
            response = f"Sorry, that's incorrect. The correct answer was: {self.current_trivia_answer}."
        
        self.current_trivia_answer = None  # Reset trivia state after verifying the answer
        return response


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