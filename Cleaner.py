from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

# Try to get the set of stopwords, if it fails download the set and retry
# You can add more words to the set if desired
try:
    stopword_set = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stopword_set = set(stopwords.words('english'))

# Get the set of characters to exclude, this is mostly for punctuation, but others can be added
char_exclusions = set(string.punctuation)
lemmatizer = WordNetLemmatizer()

def clean_string(doc_string):
    ''' Take a string and return it after its lemmatized with punctuation and stopwords removed
    
    Key Word Arguments:
    doc_string -- The string to be cleaned
    '''
    
    # Remove all excluded characters
    normalized_string = "".join([c for c in doc_string if c not in char_exclusions])
    # Make the string lower case and remove the stop words
    normalized_string = " ".join([w for w in normalized_string.lower().split(" ") if w not in stopword_set])
    
    # Lemmatize each of the words, download the word net and retry if necessary
    try:
        normalized_string = " ".join([lemmatizer.lemmatize(w) for w in normalized_string.split(" ")])
    except LookupError:
        import nltk
        nltk.download("wordnet")
        normalized_string = " ".join([lemmatizer.lemmatize(w) for w in normalized_string.split(" ")])\
        
    return normalized_string
