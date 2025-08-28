import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

def remove_background(image, model_name="u2net"):
    # Create a new session with the selected model
    session = new_session(model_name)
    
    # Remove background with adjusted parameters
    return remove(
        image,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10
    )

def main():
    st.set_page_config(page_title="Image Background Remover")
    
    st.title("Image Background Remover")
    st.write("Upload an image to remove its background")

    # Add quality settings
    st.sidebar.title("Settings")
    model_name = st.sidebar.selectbox(
        "Select Model",
        ["u2net", "u2net_human_seg", "silueta"],
        help="u2net: General purpose, u2net_human_seg: Human subjects, silueta: Fast but less accurate"
    )
    alpha_matting = st.sidebar.checkbox("Enable Alpha Matting", value=True)
    alpha_value = st.sidebar.slider("Alpha Matting Value", 0, 255, 240)
    
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Original Image")
                st.image(image, use_column_width=True)

            with st.spinner('Removing background...'):
                output = remove_background(image, model_name)
            
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
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()