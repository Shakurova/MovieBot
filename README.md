# CCMLWI Chatbot assignment

We developed a movie chatbot for Telegram. It can give you a movie score, review for a movie or recommend a movie similar to the one you mentioned.

We used [Python Telegram bot API](https://github.com/python-telegram-bot/python-telegram-bot), code is written on Python 3.5.

## Chat bot abilities
Our chatbot can handle greetings and goodbyes and can give an introduction of its abilities. ###todo
Our chatbot can manage three types of domain specific questions: give movie score, give review and recommend similar movie.

# How does it work?
The chatbot uses [Amazon movie reviews dataset](https://snap.stanford.edu/data/web-Movies.html) to get movies reviews and
[MovieDb API](https://www.themoviedb.org) to get recommendations and movie ratings.

Amazon movie reviews dataset contains movie id, reviewer id, reviewer profile name, review helpfulness and score metrics, review summary and review text.
To map the movie name with movie id we wrote a crawler for [amazon website](https://www.amazon.com/product-reviews/).

We enlarged the keyword vocabulary using **word2vec most similar words** and included **misspellings** because they often occur in chats:
```
their_greetings = ['hi', 'hello', 'good morning']
their_goodbyes = ['goodbye', 'bye', 'good-bye', 'see you later', 'cya']
their_score = ['score', 'rating', 'grade', 'average', 'socre', 'ratings', 'averge', 'avearge']
their_recommendation = ['recommend', 'recommendation', 'suggest', 'suggestion', 'propose', 'advise', 'reccomend']
their_review = ['review', 'opinion', 'impression', 'view', 'think', 'opionion', 'veiws']
```

## Intent detection

We predefined search queries for each of the intents and for each of user question we measure the **semantic distance between averaged word2vec vectors**.

## Movie title extraction
To extract the movie title from the user query we calculate all possible ngams (from unigram to 5-gram) and then
for each film in the dataset for each **ngram** we compute the **levenstain edit distance**. If distance is small enough (smaller than len(movie) / 3)
we assume that the movie was mentioned in the user query.
This approach allows us not only to look up the full titles but also take into account possible misspellings and title variations.

## Demo
