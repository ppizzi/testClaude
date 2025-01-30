import streamlit as st
import json
from PIL import Image
import PIL
import os
import base64
import boto3
from botocore.exceptions import ClientError

# -- functions --

def encode_image(image):
    #st.write("converting image to b64")
    try:
        encoded_image = base64.b64encode(image.read()).decode("utf-8") #< works with uploaded file from st.upload_file, but not with an image from PIL or from os.open
    except:
        encoded_image = base64.b64encode(image).decode("utf-8")
    #encoded_image
    #st.write("converted")
    
    return encoded_image




####--- main page ---###
st.title("Test your message to Claude API via Bedrock")

#--Select model for inference
# naming conventions: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
model_ids = ["us.anthropic.claude-3-5-sonnet-20240620-v1:0", "amazon.nova-lite-v1:0"]
model_id = model_ids[0] 
st.write("\(note: this app uses the following LLM model: ", model_id, "\)" )

#--Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_REGION"]
)

# Start a conversation with the user message.
default_message = "Say something nice about a beautiful sunny day"
user_message1 = st.text_input("Enter your message to the LLM: ") 

st.write("this app asks LLM to describe this image")
st.image("img.jpeg")
with open("img.jpeg", "rb") as f:
    image = f.read()

if user_message1:
    #st.write(user_message1)
    conversation = [
        {
            "role": "user",
            "content": [
                {"text": default_message},
                {"text": user_message1},
                {"text": "describe the following image."},
                {"image":{"format":"jpeg", "source":{"bytes": image}}}
            ],
            }
        ]

    
    
    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=conversation
        )
    
        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        st.write(response_text)
    
    except (ClientError, Exception) as e:
        st.write(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)
    
