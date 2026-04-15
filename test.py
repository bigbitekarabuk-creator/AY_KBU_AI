import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# إعداد الواجهة
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح الجديد من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # إعداد المكتبة
        genai.configure(api_key=api_key)
        
        # إنشاء الموديل
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("نسخة جامعة كارابوك - النظام المستقر (Paid Tier)")

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
                # السطر السحري: إجبار الطلب على استخدام v1 المستقرة وتجنب v1beta
                response = model.generate_content(
                    prompt,
                    request_options=RequestOptions(api_version='v1')
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        if "404" in str(e):
            st.error("السيرفر لا يزال يحاول طلب النسخة التجريبية. يرجى عمل Reboot للتطبيق من إعدادات Streamlit.")
        else:
            st.error(f"حدث خطأ: {e}")
else:
    st.error("تأكد من وضع المفتاح الجديد في Secrets باسم GOOGLE_API_KEY")
