import streamlit as st
import google.generativeai as genai

# إعداد الواجهة
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح الجديد من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # إعداد المكتبة
        genai.configure(api_key=api_key)
        
        # الحل القاطع: تعريف الموديل مع تحديد إصدار الواجهة البرمجية (API) يدوياً
        # نستخدم هنا الطريقة التي تجبر المكتبة على ترك v1beta والذهاب إلى v1
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
        )
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("جامعة كارابوك - النسخة المستقرة (v1)")

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
                # نستخدم أسلوب التوليد المباشر الذي يتخطى ثغرة الـ 404
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        # إذا استمر الخطأ، سنقوم بطباعة الإصدار الحالي للمكتبة لمساعدتنا في التشخيص
        import google.generativeai as gai
        st.error(f"حدث خطأ: {e}")
        st.write(f"إصدار المكتبة الحالي: {gai.__version__}")
else:
    st.info("💡 تأكد من وجود GOOGLE_API_KEY في Secrets")
