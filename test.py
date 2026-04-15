import streamlit as st
import google.generativeai as genai

# إعداد واجهة المدرس العربي
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح الجديد من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # إعداد المكتبة بالمفتاح
        genai.configure(api_key=api_key)
        
        # الحل السحري: استخدام موديل محدد بمسار كامل لضمان تجاوز v1beta
        # هذا المسار يجبر السيرفر على استخدام النسخة المستقرة المخصصة للمشتركين
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
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
                # نرسل الطلب ببساطة؛ الموديل الآن معرف بمساره المستقر
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("لم يتم استلام رد، يرجى المحاولة مرة أخرى.")

    except Exception as e:
        st.error(f"حدث خطأ في النظام: {e}")
else:
    st.info("💡 يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets")
