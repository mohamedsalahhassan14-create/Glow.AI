import streamlit as st
import google.generativeai as genai


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

# ضع مفتاح الـ API الجديد هنا

API_KEY = "AQ.Ab8RN6Lt-9JFJBnJ0sKtPuN2zOXEtU9R70AtfQ..."

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# إدارة سجل الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال السؤال من المستخدم (الكود مش هيبعت أي طلب للجوجل إلا لما تتكلم أنت الأول)
if user_input := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=user_input,
                #config={"tools": [{"google_search": {}}]}
            )
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
