from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
# Page configuration must be the first Streamlit command used
st.set_page_config(page_title="NutriVision - Your Nutritionist Assistant")
# Set Google API key from environment variable or directly
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "Your_Default_API_Key")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Function to interact with Google Gemini Pro Vision API
def get_gemini_response(input_prompt, image_parts, user_input):
    model = genai.GenerativeModel('gemini-pro-vision')
    full_prompt = input_prompt + "\n\n" + user_input  # Combining predefined prompt with user input
    response = model.generate_content([full_prompt, image_parts[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Insert custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")  # Ensure you have a CSS file named 'style.css'



st.title("NutriVision - Your Nutritionist Assistant")
st.markdown("""
Welcome to NutriVision! Upload an image of your meal, and let NutriVision identify the food items and calculate their total caloric content. 
We'll also provide insights on the healthiness of your meal, suggestions for a balanced diet, and how your meal choices affect your health.
""")

# Updated to include health impact information
detailed_input_prompt = """
Identify the food items in the image and calculate the total calories. Provide details of every food item's caloric intake in the format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----

Based on the identified food items, mention whether the food is healthy or not. For healthy food items, explain how they positively impact the user's health. For unhealthy food items, detail the negative health effects. Also, suggest what other food can be added to make it a more balanced diet.
"""

user_input_prompt = st.text_area("Add any specific instructions for the analysis (Optional):", 
                                 help="Provide any specific details or questions about the meal.")

uploaded_file = st.file_uploader("Choose an image of your meal", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze Meal")

# Handling the analysis and response display
if submit and uploaded_file:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(detailed_input_prompt, image_data, user_input_prompt)
        st.subheader("Analysis Results")
        st.write(response)
        
        # Add functionality to save response to a file
        if st.button("Save Results"):
            with open("NutriVision_Results.txt", "w") as file:
                file.write(response)
            st.success("Results saved successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")





