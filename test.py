import streamlit as st
import google.generativeai as genai

# إعداد واجهة المدرس العربي - جامعة كارابوك
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح المدفوع من Secrets
api_key = st.secrets.get("AIzaSyDtekqqIDwAFj6RWdjXHilMrEU4DbN73qg")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # التعديل الأهم: استخدام الموديل بدون تحديد إصدار v1beta يدوي لتركه يختار المستقر
        # الحسابات المدفوعة الآن تعمل بشكل أفضل مع هذا التعريف المباشر
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("جامعة كارابوك - النسخة الاحترافية (Stable)")

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
                    # طلب الرد
                    response = model.generate_content(prompt)
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as inner_e:
                    st.error(f"خطأ في الاتصال: {str(inner_e)}")
                    st.info("نصيحة: تأكد من أن مفتاح الـ API يبدأ بـ AIza ومأخوذ من Google AI Studio.")

    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")
else:
    st.error("المفتاح غير موجود في Secrets!")
