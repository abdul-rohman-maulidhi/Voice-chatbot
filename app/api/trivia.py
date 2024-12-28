import random
import requests
from fuzzywuzzy import fuzz

class TriviaApi:
    def __init__(self):
        self.current_trivia_answer = None
        self.trivia_api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
        
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