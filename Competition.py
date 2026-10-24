import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Iron-Deficiency & Sickle Cell AI Assistant",
    page_icon="🩸",
    layout="centered",
)

# 2. تحسين مظهر الواجهة وشفافية النصوص لقراءة الخلفية المتحركة
st.markdown(
    """
<style>
    /* جعل خلفية Streamlit شفافة جزئياً لكي تظهر حركة خلايا الدم خلف التطبيق */
    .stApp {
        background-color: rgba(10, 13, 20, 0.85) !important;
    }
    
    /* تصميم صناديق المحادثة بلمسة زجاجية أرجوانية-حمراء مع زجاج ضبابي (Backdrop Blur) */
    .stChatMessage {
        background-color: rgba(31, 41, 55, 0.88) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px !important;
    }

    /* الشريط العلوي */
    .main-banner {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.3), rgba(147, 51, 234, 0.2));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 25px rgba(239, 68, 68, 0.2);
    }
    .main-banner h1 {
        color: #f87171;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .main-banner p {
        color: #d1d5db;
        font-size: 13px;
        margin: 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. القائمة الجانبية: التحكم باللغة والأسئلة وحالة الخلايا المتحركة في الخلفية
with st.sidebar:
    st.header("🌐 Language / اللغة")
    ui_lang = st.radio(
        "Select Language / اختر اللغة:",
        ["English 🇬🇧", "العربية 🇸🇦"],
        horizontal=True,
    )

    st.markdown("---")
    st.header("🩸 Background Blood Flow / حركة خلايا الدم")
    anim_mode = st.selectbox(
        "Select Cell Pathology / نمط الخلايا في الخلفية:",
        [
            "Comparative (مقارنة شاملة)",
            "Normal RBCs (خلايا طبيعية)",
            "Iron Deficiency (نقص الحديد - صغار)",
            "Sickle Cell (فقر الدم المنجلي)",
        ],
    )

    mode_map = {
        "Comparative (مقارنة شاملة)": "comparative",
        "Normal RBCs (خلايا طبيعية)": "normal",
        "Iron Deficiency (نقص الحديد - صغار)": "iron",
        "Sickle Cell (فقر الدم المنجلي)": "sickle",
    }
    selected_js_mode = mode_map.get(anim_mode, "comparative")

    st.markdown("---")
    st.header("📋 30 Verified Questions")

    # قاعدة الأسئلة الـ 30
    QA_DATABASE = [
        {
            "id": 1,
            "q_en": "What is iron-deficiency anemia?",
            "q_ar": "ما هو فقر الدم بعوز الحديد؟",
            "a_en": "**Iron-Deficiency Anemia** is a common type of anemia where blood lacks adequate healthy red blood cells due to insufficient iron needed to produce hemoglobin. *(Source: NHS / MedlinePlus)*",
            "a_ar": "**فقر الدم بعوز الحديد:** هو حالة شائعة يفتقر فيها الدم إلى خلايا الدم الحمراء السليمة الكافية بسبب نقص الحديد اللازم لإنتاج الهيموغلوبين. *(المصدر: NHS / MedlinePlus)*",
        },
        {
            "id": 2,
            "q_en": "What is the difference between Iron Deficiency and Sickle Cell Anemia?",
            "q_ar": "ما الفرق بين فقر الدم بعوز الحديد وفقر الدم المنجلي؟",
            "a_en": "**Iron Deficiency Anemia** is an acquired nutritional deficiency causing small, pale RBCs (microcytic). **Sickle Cell Anemia** is a genetic disorder where abnormal hemoglobin (HbS) distorts RBCs into rigid crescent shapes, causing blood vessel blockages. *(Source: WHO / CDC)*",
            "a_ar": "**فقر الدم بعوز الحديد:** نقص تغذوي مكتسب يؤدي لصغر حجم الكريات وشحوبها. **فقر الدم المنجلي:** اضطراب جيني وراثي يتسبب في تشوه الكريات إلى شكل هلالي/منجلي صلب يسبب انسداد الأوعية الدموية. *(المصدر: WHO / CDC)*",
        },
        {
            "id": 3,
            "q_en": "What are the urgent warning signs requiring emergency care?",
            "q_ar": "ما هي العلامات التحذيرية الطارئة لفقر الدم؟",
            "a_en": "**URGENT WARNING SIGNS:** Seek immediate help if you experience chest pain, severe shortness of breath at rest, fainting, or signs of internal bleeding. *(Source: NHS)*",
            "a_ar": "**علامات الطوارئ:** توجه للمستشفى فوراً عند ظهور ألم بالصدر، ضيق شديد بالتنفس أثناء الراحة، إغماء، أو علامات نزيف داخلي. *(المصدر: NHS)*",
        },
    ]

    if ui_lang == "English 🇬🇧":
        question_options = ["--- Select a sample question (1-30) ---"] + [
            f"{item['id']}. {item['q_en']}" for item in QA_DATABASE
        ]
    else:
        question_options = ["--- اختر سؤالاً من القائمة (1-30) ---"] + [
            f"{item['id']}. {item['q_ar']}" for item in QA_DATABASE
        ]

    selected_q = st.selectbox("Preset:", question_options, label_visibility="collapsed")
    ask_preset_btn = st.button("🚀 Ask Selected Question", use_container_width=True)

    st.markdown("---")
    st.header("⚠️ Disclaimer / إخلاء مسؤولية")
    st.warning("Educational prototype for **Anemia Education**. Not a personal diagnosis.")

# 4. كود كافاس الخلفية المتحركة (HTML5 / JS Canvas)
background_animation_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body, html {{
    margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: transparent;
  }}
  canvas {{
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -999; pointer-events: none;
  }}
</style>
</head>
<body>
<canvas id="bgCanvas"></canvas>
<script>
const canvas = document.getElementById('bgCanvas');
const ctx = canvas.getContext('2d');

function resize() {{
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}}
window.addEventListener('resize', resize);
resize();

let currentMode = "{selected_js_mode}";

class Cell {{
  constructor(type) {{
    this.reset(type);
  }}
  reset(type) {{
    this.type = type || this.getRandomType();
    this.x = -50 - Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = Math.random() * 0.6 + 0.7;
    this.vy = (Math.random() - 0.5) * 0.2;
    this.angle = Math.random() * Math.PI * 2;
    this.vRot = (Math.random() - 0.5) * 0.02;

    if (this.type === 'normal') {{
      this.radius = 13;
      this.color = 'rgba(239, 68, 68, 0.5)';
      this.centerColor = 'rgba(153, 27, 27, 0.6)';
    }} else if (this.type === 'iron') {{
      this.radius = 8;
      this.color = 'rgba(248, 113, 113, 0.5)';
      this.centerColor = 'rgba(254, 242, 242, 0.6)';
    }} else if (this.type === 'sickle') {{
      this.radius = 15;
      this.color = 'rgba(185, 28, 28, 0.65)';
    }}
  }}
  getRandomType() {{
    if (currentMode !== 'comparative') return currentMode;
    const r = Math.random();
    if (r < 0.4) return 'normal';
    if (r < 0.7) return 'iron';
    return 'sickle';
  }}
  update() {{
    this.x += this.vx;
    this.y += this.vy;
    this.angle += this.vRot;
    if (this.x > canvas.width + 50) {{
      this.reset();
    }}
  }}
  draw() {{
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.angle);

    if (this.type === 'normal') {{
      ctx.beginPath();
      ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(0, 0, this.radius * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = this.centerColor;
      ctx.fill();
    }} else if (this.type === 'iron') {{
      ctx.beginPath();
      ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(0, 0, this.radius * 0.65, 0, Math.PI * 2);
      ctx.fillStyle = this.centerColor;
      ctx.fill();
    }} else if (this.type === 'sickle') {{
      ctx.beginPath();
      ctx.ellipse(0, 0, this.radius, this.radius * 0.35, 0, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.strokeStyle = 'rgba(127, 29, 29, 0.7)';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }}
    ctx.restore();
  }}
}}

const cells = Array.from({{ length: 55 }}, () => new Cell(currentMode === 'comparative' ? null : currentMode));

function animate() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  cells.forEach(cell => {{
    cell.update();
    cell.draw();
  }});
  requestAnimationFrame(animate);
}}
animate();
</script>
</body>
</html>
"""
components.html(background_animation_html, height=0)

# 5. العنوان الرئيسي للمشروع
st.markdown(
    """
<div class="main-banner">
    <h1>🩸 Hemoglobin Pathology & Anemia AI Assistant</h1>
    <p>Live Background Blood Flow Simulation • Iron-Deficiency & Sickle Cell Education</p>
</div>
""",
    unsafe_allow_html=True,
)

# 6. تعليمات نظام الذكاء الاصطناعي (Groq Llama-3.3)
SYSTEM_PROMPT = """
You are an intelligent, safe, educational AI Medical Chatbot specialized in "Iron-Deficiency Anemia" and related blood pathology (such as Sickle Cell Anemia differences).
RULES:
1. Respond in the EXACT language used by the user (Arabic or English).
2. Answer ONLY questions about Anemia, Iron Deficiency, Sickle Cell, Hemoglobin, Ferritin, and Nutrition.
3. Educational only. NEVER diagnose or prescribe medication doses.
4. Cite official sources at the end: (Source: WHO / NHS / CDC / MedlinePlus).
"""

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
        return available_ids[0] if available_ids else "llama-3.1-8b-instant"
    except Exception:
        return "llama-3.1-8b-instant"


def search_local_kb(user_text):
    text_lower = user_text.lower().strip()
    is_english = any(ord(c) < 128 and c.isalpha() for c in user_text)

    for item in QA_DATABASE:
        if item["q_en"].lower() in text_lower or item["q_ar"] in text_lower:
            return item["a_en"] if is_english else item["a_ar"]

    return (
        "As an educational assistant specialized in **Anemia Education**, please refer to official guidelines from **WHO, CDC, or NHS**."
        if is_english
        else "بصفتي مساعداً تعليمياً مخصصاً لموضوع **فقر الدم**، أنصحك بالرجوع إلى الإرشادات الطبية المعتمدة من **(WHO, CDC, NHS)**."
    )


# 7. واجهة وتفاعل الشات بوت
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask any question in English or Arabic / اكتب سؤالك هنا...")

if ask_preset_btn and not selected_q.startswith("---"):
    user_query = selected_q.split(". ", 1)[1] if ". " in selected_q else selected_q

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if client is not None:
            with st.spinner("Analyzing against medical sources..."):
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
                except Exception:
                    response = search_local_kb(user_query)
        else:
            response = search_local_kb(user_query)

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})