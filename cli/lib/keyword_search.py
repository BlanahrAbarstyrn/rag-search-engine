import pickle

from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords, CACHE_PATH
import string
from nltk.stem import PorterStemmer
from collections import defaultdict
import os
import pickle

stemmer = PorterStemmer()

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set) # token: [doc_id1, doc_id2]
        self.docmap = {} # map document ID: document
        self.index_path = os.path.join(CACHE_PATH, "index.pkl")
        self.docmap_path = os.path.join(CACHE_PATH, "docmap.pkl")

    def __add_document(self, doc_id, text):
        tokens = tokenize_text(text)
        for token in set(tokens):
            self.index[token].add(doc_id)

    def get_documents(self, term):
        return sorted(list(self.index[term]))

    def build(self):
        movies = load_movies()
        for movie in movies:
            doc_id = movie["id"]
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id, text)
            self.docmap[doc_id] = movie


    def save(self):
        os.makedirs(CACHE_PATH, exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)

        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)

def build_command():
    idx = InvertedIndex()
    idx.build()
    idx.save()
    docs = idx.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("","", string.punctuation))
    return text

def tokenize_text(text):
    text = clean_text(text)
    stopwords = load_stopwords()
    res = []
    def _filter(token):
        token = token.strip("\n")
        if token and token not in stopwords:
            return True
        return False
    for tok in text.split():
        if _filter(tok):
            stemmed_tok = stemmer.stem(tok)
            res.append(stemmed_tok)
    return res

def has_matching_token(query_toks, movie_toks):
    for query_tok in query_toks:
        for movie_tok in movie_toks:
            if query_tok in movie_tok:
                return True
    return False

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    query_tokens = tokenize_text(query)
    for movie in movies:
        movie_tokens = tokenize_text(movie["title"])
        if has_matching_token(query_tokens, movie_tokens):
            results.append(movie)
        if len(results) >= limit:
            break
    return results