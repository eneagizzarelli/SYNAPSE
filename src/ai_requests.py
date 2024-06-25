import openai
import readline
from dotenv import dotenv_values

# load .env file and configure OpenAI API key
config = dotenv_values("/home/enea/.env")
openai.api_key = config["OPENAI_API_KEY"]

# OpenAI models
gpt_4o_model = "gpt-4o"
gpt_3_5_turbo_0125_model = "gpt-3.5-turbo-0125"

def generate_response(messages):
    """
    Generate AI response based on the entire history file.

    Parameters:
    list[dict[str, str]]: dictionary of messages.

    Returns:
    dict[str, str]: dictionary of AI response.
    """

    # create AI response and extract the content
    response = openai.chat.completions.create(model = gpt_4o_model, messages = messages, temperature = 0.1, max_tokens = 800)
    msg = response.choices[0].message.content

    # cleaning unwanted ``` from the response
    msg_cleaned = msg.replace('```', '').strip()
    
    # cleaning unwanted \n\n from terminal response (but not from mysql response)
    if 'mysql>' not in msg_cleaned.split("\n"):
        msg_parts = [m for m in msg_cleaned.split("\n") if m]
        msg_cleaned = "\n".join(msg_parts)
    else:
        msg_cleaned = msg_cleaned.replace('sql\n', '')
    
    # create message response dictionary
    message = {"role": 'assistant', "content": msg_cleaned}
    
    return message

def generate_tab_completions(messages):
    """
    Generate AI tab completion response based on partial word.

    Parameters:
    list[dict[str, str]]: dictionary of messages.

    Returns:
    str: tab completed word string.
    """
    
    # create AI tab completion response and extract the content
    response = openai.chat.completions.create(model = gpt_3_5_turbo_0125_model, messages = messages, temperature = 0.0, max_tokens = 5)
    completions = response.choices[0].message.content

    return completions

# TODO: complete and improve
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

# Comment/Uncomment the following two lines to disable/enable (sperimental) tab completion leveraging AI
# readline.set_completer(completer)
# readline.parse_and_bind('tab: complete')