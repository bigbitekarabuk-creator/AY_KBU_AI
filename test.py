
import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# تفعيل المفتاح المدفوع
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # إجبار النظام على استخدام النسخة المستقرة v1 لتجنب خطأ 404
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("جامعة كارابوك - النسخة الاحترافية المستقرة")

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
                # استخدام "طلب صريح" للنسخة v1
                response = model.generate_content(
                    prompt,
                    request_options=RequestOptions(api_version='v1')
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # محاولة أخيرة باستخدام فلاش المستقر
        try:
            model_flash = genai.GenerativeModel('gemini-1.5-flash')
            response = model_flash.generate_content(
                prompt,
                request_options=RequestOptions(api_version='v1')
            )
            st.markdown(response.text)
        except:
            st.error("السيرفر يرفض الاتصال بالنسخ التجريبية. يرجى الانتظار دقيقة حتى يتحدث الرابط.")
else:
    st.error("المفتاح غير موجود في Secrets!")
