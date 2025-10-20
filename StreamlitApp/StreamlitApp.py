import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Load dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target

# Train a simple model
model = RandomForestClassifier()
model.fit(X, y)

st.title("Simple ML Model with Streamlit")

# User input
st.sidebar.header("Input Features")
sepal_length = st.sidebar.slider("Sepal length", float(X['sepal length (cm)'].min()), float(X['sepal length (cm)'].max()))
sepal_width = st.sidebar.slider("Sepal width", float(X['sepal width (cm)'].min()), float(X['sepal width (cm)'].max()))
petal_length = st.sidebar.slider("Petal length", float(X['petal length (cm)'].min()), float(X['petal length (cm)'].max()))
petal_width = st.sidebar.slider("Petal width", float(X['petal width (cm)'].min()), float(X['petal width (cm)'].max()))

input_df = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]], columns=X.columns)

# Make prediction
prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)

st.write(f"Predicted class: {iris.target_names[prediction[0]]}")
st.write("Prediction probabilities:")
st.write(pd.DataFrame(prediction_proba, columns=iris.target_names))