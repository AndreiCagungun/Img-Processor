import streamlit as st
from rembg import remove
from PIL import Image
import io

def remove_background(image):
    return remove(image)

def main():
    st.set_page_config(page_title="Image Background Remover")
    
    st.title("Image Background Remover")
    st.write("Upload an image to remove its background")

    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Original Image")
            st.image(image, use_column_width=True)

        # Show processing message
        with st.spinner('Removing background...'):
            output = remove_background(image)
        
        with col2:
            st.header("Processed Image")
            st.image(output, use_column_width=True)
        
        # Add download button
        buf = io.BytesIO()
        output.save(buf, format="PNG")
        st.download_button(
            label="Download processed image",
            data=buf.getvalue(),
            file_name="processed_image.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()