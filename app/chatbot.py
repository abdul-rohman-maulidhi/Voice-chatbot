import random
import json
from fuzzywuzzy import fuzz
from app.chatbot_base import ChatbotBase
from app.speech_handler import SpeechHandler

class Chatbot(ChatbotBase):
    def __init__(self):
        self.speech_handler = SpeechHandler()
        
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
        threshold = 50
        intents = self.load_intents("./app/data/intents.json")
        
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # Calculate similarity score
                similarity_score = fuzz.partial_ratio(user_input, pattern.lower())
                if similarity_score > threshold and similarity_score > highest_score:
                    highest_score = similarity_score
                    best_match = intent
        
        return best_match
    
    def generate_response(self, intent):
        if intent["tag"] == "help":
            return "\n".join(intent["responses"]) 
        else:
            return random.choice(intent["responses"])  
        
    def listen(self):
        return self.speech_handler.listen()
    
    def respond(self, text: str):
        matched_intent = self.match_intent(text)
        if matched_intent:
            return self.generate_response(matched_intent)
        else:
            return "Use \"help\" to see more information"
    
    def talk(self, response: str):
        self.speech_handler.talk(response)

