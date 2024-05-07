from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from mitreattack.stix20 import MitreAttackData
import pickle
import os

from client_data import client_ip

base_path = "/home/user/SYNAPSE/"

mitre_attack_data = MitreAttackData(base_path + 'data/enterprise-attack-10.1.json')

prompt = {"role": "user", "content": "Given the following log of commands executed in a terminal by a user with the corresponding terminal outputs, classify it as benign or malicious. Output 'True' if you think that an attack or an attempt of an attack happened. Output 'False' if you think nothing related to an attack happened.\n" + 
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
          
          "Answer: True\n\n"}

def attack_happened():
    if os.path.exists(base_path + "logs/" + client_ip + "/" + client_ip + "_classification_history.txt"):
        classification_history_file = open(base_path + "logs/" + client_ip + "/" + client_ip + "_classification_history.txt", "r", encoding="utf-8")

        classification_history = classification_history_file.read()

        print(classification_history)

        classification_history_file.close()


    return False

def get_sentence():
    return ""

def get_classification(text):
    with open(base_path + 'ml_model/MLP_classifier.sav', 'rb') as file:
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

def print_attack_object(attack_object):
    mitre_attack_data.print_stix_object(attack_object, pretty=True)