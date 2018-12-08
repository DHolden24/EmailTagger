from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

try:
    stopword_set = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stopword_set = set(stopwords.words('english'))

char_exclusions = set(string.punctuation)
lemmatizer = WordNetLemmatizer()


def clean_string(doc_string):
    normalized_string = "".join([c for c in doc_string if c not in char_exclusions])
    normalized_string = " ".join([w for w in normalized_string.lower().split(" ") if w not in stopword_set])
    try:
        normalized_string = " ".join([lemmatizer.lemmatize(w) for w in normalized_string.split(" ")])
    except LookupError:
        import nltk
        nltk.download("wordnet")
        normalized_string = " ".join([lemmatizer.lemmatize(w) for w in normalized_string.split(" ")])
    return normalized_string
