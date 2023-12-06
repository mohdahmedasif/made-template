from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_keywords_nltk(sentence):
    # Tokenize the sentence
    words = word_tokenize(sentence)

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return filtered_words

# Example usage:
sentence = "Quarterly profits at US media giant TimeWarner jumped 76% to $1.13bn (£600m) for the three months t.."
keywords_nltk = extract_keywords_nltk(sentence)
print(keywords_nltk)
