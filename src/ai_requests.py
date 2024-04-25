import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_tab_completions(messages):
    print(messages)
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 5)
    completions = response.choices[0].message.content

    return completions

def completer(text, state):
    if state == 0:
        if text == "":
            return None

        messages = [{"role": 'system', "content": "Emulate the tab autocompletion of a Linux terminal. " + 
                    "Generate words separated by " " to complete the already started one. " + 
                    "If you don't know what to answer, do not print anything. " + 
                    "Do not start in any case a conversation with the user. A terminal would not do so. \n" + 
                    "Start from the following text and complete it. \n"}]
        messages.append({"role": 'user', "content": text})

        completions = generate_tab_completions(messages)
        
        if len(completions.split(" ")) > 1:
            return None
        else:
            return completions

    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    msg = response.choices[0].message.content
    message = {"role": 'assistant', "content": msg}
    
    return message