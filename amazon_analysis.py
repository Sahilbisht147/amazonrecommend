import streamlit as st
import pandas as pd
import pickle

# Load data and similarity matrix
df = pd.read_csv('amazon.csv')
similarity = pickle.load(open('similarity_matrix.pkl', 'rb'))

# Define the function to recommend products
def recommend(product_name):
    try:
        # Find the index of the product by name
        index = df[df['product_name'] == product_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_product_names = []
        recommended_product_links = []
        for i in distances[1:6]:  # Skip the first as it's the product itself
            product_index = i[0]
            recommended_product_names.append(df.iloc[product_index]['product_name'].title())
            recommended_product_links.append(df.iloc[product_index]['product_link'])
            
        return recommended_product_names, recommended_product_links
    except IndexError:
        return [], []

# Streamlit UI
st.header('Amazon Product Recommendation System')

product_names = df['product_name'].unique()
selected_product_name = st.selectbox(
    "Select a Product to get recommendations:",
    product_names
)

if st.button("Get Recommendations"):
    recommended_product_names, recommended_product_links = recommend(selected_product_name)
    
    if recommended_product_names:
        st.write(f"Top 5 recommended products similar to '{selected_product_name}':")
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        
        for idx, col in enumerate(cols):
            col.write(f"**Product Name**: {recommended_product_names[idx]}")
            col.write(f"**Link**: [View Product]({recommended_product_links[idx]})")
    else:
        st.write(f"No recommendations found for '{selected_product_name}'.")
