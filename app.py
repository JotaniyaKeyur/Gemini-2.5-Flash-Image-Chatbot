import streamlit as st
from PIL import Image
from chatbot import chat_with_image

st.set_page_config(page_title="Gemini 2.5 Image Chatbot", layout="wide")

st.markdown("<h1 style='text-align: center;'>Welcome, Gemini 2.5 Flash Image Chatbot</h1>", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []  
if "images" not in st.session_state:
    st.session_state.images = []
if "current_image_index" not in st.session_state:
    st.session_state.current_image_index = None

# Layout: Sidebar-style
left_col, right_col = st.columns([1, 7])

# LEFT PANEL: Upload Images 
with left_col:
    st.header("📁 Upload Images")
    uploaded_files = st.file_uploader(
        "Drop images here",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.session_state.images = [Image.open(f).convert("RGB") for f in uploaded_files]
        st.session_state.current_image_index = 0

    if st.session_state.images:
        st.markdown("### Uploaded Images:")
        for i, img in enumerate(st.session_state.images):
            if st.button(f"Select Image {i+1}", key=f"select_{i}"):
                st.session_state.current_image_index = i
            st.image(img, caption=f"Image {i+1}", width=100)

        if st.session_state.current_image_index is not None:
            selected_img = st.session_state.images[st.session_state.current_image_index]
            st.markdown("### Currently Selected Image:")
            st.image(selected_img, caption=f"Image {st.session_state.current_image_index + 1}", width=150)

# RIGHT PANEL: Chat Area 
with right_col:
    if st.session_state.current_image_index is not None:
        current_image = st.session_state.images[st.session_state.current_image_index]

        # Display full chat history for selected image
        st.markdown("### 💬 Chat With Image")
        for msg in st.session_state.history:
            if msg["image_index"] == st.session_state.current_image_index:
                if msg["sender"] == "You":
                    st.markdown(f"🧑 :  {msg['message']}")
                else:
                    st.markdown(f"💬 :  {msg['message']}")

        # input at the bottom
        user_prompt = st.chat_input("Ask Gemini 2.5 Flash")

        if user_prompt:
            with st.spinner("Gemini Thinking..."):
                response = chat_with_image(user_prompt, current_image)

            st.session_state.history.append({
                "sender": "You",
                "message": user_prompt,
                "image_index": st.session_state.current_image_index
            })
            st.session_state.history.append({
                "sender": "Gemini",
                "message": response,
                "image_index": st.session_state.current_image_index
            })
            st.rerun()
    else:
        st.info("Please upload one or more images to start chatting")
