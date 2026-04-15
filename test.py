import streamlit as st
from google import genai

# إعداد الواجهة
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓")

# محاولة جلب المفتاح بأكثر من طريقة لضمان العمل
api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("api_key")

if api_key:
    try:
        # الاتصال بالمحرك الحديث 2026
        client = genai.Client(api_key=api_key)
        
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
                # استخدام الموديل المستقر المباشر
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("السيرفر لم يرسل رداً. يرجى التحقق من صلاحية المفتاح.")

    except Exception as e:
        # عرض الخطأ بشكل مبسط للمستخدم
        if "404" in str(e):
            st.error("خطأ 404: السيرفر يحاول استخدام رابط قديم. يرجى التأكد من تحديث ملف requirements.txt")
        else:
            st.error(f"حدث خطأ: {e}")
else:
    st.error("لم يتم العثور على المفتاح السري (GOOGLE_API_KEY) في إعدادات التطبيق.")
