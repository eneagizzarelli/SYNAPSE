import openai
from dotenv import dotenv_values
import readline

from client_data import client_ip

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

base_path = "/home/user/SYNAPSE/logs/"

def generate_tab_completions(messages):
    print(messages)
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 5)
    completions = response.choices[0].message.content

    return completions

def completer(text, state):
    if state == 0:
        if text == "":
            return None

        tab_completion_history = open(base_path + "tab_completion_history.txt", "a+", encoding="utf-8")
        tab_completion_history.seek(0)
        tab_completion_history_content = tab_completion_history.read()

        messages = [{"role": 'system', "content": "Emulate the tab autocompletion of a Linux terminal. " + 
                    "Generate words separated by " " to complete the already started one. " + 
                    "If you don't know what to answer, do not print anything. " + 
                    "Do not start in any case a conversation with the user. A terminal would not do so. \n" + 
                    "To generate completions, consider also the following results of ls commands: \n" + tab_completion_history_content + "\n" +
                    "Start from the following text and complete it. \n"}]
        messages.append({"role": 'user', "content": text})

        completions = generate_tab_completions(messages)
        
        if len(completions.split(" ")) > 1:
            tab_completion_history.close()
            return None
        else:
            tab_completion_history.close()
            return completions

    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    msg = response.choices[0].message.content
    message = {"role": 'assistant', "content": msg}
    
    return message