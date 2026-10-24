import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Iron-Deficiency Anemia & Sickle Cell AI Assistant",
    page_icon="🩸",
    layout="wide",
)

# 2. Custom CSS Styling
st.markdown(
    """
<style>
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .blood-banner {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.2), rgba(147, 51, 234, 0.15));
        border: 1px solid rgba(239, 68, 68, 0.35);
        padding: 18px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 25px rgba(239, 68, 68, 0.2);
    }
    .blood-banner h1 {
        color: #f87171;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .blood-banner p {
        color: #9ca3af;
        font-size: 13px;
        margin: 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. Header Banner
st.markdown(
    """
<div class="blood-banner">
    <h1>🩸 Hemoglobin Pathology & Anemia Assistant</h1>
    <p>Interactive Blood Flow Simulation & AI Educational Chatbot • WHO, NHS, CDC Guidelines</p>
</div>
""",
    unsafe_allow_html=True,
)

# 4. EMBEDDED CANVAS SIMULATION (HTML/JS)
html_visualizer_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background-color: #0a0d14; color: #e2e8f0; padding: 10px; overflow-x: hidden; }
  .sim-container { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 15px; width: 100%; }
  .controls-bar { display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: center; margin-bottom: 12px; background: #1f2937; padding: 10px 14px; border-radius: 8px; }
  .btn-group { display: flex; gap: 6px; flex-wrap: wrap; }
  .btn { background: #374151; color: #f3f4f6; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; transition: all 0.2s; }
  .btn:hover { background: #4b5563; }
  .btn.active { background: #dc2626; color: #ffffff; box-shadow: 0 0 10px rgba(220, 38, 38, 0.5); }
  canvas { width: 100%; height: 260px; background: #000; border-radius: 8px; display: block; border: 1px solid #374151; cursor: crosshair; }
  .legend { display: flex; justify-content: space-around; margin-top: 10px; font-size: 12px; color: #9ca3af; flex-wrap: wrap; gap: 10px; }
  .legend-item { display: flex; align-items: center; gap: 6px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
</style>
</head>
<body>

<div class="sim-container">
  <div class="controls-bar">
    <div class="btn-group" id="mode-group">
      <button class="btn active" onclick="setMode('comparative')">Comparative Flow</button>
      <button class="btn" onclick="setMode('normal')">Normal RBCs</button>
      <button class="btn" onclick="setMode('iron')">Iron Deficiency (Microcytic)</button>
      <button class="btn" onclick="setMode('sickle')">Sickle Cell (HbS)</button>
    </div>
    <div style="display: flex; gap: 12px; align-items: center; font-size: 12px;">
      <label>Speed: <input type="range" id="speedSlider" min="0.5" max="3" step="0.1" value="1.2" oninput="flowSpeed = parseFloat(this.value)"></label>
      <button class="btn" onclick="togglePause()" id="pauseBtn">Pause</button>
    </div>
  </div>

  <canvas id="bloodCanvas"></canvas>

  <div class="legend">
    <div class="legend-item"><span class="dot" style="background:#ef4444;"></span> Normal RBC (Biconcave Disc)</div>
    <div class="legend-item"><span class="dot" style="background:#f87171; border: 2px solid #fee2e2;"></span> Iron Deficiency (Microcytic/Hypochromic)</div>
    <div class="legend-item"><span class="dot" style="background:#b91c1c; border-radius: 2px;"></span> Sickle Cell (Rigid Crescent)</div>
  </div>
</div>

<script>
const canvas = document.getElementById('bloodCanvas');
const ctx = canvas.getContext('2d');
let animId, isPaused = false;
let currentMode = 'comparative';
let flowSpeed = 1.2;

function resizeCanvas() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class Cell {
  constructor(type) {
    this.reset(type);
  }

  reset(type) {
    this.type = type || this.getRandomType();
    this.x = -20 - Math.random() * 100;
    this.y = Math.random() * (canvas.height - 40) + 20;
    this.vx = (Math.random() * 0.8 + 1.2) * flowSpeed;
    this.vy = (Math.random() - 0.5) * 0.3;
    this.angle = Math.random() * Math.PI * 2;
    this.vRot = (Math.random() - 0.5) * 0.03;
    this.stuck = false;

    if (this.type === 'normal') {
      this.radius = 11;
      this.color = '#ef4444';
      this.centerColor = '#991b1b';
    } else if (this.type === 'iron') {
      this.radius = 7;
      this.color = '#f87171';
      this.centerColor = '#fef2f2';
    } else if (this.type === 'sickle') {
      this.radius = 12;
      this.color = '#991b1b';
    }
  }

  getRandomType() {
    if (currentMode !== 'comparative') return currentMode;
    const r = Math.random();
    if (r < 0.4) return 'normal';
    if (r < 0.7) return 'iron';
    return 'sickle';
  }

  update() {
    if (this.stuck) return;

    this.type = (currentMode === 'comparative') ? this.type : currentMode;
    this.x += this.vx * flowSpeed;
    this.y += this.vy;
    this.angle += this.vRot;

    // Sickle cells can get stuck near vessel borders
    if (this.type === 'sickle' && (this.y < 35 || this.y > canvas.height - 35) && Math.random() < 0.005) {
      this.stuck = true;
      setTimeout(() => { this.stuck = false; }, 2500);
    }

    if (this.x > canvas.width + 30) {
      this.reset();
    }
  }

  draw() {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.angle);

    if (this.type === 'normal') {
      ctx.beginPath();
      ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(0, 0, this.radius * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = this.centerColor;
      ctx.fill();
    } else if (this.type === 'iron') {
      ctx.beginPath();
      ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(0, 0, this.radius * 0.65, 0, Math.PI * 2);
      ctx.fillStyle = this.centerColor;
      ctx.fill();
    } else if (this.type === 'sickle') {
      ctx.beginPath();
      ctx.ellipse(0, 0, this.radius, this.radius * 0.35, 0, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.strokeStyle = '#7f1d1d';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
    ctx.restore();
  }
}

const cells = Array.from({ length: 45 }, () => new Cell());

function setMode(mode) {
  currentMode = mode;
  document.querySelectorAll('#mode-group .btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  cells.forEach(c => c.reset(mode === 'comparative' ? null : mode));
}

function togglePause() {
  isPaused = !isPaused;
  document.getElementById('pauseBtn').innerText = isPaused ? 'Resume' : 'Pause';
  if (!isPaused) animate();
}

function animate() {
  if (isPaused) return;

  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw vessel borders
  ctx.fillStyle = 'rgba(220, 38, 38, 0.15)';
  ctx.fillRect(0, 0, canvas.width, 18);
  ctx.fillRect(0, canvas.height - 18, canvas.width, 18);

  ctx.strokeStyle = '#b91c1c';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, 18); ctx.lineTo(canvas.width, 18);
  ctx.moveTo(0, canvas.height - 18); ctx.lineTo(canvas.width, canvas.height - 18);
  ctx.stroke();

  cells.forEach(cell => {
    cell.update();
    cell.draw();
  });

  animId = requestAnimationFrame(animate);
}

animate();
</script>
</body>
</html>
"""

# Render the custom canvas component inside Streamlit
components.html(html_visualizer_code, height=360)

st.markdown("---")

# 5. Database of 30 Questions (English & Arabic)
QA_DATABASE = [
    {
        "id": 1,
        "q_en": "What is iron-deficiency anemia?",
        "q_ar": "ما هو فقر الدم بعوز الحديد؟",
        "kw_en": [
            "what is iron-deficiency",
            "define iron deficiency",
            "what is anemia",
        ],
        "kw_ar": ["ما هو فقر الدم", "تعريف فقر الدم", "عوز الحديد"],
        "a_en": "**Iron-Deficiency Anemia** is a common type of anemia where the blood lacks adequate healthy red blood cells due to insufficient iron, which is needed to produce hemoglobin. *(Source: NHS / MedlinePlus)*",
        "a_ar": "**فقر الدم بعوز الحديد:** هو حالة شائعة يفتقر فيها الدم إلى خلايا الدم الحمراء السليمة الكافية بسبب نقص الحديد اللازم لإنتاج الهيموغلوبين. *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 2,
        "q_en": "What is the difference between Iron Deficiency and Sickle Cell Anemia?",
        "q_ar": "ما الفرق بين فقر الدم بعوز الحديد وفقر الدم المنجلي؟",
        "kw_en": [
            "sickle cell vs iron",
            "difference between sickle",
            "sickle cell anemia",
        ],
        "kw_ar": ["المنجلي", "فقر الدم المنجلي", "الفرق بين المنجلي والحديد"],
        "a_en": "**Iron Deficiency Anemia** is an acquired nutritional deficiency causing small, pale RBCs (microcytic/hypochromic). **Sickle Cell Anemia** is a genetic disorder where abnormal hemoglobin (HbS) causes RBCs to distort into rigid crescent/sickle shapes, leading to blood vessel blockages and pain crises. *(Source: WHO / CDC)*",
        "a_ar": "**فقر الدم بعوز الحديد:** هو نقص تغذوي مكتسب يؤدي لصغر حجم الكريات وشحوبها. **فقر الدم المنجلي:** هو اضطراب جيني وراثي يتسبب في تشوه خلايا الدم الحمراء إلى شكل هلالي/منجلي صلب، مما يسبب انسداد الأوعية الدموية ونوبات ألم حادة. *(المصدر: WHO / CDC)*",
    },
    {
        "id": 3,
        "q_en": "What is the role of iron and hemoglobin in the body?",
        "q_ar": "ما هي وظيفة الحديد والهيموغلوبين في الجسم؟",
        "kw_en": [
            "role of iron",
            "function of hemoglobin",
            "why do we need iron",
        ],
        "kw_ar": ["وظيفة الحديد", "دور الهيموغلوبين", "أهمية الحديد"],
        "a_en": "**Role of Iron & Hemoglobin:** Iron is essential for making hemoglobin, a protein in red blood cells that enables them to carry oxygen from the lungs to tissues and organs throughout the body. *(Source: WHO)*",
        "a_ar": "**وظيفة الحديد والهيموغلوبين:** الحديد عنصر أساسي لتكوين الهيموغلوبين، وهو بروتين في خلايا الدم الحمراء يحمل الأكسجين من الرئتين إلى جميع أنسجة وأعضاء الجسم. *(المصدر: WHO)*",
    },
    {
        "id": 4,
        "q_en": "What are the most common symptoms of iron-deficiency anemia?",
        "q_ar": "ما هي الأعراض الأكثر شيوعاً لفقر الدم بعوز الحديد؟",
        "kw_en": [
            "common symptoms",
            "signs of anemia",
            "what are the symptoms",
        ],
        "kw_ar": ["الأعراض الأكثر شيوعاً", "أعراض فقر الدم", "علامات نقص الحديد"],
        "a_en": "**Common Symptoms:** Extreme fatigue, weakness, pale skin (pallor), shortness of breath, dizziness or lightheadedness, headache, and cold hands and feet. *(Source: NHS)*",
        "a_ar": "**الأعراض الشائعة:** الإرهاق والتعب الشديد، الضعف العام، شحوب الجلد، ضيق التنفس، الدوار أو الدوخة، الصداع، وبرودة اليدين والقدمين. *(المصدر: NHS)*",
    },
    {
        "id": 5,
        "q_en": "What are the urgent warning signs that require emergency medical care?",
        "q_ar": "ما هي العلامات التحذيرية الطارئة لفقر الدم التي تستدعي الذهاب للمستشفى فوراً؟",
        "kw_en": [
            "urgent",
            "emergency",
            "warning signs",
            "chest pain",
            "fainting",
        ],
        "kw_ar": [
            "الطارئة",
            "طوارئ",
            "علامات التحذير",
            "ألم في الصدر",
            "إغماء",
        ],
        "a_en": "**URGENT WARNING SIGNS:** Seek immediate emergency medical help if you experience chest pain, severe shortness of breath at rest, rapid or irregular heartbeat (palpitations), fainting, or signs of internal bleeding (vomiting blood or tarry black stools). *(Source: NHS / MedlinePlus)*",
        "a_ar": "**علامات التحذير الطارئة:** يجب التوجه للطوارئ فوراً عند ظهور ألم في الصدر، ضيق شديد في التنفس أثناء الراحة، خفقان سريع أو غير منتظم بالقلب، إغماء، أو علامات نزيف داخلي. *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 6,
        "q_en": "Does this AI chatbot replace a doctor or provide personal medical prescriptions?",
        "q_ar": "هل يغني هذا الروبوت عن استشارة الطبيب أو يصف جرعات الأدوية؟",
        "kw_en": ["replace a doctor", "prescribe", "purpose of this chatbot"],
        "kw_ar": ["يغني عن", "استشارة الطبيب", "يصف أدوية"],
        "a_en": "**Medical Safety Boundary:** No. This chatbot is strictly an educational prototype. It cannot diagnose conditions, interpret personal lab reports, or prescribe medication doses. Always consult a qualified healthcare professional. *(Safety Rule)*",
        "a_ar": "**حدود الأمان الطبي:** لا إطلاقاً؛ هذا الروبوت هو نموذج تعليمي وتوعوي فقط، ولا يقوم بالتشخيص الشخصي أو وصف الأدوية والجرعات، ولا يغني أبداً عن مراجعة الطبيب المختص. *(نظام السلامة)*",
    },
]

# 6. Sidebar Controls & Preset Questions
with st.sidebar:
    st.header("🌐 Language / اللغة")
    ui_lang = st.radio(
        "Select Language:", ["English 🇬🇧", "العربية 🇮🇶"], horizontal=True
    )

    st.markdown("---")
    st.header("📋 Preset Questions")

    if ui_lang == "English 🇬🇧":
        question_options = ["--- Select a question ---"] + [
            f"{item['id']}. {item['q_en']}" for item in QA_DATABASE
        ]
    else:
        question_options = ["--- اختر سؤالاً ---"] + [
            f"{item['id']}. {item['q_ar']}" for item in QA_DATABASE
        ]

    selected_q = st.selectbox(
        "Questions:", question_options, label_visibility="collapsed"
    )
    ask_preset_btn = st.button(
        "🚀 Ask Selected Question", use_container_width=True
    )

    st.markdown("---")
    st.header("⚠️ Disclaimer")
    st.warning(
        "Educational prototype for **Iron-Deficiency & Anemia Education**. "
        "No personal diagnosis or prescription. Seek emergency care for severe symptoms."
    )
    st.subheader("📚 Approved Sources")
    st.markdown(
        "- [WHO - Anaemia](https://www.who.int/news-room/fact-sheets/detail/anaemia)\n"
        "- [NHS - Iron Deficiency](https://www.nhs.uk/conditions/iron-deficiency-anaemia/)\n"
        "- [CDC - Anemia](https://www.cdc.gov/nutrition/micronutrient-malnutrition/about-iron/)"
    )

# 7. AI System Prompt
SYSTEM_PROMPT = """
You are an intelligent, safe, educational AI Medical Chatbot specialized EXCLUSIVELY in "Iron-Deficiency Anemia" and related blood pathology concepts (like Sickle Cell Anemia differences).

RULES:
1. Respond in the EXACT language used by the user (Arabic or English).
2. Answer ONLY questions about Anemia, Iron Deficiency, Hemoglobin, Ferritin, Nutrition, Symptoms, and Blood Cell Pathology. Politely refuse non-related medical conditions.
3. Educational only. NEVER diagnose or prescribe medication doses.
4. Highlight urgent warning signs if chest pain, severe shortness of breath, or fainting are mentioned.
5. Always cite official sources at the end: (Source: WHO / NHS / CDC / MedlinePlus).
"""

# Initialize Groq Client
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
            if all(
                x not in m.id.lower()
                for x in ["whisper", "guard", "tts", "vision"]
            )
        ]
        preferred = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
        ]
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
        "As an educational assistant specialized in **Anemia Education**, please refer to official guidelines from **WHO, CDC, or NHS**. This tool is for educational purposes only."
        if is_english
        else "بصفتي مساعداً تعليمياً مخصصاً لموضوع **فقر الدم**، أنصحك بالرجوع إلى الإرشادات الطبية المعتمدة من **(WHO, CDC, NHS)**. هذه الأداة لأغراض تعليمية فقط."
    )


# 8. Chat Interface & Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask any question about Anemia or Blood Cells...")

if ask_preset_btn and not selected_q.startswith("---"):
    user_query = (
        selected_q.split(". ", 1)[1] if ". " in selected_q else selected_q
    )

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if client is not None:
            with st.spinner("Analyzing against medical sources..."):
                try:
                    active_model = get_working_model(client)
                    messages_for_api = [
                        {"role": "system", "content": SYSTEM_PROMPT}
                    ]
                    for m in st.session_state.messages[-6:]:
                        messages_for_api.append(
                            {"role": m["role"], "content": m["content"]}
                        )

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