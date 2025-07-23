import base64
import io
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Initialize Gemini 2.5 Flash model once
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def image_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def chat_with_image(user_prompt: str, image: Image.Image) -> str:
    img_base64 = image_to_base64(image)
    message = [
        HumanMessage(content=[
            {"type": "text", "text": user_prompt},
            {
                "type": "media",
                "mime_type": "image/jpeg",
                "data": img_base64
            }
        ])
    ]
    response = llm.invoke(message)
    return response.content
