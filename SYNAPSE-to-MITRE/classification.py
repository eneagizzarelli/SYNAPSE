import os
import sys
import pickle
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from mitreattack.stix20 import MitreAttackData

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

SYNAPSE_to_MITRE_path = "/home/enea/SYNAPSE/SYNAPSE-to-MITRE/"
enterprise_attack_path = SYNAPSE_to_MITRE_path + "data/enterprise-attack/enterprise-attack.json"
logs_path = "/home/enea/SYNAPSE/logs/"

# initialize MITRE ATT&CK data object
mitre_attack_data = MitreAttackData(enterprise_attack_path)

def attack_happened(classification_file, client_ip):
    """
    Make AI decide if an attack happened given a classification history file.

    Parameters:
    str: classification filename string.
    str: client IP address string.

    Returns:
    bool: True if an attack happened, False otherwise.
    """
    
    with open(logs_path + client_ip + "/" + client_ip + "_attacks/" + classification_file, "r", encoding="utf-8") as classification_history_file:
        classification_history = classification_history_file.read()

        # classification messages initialization
        classification_messages = [{"role": "system", "content": "Given the following log of commands executed in a terminal by a user with the corresponding terminal outputs, classify it as benign or malicious. Output 'True' if you think that an attack or an attempt of an attack happened in the command inserted by the user. Output 'False' if you think nothing related to an attack happened.\n" + 
        "Examples: \n" + 
        "enea@datalab:~$ ls\n" +
        "Desktop  Documents  Downloads  Music  Pictures  Videos\n" +
        "enea@datalab:~$ cd Desktop\n" +
        "enea@datalab:~/Desktop$ exit\n" +
        "logout\n\n" +
        "Answer: False\n\n" +

        "enea@datalab:~$ mysql\n" +
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
        "enea@datalab:~$ exit\n\n" +
        
        "Answer: True\n\n"}]

        # append classification history to classification messages
        classification_messages.append({"role": "user", "content": classification_history})

        # generate a response about attack happening or not by contacting AI
        response = generate_response(classification_messages)

        if "True" in response["content"]:
            return True
        return False

def get_sentence(classification_file, client_ip):
    """
    Get an AI generated unstructured CTI sentence starting from command logs.

    Parameters:
    str: classification filename string.
    str: client IP address string.

    Returns:
    str: unstructured CTI sentence string.
    """
        
    with open(logs_path + client_ip + "/" + client_ip + "_attacks/" + classification_file, "r", encoding="utf-8") as classification_history_file:
        classification_history = classification_history_file.read()

        # classification messages initialization
        classification_messages = [{"role": "system", "content": "Given the following log of commands executed in a terminal by a user, you need to take in mind that it corresponds to an attack. " +
                                    "You have to generate a brief sentence that describes the attack. " +
                                    "Be aware that your summary will be mapped to the MITRE ATT&CK database using a specific ML model trained on a specific dataset. " +
                                    "Try to use words in a way that the automatic mapping is accurate. " +
                                    "The dataset is composed of the following fields: 'technique label', 'sub-technique label', 'technique name', 'sentence'." +
                                    "The mapping will be done using the 'sentence' field, passing to the model the summary you generated. " +
                                    "Here there are few examples from the dataset to let you understand how sentences should be structured: \n" +
                                    "1. 'Adversaries may destroy data and files on specific systems or in large numbers on a network to interrupt availability to systems, services, and network resources.'\n" +
                                    "2. 'Adversaries may delete or modify artifacts generated within systems to remove evidence of their presence or hinder defenses.'\n" +
                                    "3. 'Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries.'\n" +
                                    "4. 'Adversaries may insert, delete, or manipulate data at rest in order to manipulate external outcomes or hide activity.'\n" +
                                    "5. 'Adversaries may attempt to make an executable or file difficult to discover or analyze by encrypting, encoding, or otherwise obfuscating its contents on the system or in transit.'\n" +
                                    "6. 'Adversaries may exploit software vulnerabilities in an attempt to elevate privileges.'\n" +
                                    "Be aware: you MUST be careful about each single word you use. " +
                                    "The model will output a mapping based on the words you produce, so try to avoid using misleading words that can bring the model to output the wrong result. " +
                                    "Try to use just words that are strictly related to the attack you are summarizing.\n\n"}]

        # append classification history to classification messages
        classification_messages.append({"role": "user", "content": classification_history})

        # generate a response about the unstructured CTI sentence by contacting AI
        response = generate_response(classification_messages)
        
        return response["content"]

def get_classifications(text):
    """
    Get top three MITRE ATT&CK IDs starting from an unstructured CTI sentence.

    Parameters:
    str: unstructured CTI sentence string.

    Returns:
    list[Any]: list of MITRE ATT&CK ID strings.
    """
        
    with open(SYNAPSE_to_MITRE_path + 'ml_model/MLP_classifier.sav', 'rb') as file:
        vectorizer, classifier = pickle.load(file)

    lemmatizer = WordNetLemmatizer()
    ps = porter.PorterStemmer()

    word_list = word_tokenize(text)

    lemmatized_list = [lemmatizer.lemmatize(w) for w in word_list]
    stemmed_list = [ps.stem(w) for w in lemmatized_list]
    preprocessed_text = ' '.join(stemmed_list)
    text_vectorized = vectorizer.transform([preprocessed_text])

    probabilities = classifier.predict_proba(text_vectorized)
    top_3_indices = np.argsort(probabilities[0])[-3:][::-1]
    top_3_labels = [classifier.classes_[index] for index in top_3_indices]

    return top_3_labels

def get_attack_objects(attack_ids):
    """
    Get MITRE ATT&CK objects starting from top three attack IDs.

    Parameters:
    list[Any]: list of attack ID strings.

    Returns:
    list[object]: MITRE ATT&CK objects.
    """
        
    # get MITRE ATT&CK object by attack ID
    attack_objects = [mitre_attack_data.get_object_by_attack_id(str(attack_id), "attack-pattern") for attack_id in attack_ids]

    return attack_objects

def print_attack_objects_to_file(attack_objects, sentence, client_ip):
    """
    Print MITRE ATT&CK objects to a file.

    Parameters:
    list[object]: MITRE ATT&CK objects.
    str: unstructured CTI sentence string.
    str: client IP address string.

    Returns: 
    int: current attack directory number.
    """
    
    attack_path = logs_path + client_ip + "/" + client_ip + "_attacks/"
    count_attack_directories = 0

    # count total number of attack files to create a new one with correct name numbering
    for item in os.listdir(attack_path):
        if os.path.isdir(attack_path + item) and item.startswith(client_ip + "_attack_"):
            count_attack_directories += 1

    current_attack_path = attack_path + client_ip + "_attack_" + str(count_attack_directories) + "/"
    count_current_attack_file = 0

    # create directory for the current attack
    os.mkdir(current_attack_path)

    # for each attack object
    for attack_object in attack_objects:
        # open/create new attack file
        with open(current_attack_path + client_ip + "_attack_" + str(count_attack_directories) + "_mapping_" + str(count_current_attack_file) + ".txt", 'w') as attack_file:
            original_stdout = sys.stdout
            sys.stdout = attack_file

            # print unstructured CTI sentence to file
            print("Unstructured CTI: " + sentence + "\n")

            # print MITRE ATT&CK object to file
            mitre_attack_data.print_stix_object(attack_object, pretty=True)

            sys.stdout = original_stdout

            # increment attack file number for the next file
            count_current_attack_file += 1

    return count_attack_directories

def rename_classification_history(classification_file, attack_directory_number, client_ip):
    """
    Rename and move classification history into attack history file.

    Parameters:
    str: classification filename string.
    int: attack file number.
    str: client IP address string.

    Returns: none.
    """

    attack_path = logs_path + client_ip + "/" + client_ip + "_attacks/"
    current_attack_path = attack_path + client_ip + "_attack_" + str(attack_directory_number) + "/"

    if os.path.exists(attack_path + classification_file):
        os.rename(attack_path + classification_file, current_attack_path + client_ip + "_attack_history_" + str(attack_directory_number) + ".txt")

def remove_classification_history(classification_file, client_ip):
    """
    Remove classification history file.

    Parameters:
    str: classification filename string.
    str: client IP address string.

    Returns: none.
    """

    attack_path = logs_path + client_ip + "/" + client_ip + "_attacks/"

    if os.path.exists(attack_path + classification_file):
        os.remove(attack_path + classification_file)