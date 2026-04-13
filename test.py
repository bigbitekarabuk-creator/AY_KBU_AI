import streamlit as st
import google.generativeai as genai
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# --- الاتصال بـ Gemini ---
def configure_genai():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# --- واجهة المستخدم ---
st.title("🎓 المدرس العربي الذكي")
st.subheader("مرحباً بك في تطبيق جامعة كارابوك للذكاء الاصطناعي")

if configure_genai():
    # محاولة العثور على نموذج متاح وتجهيزه
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # اختبار بسيط للتأكد من عمل النموذج
        model.generate_content("test")
    except:
        model = genai.GenerativeModel('gemini-pro')

    # نظام المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
else:
    st.error("⚠️ لم يتم العثور على مفتاح API في الإعدادات.")
    
