import openai
import readline
from dotenv import dotenv_values

config = dotenv_values("/home/enea/.env")
openai.api_key = config["OPENAI_API_KEY"]

gpt_4o_model = "gpt-4o"
gpt_3_5_turbo_0125_model = "gpt-3.5-turbo-0125"

def generate_response(messages):
    response = openai.chat.completions.create(model = gpt_4o_model, messages = messages, temperature = 0.1, max_tokens = 800)

    print(response.choices[0].message)

    # possible presence of ``` in the response
    msg = response.choices[0].message.content

    # cleaning response
    msg_cleaned = msg.replace('\n```\nenea', '\nenea').strip()
    msg_cleaned = msg.replace('\n\nenea', '\nenea').strip()
    msg_cleaned = msg.replace('```', '').strip()
    
    message = {"role": 'assistant', "content": msg_cleaned}
    
    return message

def generate_tab_completions(messages):
    response = openai.chat.completions.create(model = gpt_3_5_turbo_0125_model, messages = messages, temperature = 0.0, max_tokens = 5)

    completions = response.choices[0].message.content

    return completions

# TODO: to improve
def completer(text, state):
    if state == 0:
        if text == "":
            return None

        messages = [{"role": 'system', "content": "Emulate the tab autocompletion of a Linux terminal. " + 
                     "Generate words separated by " " to complete the already started one. " + 
                     "If you don't know what to answer, do not print anything. " + 
                     "Do not start in any case a conversation with the user. A terminal would not do so. " + 
                     "Start from the following text and generate the completed word. \n"}]
        messages.append({"role": 'user', "content": text})

        completions = generate_tab_completions(messages)
        
        if len(completions.split(" ")) > 1:
            return None
        else:
            return completions

    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')