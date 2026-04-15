import streamlit as st
from google import genai

# إعداد الواجهة
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح المدفوع
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # استخدام العميل الجديد لعام 2026
        client = genai.Client(api_key=api_key)
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("جامعة كارابوك - النسخة الحديثة 2026")

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
                # طلب التوليد باستخدام الطريقة الجديدة
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"خطأ في المحرك الجديد: {e}")
else:
    st.error("المفتاح غير موجود في Secrets!")
