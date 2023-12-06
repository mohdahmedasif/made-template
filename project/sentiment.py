import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    # Tokenize the headline
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Initialize SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Calculate sentiment scores
    compound_score = sia.polarity_scores(' '.join(filtered_tokens))['compound']

    # Classify sentiment based on compound score
    if compound_score >= 0.05:
        sentiment = 'Positive'
    elif compound_score <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    # Return results
    return compound_score

# Example usage
#text = "Stock market reaches new highs as investors remain optimistic"
#print(analyze_sentiment(text))
