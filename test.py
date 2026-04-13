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
    # محرك اختيار النموذج الذكي - يتجاوز خطأ 404
    if "model" not in st.session_state:
        try:
            # محاولة البحث عن أي نموذج متاح يدعم التوليد
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # اختيار أول نموذج متاح (غالباً سيكون gemini-1.5-flash أو pro)
                target_model = available_models[0]
                st.session_state.model = genai.GenerativeModel(target_model)
            else:
                st.error("لم يتم العثور على نماذج متاحة في هذا الحساب.")
        except Exception as e:
            # إذا فشل الفحص، نجرب المسار اليدوي كخيار أخير
            try:
                st.session_state.model = genai.GenerativeModel('models/gemini-1.5-flash')
            except:
                st.error(f"عذراً، هناك مشكلة في الاتصال: {str(e)}")

    # نظام المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = st.session_state.model.generate_content(prompt)
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"حدث خطأ أثناء استلام الرد: {str(e)}")
else:
    st.error("⚠️ لم يتم العثور على مفتاح API في Secrets.")

# --- التذييل ---
st.sidebar.markdown("---")
st.sidebar.write("تطوير كلية الإلهيات - جامعة كارابوك")
