import streamlit as st
import google.generativeai as genai
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# --- الاتصال بـ Gemini باستخدام المفتاح السري ---
def configure_genai():
    # محاولة الحصول على المفتاح من إعدادات سترمليت (Secrets)
    api_key = st.secrets.get("GOOGLE_API_KEY")
    
    # إذا لم يوجد في Secrets، نبحث عنه في بيئة النظام (للتجربة المحلية)
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
    # إعداد النموذج
    # محاولة العثور على أي نموذج متاح يعمل
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    # تجربة سريعة للتأكد
    model.generate_content("test")
except:
    try:
        model = genai.GenerativeModel('gemini-pro')
    except:
        st.error("عذراً، لا يوجد نموذج متاح حالياً في حسابك.")
    # صندوق المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال سؤال المستخدم
    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # إرسال الطلب للذكاء الاصطناعي
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}")
else:
    st.error("⚠️ فشل الاتصال: لم يتم العثور على مفتاح API. تأكد من وضعه في Secrets.")

# --- التذييل ---
st.sidebar.markdown("---")
st.sidebar.write("تطوير كلية الإلهيات - جامعة كارابوك")
