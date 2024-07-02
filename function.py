import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    df = pd.read_csv(f'df.csv')
    return df

def recommend_products(df, user_id_encoded, top_n=5,decay_rate=0.1):
    df['about_product'] = df['about_product'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['about_product'])
    
    user_history=df[df['user_id_encoded']==user_id_encoded]
    if not user_history.empty:
        indices = user_history.index.tolist()
        num_items = len(indices)
        cosine_sim_user = cosine_similarity(tfidf_matrix[indices], tfidf_matrix)
        
        # Apply exponential decay to weight recent purchases more
        weights = np.exp(-decay_rate * np.arange(num_items)[::-1])  # Decaying weights for each past purchase
        weighted_sim = cosine_sim_user.T @ weights / weights.sum()
        # Exclude already purchased items
        weighted_sim[indices] = 0 
        
        similarity_scores = sorted(enumerate(weighted_sim), key=lambda x: x[1], reverse=True)
        
        top_n_index = [i[0] for i in similarity_scores[1:top_n + 1]]
        product_names = df.loc[top_n_index, 'product_name'].tolist()
        scores = [similarity_scores[i][1] for i in range(top_n)]
        result=pd.DataFrame({'Id Encoded': [user_id_encoded] * top_n,
                                   'recommended product': product_names,
                                   'scores': scores})
        return result
    else:
        return 'User not found'