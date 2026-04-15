import streamlit as st
import google.generativeai as genai

# إعداد واجهة المدرس العربي - جامعة كارابوك
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# تفعيل المفتاح المدفوع من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # استخدام الموديل المستقر (تجنب v1beta)
        # نستخدم الاسم المباشر للموديل لضمان التوافق مع الحساب المدفوع
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
                # طلب توليد المحتوى مع معالجة الأخطاء
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("لم يتمكن الموديل من الرد، يرجى المحاولة مرة أخرى.")

    except Exception as e:
        # حل بديل سريع في حال وجود ضغط على السيرفر
        st.warning("نحول الاتصال للمحرك السريع...")
        model_alt = genai.GenerativeModel('gemini-1.5-flash')
        response = model_alt.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.error("يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets")
