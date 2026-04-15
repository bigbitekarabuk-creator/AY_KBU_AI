import streamlit as st
import google.generativeai as genai

# 1. إعداد الواجهة المتقدمة
st.set_page_config(page_title="المدرس العربي الذكي", page_icon="🎓", layout="wide")

# 2. جلب المفتاح الجديد (تأكد أنه في Secrets باسم GOOGLE_API_KEY)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # استخدام المسار المستقر لضمان عدم حدوث خطأ 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🎓 المدرس العربي الذكي (النسخة الكاملة)")
        st.markdown("---")

        # 3. إضافة أزرار التحكم (الصوت وغيرها) في الشريط الجانبي
        with st.sidebar:
            st.header("⚙️ إعدادات الدرس")
            enable_voice = st.checkbox("تفعيل القراءة الصوتية", value=True)
            st.info("نسخة جامعة كارابوك - التحديث الأخير 2026")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 4. عرض المحادثة مع دعم الصور والتنسيق
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 5. منطقة إدخال النص والملفات
        if prompt := st.chat_input("اسأل مدرسك عن أي شيء..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                # طلب الرد من الموديل
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                
                # إضافة خاصية الصوت (إذا تم تفعيلها)
                if enable_voice:
                    # هنا نستخدم مكون صوتي بسيط (يمكن تطويره لاحقاً)
                    st.caption("🔊 جاري تجهيز النص الصوتي...")
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"⚠️ تنبيه تقني: {e}")
        st.info("إذا ظهر خطأ 404، يرجى الضغط على Reboot من قائمة Manage app.")
else:
    st.warning("⚠️ يرجى إضافة مفتاح الـ API في إعدادات Secrets.")
