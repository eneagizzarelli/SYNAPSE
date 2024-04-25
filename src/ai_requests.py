import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_tab_completions(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.1, max_tokens = 20, n=10)
    completions = [choice.message.content for choice in response.choices]

    print(completions)

    return completions

def complete(text, state):

    if state == 0:
        if text == "":
            return None
    
        messages = [{"role": 'system', "content": "Emulate the tab autocompletion of a Linux terminal. " + 
                 "Generate words to complete the already started one. " + 
                 "If you don't know what to answer, do not print anything. " + 
                 "Do not start in any case a conversation with the user. A terminal would not do so. " + 
                 "Start from the following text and complete it. \n"}]
        messages.append({"role": 'user', "content": text})

        completions = generate_tab_completions(messages)
        matches = [option for option in completions if option.startswith(text)]

    if state < len(matches):
        return matches[state]
    else:
        return None

    
readline.set_completer(complete)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    msg = response.choices[0].message.content
    message = {"role": 'assistant', "content": msg}
    
    return message