import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(
    page_title="Blood Pressure AI Assistant",
    page_icon="🩺",
    layout="centered",
)

# الشريط الجانبي لإخلاء المسؤولية والمعلومات
with st.sidebar:
    st.header("⚠️ Disclaimer / إخلاء مسؤولية")
    st.warning(
        "**EN:** This AI chatbot is an educational prototype for **High Blood Pressure**. "
        "It does NOT provide medical diagnosis, personalized treatment, or medication dosing. "
        "In case of emergency, seek immediate medical help.\n\n"
        "**AR:** هذا الروبوت نموذج تعليمي لموضوع **ارتفاع ضغط الدم**. "
        "لا يقدم تشخيصاً طبياً شخصياً أو وصفات أدوية أو جرعات. في حالات الطوارئ، راجع الطبيب فوراً."
    )
    st.markdown("---")
    st.subheader("📚 Approved Sources / المصادر")
    st.markdown(
        "- [World Health Organization (WHO)](https://www.who.int/news-room/fact-sheets/detail/hypertension)\n"
        "- [CDC - High Blood Pressure](https://www.cdc.gov/blood-pressure/)\n"
        "- [NHS - Hypertension](https://www.nhs.uk/conditions/high-blood-pressure-hypertension/)\n"
        "- [MedlinePlus](https://medlineplus.gov/highbloodpressure.html)"
    )

st.title("🩺 High Blood Pressure AI Assistant")
st.subheader("مساعد الذكاء الاصطناعي التعليمي لارتفاع ضغط الدم")
st.write(
    "Ask any question in **English** or **Arabic** using your own words! / "
    "اطرح سؤالك بأي صيغة باللغتين **العربية** أو **الإنجليزية**!"
)

# تعليمات النظام الصارمة (System Prompt)
SYSTEM_PROMPT = """
You are an intelligent, safe, educational AI Medical Chatbot specialized EXCLUSIVELY in "High Blood Pressure (Hypertension)".

STRICT COMPETITION RULES YOU MUST FOLLOW:
1. LANGUAGE: Respond in the EXACT SAME LANGUAGE the user used (if Arabic -> respond in clear Arabic; if English -> respond in clear English).
2. TOPIC BOUNDARY (Appropriate Uncertainty): You ONLY answer questions related to High Blood Pressure (blood pressure readings, risk factors, lifestyle, diet, prevention, monitoring, symptoms, misconceptions, warning signs). If a user asks about ANY OTHER medical condition (e.g., diabetes, asthma, flu, broken bones) or non-medical topics, politely state that your scope is strictly limited to High Blood Pressure education and you cannot answer outside your topic. Do NOT guess or fabricate.
3. MEDICAL SAFETY:
   - Use educational wording only.
   - NEVER diagnose a user personally.
   - NEVER prescribe medications, suggest specific drug names to take, or give medication dosing instructions.
   - If a user asks whether to stop or change their medication, firmly advise them NOT to stop or alter medication without consulting their prescribing doctor.
   - Always remind the user briefly that this information does not replace a healthcare professional.
4. URGENT WARNING SIGNS: If the user mentions readings above 180/120 mmHg, or symptoms like chest pain, shortness of breath, dizziness with high readings, numbness/weakness, vision changes, or difficulty speaking, immediately highlight that this requires urgent medical evaluation or emergency care.
5. RELIABLE SOURCES & FACTS TO USE:
   - Cite authoritative sources naturally at the end of your response: (Source: WHO / CDC / NHS / MedlinePlus). Never invent fake links or fake studies.
   - Normal BP: Less than 120/80 mmHg (CDC/NHS).
   - High BP (Hypertension): Consistently 130/80 mmHg or higher (CDC) or 140/90 mmHg or higher (NHS/WHO).
   - Silent Killer: Usually has NO symptoms at all.
   - Risk Factors: Age, family history/genetics, high sodium (salt) diet, obesity, physical inactivity, smoking, alcohol, chronic stress.
   - Prevention & Self-care: DASH diet (fruits, vegetables, whole grains, low saturated fat), reducing sodium/salt, regular aerobic exercise, maintaining healthy weight, quitting smoking, home monitoring with a cuff (sphygmomanometer) at the same time daily while resting.
"""

# تهيئة اتصال الذكاء الاصطناعي
client = None
if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    except Exception:
        client = None


# دالة ذكية لاختيار النموذج المتاح في حساب Groq تلقائياً لتجنب خطأ 404
@st.cache_resource
def get_working_model(_client):
    try:
        models = _client.models.list()
        available_ids = [
            m.id
            for m in models.data
            if "whisper" not in m.id.lower()
            and "guard" not in m.id.lower()
            and "tts" not in m.id.lower()
            and "vision" not in m.id.lower()
        ]
        # قائمة النماذج المفضلة بالترتيب
        preferred = [
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "llama3-70b-8192",
            "gemma2-9b-it",
            "mixtral-8x7b-32768",
        ]
        for p in preferred:
            if p in available_ids:
                return p
        # إذا تغيرت الأسماء مستقبلاً، يختار أول نموذج محادثة متاح تلقائياً
        for m_id in available_ids:
            if "llama" in m_id.lower() or "gemma" in m_id.lower() or "qwen" in m_id.lower():
                return m_id
        return available_ids[0] if available_ids else "llama-3.1-8b-instant"
    except Exception:
        return "llama-3.1-8b-instant"


# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال المستخدم
if prompt := st.chat_input("اكتب سؤالك بأي صيغة هنا... / Ask anything about High Blood Pressure..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if client is not None:
            with st.spinner("Thinking... / جاري تحليل السؤال وصياغة الإجابة..."):
                try:
                    active_model = get_working_model(client)
                    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.messages[-6:]:
                        messages_for_api.append({"role": m["role"], "content": m["content"]})

                    completion = client.chat.completions.create(
                        model=active_model,
                        messages=messages_for_api,
                        temperature=0.2,
                        max_tokens=600,
                    )
                    response = completion.choices[0].message.content
                except Exception as e:
                    response = f"⚠️ حدث خطأ في الاتصال بالنموذج الذكي: {e}"
        else:
            response = (
                "⚠️ **تنبيه إعداد المفتاح:** لم يتم العثور على مفتاح `GROQ_API_KEY` في إعدادات `Secrets` داخل Streamlit Cloud."
            )

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})