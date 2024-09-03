import streamlit as st
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image

# Custom CSS for styling
def set_css():
    st.markdown(
        """
        <style>
        /* General styling */
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .stApp {
            background-color: #f0f2f6;
        }
        /* Header styling */
        h1, h4 {
            color: #1f77b4;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        /* File upload boxes */
        .stFileUploader {
            border: 2px dashed #1f77b4;
            padding: 10px;
            background-color: #ffffff;
            border-radius: 10px;
            text-align: center;
        }
        /* Buttons */
        .stButton button {
            background-color: #1f77b4;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 20px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #0d5b91;
        }
        /* Result display */
        .stMarkdown {
            text-align: center;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_css()

# Set page config
st.set_page_config(
    page_title="Image Similarity Check",
    page_icon=":camera:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Header
st.markdown("<h1>Image Similarity Check</h1>", unsafe_allow_html=True)
st.markdown("<h4>Using AWS Rekognition</h4>", unsafe_allow_html=True)

# Image upload section with custom styling
st.markdown("### Upload Your Images Below:")
image1 = st.file_uploader("Upload First Image", type=["jpg", "jpeg", "png"], key="image1")
image2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png"], key="image2")

# Button to trigger comparison
if image1 and image2:
    compare_button = st.button("Compare Images", key="compare_button")

    if compare_button:
        image1_bytes = image1.read()
        image2_bytes = image2.read()

        with st.spinner("Comparing Images..."):
            result = compare_images(image1_bytes, image2_bytes)
        
        # Display results
        if result:
            st.markdown("### Results:")
            if result['FaceMatches']:
                for match in result['FaceMatches']:
                    st.success(f"Similarity: {match['Similarity']}%", icon="✅")
            else:
                st.error("No match found.", icon="❌")
        else:
            st.error("An error occurred while processing the images.")
else:
    st.warning("Please upload both images to compare.", icon="⚠️")

# Function to compare two images using AWS Rekognition
def compare_images(image1, image2):
    try:
        client = boto3.client('rekognition')

        response = client.compare_faces(
            SourceImage={'Bytes': image1},
            TargetImage={'Bytes': image2},
            SimilarityThreshold=80
        )
        return response
    except (BotoCoreError, ClientError) as e:
        st.error(f"Error comparing images: {e}")
        return None

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by AWS Rekognition</p>", unsafe_allow_html=True)
