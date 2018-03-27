# CCMLWI Chatbot assignment

We developed a movie chatbot. It can give you a movie score, review for a movie or recommend a movie similar to the one you mentioned.

## Chat bot abilities
Our chatbot can handle greetings and goodbyes and can give an introduction of its abilities. ###todo
Our chatbot can manage three types of domain specific questions: give movie score, give review and recommend similar movie.

# How it works?
It uses amazon film dataset https://snap.stanford.edu/data/web-Movies.html and https://www.themoviedb.org API[https://www.themoviedb.org].

The dataset contains movie id, reviewer id, reviewer profile name, review helpfulness and score metrics, review summary and review text.
To map the movie name with movie id we wrote a crawler for amazon website.

```
their_greetings = ['hi', 'hello', 'good morning']
their_goodbyes = ['goodbye', 'bye', 'good-bye', 'see you later', 'cya']
their_score = ['score', 'rating', 'grade', 'average', 'socre', 'ratings', 'averge', 'avearge']
their_recommendation = ['recommend', 'recommendation', 'suggest', 'suggestion', 'propose', 'advise', 'reccomend']
their_review = ['review', 'opinion', 'impression', 'view', 'think', 'opionion', 'veiws']
```

We enlarged the keyword vocabulary using word2vec most similar words and included misspellings because they often occur in chats.

## Intent detection

We predefined search queries for each of the intents and for each of user question we measure the semantic distance between averaged word2vec vectors.
To identify the intent we use word2vec averaged vectors.

## Movie title extraction
To extract the movie title from the user query we use bigrams and minumal levenstain distance

## Demo
