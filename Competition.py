import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Iron-Deficiency Anemia AI Assistant",
    page_icon="🩸",
    layout="centered",
)

# 2. تنسيق الواجهة بشكل نظيف واحترافي
st.markdown(
    """
<style>
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .main-banner {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.2), rgba(147, 51, 234, 0.15));
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
    }
    .main-banner h1 {
        color: #f87171;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .main-banner p {
        color: #9ca3af;
        font-size: 13px;
        margin: 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. قائمة الأسئلة الـ 30 المعتمدة (تستخدم كاختصارات سريعة في القائمة الجانبية)
QA_DATABASE = [
    {
        "id": 1,
        "q_en": "What is iron-deficiency anemia?",
        "q_ar": "ما هو فقر الدم بعوز الحديد؟",
    },
    {
        "id": 2,
        "q_en": "What is the role of iron and hemoglobin in the body?",
        "q_ar": "ما هي وظيفة الحديد والهيموغلوبين في الجسم؟",
    },
    {
        "id": 3,
        "q_en": "How does iron deficiency progress into full anemia?",
        "q_ar": "كيف يتطور نقص الحديد إلى فقر دم كامل؟",
    },
    {
        "id": 4,
        "q_en": "What is the difference between Heme and Non-Heme iron?",
        "q_ar": "ما الفرق بين الحديد الهيمي وغير الهيمي؟",
    },
    {
        "id": 5,
        "q_en": "Which populations are at the highest risk for iron-deficiency anemia?",
        "q_ar": "من هم الفئات الأكثر عرضة للإصابة بفقر الدم بعوز الحديد؟",
    },
    {
        "id": 6,
        "q_en": "Why are pregnant women at high risk for iron deficiency?",
        "q_ar": "لماذا تعتبر النساء الحوامل أكثر عرضة لنقص الحديد؟",
    },
    {
        "id": 7,
        "q_en": "What are the most common symptoms of iron-deficiency anemia?",
        "q_ar": "ما هي الأعراض الأكثر شيوعاً لفقر الدم بعوز الحديد؟",
    },
    {
        "id": 8,
        "q_en": "Can mild iron-deficiency anemia have no symptoms at all?",
        "q_ar": "هل يمكن ألا يسبب فقر الدم الخفيف أي أعراض؟",
    },
    {
        "id": 9,
        "q_en": "How does iron-deficiency anemia affect fingernails and hair?",
        "q_ar": "كيف يؤثر نقص الحديد على الأظافر والشعر؟",
    },
    {
        "id": 10,
        "q_en": "What is 'Pica' and how is it linked to iron deficiency?",
        "q_ar": "ما هي ظاهرة (بيكا - Pica) وما علاقتها بنقص الحديد؟",
    },
    {
        "id": 11,
        "q_en": "How does iron deficiency affect the tongue and mouth?",
        "q_ar": "كيف يؤثر فقر الدم بعوز الحديد على اللسان والفم؟",
    },
    {
        "id": 12,
        "q_en": "Can iron-deficiency anemia cause Restless Legs Syndrome?",
        "q_ar": "هل يسبب نقص الحديد متلازمة تململ الساقين؟",
    },
    {
        "id": 13,
        "q_en": "What are the main causes of blood loss that lead to iron deficiency?",
        "q_ar": "ما هي الأسباب الرئيسية لفقدان الدم التي تؤدي لنقص الحديد؟",
    },
    {
        "id": 14,
        "q_en": "How do digestive disorders like Celiac disease cause iron-deficiency anemia?",
        "q_ar": "كيف تسبب أمراض الجهاز الهضمي مثل السيلياك فقر الدم؟",
    },
    {
        "id": 15,
        "q_en": "What are the best animal-based dietary sources of iron?",
        "q_ar": "ما هي أفضل المصادر الغذائية الحيوانية الغنية بالحديد؟",
    },
    {
        "id": 16,
        "q_en": "What are the best plant-based dietary sources of iron for vegetarians?",
        "q_ar": "ما هي أفضل المصادر النباتية الغنية بالحديد للنباتيين؟",
    },
    {
        "id": 17,
        "q_en": "How does Vitamin C affect iron absorption?",
        "q_ar": "كيف يؤثر فيتامين C على امتصاص الحديد في الجسم؟",
    },
    {
        "id": 18,
        "q_en": "Why should tea and coffee be avoided directly with iron-rich meals?",
        "q_ar": "لماذا يُنصح بتجنب شرب الشاي والقهوة مباشرة مع الوجبات الغنية بالحديد؟",
    },
    {
        "id": 19,
        "q_en": "How does calcium (milk and dairy) interact with iron absorption?",
        "q_ar": "كيف يتفاعل الكالسيوم (الحليب ومشتقاته) مع امتصاص الحديد؟",
    },
    {
        "id": 20,
        "q_en": "What blood tests are used by doctors to diagnose iron-deficiency anemia?",
        "q_ar": "ما هي التحاليل الطبية المخبرية المستخدمة لتشخيص فقر الدم بعوز الحديد؟",
    },
    {
        "id": 21,
        "q_en": "What is the difference between Hemoglobin and Serum Ferritin in blood tests?",
        "q_ar": "ما الفرق بين تحليل الهيموغلوبين وتحليل مخزون الحديد (Ferritin)؟",
    },
    {
        "id": 22,
        "q_en": "What does a low MCV (microcytic red blood cells) mean in an anemia test?",
        "q_ar": "ماذا يعني انخفاض مؤشر (MCV) في تحليل الدم؟",
    },
    {
        "id": 23,
        "q_en": "Can I take high-dose iron supplements on my own without seeing a doctor?",
        "q_ar": "هل يمكنني تناول مكملات الحديد بجرعات عالية من تلقاء نفسي بدون طبيب؟",
    },
    {
        "id": 24,
        "q_en": "Does feeling tired and exhausted always mean I have iron-deficiency anemia?",
        "q_ar": "هل الشعور بالتعب والإرهاق يعني دائماً أنني مصاب بفقر الدم؟",
    },
    {
        "id": 25,
        "q_en": "Is eating spinach alone enough to cure severe iron-deficiency anemia?",
        "q_ar": "هل تناول السبانخ أو الغذاء وحده يكفي لعلاج فقر الدم الحاد؟",
    },
    {
        "id": 26,
        "q_en": "What are the common side effects of oral iron supplements?",
        "q_ar": "ما هي الآثار الجانبية الشائعة لحبوب الحديد؟",
    },
    {
        "id": 27,
        "q_en": "How long does it usually take to replenish iron stores under medical supervision?",
        "q_ar": "كم يستغرق تعويض مخزون الحديد في الجسم تحت الإشراف الطبي؟",
    },
    {
        "id": 28,
        "q_en": "What are the urgent warning signs of anemia that require immediate emergency care?",
        "q_ar": "ما هي العلامات التحذيرية الطارئة لفقر الدم التي تستدعي الذهاب للمستشفى فوراً؟",
    },
    {
        "id": 29,
        "q_en": "Does this AI chatbot replace a doctor or provide personal medical prescriptions?",
        "q_ar": "هل يغني هذا الروبوت عن استشارة الطبيب أو يصف جرعات الأدوية؟",
    },
    {
        "id": 30,
        "q_en": "What is the best treatment for Type 2 Diabetes or High Blood Pressure?",
        "q_ar": "ما هو أفضل علاج لمرض السكري أو ارتفاع ضغط الدم؟",
    },
]

# 4. الشريط الجانبي (اللغة، القائمة السريعة للأسئلة، والمصادر)
with st.sidebar:
    st.header("🌐 Language / اللغة")
    ui_lang = st.radio(
        "Select Language / اختر اللغة:",
        ["English 🇬🇧", "العربية 🇸🇦"],
        horizontal=True,
    )

    st.markdown("---")
    st.header("📋 Preset Questions (30)")
    st.caption("Quick shortcuts or type any custom question below:")

    if ui_lang == "English 🇬🇧":
        question_options = ["--- Select a sample question ---"] + [
            f"{item['id']}. {item['q_en']}" for item in QA_DATABASE
        ]
    else:
        question_options = ["--- اختر سؤالاً من القائمة ---"] + [
            f"{item['id']}. {item['q_ar']}" for item in QA_DATABASE
        ]

    selected_q = st.selectbox("Preset:", question_options, label_visibility="collapsed")
    ask_preset_btn = st.button("🚀 Ask Selected Question", use_container_width=True)

    st.markdown("---")
    st.header("⚠️ Disclaimer / إخلاء مسؤولية")
    st.warning(
        "Educational prototype for **Iron-Deficiency Anemia**. "
        "Not a personal diagnosis or supplement prescription. Seek emergency care for severe symptoms."
    )
    st.subheader("📚 Approved Sources")
    st.markdown(
        "- [WHO - Anaemia](https://www.who.int/news-room/fact-sheets/detail/anaemia)\n"
        "- [NHS - Iron Deficiency](https://www.nhs.uk/conditions/iron-deficiency-anaemia/)\n"
        "- [MedlinePlus](https://medlineplus.gov/irondeficiencyanemia.html)\n"
        "- [CDC - Iron](https://www.cdc.gov/nutrition/micronutrient-malnutrition/about-iron/)"
    )

# 5. عنوان الصفحة الرئيسي
st.markdown(
    """
<div class="main-banner">
    <h1>🩸 Iron-Deficiency Anemia AI Assistant</h1>
    <p>Educational Medical Chatbot • Ask any open-ended question in English or Arabic</p>
</div>
""",
    unsafe_allow_html=True,
)

# 6. تعليمات النظام الذكية التي تجعل النموذج يجيب على أي سؤال حر في التخصص
SYSTEM_PROMPT = """
You are an intelligent, safe, educational AI Medical Chatbot specialized EXCLUSIVELY in "Iron-Deficiency Anemia (فقر الدم بعوز الحديد)".

STRICT RULES YOU MUST FOLLOW:
1. OPEN-ENDED CAPABILITY: You can answer ANY free-form, open-ended question about iron-deficiency anemia, its causes, symptoms, diagnosis (CBC, Ferritin, MCV), nutrition, absorption factors, or related blood concepts dynamically and accurately using medical knowledge.
2. LANGUAGE: Respond in the EXACT same language the user used (if English -> clear English; if Arabic -> clear Arabic).
3. TOPIC BOUNDARY (Appropriate Uncertainty): You ONLY answer questions related to Iron-Deficiency Anemia and its direct context. If the user asks about unrelated conditions (e.g., diabetes, high blood pressure, asthma), politely state that your scope is strictly limited to Iron-Deficiency Anemia education. Do NOT guess or fabricate.
4. MEDICAL SAFETY:
   - Use educational wording only.
   - NEVER diagnose a user personally or prescribe iron supplement doses.
   - Warn against high-dose self-supplementation due to toxicity risks.
   - Remind the user that this does not replace a doctor.
5. URGENT WARNING SIGNS: If the user mentions chest pain, severe shortness of breath at rest, fainting, or signs of internal bleeding, immediately instruct them to seek emergency medical care.
6. CITATIONS: Always cite authoritative sources naturally at the end of your response: (Source: WHO / NHS / MedlinePlus / CDC).
"""

# تهيئة اتصال Groq API
client = None
if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    except Exception:
        client = None


@st.cache_resource
def get_working_model(_client):
    try:
        models = _client.models.list()
        available_ids = [
            m.id
            for m in models.data
            if all(x not in m.id.lower() for x in ["whisper", "guard", "tts", "vision"])
        ]
        preferred = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-8b-8192"]
        for p in preferred:
            if p in available_ids:
                return p
        return available_ids[0] if available_ids else "llama-3.3-70b-versatile"
    except Exception:
        return "llama-3.3-70b-versatile"


# 7. إدارة ذاكرة المحادثة والشات بوت المفتوح
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# التقاط السؤال سواء من كتابة المستخدم الحرة أو من القائمة الجانبية
user_query = st.chat_input("Ask any question freely in English or Arabic... / اطرح أي سؤال حر هنا...")

if ask_preset_btn and not selected_q.startswith("---"):
    user_query = selected_q.split(". ", 1)[1] if ". " in selected_q else selected_q

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if client is not None:
            with st.spinner("Thinking & analyzing against medical guidelines... / جاري تحليل السؤال..."):
                try:
                    active_model = get_working_model(client)
                    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.messages[-8:]:
                        messages_for_api.append({"role": m["role"], "content": m["content"]})

                    completion = client.chat.completions.create(
                        model=active_model,
                        messages=messages_for_api,
                        temperature=0.3,
                        max_tokens=700,
                    )
                    response = completion.choices[0].message.content
                except Exception as e:
                    response = f"⚠️ حدث خطأ أثناء الاتصال بمحرك الذكاء الاصطناعي: {e}"
        else:
            response = (
                "⚠️ **تنبيه إعداد المفتاح:** لم يتم العثور على مفتاح `GROQ_API_KEY` في إعدادات `Secrets` على منصة Streamlit Cloud. "
                "يرجى إضافته ليعمل الذكاء الاصطناعي ويجيب على الأسئلة الحرة."
            )

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})