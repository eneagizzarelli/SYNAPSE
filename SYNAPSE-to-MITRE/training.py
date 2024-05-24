import os
import pickle
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, porter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import precision_recall_fscore_support, top_k_accuracy_score

model_path = "/home/enea/SYNAPSE/SYNAPSE-to-MITRE/ml-model"
dataset_path = "/home/enea/SYNAPSE/SYNAPSE-to-MITRE/data/dataset.csv"

TRAINING_SIZE = 0.80
vectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english', max_features=10000, ngram_range=(1,2))

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
    train_set_x, test_set_x, train_set_y, test_set_y = train_test_split(X, Y, test_size=(1-TRAINING_SIZE),  random_state=4)
    
    stemmatized_set = stemmatize_set(train_set_x)
    lemmatized_set = lemmatize_set(stemmatized_set)
    x_train_vectors = vectorizer.fit_transform(lemmatized_set)

    classifier.fit(x_train_vectors, train_set_y)

    print("Model has been trained!")

    stemmatized_set = stemmatize_set(test_set_x)
    lemmatized_set = lemmatize_set(stemmatized_set)
    x_test_vectors = vectorizer.transform(lemmatized_set)
    predicted = classifier.predict(x_test_vectors)
    
    precision, recall, fscore, support = precision_recall_fscore_support(test_set_y, predicted, average='weighted', zero_division=0)

    print("Results for" + name + "\n")
    print("Precision: " + str(precision) + " Recall: " + str(recall) + " F-Score: " + str(fscore) + "\n")

    try:
        os.mkdir(model_path)
    except OSError as error:
        print(error)

    filename = model_path + '/' + name + '.sav'
    pickle.dump((vectorizer, classifier), open(filename, 'wb'))

def main():
    data_df = pd.read_csv(dataset_path)
    num_classes = len(data_df['label_tec'].value_counts())

    print(num_classes)

    data_df['sentence'] = data_df['sentence'].astype(str)

    nn_clf = MLPClassifier(max_iter=1000, early_stopping=True)

    train_classifier(nn_clf, "MLP_classifier",  data_df.sentence, data_df.label_tec)

if __name__ == "__main__":
    main()