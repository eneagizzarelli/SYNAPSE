import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

current_state = 0

def generate_tab_completions(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.1, max_tokens = 20)
    completions = response.choices[0].message.content.split(" ")

    return completions

def completer(text, state):
    global current_state
    
    if state == 0:
        if text == "":
            current_state = 0
            return None
    
        messages = [{"role": 'system', "content": "Emulate the tab autocompletion of a Linux terminal. " + 
                 "Generate many DIFFERENT words separated by ' ' to complete the already started one. " + 
                 "If you don't know what to answer, do not print anything. " + 
                 "Do not start in any case a conversation with the user. A terminal would not do so. " + 
                 "Start from the following text and complete it. \n"}]
        messages.append({"role": 'user', "content": text})

        completions = generate_tab_completions(messages)
        matches = [option for option in completions if option.startswith(text)]

    return matches[state]
    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    msg = response.choices[0].message.content
    message = {"role": 'assistant', "content": msg}
    
    return message