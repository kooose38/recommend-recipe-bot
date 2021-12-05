import pandas as pd 
import numpy as np 
import pickle 
import joblib 
from janome.tokenizer import Tokenizer
import re 
import neologdn
import emoji

t = Tokenizer()

def load_word_processor():
    tf_model = pickle.load(open("data/tfidf.pkl", "rb"))
    return tf_model 

def load_model():
    model = joblib.load("data/classification.sav")
    return model 

def clean(doc: str) -> str:
    doc = neologdn.normalize(doc)
    doc = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', doc)
    doc = "".join(["" if c in emoji.UNICODE_EMOJI else c for c in doc])
    doc = re.sub(r'(\d)([,.])(\d+)', r'\1\3', doc)
    doc = re.sub(r'\d+', '0', doc)
    doc = re.sub(r'[!-/:-@[-`{-~]', r' ', doc)
    doc = re.sub(u'[■-♯]', ' ', doc)
    return doc 

def get_token(doc: str):
    tokens = []
    doc = clean(doc)
    for token in t.tokenize(doc, wakati=True):
        tokens.append(token)
    return [" ".join(tokens)] 


def find_similar_recipe(keywords: str):
    try:
        if keywords in "http":
            raise NotImplementedError
        df = pd.read_csv("data/recipe_processd1205.csv") 
        tfidf = load_word_processor()
        model = load_model()

        x = tfidf.transform(get_token(keywords)).toarray()
        pred = model.predict(x).flatten()[0]

        return df[df.cluster == pred].sample(10)
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

find_similar_recipe("こんにちは")