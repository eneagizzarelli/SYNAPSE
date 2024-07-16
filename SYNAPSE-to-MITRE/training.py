import os
import pickle
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import precision_recall_fscore_support

SYNAPSE_path = "/home/enea/SYNAPSE/"
SYNAPSE_to_MITRE_path = SYNAPSE_path + "SYNAPSE-to-MITRE/"

model_path = SYNAPSE_to_MITRE_path + "ml_model/"

TRAINING_SIZE = 0.80

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

def train_classifier(classifier, name, X, Y):
    vectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english', max_features=10000, ngram_range=(1,2))

    train_set_x, test_set_x, train_set_y, test_set_y = train_test_split(X, Y, test_size=(1-TRAINING_SIZE),  random_state=4)
    
    stemmatized_set = stemmatize_set(train_set_x)
    lemmatized_set = lemmatize_set(stemmatized_set)
    x_train_vectors = vectorizer.fit_transform(lemmatized_set)

    classifier.fit(x_train_vectors, train_set_y)

    print("Model has been trained!")

    stemmatized_set = stemmatize_set(test_set_x)
    lemmatized_set = lemmatize_set(stemmatized_set)
    x_test_vectors = vectorizer.transform(lemmatized_set)
    probabilities = classifier.predict_proba(x_test_vectors)

    top_3_indices = np.argsort(probabilities, axis=1)[:, -3:]
    top_3_labels = np.array(classifier.classes_)[top_3_indices]

    top_3_correct = []

    for i in range(len(test_set_y)):
        if test_set_y.iloc[i] in top_3_labels[i]:
            top_3_correct.append(test_set_y.iloc[i])
        else:
            top_3_correct.append("Not_in_top_3")

    top_3_correct = pd.Series(top_3_correct, index=test_set_y.index)

    precision, recall, f1, _ = precision_recall_fscore_support(test_set_y, top_3_correct, average='weighted', zero_division=0)

    print("Results for " + name + "\n")
    print(f"Precision: {precision} Recall: {recall} F-Score: {f1}\n")

    try:
        os.mkdir(model_path)
    except OSError as error:
        print(error)

    filename = model_path + name + '.sav'
    pickle.dump((vectorizer, classifier), open(filename, 'wb'))

def main():
    data_df = pd.read_csv(SYNAPSE_to_MITRE_path + "data/dataset.csv")
    num_classes = len(data_df['label_tec'].value_counts())

    print(num_classes)

    data_df['sentence'] = data_df['sentence'].astype(str)

    # MPL Classifier
    nn_clf = MLPClassifier(max_iter=1000, early_stopping=True)
    train_classifier(nn_clf, "MLP_classifier",  data_df.sentence, data_df.label_tec)

if __name__ == "__main__":
    main()