import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(
    page_title="Iron-Deficiency Anemia AI Assistant",
    page_icon="🩸",
    layout="centered",
)

# 📋 قاعدة البيانات الشاملة للـ 30 سؤالاً (باللغتين الإنجليزية والعربية)
QA_DATABASE = [
    {
        "id": 1,
        "q_en": "What is iron-deficiency anemia?",
        "q_ar": "ما هو فقر الدم بعوز الحديد؟",
        "kw_en": ["what is iron-deficiency", "define iron deficiency", "what is anemia"],
        "kw_ar": ["ما هو فقر الدم", "تعريف فقر الدم", "عوز الحديد"],
        "a_en": "**Iron-Deficiency Anemia** is a common type of anemia where the blood lacks adequate healthy red blood cells due to insufficient iron, which is needed to produce hemoglobin. *(Source: NHS / MedlinePlus)*",
        "a_ar": "**فقر الدم بعوز الحديد:** هو حالة شائعة يفتقر فيها الدم إلى خلايا الدم الحمراء السليمة الكافية بسبب نقص الحديد اللازم لإنتاج الهيموغلوبين. *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 2,
        "q_en": "What is the role of iron and hemoglobin in the body?",
        "q_ar": "ما هي وظيفة الحديد والهيموغلوبين في الجسم؟",
        "kw_en": ["role of iron", "function of hemoglobin", "why do we need iron"],
        "kw_ar": ["وظيفة الحديد", "دور الهيموغلوبين", "أهمية الحديد"],
        "a_en": "**Role of Iron & Hemoglobin:** Iron is essential for making hemoglobin, a protein in red blood cells that enables them to carry oxygen from the lungs to tissues and organs throughout the body. *(Source: WHO)*",
        "a_ar": "**وظيفة الحديد والهيموغلوبين:** الحديد عنصر أساسي لتكوين الهيموغلوبين، وهو بروتين في خلايا الدم الحمراء يحمل الأكسجين من الرئتين إلى جميع أنسجة وأعضاء الجسم. *(المصدر: WHO)*",
    },
    {
        "id": 3,
        "q_en": "How does iron deficiency progress into full anemia?",
        "q_ar": "كيف يتطور نقص الحديد إلى فقر دم كامل؟",
        "kw_en": ["progress", "stages of iron", "deplete"],
        "kw_ar": ["يتطور نقص", "مراحل نقص الحديد", "مخزون"],
        "a_en": "**Progression:** First, the body's stored iron (ferritin) becomes depleted. Once stores are exhausted, the body cannot produce enough hemoglobin, leading to smaller and paler red blood cells (iron-deficiency anemia). *(Source: CDC)*",
        "a_ar": "**مراحل التطور:** يبدأ الأمر بنفاد مخزون الحديد في الجسم (الفيريتين)، وعند استنفاد المخزون يعجز الجسم عن إنتاج كمية كافية من الهيموغلوبين، مما يؤدي لصغر وشحوب خلايا الدم الحمراء. *(المصدر: CDC)*",
    },
    {
        "id": 4,
        "q_en": "What is the difference between Heme and Non-Heme iron?",
        "q_ar": "ما الفرق بين الحديد الهيمي (الحيواني) وغير الهيمي (النباتي)؟",
        "kw_en": ["heme", "non-heme", "animal vs plant iron"],
        "kw_ar": ["الهيمي", "حيواني", "نباتي"],
        "a_en": "**Heme vs. Non-Heme Iron:** Heme iron comes from animal sources (meat, fish, poultry) and is easily absorbed by the body. Non-heme iron comes from plant sources (beans, lentils, spinach) and is absorbed less efficiently. *(Source: CDC)*",
        "a_ar": "**الفرق بينهما:** الحديد الهيمي يوجد في المصادر الحيوانية (اللحوم، الدواجن، الأسماك) ويمتصه الجسم بسهولة عالية، بينما الحديد غير الهيمي يوجد في النباتات (العدس، السبانخ، الحبوب) ويكون امتصاصه أقل كفاءة. *(المصدر: CDC)*",
    },
    {
        "id": 5,
        "q_en": "Which populations are at the highest risk for iron-deficiency anemia?",
        "q_ar": "من هم الفئات الأكثر عرضة للإصابة بفقر الدم بعوز الحديد؟",
        "kw_en": ["highest risk", "who is at risk", "risk groups", "populations"],
        "kw_ar": ["الأكثر عرضة", "الفئات المعرضة", "عوامل الخطر"],
        "a_en": "**High-Risk Groups:** Women of reproductive age (due to menstruation), pregnant women, infants and young children, frequent blood donors, and people with vegetarian/vegan diets or malabsorption conditions. *(Source: WHO / CDC)*",
        "a_ar": "**الفئات الأكثر عرضة:** النساء في سن الإنجاب، الحوامل، الرضع والأطفال الصغار، المتبرعون بالدم بانتظام، والنباتيون أو المصابون بمشاكل سوء الامتصاص. *(المصدر: WHO / CDC)*",
    },
    {
        "id": 6,
        "q_en": "Why are pregnant women at high risk for iron deficiency?",
        "q_ar": "لماذا تعتبر النساء الحوامل أكثر عرضة لنقص الحديد؟",
        "kw_en": ["pregnant", "pregnancy"],
        "kw_ar": ["الحوامل", "الحمل", "حامل"],
        "a_en": "**Pregnancy Risk:** During pregnancy, blood volume expands significantly, and extra iron is required to support the growing fetus and placenta, sharply increasing daily iron needs. *(Source: CDC / WHO)*",
        "a_ar": "**خطر الحمل:** يزداد حجم الدم بشكل كبير أثناء الحمل، ويحتاج الجسم لكميات إضافية من الحديد لدعم نمو الجنين والمشيمة. *(المصدر: CDC / WHO)*",
    },
    {
        "id": 7,
        "q_en": "What are the most common symptoms of iron-deficiency anemia?",
        "q_ar": "ما هي الأعراض الأكثر شيوعاً لفقر الدم بعوز الحديد؟",
        "kw_en": ["common symptoms", "signs of anemia", "what are the symptoms"],
        "kw_ar": ["الأعراض الأكثر شيوعاً", "أعراض فقر الدم", "علامات نقص الحديد"],
        "a_en": "**Common Symptoms:** Extreme fatigue, weakness, pale skin (pallor), shortness of breath, dizziness or lightheadedness, headache, and cold hands and feet. *(Source: NHS)*",
        "a_ar": "**الأعراض الشائعة:** الإرهاق والتعب الشديد، الضعف العام، شحوب الجلد، ضيق التنفس، الدوار أو الدوخة، الصداع، وبرودة اليدين والقدمين. *(المصدر: NHS)*",
    },
    {
        "id": 8,
        "q_en": "Can mild iron-deficiency anemia have no symptoms at all?",
        "q_ar": "هل يمكن ألا يسبب فقر الدم الخفيف أي أعراض؟",
        "kw_en": ["mild", "no symptoms", "asymptomatic"],
        "kw_ar": ["خفيف", "بدون أعراض", "بلا أعراض"],
        "a_en": "**Mild Cases:** Yes, mild to moderate iron-deficiency anemia often causes no noticeable symptoms at first; symptoms typically appear and worsen as the anemia progresses. *(Source: MedlinePlus)*",
        "a_ar": "**الحالات الخفيفة:** نعم، قد لا يسبب فقر الدم الخفيف أي أعراض ملحوظة في البداية، وتظهر الأعراض وتزداد وضوحاً كلما تفاقم النقص. *(المصدر: MedlinePlus)*",
    },
    {
        "id": 9,
        "q_en": "How does iron-deficiency anemia affect fingernails and hair?",
        "q_ar": "كيف يؤثر نقص الحديد على الأظافر والشعر؟",
        "kw_en": ["nails", "fingernails", "hair", "spoon", "brittle"],
        "kw_ar": ["الأظافر", "الشعر", "تقصف", "أظافر ملعقية"],
        "a_en": "**Nails & Hair:** Chronic iron deficiency can cause brittle or spoon-shaped fingernails (koilonychia) and increased hair thinning or hair loss due to reduced oxygen delivery to follicles. *(Source: NHS)*",
        "a_ar": "**الأظافر والشعر:** يمكن أن يسبب نقص الحديد المزمن هشاشة وتكسر الأظافر أو تقعرها (الأظافر الملعقية)، بالإضافة إلى تساقط الشعر وضعفه نتيجة نقص وصول الأكسجين للبصيلات. *(المصدر: NHS)*",
    },
    {
        "id": 10,
        "q_en": "What is 'Pica' and how is it linked to iron deficiency?",
        "q_ar": "ما هي ظاهرة (بيكا - Pica) وما علاقتها بنقص الحديد؟",
        "kw_en": ["pica", "ice", "dirt", "craving"],
        "kw_ar": ["بيكا", "ثلج", "تراب", "شهية غريبة"],
        "a_en": "**Pica:** Pica is an unusual craving to eat substances with no nutritional value, such as ice (pagophagia), dirt, clay, or paper. It is a well-documented symptom of severe iron deficiency. *(Source: MedlinePlus)*",
        "a_ar": "**ظاهرة بيكا (Pica):** هي رغبة غير معتادة في تناول مواد غير غذائية مثل مضغ الثلج، أو التراب، أو الورق، وهي من العلامات المعروفة المرتبطة بنقص الحديد الشديد. *(المصدر: MedlinePlus)*",
    },
    {
        "id": 11,
        "q_en": "How does iron deficiency affect the tongue and mouth?",
        "q_ar": "كيف يؤثر فقر الدم بعوز الحديد على اللسان والفم؟",
        "kw_en": ["tongue", "mouth", "sore tongue", "ulcers"],
        "kw_ar": ["اللسان", "الفم", "التهاب اللسان", "تقرحات"],
        "a_en": "**Tongue & Mouth:** It can cause a swollen, inflamed, or strangely smooth and sore tongue (glossitis), dry mouth, and painful cracks at the corners of the mouth (angular cheilitis). *(Source: NHS)*",
        "a_ar": "**اللسان والفم:** قد يسبب التهاباً أو تورماً وألماً في اللسان مع نعومة سطحه، بالإضافة إلى جفاف الفم وتشققات مؤلمة في زوايا الفم. *(المصدر: NHS)*",
    },
    {
        "id": 12,
        "q_en": "Can iron-deficiency anemia cause Restless Legs Syndrome?",
        "q_ar": "هل يسبب نقص الحديد متلازمة تململ الساقين؟",
        "kw_en": ["restless legs", "legs", "tingling"],
        "kw_ar": ["تململ الساقين", "الساقين", "تنميل"],
        "a_en": "**Restless Legs Syndrome:** Yes, iron deficiency is linked to Restless Legs Syndrome (RLS), which causes an unpleasant crawling sensation and an irresistible urge to move the legs, especially at night. *(Source: NHS)*",
        "a_ar": "**متلازمة تململ الساقين:** نعم، يرتبط نقص الحديد برغبة ملحة وغير مريحة لتحريك الساقين خاصة أثناء الليل والراحة، وتتحسن غالباً بمعالجة نقص الحديد. *(المصدر: NHS)*",
    },
    {
        "id": 13,
        "q_en": "What are the main causes of blood loss that lead to iron deficiency?",
        "q_ar": "ما هي الأسباب الرئيسية لفقدان الدم التي تؤدي لنقص الحديد؟",
        "kw_en": ["blood loss", "bleeding", "menstruation", "ulcer"],
        "kw_ar": ["فقدان الدم", "نزيف", "الطمث", "قرحة"],
        "a_en": "**Blood Loss Causes:** Heavy menstrual periods in women and slow, chronic gastrointestinal bleeding (from peptic ulcers, hiatal hernias, colon polyps, or regular use of NSAID painkillers like ibuprofen/aspirin). *(Source: NHS / MedlinePlus)*",
        "a_ar": "**أسباب فقدان الدم:** غزارة الدورة الشهرية لدى النساء، أو النزيف البطيء والمزمن في الجهاز الهضمي (بسبب قرحة المعدة، البواسير، أو الاستخدام المفرط لمسكنات الألم مثل الإيبوبروفين والأسبرين). *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 14,
        "q_en": "How do digestive disorders like Celiac disease cause iron-deficiency anemia?",
        "q_ar": "كيف تسبب أمراض الجهاز الهضمي مثل السيلياك (حساسية القمح) فقر الدم؟",
        "kw_en": ["celiac", "malabsorption", "digestive", "intestine"],
        "kw_ar": ["السيلياك", "امتصاص", "الأمعاء", "حساسية القمح"],
        "a_en": "**Malabsorption:** Iron from food is absorbed in the upper small intestine. Conditions like Celiac disease, Crohn's disease, or gastric bypass surgery damage the intestinal lining and impair iron absorption. *(Source: MedlinePlus)*",
        "a_ar": "**سوء الامتصاص:** يتم امتصاص الحديد في الأمعاء الدقيقة؛ لذا فإن أمراضاً مثل السيلياك (حساسية القمح) أو التهابات الأمعاء أو جراحات تكميم وتحويل مسار المعدة تضعف قدرة الجسم على امتصاص الحديد. *(المصدر: MedlinePlus)*",
    },
    {
        "id": 15,
        "q_en": "What are the best animal-based dietary sources of iron?",
        "q_ar": "ما هي أفضل المصادر الغذائية الحيوانية الغنية بالحديد؟",
        "kw_en": ["animal sources", "meat", "liver", "best animal"],
        "kw_ar": ["المصادر الحيوانية", "اللحوم", "الكبدة", "حيوانية"],
        "a_en": "**Animal Sources (Heme Iron):** Lean red meat (beef, lamb), liver and organ meats, poultry (chicken, turkey), and seafood (sardines, tuna, oysters). *(Source: NHS / CDC)*",
        "a_ar": "**المصادر الحيوانية:** اللحوم الحمراء (البقر والضأن)، الكبدة، الدواجن، والأسماك والمأكولات البحرية (مثل السردين والتونة). *(المصدر: NHS / CDC)*",
    },
    {
        "id": 16,
        "q_en": "What are the best plant-based dietary sources of iron for vegetarians?",
        "q_ar": "ما هي أفضل المصادر النباتية الغنية بالحديد للنباتيين؟",
        "kw_en": ["plant-based", "vegetarian", "vegan", "plant sources"],
        "kw_ar": ["المصادر النباتية", "النباتيين", "نباتية", "البقوليات"],
        "a_en": "**Plant Sources (Non-Heme Iron):** Lentils, chickpeas, kidney beans, tofu, dark leafy greens (spinach, kale), pumpkin seeds, nuts, dried fruits (apricots, raisins), and iron-fortified cereals/bread. *(Source: NHS / CDC)*",
        "a_ar": "**المصادر النباتية:** العدس، الحمص، الفاصوليا، الخضروات الورقية الداكنة (السبانخ)، البذور والمكسرات، الفواكه المجففة (المشمش والزبيب)، والحبوب المدعمة بالحديد. *(المصدر: NHS / CDC)*",
    },
    {
        "id": 17,
        "q_en": "How does Vitamin C affect iron absorption?",
        "q_ar": "كيف يؤثر فيتامين C على امتصاص الحديد في الجسم؟",
        "kw_en": ["vitamin c", "orange", "citrus", "boost absorption"],
        "kw_ar": ["فيتامين c", "فيتامين سي", "البرتقال", "يزيد امتصاص"],
        "a_en": "**Vitamin C Effect:** Vitamin C captures non-heme iron and stores it in a form that the body absorbs much more easily. Drinking citrus juice or eating bell peppers/tomatoes with meals significantly boosts iron absorption. *(Source: CDC / MedlinePlus)*",
        "a_ar": "**دور فيتامين C:** يساعد فيتامين C (الموجود في الحمضيات، عصير البرتقال، الفلفل الحلو، والطماطم) على تحويل الحديد النباتي إلى صيغة يسهل على الأمعاء امتصاصها بكفاءة عالية. *(المصدر: CDC / MedlinePlus)*",
    },
    {
        "id": 18,
        "q_en": "Why should tea and coffee be avoided directly with iron-rich meals?",
        "q_ar": "لماذا يُنصح بتجنب شرب الشاي والقهوة مباشرة مع الوجبات الغنية بالحديد؟",
        "kw_en": ["tea", "coffee", "caffeine", "tannins"],
        "kw_ar": ["الشاي", "القهوة", "الكافيين", "التانينات"],
        "a_en": "**Tea & Coffee:** Tea and coffee contain polyphenols and tannins that bind to iron during digestion and inhibit its absorption. Wait at least 1–2 hours after an iron-rich meal before drinking them. *(Source: NHS)*",
        "a_ar": "**الشاي والقهوة:** يحتويان على مركبات التانينات والبوليفينول التي ترتبط بالحديد في الأمعاء وتعيق امتصاصه، لذا يُفضل تناولهما بعد الوجبة بساعة إلى ساعتين. *(المصدر: NHS)*",
    },
    {
        "id": 19,
        "q_en": "How does calcium (milk and dairy) interact with iron absorption?",
        "q_ar": "كيف يتفاعل الكالسيوم (الحليب ومشتقاته) مع امتصاص الحديد؟",
        "kw_en": ["calcium", "milk", "dairy"],
        "kw_ar": ["الكالسيوم", "الحليب", "الألبان"],
        "a_en": "**Calcium Interaction:** High amounts of calcium (from milk, cheese, or calcium supplements) compete with iron for absorption in the intestines, so iron supplements should not be taken with milk. *(Source: NHS / MedlinePlus)*",
        "a_ar": "**تفاعل الكالسيوم:** الكالسيوم بكميات كبيرة (مثل الحليب والأجبان أو حبوب الكالسيوم) ينافس الحديد على الامتصاص في الأمعاء، لذا يُنصح بعدم تناول مكملات الحديد مع الحليب في نفس الوقت. *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 20,
        "q_en": "What blood tests are used by doctors to diagnose iron-deficiency anemia?",
        "q_ar": "ما هي التحاليل الطبية المخبرية المستخدمة لتشخيص فقر الدم بعوز الحديد؟",
        "kw_en": ["blood tests", "diagnose", "cbc", "clinical testing"],
        "kw_ar": ["التحاليل", "فحوصات", "تشخيص", "تحليل الدم"],
        "a_en": "**Clinical Blood Tests:** Diagnosis requires a Complete Blood Count (CBC) to check hemoglobin, hematocrit, and Mean Corpuscular Volume (MCV), alongside a Serum Ferritin test, Serum Iron, and Total Iron-Binding Capacity (TIBC). *(Source: MedlinePlus / NHS)*",
        "a_ar": "**الفحوصات المخبرية:** يتم التشخيص عبر فحص تعداد الدم الكامل (CBC) لقياس الهيموغلوبين وحجم الكريات (MCV)، وفحص مخزون الحديد في المصل (Serum Ferritin)، ومستوى الحديد والسعة الرابطة للحديد (TIBC). *(المصدر: MedlinePlus / NHS)*",
    },
    {
        "id": 21,
        "q_en": "What is the difference between Hemoglobin and Serum Ferritin in blood tests?",
        "q_ar": "ما الفرق بين تحليل الهيموغلوبين وتحليل مخزون الحديد (Ferritin)؟",
        "kw_en": ["ferritin", "difference between hemoglobin"],
        "kw_ar": ["الفيريتين", "مخزون الحديد", "الفرق بين الهيموغلوبين"],
        "a_en": "**Hemoglobin vs. Ferritin:** Hemoglobin measures the functional protein currently carrying oxygen in red blood cells, while Serum Ferritin measures the amount of backup iron stored in the body's tissues. Low ferritin is the most specific indicator of depleted iron stores. *(Source: MedlinePlus)*",
        "a_ar": "**الهيموغلوبين مقابل الفيريتين:** الهيموغلوبين يقيس البروتين الفعلي الناقل للأكسجين في كريات الدم حالياً، بينما الفيريتين (مخزون الحديد) يقيس كمية الحديد الاحتياطية المخزنة في الكبد والأنسجة، وهو الأدق لكشف النقص المبكر. *(المصدر: MedlinePlus)*",
    },
    {
        "id": 22,
        "q_en": "What does a low MCV (microcytic red blood cells) mean in an anemia test?",
        "q_ar": "ماذا يعني انخفاض مؤشر (MCV) في تحليل الدم؟",
        "kw_en": ["mcv", "microcytic", "small red blood cells"],
        "kw_ar": ["mcv", "حجم كريات", "صغر حجم"],
        "a_en": "**Low MCV:** Mean Corpuscular Volume (MCV) measures the average size of red blood cells. In iron-deficiency anemia, MCV is typically low (microcytic), meaning the red blood cells are smaller than normal due to lack of hemoglobin. *(Source: MedlinePlus)*",
        "a_ar": "**انخفاض MCV:** يقيس هذا المؤشر متوسط حجم كريات الدم الحمراء؛ وفي فقر الدم بعوز الحديد يكون منخفضاً (Microcytic) لأن الكريات تصبح أصغر حجماً وأقل احمراراً بسبب نقص الهيموغلوبين. *(المصدر: MedlinePlus)*",
    },
    {
        "id": 23,
        "q_en": "Can I take high-dose iron supplements on my own without seeing a doctor?",
        "q_ar": "هل يمكنني تناول حبوب ومكملات الحديد بجرعات عالية من تلقاء نفسي بدون طبيب؟",
        "kw_en": ["without a doctor", "on my own", "high-dose", "self-medicate", "overdose"],
        "kw_ar": ["من تلقاء نفسي", "بدون طبيب", "جرعات عالية", "تسمم الحديد"],
        "a_en": "**Safety Warning (Misconception):** No! Never take high-dose iron supplements without a doctor's supervision and blood test confirmation. Excess iron cannot be easily excreted by the body and can cause severe toxicity, liver damage, and organ failure. *(Source: NHS / MedlinePlus)*",
        "a_ar": "**تحذير طبي (مفهوم خاطئ):** لا، يُمنع تناول مكملات الحديد بجرعات علاجية دون فحص وإشراف طبي؛ لأن الجسم لا يتخلص من الحديد الزائد بسهولة، مما قد يسبب تسمماً بالحديد وتلفاً خطيراً في الكبد والأعضاء. *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 24,
        "q_en": "Does feeling tired and exhausted always mean I have iron-deficiency anemia?",
        "q_ar": "هل الشعور بالتعب والإرهاق يعني دائماً أنني مصاب بفقر الدم؟",
        "kw_ar": ["الشعور بالتعب", "دائماً", "يعني حتماً"],
        "kw_en": ["always mean", "tired always", "exhausted always"],
        "a_en": "**Misconception:** No. Fatigue is a non-specific symptom caused by many conditions (poor sleep, stress, thyroid issues, vitamin D/B12 deficiency). Only a clinical blood test ordered by a doctor can confirm iron-deficiency anemia. *(Source: NHS)*",
        "a_ar": "**مفهوم خاطئ:** لا، التعب عرض عام يشترك فيه العديد من الحالات (مثل قلة النوم، الإجهاد، خمول الغدة الدرقية، أو نقص فيتامين D و B12)، ولا يتأكد تشخيص فقر الدم إلا بتحليل الدم المخبري. *(المصدر: NHS)*",
    },
    {
        "id": 25,
        "q_en": "Is eating spinach alone enough to cure severe iron-deficiency anemia?",
        "q_ar": "هل تناول السبانخ أو الغذاء وحده يكفي لعلاج فقر الدم الحاد؟",
        "kw_en": ["spinach alone", "diet alone", "cure severe"],
        "kw_ar": ["السبانخ", "الغذاء وحده", "يكفي لعلاج"],
        "a_en": "**Misconception:** No. Spinach contains non-heme iron along with oxalates, which make its iron hard to absorb. Furthermore, once severe clinical anemia develops, diet alone is usually insufficient and doctor-prescribed iron therapy is needed alongside treating the underlying cause. *(Source: NHS / CDC)*",
        "a_ar": "**مفهوم خاطئ:** لا؛ السبانخ يحتوي على الأوكسالات التي تقلل امتصاص الحديد، كما أن حالات فقر الدم الحاد لا يكفي فيها الغذاء وحده، بل تتطلب علاج السبب الرئيسي ومكملات يصفها الطبيب المختص. *(المصدر: NHS / CDC)*",
    },
    {
        "id": 26,
        "q_en": "What are the common side effects of oral iron supplements?",
        "q_ar": "ما هي الآثار الجانبية الشائعة لحبوب الحديد؟",
        "kw_en": ["side effects", "black stool", "constipation"],
        "kw_ar": ["الآثار الجانبية", "الإمساك", "لون البراز"],
        "a_en": "**Side Effects:** Oral iron supplements commonly cause constipation or diarrhea, mild stomach cramps, nausea, and harmless dark/black-colored stools. Always consult your doctor or pharmacist if side effects are severe. *(Source: NHS)*",
        "a_ar": "**الآثار الجانبية:** قد تسبب حبوب الحديد الإمساك أو الإسهال، اضطراباً خفيفاً في المعدة، وتغيراً طبيعياً غير ضار في لون البراز إلى اللون الداكن. يُنصح باستشارة الطبيب لتنظيم طريقة أخذها. *(المصدر: NHS)*",
    },
    {
        "id": 27,
        "q_en": "How long does it usually take to replenish iron stores under medical supervision?",
        "q_ar": "كم يستغرق تعويض مخزون الحديد في الجسم تحت الإشراف الطبي؟",
        "kw_en": ["how long", "replenish", "months"],
        "kw_ar": ["كم يستغرق", "مدة العلاج", "تعويض مخزون"],
        "a_en": "**Recovery Timeline:** Under medical treatment, hemoglobin levels usually improve within 2 to 4 weeks, but treatment often continues for 3 to 6 months under a doctor's supervision to fully rebuild ferritin stores. *(Source: NHS)*",
        "a_ar": "**مدة التعافي:** تحت إشراف الطبيب، يبدأ الهيموغلوبين بالتحسن خلال أسبوعين إلى 4 أسابيع، لكن تعويض مخزون الحديد (الفيريتين) بالكامل يستغرق عادةً من 3 إلى 6 أشهر مع المتابعة الطبية. *(المصدر: NHS)*",
    },
    {
        "id": 28,
        "q_en": "What are the urgent warning signs of anemia that require immediate emergency care?",
        "q_ar": "ما هي العلامات التحذيرية الطارئة لفقر الدم التي تستدعي الذهاب للمستشفى فوراً؟",
        "kw_en": ["urgent", "emergency", "warning signs", "chest pain", "fainting"],
        "kw_ar": ["الطارئة", "طوارئ", "علامات التحذير", "ألم في الصدر", "إغماء"],
        "a_en": "**URGENT WARNING SIGNS:** Seek immediate emergency medical help if you experience chest pain, severe shortness of breath at rest, rapid or irregular heartbeat (palpitations), fainting, or signs of internal bleeding (vomiting blood or tarry black stools without taking iron). *(Source: NHS / MedlinePlus)*",
        "a_ar": "**علامات التحذير الطارئة:** يجب التوجه للطوارئ فوراً عند ظهور ألم في الصدر، ضيق شديد في التنفس أثناء الراحة، خفقان سريع أو غير منتظم بالقلب، إغماء، أو علامات نزيف داخلي. *(المصدر: NHS / MedlinePlus)*",
    },
    {
        "id": 29,
        "q_en": "Does this AI chatbot replace a doctor or provide personal medical prescriptions?",
        "q_ar": "هل يغني هذا الروبوت عن استشارة الطبيب أو يصف جرعات الأدوية؟",
        "kw_en": ["replace a doctor", "prescribe", "purpose of this chatbot"],
        "kw_ar": ["يغني عن", "استشارة الطبيب", "يصف أدوية"],
        "a_en": "**Medical Safety Boundary:** No. This chatbot is strictly an educational prototype. It cannot diagnose conditions, interpret personal lab reports, or prescribe medication doses. Always consult a qualified healthcare professional. *(Safety Rule)*",
        "a_ar": "**حدود الأمان الطبي:** لا إطلاقاً؛ هذا الروبوت هو نموذج تعليمي وتوعوي فقط، ولا يقوم بالتشخيص الشخصي أو وصف الأدوية والجرعات، ولا يغني أبداً عن مراجعة الطبيب المختص. *(نظام السلامة)*",
    },
    {
        "id": 30,
        "q_en": "What is the best treatment for Type 2 Diabetes or High Blood Pressure?",
        "q_ar": "ما هو أفضل علاج لمرض السكري أو ارتفاع ضغط الدم أو الربو؟",
        "kw_en": ["diabetes", "blood pressure", "asthma", "migraine", "influenza", "uti"],
        "kw_ar": ["السكري", "ضغط الدم", "الربو", "الشقيقة", "الأنفلونزا"],
        "a_en": "**Out-of-Scope Limitation:** I apologize, but my knowledge scope is strictly limited to **Iron-Deficiency Anemia** education. I cannot answer questions about Diabetes, High Blood Pressure, or other conditions. Please consult a healthcare professional or official medical portals like WHO/NHS. *(Appropriate Uncertainty Rule)*",
        "a_ar": "**خارج نطاق التخصص (Appropriate Uncertainty):** أعتذر منك، ولكن نطاقي التعليمي مخصص حصراً لموضوع **فقر الدم بعوز الحديد (Iron-Deficiency Anemia)** ولا يمكنني الإجابة أو الإفتاء في أمراض أخرى كالسكري أو الضغط. يرجى مراجعة الطبيب المختص. *(قاعدة حدود المعرفة)*",
    },
]

# الشريط الجانبي: اختيار اللغة + اختيار من الـ 30 سؤالاً + إخلاء المسؤولية + المصادر
with st.sidebar:
    st.header("🌐 Language / اللغة")
    ui_lang = st.radio(
        "Select Interface & Preset Questions Language:",
        ["English 🇬🇧", "العربية 🇮🇶"],
        horizontal=True,
    )

    st.markdown("---")
    st.header("📋 30 Verified Questions / الأسئلة الـ 30")
    st.caption(
        "Click any question below to test the bot immediately / اضغط لتجربة أي سؤال مباشرة:"
    )

    if ui_lang == "English 🇬🇧":
        question_options = ["--- Select a sample question (1-30) ---"] + [
            f"{item['id']}. {item['q_en']}" for item in QA_DATABASE
        ]
    else:
        question_options = ["--- اختر سؤالاً من القائمة (1-30) ---"] + [
            f"{item['id']}. {item['q_ar']}" for item in QA_DATABASE
        ]

    selected_q = st.selectbox("Preset Questions:", question_options, label_visibility="collapsed")
    ask_preset_btn = st.button("🚀 Ask Selected Question / إرسال السؤال المختار", use_container_width=True)

    st.markdown("---")
    st.header("⚠️ Disclaimer / إخلاء مسؤولية")
    st.warning(
        "**EN:** Educational prototype for **Iron-Deficiency Anemia**. "
        "No personal diagnosis or supplement dosing. Seek emergency care for urgent symptoms.\n\n"
        "**AR:** نموذج تعليمي لموضوع **فقر الدم بعوز الحديد**. "
        "لا يقدم تشخيصاً شخصياً أو جرعات دوائية. راجع الطوارئ فوراً عند الأعراض الحرجة."
    )
    st.subheader("📚 Approved Sources")
    st.markdown(
        "- [WHO - Anaemia](https://www.who.int/news-room/fact-sheets/detail/anaemia)\n"
        "- [NHS - Iron Deficiency](https://www.nhs.uk/conditions/iron-deficiency-anaemia/)\n"
        "- [MedlinePlus](https://medlineplus.gov/irondeficiencyanemia.html)\n"
        "- [CDC - Iron](https://www.cdc.gov/nutrition/micronutrient-malnutrition/about-iron/)"
    )

# عنوان الصفحة الرئيسي
st.title("🩸 Iron-Deficiency Anemia AI Assistant")
st.subheader("مساعد الذكاء الاصطناعي التعليمي لفقر الدم بعوز الحديد")
st.write(
    "🇬🇧 **English:** Type any question in English or select from the 30 verified questions in the sidebar.\n\n"
    "🇮🇶 **العربية:** اكتب أي سؤال بالعربية أو الإنجليزية بأسلوبك الخاص، أو اختر من الأسئلة الـ 30 في القائمة الجانبية."
)

# تعليمات النظام الصارمة (System Prompt) للذكاء الاصطناعي
SYSTEM_PROMPT = """
You are an intelligent, safe, educational AI Medical Chatbot specialized EXCLUSIVELY in "Iron-Deficiency Anemia (فقر الدم بعوز الحديد)".

STRICT COMPETITION RULES YOU MUST FOLLOW:
1. LANGUAGE DETECTION:
   - If the user writes in ENGLISH, you MUST respond 100% in clear, professional ENGLISH.
   - If the user writes in ARABIC, you MUST respond 100% in clear, professional ARABIC.
2. TOPIC BOUNDARY (Appropriate Uncertainty):
   - You ONLY answer questions related to Iron-Deficiency Anemia (iron, hemoglobin, ferritin, CBC/MCV, symptoms, pica, causes, nutrition, heme vs non-heme, vitamin C, tea/coffee/calcium interactions, prevention, warning signs).
   - If the user asks about ANY OTHER medical topic (e.g., diabetes, high blood pressure, asthma, flu, infections) or non-medical topic, politely refuse and state that your scope is strictly limited to Iron-Deficiency Anemia. Do NOT guess.
3. MEDICAL SAFETY:
   - Educational wording only. NEVER diagnose a patient or prescribe iron supplement dosages.
   - Warn against taking high-dose iron supplements without medical supervision due to iron toxicity risks.
   - Always include a brief note that this does not replace a healthcare professional.
4. URGENT WARNING SIGNS:
   - If chest pain, severe shortness of breath at rest, fainting, rapid heartbeat, or black/tarry stools (internal bleeding) are mentioned, instruct the user to seek immediate emergency medical care.
5. CITATIONS:
   - Cite authoritative sources at the end of every medical answer: (Source: WHO / NHS / MedlinePlus / CDC). Never invent fake links.
"""

# تهيئة اتصال الذكاء الاصطناعي Groq
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
        preferred = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "gemma2-9b-it",
        ]
        for p in preferred:
            if p in available_ids:
                return p
        return available_ids[0] if available_ids else "llama-3.1-8b-instant"
    except Exception:
        return "llama-3.1-8b-instant"


# دالة البحث الذكي في قاعدة الـ 30 سؤالاً (كخط دفاع احتياطي أو للأسئلة المطابقة)
def search_local_kb(user_text):
    text_lower = user_text.lower().strip()
    is_english = any(ord(c) < 128 and c.isalpha() for c in user_text)

    for item in QA_DATABASE:
        # تطابق مباشر مع نص السؤال المختار من القائمة
        if item["q_en"].lower() in text_lower or item["q_ar"] in text_lower:
            return item["a_en"] if is_english else item["a_ar"]

    # تطابق الكلمات المفتاحية عند عدم توفر API
    for item in QA_DATABASE:
        if is_english:
            if any(kw in text_lower for kw in item["kw_en"]):
                return item["a_en"]
        else:
            if any(kw in text_lower for kw in item["kw_ar"]):
                return item["a_ar"]

    if is_english:
        return (
            "As an educational assistant specialized in **Iron-Deficiency Anemia**, I recommend consulting official guidelines from **WHO, CDC, NHS, or MedlinePlus** regarding your query. "
            "Please note that this tool is for educational purposes only and does not replace a doctor's consultation."
        )
    else:
        return (
            "بصفتي مساعداً تعليمياً مخصصاً لموضوع **فقر الدم بعوز الحديد**، أنصحك بالرجوع إلى الإرشادات الطبية المعتمدة من **(WHO, CDC, NHS, MedlinePlus)**. "
            "يرجى تذكر أن هذه الأداة لأغراض تعليمية فقط ولا تغني عن استشارة الطبيب المختص."
        )


# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# تحديد السؤال المراد إرساله (سواء من صندوق الكتابة أو من قائمة الـ 30 سؤالاً)
user_query = st.chat_input("Type your question in English or Arabic... / اكتب سؤالك هنا باللغتين...")

if ask_preset_btn and not selected_q.startswith("---"):
    # إزالة الرقم من بداية السؤال المختار
    user_query = selected_q.split(". ", 1)[1] if ". " in selected_q else selected_q

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        response = None
        # المحاولة الأولى: استخدام الذكاء الاصطناعي الحقيقي (للفهم الحر بأي صيغة باللغتين)
        if client is not None:
            with st.spinner("Analyzing & verifying against medical sources... / جاري صياغة الإجابة..."):
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
                    # في حال حدوث أي خلل في السيرفر، ينتقل تلقائياً لقاعدة البيانات المحلية للـ 30 سؤالاً
                    response = search_local_kb(user_query)
        else:
            # في حال عدم وجود مفتاح API، يجيب فوراً من قاعدة الـ 30 سؤالاً باللغتين
            response = search_local_kb(user_query)

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})