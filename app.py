from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Set Google API key from environment variable or directly
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyDi1coBD4Ulpa8eg5vqFkFuT-s-f-Q479c")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Function to interact with Google Gemini Pro Vision API
def get_gemini_response(input_prompt, image_parts, user_input):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_parts[0], user_input])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App UI Enhancements
st.set_page_config(page_title="NutriVision - Your Nutritionist Assistant")

st.title("NutriVision - Your Nutritionist Assistant")
st.markdown("""
Welcome to NutriVision! This app helps you understand the nutritional value of your meals by analyzing images. 
Just upload an image of your meal, and let NutriVision tell you about its caloric content, healthiness, and how to make it more balanced.
""")

input_prompt = st.text_area("Input Prompt (Optional): Provide any specific instructions or details you're interested in.",
                            key="input", help="E.g., Focus on identifying fruits.")

uploaded_file = st.file_uploader("Choose an image of your meal", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze Meal")

# Handling response
if submit and uploaded_file:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_prompt)
        st.subheader("Analysis Results")
        st.write(response)
        # Optional: Add functionality to save response to a file
        if st.button("Save Results"):
            with open("NutriVision_Results.txt", "w") as file:
                file.write(response)
            st.success("Results saved successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

