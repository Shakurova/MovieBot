import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity

from intent import phrases
from normalization import normalize


class IntentFinder():
    def __init__(self, questions_answers, model=None):
        self.questions_answers = questions_answers
        if model != None:
            self.model = model
            self.intent_vectors = self.getAvgFeatureVecs([x[0] for x in self.questions_answers], self.model, self.model.vector_size)

    def find_intent_answers(self, message):
        if self.model != None:
            return self.model_distance(message)
        else:
            return self.nr_of_similar_words_score(message)

    def nr_of_similar_words_score(self, message):
        text = message.split()
        # We substract to make lower scores better, because other (distance) metrics work like that
        return len(text) - sum(text.count(m) for m in self.questions_answers[1])

    def model_distance(self, message, treshold_distance=0.8):
        message_vec = self.makeFeatureVec(message.split(), self.model, self.model.vector_size)
        best_score = sys.maxsize
        best_score_index = None
        if not any(np.isnan(message_vec)):
            for i in range(len(self.intent_vectors)):
                intent_vector = self.intent_vectors[i]
                # We substract to make lower scores better, because other (distance) metrics work like that
                score = 1 - cosine_similarity(message_vec.reshape(1, -1), intent_vector.reshape(1, -1))
                if score < best_score:
                    best_score = score
                    best_score_index = i
                print("Model distance between '{}' and {}: {}".format(message, phrases.questions_answers[i][0], score))

            return self.questions_answers[best_score_index][1] if best_score < treshold_distance else None
        else:
            return None

    def makeFeatureVec(self, words, model, num_features):
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
                featureVec = np.add(featureVec, model[word])
        #
        # Divide the result by the number of words to get the average
        featureVec = np.divide(featureVec, nwords)
        return featureVec

    def getAvgFeatureVecs(self, message, model, num_features):
        # Given a set of reviews (each one a list of words), calculate
        # the average feature vector for each one and return a 2D numpy array
        #
        # Initialize a counter
        counter = 0
        #
        # Preallocate a 2D numpy array, for speed
        reviewFeatureVecs = np.zeros((len(message), num_features), dtype="float32")
        #
        # Loop through the reviews
        for review in message:
            #
            # Print a status message every 1000th review
            if counter % 1000. == 0.:
                print
                "Review %d of %d" % (counter, len(message))
            #
            # Call the function (defined above) that makes average feature vectors
            reviewFeatureVecs[counter] = self.makeFeatureVec(review, model, num_features)
            #
            # Increment the counter
            counter = counter + 1
        return reviewFeatureVecs
