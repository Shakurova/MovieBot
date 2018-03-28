# -*- coding: utf-8 -*-

import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity

# from intent import phrases
from gensim.models import KeyedVectors

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = KeyedVectors.load_word2vec_format('../../wg3-semantic_space_models/GoogleNews-vectors-negative300.bin', binary=True)


import string
import re

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from stop_words import get_stop_words
english_stopwords = get_stop_words('en')

LETTERS = string.ascii_lowercase
wordnet_lemmatizer = WordNetLemmatizer()


def normalize(text):
    """ Normalization function. """
    # 1. Lowercase
    text_text = text.lower()

    # 2. Remove non-letters
    letters_only = ''
    for _c in text_text:
        if _c in LETTERS:
            letters_only += _c
        else:
            letters_only += ' '

    # 3. Remove multiple spaces
    while '  ' in letters_only:
        letters_only = letters_only.replace('  ', ' ')

    # 4. Tokenization
    word_list = word_tokenize(letters_only)

    # 5. Lemmatization
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list]

    # 6. Remove stop words
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list if word not in english_stopwords]

    return ' '.join(word_list)



def makeFeatureVec(words, model, num_features):
    # Function to average all of the word vectors in a given
    # paragraph
    #
    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((num_features,), dtype="float32")
    #
    nwords = 0.
    #
    # Index2word is a list that contains the names of the words in
    # the model's vocabulary. Convert it to a set, for speed
    index2word_set = set(model.index2word)
    #
    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec,model[word])
    #
    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec,nwords)
    return featureVec


def getAvgFeatureVecs(reviews, model, num_features):
    # Given a set of reviews (each one a list of words), calculate
    # the average feature vector for each one and return a 2D numpy array
    #
    # Initialize a counter
    counter = 0.
    #
    # Preallocate a 2D numpy array, for speed
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    #
    # Loop through the reviews
    for review in reviews:
       #
       # Print a status message every 1000th review
       if counter%1000. == 0.:
           print ("Review %d of %d" % (counter, len(reviews)))
       #
       # Call the function (defined above) that makes average feature vectors
       reviewFeatureVecs[counter] = makeFeatureVec(review, model, num_features)
       #
       # Increment the counter
       counter = counter + 1.
    return reviewFeatureVecs


def calculate_intent(self, message):
    print(message.split())
    message_vec = self.makeFeatureVec(message.split(), self.model, self.model.vector_size)
    # calculate an averaged vector for all reviews i
    intent_type = ''
    return intent_type


if __name__ == '__main__':

    recommendation = ['Could you recommend me a movie similar to movie?', 'Do you have any suggestions for me?',
                      'Do you have any recommendations?',
                      'Can you advise me a movie?', 'I need your advice']
    score = ['What is the movie rating?', 'What is the movie score?', 'How was the movie scored?']
    review = ['What is your opinion on this movie?', 'What is your impression?', 'What do you think about the movie?',
              'What is your point of view on this movie?', 'Can you give me a movie review?']

    train = {}
    train['recommendation'] = recommendation
    train['score'] = score
    train['review'] = review

    clean_train_reviews = []
    for review in train["review"]:
        clean_train_reviews.append(normalize(review).split())

    print(clean_train_reviews)

    trainDataVecs = getAvgFeatureVecs(clean_train_reviews, model, 300)

    print(trainDataVecs)
    # recommendation = getAvgFeatureVecs([normalize(r).split() for r in phrases.recommendation], model, 200)
    # templates = getAvgFeatureVecs([x[0] for x in questions_answers], model, model.vector_size)