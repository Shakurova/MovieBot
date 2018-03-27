# CCMLWI Chatbot assignment

This is a movie chatbot. It uses amazon film dataset https://snap.stanford.edu/data/web-Movies.html and https://www.themoviedb.org API.

The dataset contains movie id, reviewer id, reviewer profile name, review helpfulness and score metrics, review summary and review text.
To map the movie name with movie id we wrote a crawler for amazon website.


## Chat bot abilities
Our chatbot can handle greetings and goodbyes and can give an introduction of its abilities. ###todo
Our chatbot can manage three types of domain specific questions: give movie score, give review and recommend similar movie.

## Intent detection
We predefined search queries for each of the intents and for each of user question we measure the semantic distance between averaged word2vec vectors.
To identify the intent we use word2vec averaged vectors.

## Movie title extraction
To extract movie title from the user query we use bigrams and minumal levenstain distance


## Do something else than just querying a database

