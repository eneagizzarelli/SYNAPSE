import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_tab_completions(text):
    print("ciao")
    response = openai.chat.completions.create(model = model, messages = text, temperature = 0.0, max_tokens = 500, n = 5)
    print("ciao1")
    completions = [choice.message.strip() for choice in response.choices]

    return completions

def completer(text, state):
    completions = generate_tab_completions(text)
    print("COMPLETIONS: [" + completions + "]")

    matches = [option for option in completions if option.startswith(text)]
    
    if state < len(matches):
        return matches[state]
    else:
        return None
    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    terminal_msg = response.choices[0].message.content
    terminal_message = {"role": 'assistant', "content": terminal_msg}
    
    return terminal_message