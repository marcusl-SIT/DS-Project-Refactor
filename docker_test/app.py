import os
import streamlit as st  
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np


def predict_image_class(image_data, model, w=224, h=224):
        size = (w,h)
        image = ImageOps.fit(image_data, size, Image.LANCZOS)
        img = np.asarray(image)
        if len(img.shape) > 2 and img.shape[2] == 4:
        #slice off the alpha channel if it exists
          img = img[:, :, :3]
        img = np.expand_dims(img, axis=0) # for models expecting a batch
        prediction = model.predict(img)
        return prediction


@st.cache_resource
def load_model():
    model=tf.keras.models.load_model('model.keras')
    return model


st.set_page_config(
    page_title="Cat Detector",
    page_icon = ":cat:",
    initial_sidebar_state = 'auto'
)

with st.sidebar:
        #st.image('image_path.png')
        st.title("Cat Detection Model")
        st.subheader("Description of what your model is doing.")

st.write("""
         # Cat Detection Tool
         """
         )

img_file = st.file_uploader("", type=["jpg", "png"])

if 'model.keras' not in os.listdir():
  gdown.download(id='1yCX8K64iAjpGGUGfOdxLdW77dlHpaWq4')
with st.spinner('Model is being loaded...'):
  model=load_model()

if img_file is None:
    st.text("Please upload an image file")
else:
  image = Image.open(img_file)
  st.image(image, use_container_width=False)
  predictions = predict_image_class(image, model)

  #### FOR THIS EXAMPLE ONLY
  from tf.keras.applications.imagenet_utils import decode_predictions
  top5_preds = decode_predictions(predictions, top=5)
  st.info(top5_preds[0])
  top_pred = top5_preds[0][0][1]
  #################

  string = "Detected class: " + top_pred

  if 'cat' in top_pred.lower() or top_pred.lower() == 'tabby':
    st.balloons()
    st.sidebar.success(string)
    st.write("""
    # C A T""")
  else:
    st.sidebar.warning(string)
    st.markdown("## Issue detected:")
    st.info("Not a cat.")
