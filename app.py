import streamlit as st
import requests
from PIL import Image
import io

# 1. Configure your Roboflow API details
API_KEY = "9PnwxjuB0q8VCW0lSlU7"
PROJECT_ID = "garbage-classification-3"  # or "material-identification/garbage-classification-3" if needed
MODEL_VERSION = "2"

# 2. Build the endpoint URL (for object detection or classification)
url = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

def classify_image(image):
    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # POST request to Roboflow
    response = requests.post(url, files={"file": img_byte_arr})

    # Optional debug
    st.write("*Status Code:*", response.status_code)
    st.write("*Response Text:*", response.text)

    # Return JSON response (dict)
    return response.json()

# 3. Streamlit UI
st.title("Garbage Classification Demo")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Call our function
    result = classify_image(image)

    # Extract predictions from JSON
    predictions = result.get("predictions", [])     
    
    # If no predictions found
    if not predictions:
        st.write("No materials detected. Try a different image or lower confidence threshold.")
    else:
        # Sort by confidence, highest first (optional)
        predictions = sorted(predictions, key=lambda x: x["confidence"], reverse=True)
        
        # Display each prediction in a user-friendly way
        st.subheader("Predictions:")
        for i, pred in enumerate(predictions, start=1):
            class_label = pred["class"]
            confidence = round(pred["confidence"] * 100, 2)
            
            st.write(f"{i}. {class_label}** — Confidence: {confidence}%")

        # If you only want the top prediction:
        top_prediction = predictions[0]
        top_class = top_prediction["class"]
        top_conf = round(top_prediction["confidence"] * 100, 2)
        st.success(f"*Top Prediction:* {top_class} ({top_conf}% confidence)")