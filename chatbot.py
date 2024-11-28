import speech_recognition as sr
import pyttsx3
import wikipedia
from abc import ABC, abstractmethod

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

    def listen(self):
        return self.speech_handler.listen()

    def respond(self, text: str):
        if "wikipedia" in text.lower():
            return self.search_wikipedia(text)
        elif "hello" in text.lower():
            return "Hello! How can I assist you today?"
        elif "how are you" in text.lower():
            return "I'm just a program, but I'm functioning as expected!"
        else:
            return "I can only answer basic queries or fetch information from Wikipedia."

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
