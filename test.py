import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="المدرس العربي الذكي")

# جلب المفتاح
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # اختيار النموذج المباشر والأكثر استقراراً
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🎓 المدرس العربي الذكي")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("اسألني أي شيء..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطأ في الرد: {e}")
else:
    st.error("المفتاح غير موجود في Secrets")
