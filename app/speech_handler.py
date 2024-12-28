import pyttsx3
import speech_recognition as sr

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