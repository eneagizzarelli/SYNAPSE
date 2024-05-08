from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from mitreattack.stix20 import MitreAttackData
import pickle
import sys
import os

from src.ai_requests import generate_response

base_path = "/home/user/SYNAPSE/"

mitre_attack_data = MitreAttackData(base_path + 'SYNAPSE-to-MITRE/' + 'data/enterprise-attack-10.1.json')

def attack_happened(client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_classification_history.txt", "r", encoding="utf-8") as classification_history_file:
        classification_history = classification_history_file.read()

        classification_messages = [{"role": "system", "content": "Given the following log of commands executed in a terminal by a user with the corresponding terminal outputs, classify it as benign or malicious. Output 'True' if you think that an attack or an attempt of an attack happened in the command inserted by the user. Output 'False' if you think nothing related to an attack happened.\n" + 
        "Examples: \n" + 
        "alex@datalab:~$ ls\n" +
        "Desktop  Documents  Downloads  Music  Pictures  Videos\n" +
        "alex@datalab:~$ cd Desktop\n" +
        "alex@datalab:~/Desktop$ exit\n" +
        "logout\n\n" +
        "Answer: False\n\n" +

        "alex@datalab:~$ mysql\n" +
        "Welcome to the MySQL monitor.  Commands end with ; or \\g.\n" +
        "Your MySQL connection id is 8\n" +
        "Server version: 8.0.28-0ubuntu0.20.04.3 (Ubuntu)\n" +
        "Type 'help;' or '\\h' for help. Type '\\c' to clear the current input statement.\n" +
        "mysql> SHOW DATABASES;\n" +
        "+--------------------+\n" +
        "| Database           |\n" +
        "+--------------------+\n" +
        "| information_schema |\n" +
        "| mysql              |\n" +
        "| performance_schema |\n" +
        "| Users              |\n" +
        "+--------------------+\n" +
        "4 rows in set (0.01 sec)\n" +
        "mysql> USE Users;\n" +
        "Database changed\n" +
        "mysql> SELECT * FROM Users WHERE UserId = 105 OR 1=1;\n" +
        "+--------+-----------------+-----------------+\n" +
        "| UserId | Username        | Password        |\n" +
        "+--------+-----------------+-----------------+\n" +
        "| 105    | admin           | admin           |\n" +
        "| 106    | root            | toor            |\n" +
        "| 107    | administrator   | password        |\n" +
        "+--------+-----------------+-----------------+\n" +
        "3 rows in set (0.00 sec)\n" +
        "mysql> \q\n" +
        "Bye\n" +
        "alex@datalab:~$ exit\n\n" +
        
        "Answer: True\n\n"}]

        classification_messages.append({"role": "user", "content": classification_history})

        response = generate_response(classification_messages)

        if "True" in response["content"]:
            return True
        return False

def get_sentence(client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_classification_history.txt", "r", encoding="utf-8") as classification_history_file:
        classification_history = classification_history_file.read()

        classification_messages = [{"role": "system", "content": "Given the following log of commands executed in a terminal by a user with the corresponding terminal outputs, you need to take in mind that it corresponds to an attack. You have to generate a brief sentence that describes the attack, without too much care about responses. The output will be mapped to the MITRE ATT&CK database. Try to use words that help the automatic mapping. \n\n"}]

        classification_messages.append({"role": "user", "content": classification_history})

        response = generate_response(classification_messages)
        
        return response["content"]

def get_classification(text):
    with open(base_path + 'SYNAPSE-to-MITRE/' + 'ml_model/MLP_classifier.sav', 'rb') as file:
        vectorizer, classifier = pickle.load(file)

    lemmatizer = WordNetLemmatizer()
    ps = porter.PorterStemmer()

    word_list = word_tokenize(text)

    lemmatized_list = [lemmatizer.lemmatize(w) for w in word_list]
    stemmed_list = [ps.stem(w) for w in lemmatized_list]
    preprocessed_text = ' '.join(stemmed_list)
    text_vectorized = vectorizer.transform([preprocessed_text])

    predicted_label = classifier.predict(text_vectorized)

    return predicted_label[0]

def get_attack_object(attack_id):
    attack_object = mitre_attack_data.get_object_by_attack_id(attack_id, "attack-pattern")

    return attack_object

def print_attack_object_to_file(attack_object, client_ip):
    count_attack_files = 0

    for attack_file in os.listdir(base_path + "logs/" + client_ip):
        if attack_file.startswith(client_ip + "_attack_"):
            count_attack_files += 1

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_attack_" + str(count_attack_files) + ".txt", 'w') as attack_file:
        original_stdout = sys.stdout

        sys.stdout = attack_file

        mitre_attack_data.print_stix_object(attack_object, pretty=True)

        sys.stdout = original_stdout

def remove_classification_history(client_ip):
    if os.path.exists(base_path + "logs/" + client_ip + "/" + client_ip + "_classification_history.txt"):
        os.remove(base_path + "logs/" + client_ip + "/" + client_ip + "_classification_history.txt")