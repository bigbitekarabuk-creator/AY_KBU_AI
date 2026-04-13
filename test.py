import streamlit as st
import google.generativeai as genai
import os

# --- 1. إعداد المفتاح الخاص بك ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# --- 2. وظيفة اختيار الموديل تلقائياً ---
@st.cache_resource
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                active_model = genai.GenerativeModel(m.name)
                return active_model, m.name
    except Exception:
        for name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(name)
                m.generate_content("test")
                return m, name
            except: continue
    return None, None

model, active_model_name = get_working_model()

# --- 3. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="المدرس العربي الذكي - UNIKA", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-title { color: #003366; text-align: center; font-size: 38px; font-weight: bold; margin-top: 10px; }
    .uni-title { color: #d4af37; text-align: center; font-size: 24px; font-weight: bold; }
    .faculty-title { color: #003366; text-align: center; font-size: 20px; font-style: italic; margin-bottom: 20px; }
    .stImage > img { display: block; margin-left: auto; margin-right: auto; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .audio-btn { border: none; padding: 10px 22px; border-radius: 25px; cursor: pointer; font-weight: bold; transition: 0.3s; }
    .dinle-btn { background-color: #003366; color: white; }
    .durdur-btn { background-color: #d9534f; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (تخصيص المنهج) ---
st.sidebar.title("📚 إعدادات المنهج")

# محاولة عرض الشعار في الجانب بطريقة آمنة
logo_path = "karabuk_logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=100)
else:
    st.sidebar.info("💡 ضع ملف 'karabuk_logo.png' في المجلد ليظهر الشعار هنا.")

st.sidebar.markdown("---")
book_part = st.sidebar.selectbox(
    "اختر مستوى كتاب (العربية بين يديك):",
    ["عام (General)", "الكتاب الأول (1. Kitap)", "الكتاب الثاني (2. Kitap)", "الكتاب الثالث (3. Kitap)"]
)
st.sidebar.write(f"المستوى الحالي: **{book_part}**")

# --- 5. عرض الهوية البصرية في الصفحة الرئيسية (طريقة آمنة) ---

# أ- الصورة الترحيبية
if os.path.exists("welcome_bg.jpg"):
    st.image("welcome_bg.jpg", use_column_width=True)
else:
    st.info("🖼️ يمكنك إضافة صورة ترحيبية بتسميتها 'welcome_bg.jpg'")

# ب- شعار الجامعة في المنتصف
if os.path.exists(logo_path):
    st.image(logo_path, width=150)

st.markdown('<div class="main-title">المدرس العربي الذكي</div>', unsafe_allow_html=True)
st.markdown('<div class="uni-title">Karabük Üniversitesi</div>', unsafe_allow_html=True)
st.markdown('<div class="faculty-title">İlahiyat Fakültesi</div>', unsafe_allow_html=True)

if model is None:
    st.error("⚠️ فشل الاتصال بالذكاء الاصطناعي.")
    st.stop()

# --- 6. نظام المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # صياغة التعليمات بناءً على المنهج المختار
        instruction = f"أنت مدرس خبير لطلاب كلية الإلهيات. تخصصك سلسلة العربية بين يديك - {book_part}. أجب بالتركية ووضح الكلمات العربية:"
        res = model.generate_content(f"{instruction}\nالطالب يسأل: {prompt}")
        response_text = res.text
        
        with st.chat_message("assistant"):
            st.markdown(response_text)
            
            # كود النطق والإيقاف
            tts_script = f"""
                <script>
                var msg = new SpeechSynthesisUtterance('{response_text.replace("'", "\\'").replace("\n", " ")}');
                msg.lang = 'ar-SA';
                msg.rate = 0.85;
                function speak() {{ window.speechSynthesis.cancel(); window.speechSynthesis.speak(msg); }}
                function stopSpeaking() {{ window.speechSynthesis.cancel(); }}
                window.onbeforeunload = function () {{ window.speechSynthesis.cancel(); }}
                </script>
                <div style="text-align: center; display: flex; justify-content: center; gap: 15px; margin-top: 15px;">
                    <button onclick="speak()" class="audio-btn dinle-btn">🔊 Dinle (استمع)</button>
                    <button onclick="stopSpeaking()" class="audio-btn durdur-btn">🛑 Durdur (إيقاف)</button>
                </div>
            """
            st.components.v1.html(tts_script, height=100)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
