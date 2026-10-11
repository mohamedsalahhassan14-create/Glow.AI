import streamlit as st
import requests
import json

# ضبط عنوان الصفحة والدعم للغة العربية
st.set_page_config(page_title="Glow AI", page_icon="🤖")

st.markdown("""
<style>
    body, div, input, textarea {
        direction: RTL;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Glow AI")

# مفتاح الـ API الخاص بك
API_KEY = "AQ.Ab8RN6Lt-9JFJBnJ0sKtPuN2zOXEtU9R70AtfQ..."

# دالة إرسال الطلب مباشرة لسيرفرات جوجل (لتجنب مشاكل 401 و OAuth)
def call_gemini_api(prompt_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"حدث خطأ في الاتصال (كود الخادم: {response.status_code})"
    except Exception as e:
        return f"حدث خطأ: {e}"

# إدارة سجل الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# السؤال من المستخدم
if user_input := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            reply = call_gemini_api(user_input)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
