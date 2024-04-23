import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_tab_completions(text):
    response = openai.chat.completions.create(model = model, messages = text, max_tokens = 5, n = 5)
    completions = [choice['text'].strip() for choice in response['choices']]
    return completions

def completer(text, state):
    print(text)
    completions = generate_tab_completions(text)
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