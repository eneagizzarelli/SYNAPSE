import pickle
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from sklearn.metrics import precision_recall_fscore_support

SYNAPSE_path = "/home/enea/SYNAPSE/"
SYNAPSE_to_MITRE_path = SYNAPSE_path + "SYNAPSE-to-MITRE/"

model_path = SYNAPSE_to_MITRE_path + "ml_model/"

def lemmatize_set(dataset):
    lemmatizer = WordNetLemmatizer()
    lemmatized_list = []

    for sentence in dataset:
        word_list = word_tokenize(sentence)
        lemma_list = [lemmatizer.lemmatize(w) for w in word_list]
        lemmatized_list.append(' '.join(lemma_list))

    return lemmatized_list

def stemmatize_set(dataset):
    ps = porter.PorterStemmer()
    stemmatize_list = []

    for sentence in dataset:
        word_list = word_tokenize(sentence)
        stemma_list = [ps.stem(w) for w in word_list]
        stemmatize_list.append(' '.join(stemma_list))

    return stemmatize_list

def main():
    real_data = pd.read_csv(SYNAPSE_to_MITRE_path + "data/my_dataset.csv")
    
    real_data['sentence'] = real_data['sentence'].astype(str)

    real_sentences = real_data['sentence']
    real_labels = real_data['label_tec']

    with open(SYNAPSE_to_MITRE_path + 'ml_model/MLP_classifier.sav', 'rb') as model_file:
        vectorizer, classifier = pickle.load(model_file)

    stemmatized_set = stemmatize_set(real_sentences)
    lemmatized_set = lemmatize_set(stemmatized_set)
    x_real_vectors = vectorizer.transform(lemmatized_set)

    probabilities = classifier.predict_proba(x_real_vectors)
    top_3_indices = np.argsort(probabilities, axis=1)[:, -3:]
    top_3_labels = np.array(classifier.classes_)[top_3_indices]

    top_3_correct = []

    for i in range(len(real_labels)):
        if real_labels.iloc[i] in top_3_labels[i]:
            top_3_correct.append(real_labels.iloc[i])
        else:
            top_3_correct.append("Not_in_top_3")

    top_3_correct = pd.Series(top_3_correct, index=real_labels.index)

    precision, recall, f1, _ = precision_recall_fscore_support(real_labels, top_3_correct, average='weighted', zero_division=0)

    print(f"Results on Real Data\nPrecision: {precision} Recall: {recall} F-Score: {f1}")

    
if __name__ == "__main__":
    main()