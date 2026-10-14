import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="المساعد الطبي التفاعلي التعليمي", page_icon="🏥", layout="centered"
)

# شريط جانبي لإخلاء المسؤولية (إلزامي لمتطلبات السلامة الطبية)
with st.sidebar:
    st.header("⚠️ إخطار وإخلاء مسؤولية")
    st.write(
        "هذا الروبوت هو نموذج تعليمي وبحثي ولا يقدم تشخيصاً نهائياً أو وصفات علاجية. في حال الطوارئ، يرجى مراجعة الطبيب فوراً."
    )
    st.markdown("---")
    st.info("موضوع المشروع: روبوت محادثة طبي تعليمي مستند إلى مصادر موثوقة.")

st.title("🏥 المساعد الطبي التفاعلي التعليمي")
st.write(
    "أهلاً بك! اطرح سؤالك الصحي وسيقوم المساعد بإجابتك استناداً إلى المعايير الطبية المعتمدة."
)

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب سؤالك الطبي هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد الآمن والتعليمي
    with st.chat_message("assistant"):
        # منطق الردود التعليمية بناءً على المدخلات أو رد افتراضي موثوق
        query_lower = prompt.lower()
        if "أعراض" in query_lower or "symptoms" in query_lower:
            response = (
                "بناءً على الإرشادات الطبية الموثوقة (مثل WHO و MedlinePlus)، تختلف الأعراض حسب الحالة المخصصة."
                " يُنصح دائماً بمراقبة العلامات المبكرة واستشارة المختصين وعدم الاعتماد على التشخيص الذاتي."
            )
        elif "وقاية" in query_lower or "prevention" in query_lower:
            response = (
                "الوقاية تعتمد على اتباع نمط حياة صحي، الالتزام بالإرشادات الوقائية، والفحوصات الدورية المنتظمة."
            )
        else:
            response = (
                f"شكراً لسؤالك حول ({prompt}). بصفتي مساعداً تعليمياً، أُذّنك بأن هذه المعلومات هي لأغراض توعوية فقط، "
                "ولا تغني عن استشارة الطبيب المختص. يرجى دائماً الرجوع إلى مصادر مثل CDC أو NHS للمعلومات السريرية."
            )

        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})