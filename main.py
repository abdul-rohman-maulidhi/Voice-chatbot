import eel
from chatbot import Chatbot, AdvancedChatbot

# Initialize Eel
eel.init('web')

chatbot = AdvancedChatbot()

# Expose Python functions to JavaScript
@eel.expose
def get_response(user_input):
    response = chatbot.respond(user_input)
    # chatbot.talk(response)
    return response


@eel.expose
def listen_and_respond():
    user_input = chatbot.speech_handler.listen()
    response = chatbot.respond(user_input)
    # chatbot.talk(response)
    return {"user_input": user_input, "response": response}


# Start the Eel app
if __name__ == "__main__":
    eel.start('index.html', size=(800, 600))