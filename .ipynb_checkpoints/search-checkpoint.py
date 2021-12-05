import pandas as pd 
import numpy as np 

def find_similar_recipe(kwd: str):
    df = pd.read_csv("data/recipe.csv") # 元のデータ
    title = df.recipeTitle[df.recipeTitle.str.contains(kwd)].index.tolist()
    title = np.random.choice(title, 1)[0]
    
    v = np.load("data/vector.npy")
    indics = np.argsort(-v[title])[:10].tolist()
    conf = v[title][indics].tolist()
    
    return df.iloc[indics], conf
    