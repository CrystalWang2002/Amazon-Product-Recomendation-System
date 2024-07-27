import streamlit as st
import function as func
import numpy as np
# part 8
st.set_page_config(layout="wide")
#st.set_option('deprecation.showPyplotGlobalUse', False)
#st.set_option('deprecation.showfileUploaderEncoding', False)

# Title of the app
st.title('Recommendation System for Amazon Products')
st.write("Fill in the following information to get the recommendation 👩🏻‍💻")
#insert pictures
col1, col2 = st.columns(2)
with col1:
    st.image("./pictures/Amazon.jpg", use_column_width=True)
with col2:
    st.image("./pictures/Amazon1.png", use_column_width=True)

df = func.load_data()
list=np.arange(0,1192,1)
user_id_encoded = st.selectbox("Select the User ID you want to give recommendation:", list)
top_n = st.number_input("Type in the number of recommend items you want:", min_value=1, max_value=20, step=1, format="%d")

if st.button("Recommend"):
    st.write(func.recommend_products(df, user_id_encoded, top_n))
else:
    st.write(func.recommend_products(df, 0, 5))
