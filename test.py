import streamlit as st
from google import genai

# إعداد الواجهة - جامعة كارابوك
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح الجديد من الخزنة (Secrets)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # الربط مع المحرك الحديث لعام 2026
        client = genai.Client(api_key=api_key)
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("نسخة جامعة كارابوك - الأداء العالي (Paid Tier)")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض المحادثة
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # إدخال السؤال
        if prompt := st.chat_input("تحدث مع مدرسك الآن..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                # استخدام الموديل المستقر (Flash هو الأسرع للمحادثات)
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("المفتاح الجديد قيد التفعيل.. جرب إرسال الرسالة مرة أخرى بعد دقيقة.")

    except Exception as e:
        st.error(f"خطأ في الاتصال بالمحرك: {e}")
else:
    st.info("💡 بانتظار إضافة المفتاح الجديد في إعدادات Secrets باسم GOOGLE_API_KEY")
