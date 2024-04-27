from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from mitreattack.stix20 import MitreAttackData
import pickle

base_path = "/home/user/SYNAPSE/"

mitre_attack_data = MitreAttackData(base_path + 'data/enterprise-attack-10.1.json')

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