import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

def generate_tab_completions(prompt):
    response = openai.completions.create(model = "gpt-3.5-turbo-instruct", prompt = prompt, temperature = 0.1, max_tokens = 50)
    completions = response.choices[0].text.split("\n").

    return completions

def completer(text, state):
    if text == "":
        return None
    
    prompt = "Emulate the tab autocompletion of a Linux terminal. Generate many words separated by '\n' to complete the already started one. If you don't know what to answer, do not print anything. Do not start in any case a conversation with the user. A terminal would not do so. Start from the following text and complete it: " + text

    completions = generate_tab_completions(prompt)

    matches = [option for option in completions if option.startswith(text) and option != '']

    print(matches)
    print(matches[state])
    print(len(matches))

    if state < len(matches):
        return matches[state]
    else:
        return None
    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = "gpt-3.5-turbo-0125", messages = messages, temperature = 0.0, max_tokens = 800)
    msg = response.choices[0].message.content
    message = {"role": 'assistant', "content": msg}
    
    return message