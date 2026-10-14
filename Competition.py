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
    "EN: Ask any question about Blood Pressure or choose from the 15 verified questions.\n\n"
    "AR: يمكنك طرح أي سؤال أو اختبار الأسئلة الـ 15 المعتمدة لموضوع ضغط الدم."
)

# 📋 قاعدة بيانات الأسئلة الـ 15 وإجاباتها الموثوقة (يمكنك إضافة أو تعديل أي سؤال هنا)
knowledge_base = {
    # 1
    "what is high blood pressure": "**CDC:** High blood pressure is a condition where the force of blood against artery walls is too high, measured in mmHg.",
    "ما هو ارتفاع ضغط الدم": "**CDC:** ارتفاع ضغط الدم هو حالة تكون فيها قوة دفع الدم ضد جدران الشرايين عالية، وتُقاس بالمليمتر زئبق.",
    # 2
    "silent killer": "**NHS:** It's called the silent killer because it often has no symptoms for years while damaging arteries.",
    "القاتل الصامت": "**NHS:** يُسمى بالقاتل الصامت لعدم ظهور أعراض واضحة للمصابين به لسنوات رغم تأثيره المدمر على الشرايين.",
    # 3
    "early symptoms": "**MedlinePlus:** There are usually no early symptoms, which makes regular screening essential.",
    "الأعراض الشائعة": "**MedlinePlus:** لا توجد أعراض مبكرة عادةً، مما يحتم الفحص الدوري بانتظام.",
    # 4
    "severe hypertension symptoms": "**NHS:** Severe high blood pressure can cause severe headaches, shortness of breath, or nosebleeds.",
    "الأعراض المصاحبة لأزمات": "**NHS:** الحالات الحرجة قد يصاحبها صداع شديد، ضيق تنفس، ونزيف أنفي.",
    # 5
    "who is most at risk": "**WHO:** Older adults, people with a family history, and those who are obese or physically inactive.",
    "الأشخاص الأكثر عرضة": "**WHO:** كبار السن، أصحاب التاريخ العائلي، ومن يعانون من السمنة وقلة الحركة.",
    # 6
    "how does sodium affect bp": "**CDC:** Too much sodium holds excess fluid in the body, creating extra pressure on artery walls.",
    "تأثير تناول الملح": "**CDC:** الإفراط في الصوديوم يحبس السوائل ويزيد الضغط على جدران الشرايين.",
    # 7
    "normal blood pressure ranges": "**NHS:** Normal blood pressure is generally less than 120/80 mmHg.",
    "المستويات الطبيعية": "**NHS:** أقل من 120/80 مم زئبق يعتبر النطاق الصحي الطبيعي.",
    # 8
    "how to properly monitor bp": "**NHS:** Use a sphygmomanometer and log your readings regularly at the same time each day.",
    "كيف يتم قياس ضغط الدم": "**NHS:** باستخدام جهاز قياس الضغط وسجل القراءات بانتظام في نفس الوقت يومياً.",
    # 9
    "does stress affect blood pressure": "**WHO:** Yes, chronic stress can cause repeated temporary spikes in blood pressure.",
    "التوتر والقلق": "**WHO:** نعم، التوتر المزمن يؤدي لارتفاع مؤقت ومتكرر في ضغط الدم.",
    # 10
    "dash diet": "**CDC:** A dietary approach rich in vegetables, fruits, and whole grains designed to lower blood pressure.",
    "حمية داش": "**CDC:** نظام غذائي غني بالخضروات والفواكه والحبوب الكاملة لخفض الضغط.",
    # 11
    "is exercise helpful": "**NHS:** Yes, regular physical activity strengthens the heart and effectively lowers blood pressure.",
    "الرياضة": "**NHS:** نعم، النشاط البدني المنتظم يقوي القلب ويخفض الضغط بفعالية.",
    # 12
    "stop medication": "**NHS:** Never stop blood pressure medication without direct instructions from your prescribing doctor.",
    "إيقاف دواء الضغط": "**NHS:** خطأ جسيم؛ لا يجب إيقاف الأدوية إلا بأمر وتوجيه طبي مباشر من الطبيب المعالج.",
    # 13
    "does smoking increase blood pressure": "**CDC:** Yes, nicotine temporarily raises blood pressure and damages blood vessel walls over time.",
    "التدخين": "**CDC:** نعم، النيكوتين يرفع الضغط مؤقتاً ويدمر جدران الأوعية الدموية على المدى الطويل.",
    # 14
    "medical emergency": "**NHS:** A reading over 180/120 mmHg with chest pain or difficulty breathing requires emergency care.",
    "حالة طوارئ طبية": "**NHS:** إذا زاد عن 180/120 مم زئبق مع ألم بالصدر أو صعوبة في التنفس، فهذه طوارئ.",
    # 15
    "does this chatbot replace a doctor": "**Safety Rule:** No, this is an educational tool and does not provide personal medical diagnosis.",
    "هل يغني هذا الروبوت": "**نظام السلامة:** لا، هذا النظام تعليمي فقط ولا يقدم تشخيصاً طبياً نهائياً.",
}

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب سؤالك هنا / Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_lower = prompt.lower().strip()

        # البحث الذكي: هل السؤال مطابق أو يحتوي على كلمات من الأسئلة الـ 15 المسجلة؟
        found_response = None
        for key, ans in knowledge_base.items():
            if key in p_lower:
                found_response = ans
                break

        # إذا وجدنا إجابة مطابقة من الـ 15 سؤالاً
        if found_response:
            response = found_response
        else:
            # رد افتراضي ذكي وآمن في حال كان السؤال خارج القائمة ولكن ضمن التخصص
            response = (
                f"شكراً لسؤالك ({prompt}). بصفتي مساعداً تعليمياً لارتفاع ضغط الدم، أنصح بالاستناد إلى التوجيهات الطبية الرسمية (WHO, CDC, NHS). يرجى ملاحظة أن هذه المعلومات تعليمية فقط ولا تغني عن استشارة الطبيب المختص.\n\n"
                f"*(Thank you for your question. Please refer to official guidelines from WHO, CDC, or NHS. This is for educational purposes only.)*"
            )

        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})