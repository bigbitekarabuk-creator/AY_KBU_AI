import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح المدفوع
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # التعديل الجوهري: استخدام النسخة المستقرة لتجنب خطأ 404
        # نستخدم gemini-1.5-pro كخيار أول للحساب المدفوع
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("نسخة جامعة كارابوك - الأداء العالي (Paid Tier)")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("اسأل مدرسك الآن..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                # محاولة توليد الرد
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # إذا استمر الخطأ، سنقوم بتجربة فلاش تلقائياً
        st.warning("نحاول الاتصال بالمحرك البديل لضمان السرعة...")
        model_alt = genai.GenerativeModel('gemini-1.5-flash')
        response = model_alt.generate_content(prompt)
        st.markdown(response.text)
else:
    st.error("المفتاح غير موجود في Secrets!")
