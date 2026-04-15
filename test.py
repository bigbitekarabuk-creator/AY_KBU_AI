import streamlit as st
import google.generativeai as genai

# إعداد واجهة المدرس العربي
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# جلب المفتاح الجديد من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # إعداد المكتبة
        genai.configure(api_key=api_key)
        
        # استخدام الموديل بدون أي تحديد لإصدارات بيتا
        # هذا يجعله يستخدم v1 المستقرة تلقائياً
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🎓 المدرس العربي الذكي")
        st.caption("نسخة جامعة كارابوك - النظام الاحترافي المستقر")

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
                # طلب التوليد المباشر
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("السيرفر مشغول حالياً، يرجى إعادة المحاولة.")

    except Exception as e:
        # إذا ظهر خطأ 404، فهذا يعني أن السيرفر يحتاج لـ Reboot حقيقي
        if "404" in str(e):
            st.error("تنبيه: السيرفر لا يزال عالقاً في الذاكرة القديمة. يرجى الضغط على Manage app ثم Reboot.")
        else:
            st.error(f"حدث خطأ: {e}")
else:
    st.info("💡 يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets")
