import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="Blood Pressure Educational Assistant",
    page_icon="🩺",
    layout="centered",
)

# شريط جانبي لإخلاء المسؤولية
with st.sidebar:
    st.header("⚠️ Disclaimer / إخلاء مسؤولية")
    st.write(
        "EN: This chatbot is an educational prototype for High Blood Pressure and does not provide final medical diagnosis.\n\n"
        "AR: هذا الروبوت هو نموذج تعليمي لارتفاع ضغط الدم ولا يقدم تشخيصاً نهائياً."
    )
    st.markdown("---")
    st.info("Topic: High Blood Pressure (موضوع المشروع: ارتفاع ضغط الدم)")

st.title("🩺 Blood Pressure Assistant / مساعد ضغط الدم التعليمي")
st.write(
    "EN: Ask any question about Blood Pressure in English or Arabic.\n\n"
    "AR: يمكنك طرح أي سؤال باللغتين العربية أو الإنجليزية."
)

# 🇬🇧 قاعدة بيانات الأسئلة باللغة الإنجليزية
kb_english = {
    "what is": "**CDC:** High blood pressure is a condition where the force of blood against artery walls is too high, measured in mmHg.",
    "silent killer": "**NHS:** It's called the silent killer because it often has no symptoms for years while damaging arteries.",
    "symptom": "**MedlinePlus:** There are usually no early symptoms, which makes regular screening essential. Severe cases can cause headaches or shortness of breath.",
    "risk": "**WHO:** Older adults, people with a family history, obesity, physical inactivity, and smoking are at higher risk.",
    "sodium": "**CDC:** Too much sodium holds excess fluid in the body, creating extra pressure on artery walls.",
    "normal": "**NHS:** Normal blood pressure is generally less than 120/80 mmHg.",
    "monitor": "**NHS:** Use a sphygmomanometer and log your readings regularly at the same time each day.",
    "stress": "**WHO:** Yes, chronic stress can cause repeated temporary spikes in blood pressure.",
    "dash": "**CDC:** A dietary approach rich in vegetables, fruits, and whole grains designed to lower blood pressure.",
    "exercise": "**NHS:** Yes, regular physical activity strengthens the heart and effectively lowers blood pressure.",
    "medication": "**NHS:** Never stop blood pressure medication without direct instructions from your prescribing doctor.",
    "smoke": "**CDC:** Yes, nicotine temporarily raises blood pressure and damages blood vessel walls over time.",
    "emergency": "**NHS:** A reading over 180/120 mmHg with chest pain or difficulty breathing requires emergency care.",
    "doctor": "**Safety Rule:** No, this is an educational tool and does not provide personal medical diagnosis. Always consult a physician.",
}

# 🇸🇦 قاعدة بيانات الأسئلة باللغة العربية
kb_arabic = {
    "ما هو": "**CDC:** ارتفاع ضغط الدم هو حالة تكون فيها قوة دفع الدم ضد جدران الشرايين عالية، وتُقاس بالمليمتر زئبق.",
    "القاتل الصامت": "**NHS:** يُسمى بالقاتل الصامت لعدم ظهور أعراض واضحة للمصابين به لسنوات رغم تأثيره المدمر.",
    "أعراض": "**MedlinePlus:** لا توجد أعراض مبكرة عادةً. الحالات الحرجة قد يصاحبها صداع شديد أو ضيق تنفس.",
    "أسباب": "**WHO:** تتضمن التقدم في العمر، السمنة، الوراثة، قلة الحركة، زيادة تناول الملح، والتدخين.",
    "ملح": "**CDC:** الإفراط في الصوديوم يحبس السوائل ويزيد الضغط على جدران الشرايين.",
    "مستويات": "**NHS:** أقل من 120/80 مم زئبق يعتبر النطاق الصحي الطبيعي.",
    "قياس": "**NHS:** باستخدام جهاز قياس الضغط وسجل القراءات بانتظام في نفس الوقت يومياً.",
    "التوتر": "**WHO:** نعم، التوتر المزمن يؤدي لارتفاع مؤقت ومتكرر في ضغط الدم.",
    "داش": "**CDC:** نظام غذائي غني بالخضروات والفواكه والحبوب الكاملة لخفض الضغط.",
    "رياضة": "**NHS:** نعم، النشاط البدني المنتظم يقوي القلب ويخفض الضغط بفعالية.",
    "دواء": "**NHS:** خطأ جسيم؛ لا يجب إيقاف الأدوية إلا بأمر وتوجيه طبي مباشر من الطبيب المعالج.",
    "تدخين": "**CDC:** نعم، النيكوتين يرفع الضغط مؤقتاً ويدمر جدران الأوعية الدموية على المدى الطويل.",
    "طوارئ": "**NHS:** إذا زاد عن 180/120 مم زئبق مع ألم بالصدر أو صعوبة في التنفس، فهذه طوارئ.",
    "طبيب": "**نظام السلامة:** لا، هذا النظام تعليمي فقط ولا يقدم تشخيصاً طبياً نهائياً ويجب استشارة الطبيب.",
}

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input(
    "اكتب سؤالك هنا / Type your question in English or Arabic..."
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_lower = prompt.lower().strip()

        # كشف اللغة: هل الحروف لاتينية (إنجليزية) أم عربية؟
        is_english = any(ord(c) < 128 and c.isalpha() for c in prompt)

        found_response = None

        if is_english:
            # البحث في القاموس الإنجليزي
            for keyword, ans in kb_english.items():
                if keyword in p_lower:
                    found_response = ans
                    break
            if not found_response:
                found_response = (
                    f"Thank you for your question about '{prompt}'. As an educational assistant for High Blood Pressure, please refer to official guidelines from WHO, CDC, or NHS. This is for educational purposes only."
                )
        else:
            # البحث في القاموس العربي
            for keyword, ans in kb_arabic.items():
                if keyword in p_lower:
                    found_response = ans
                    break
            if not found_response:
                found_response = (
                    f"شكراً لسؤالك حول ({prompt}). بصفتي مساعداً تعليمياً لارتفاع ضغط الدم، أنصح بالاستناد إلى التوجيهات الطبية الرسمية (WHO, CDC, NHS). هذه المعلومات تعليمية فقط ولا تغني عن استشارة الطبيب."
                )

        response = found_response
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})