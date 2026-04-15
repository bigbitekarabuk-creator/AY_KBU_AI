import streamlit as st
import google.generativeai as genai

# إعداد واجهة المدرس العربي - جامعة كارابوك
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# تفعيل المفتاح المدفوع
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # استخدام نسخة Pro الاحترافية المتوفرة في اشتراكك
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    st.title("🎓 المدرس العربي الذكي")
    st.caption("نسخة جامعة كارابوك - الأداء العالي (Paid Tier)")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("تحدث مع مدرسك الآن..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"تنبيه: تأكد من صحة المفتاح المدفوع. الخطأ: {e}")
else:
    st.error("يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets")
