import streamlit as st
import google.generativeai as genai
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# --- الاتصال بـ Gemini ---
def configure_genai():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# --- واجهة المستخدم ---
st.title("🎓 المدرس العربي الذكي")
st.subheader("مرحباً بك في تطبيق جامعة كارابوك للذكاء الاصطناعي")

if configure_genai():
    # محاولة العثور على نموذج متاح باستخدام الأسماء الكاملة
    if "model" not in st.session_state:
        try:
            # تجربة النموذج الأحدث أولاً بالمسار الكامل
            st.session_state.model = genai.GenerativeModel('models/gemini-1.5-flash')
            st.session_state.model.generate_content("test")
        except:
            try:
                # تجربة النموذج المستقر كخيار بديل
                st.session_state.model = genai.GenerativeModel('models/gemini-pro')
            except Exception as e:
                st.error(f"عذراً، لا يوجد نموذج متاح حالياً. الخطأ: {str(e)}")

    # نظام إدارة الرسائل
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض تاريخ المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال سؤال المستخدم ومعالجته
    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # إرسال السؤال للنموذج المختار
                response = st.session_state.model.generate_content(prompt)
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"حدث خطأ أثناء استلام الرد: {str(e)}")
else:
    st.error("⚠️ لم يتم العثور على مفتاح API. تأكد من وضعه في إعدادات Secrets باسم GOOGLE_API_KEY")

# --- التذييل ---
st.sidebar.markdown("---")
st.sidebar.write("تطوير كلية الإلهيات - جامعة كارابوك")
