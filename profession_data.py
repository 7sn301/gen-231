"""
وحدة المهن والتعليم - لإضافة واقعية للحسابات المُولّدة
Professions, Education & Bio Generator Module
"""

import random

# ===========================
# قاعدة بيانات المهن والاهتمامات
# ===========================
PROFESSIONS = {
    "doctor": {
        "ar": "طبيب",
        "en": "Doctor",
        "specialties_ar": ["طب أسنان", "طب عام", "جراحة", "طب أطفال", "طب نساء", "أمراض قلب", "جلدية"],
        "specialties_en": ["Dentistry", "General Medicine", "Surgery", "Pediatrics", "Gynecology", "Cardiology", "Dermatology"],
        "hashtags": ["#طب", "#أطباء", "#صحة", "#medical"],
        "emoji": "🩺",
    },
    "medical_student": {
        "ar": "طالب طب",
        "en": "Medical Student",
        "specialties_ar": ["طب بشري", "طب أسنان", "صيدلة", "تمريض"],
        "specialties_en": ["Medicine", "Dentistry", "Pharmacy", "Nursing"],
        "hashtags": ["#الدراسة_في_الخارج", "#طالب_طب", "#medstudent"],
        "emoji": "🎓",
    },
    "engineer": {
        "ar": "مهندس",
        "en": "Engineer",
        "specialties_ar": ["مدني", "كهربائي", "ميكانيكي", "برمجيات", "معماري"],
        "specialties_en": ["Civil", "Electrical", "Mechanical", "Software", "Architectural"],
        "hashtags": ["#هندسة", "#engineering", "#tech"],
        "emoji": "👷",
    },
    "developer": {
        "ar": "مطور برامج",
        "en": "Software Developer",
        "specialties_ar": ["Full Stack", "Backend", "Frontend", "Mobile", "DevOps"],
        "specialties_en": ["Full Stack", "Backend", "Frontend", "Mobile", "DevOps"],
        "hashtags": ["#programming", "#coding", "#developer", "#tech"],
        "emoji": "💻",
    },
    "businessman": {
        "ar": "رجل أعمال",
        "en": "Businessman",
        "specialties_ar": ["تجارة", "استثمار", "عقارات", "استيراد وتصدير"],
        "specialties_en": ["Trading", "Investment", "Real Estate", "Import & Export"],
        "hashtags": ["#أعمال", "#business", "#entrepreneur"],
        "emoji": "💼",
    },
    "student": {
        "ar": "طالب جامعي",
        "en": "University Student",
        "specialties_ar": ["إدارة أعمال", "علوم حاسوب", "اقتصاد", "علوم سياسية", "لغات"],
        "specialties_en": ["Business Admin", "Computer Science", "Economics", "Political Science", "Languages"],
        "hashtags": ["#طلاب", "#student", "#الدراسة_في_الخارج"],
        "emoji": "🎓",
    },
    "content_creator": {
        "ar": "صانع محتوى",
        "en": "Content Creator",
        "specialties_ar": ["سفر", "طعام", "موضة", "ألعاب", "تعليم"],
        "specialties_en": ["Travel", "Food", "Fashion", "Gaming", "Education"],
        "hashtags": ["#contentcreator", "#fyp", "#viral", "#explore"],
        "emoji": "🎬",
    },
    "photographer": {
        "ar": "مصور",
        "en": "Photographer",
        "specialties_ar": ["تصوير سفر", "تصوير منتجات", "تصوير زفاف", "تصوير طبيعة"],
        "specialties_en": ["Travel", "Product", "Wedding", "Nature"],
        "hashtags": ["#photography", "#photo", "#travel"],
        "emoji": "📸",
    },
    "chef": {
        "ar": "شيف",
        "en": "Chef",
        "specialties_ar": ["مأكولات شرقية", "مأكولات إيطالية", "حلويات", "صحي"],
        "specialties_en": ["Middle Eastern", "Italian", "Desserts", "Healthy"],
        "hashtags": ["#food", "#chef", "#طبخ"],
        "emoji": "👨‍🍳",
    },
    "teacher": {
        "ar": "معلم",
        "en": "Teacher",
        "specialties_ar": ["لغة عربية", "رياضيات", "علوم", "لغة إنجليزية"],
        "specialties_en": ["Arabic", "Math", "Science", "English"],
        "hashtags": ["#teacher", "#education", "#تعليم"],
        "emoji": "👨‍🏫",
    },
    "athlete": {
        "ar": "رياضي",
        "en": "Athlete",
        "specialties_ar": ["كرة قدم", "كمال أجسام", "كروس فت", "ملاكمة"],
        "specialties_en": ["Football", "Bodybuilding", "CrossFit", "Boxing"],
        "hashtags": ["#fitness", "#sport", "#رياضة"],
        "emoji": "💪",
    },
    "designer": {
        "ar": "مصمم",
        "en": "Designer",
        "specialties_ar": ["جرافيك", "تصميم داخلي", "أزياء", "UX/UI"],
        "specialties_en": ["Graphic", "Interior", "Fashion", "UX/UI"],
        "hashtags": ["#design", "#designer", "#تصميم"],
        "emoji": "🎨",
    },
}


# ===========================
# الجامعات حسب الدولة
# ===========================
UNIVERSITIES = {
    "RU": ["جامعة موسكو الحكومية MGU", "جامعة سانت بطرسبرغ الحكومية", "جامعة تشوفاش الحكومية ЧГУ",
           "جامعة كازان الفيدرالية", "جامعة الصداقة RUDN", "جامعة نوفوسيبيرسك الحكومية"],
    "CN": ["جامعة بكين", "جامعة تسينغهوا", "جامعة فودان", "جامعة شنغهاي جياو تونغ", "جامعة تشجيانغ"],
    "US": ["Harvard University", "MIT", "Stanford University", "UCLA", "NYU"],
    "GB": ["University of Oxford", "University of Cambridge", "Imperial College London", "UCL"],
    "DE": ["TU München", "Heidelberg University", "Humboldt University Berlin", "RWTH Aachen"],
    "TR": ["جامعة إسطنبول", "جامعة بوغازيتشي", "جامعة الشرق الأوسط التقنية", "جامعة أنقرة"],
    "EG": ["جامعة القاهرة", "جامعة عين شمس", "الجامعة الأمريكية بالقاهرة", "جامعة الإسكندرية"],
    "SA": ["جامعة الملك سعود", "جامعة الملك عبدالعزيز", "جامعة الملك فهد للبترول", "جامعة الإمام"],
    "AE": ["جامعة الإمارات", "الجامعة الأمريكية في الشارقة", "جامعة زايد", "جامعة خليفة"],
    "FR": ["Sorbonne University", "Sciences Po", "École Polytechnique", "ENS Paris"],
    "IT": ["University of Bologna", "Sapienza University", "Politecnico di Milano", "University of Padua"],
    "JP": ["University of Tokyo", "Kyoto University", "Osaka University", "Waseda University"],
    "MA": ["جامعة محمد الخامس", "جامعة القاضي عياض", "جامعة الأخوين", "جامعة الحسن الثاني"],
    "JO": ["الجامعة الأردنية", "جامعة العلوم والتكنولوجيا", "جامعة اليرموك"],
    "IQ": ["جامعة بغداد", "الجامعة المستنصرية", "جامعة الموصل", "جامعة البصرة"],
    "_DEFAULT_": ["State University", "National University", "Technical University", "Central University"],
}


# ===========================
# نوايا الحياة / الأهداف
# ===========================
LIFE_GOALS_AR = [
    "أتمنى الكل يحقق أحلامه 🤍",
    "هدفي نوصل {target}K متابع 🔥",
    "نشارك تجربتنا حتى نفيد غيرنا ❤️",
    "محتوى يومي عن حياتي في {country}",
    "أنشر معلومات تفيد الشباب العربي 🌍",
    "نوثق الرحلة من الصفر للقمة 🚀",
    "محتوى تعليمي وترفيهي 📚🎬",
    "نخلي اليوم أحلى من امبارح ✨",
]

LIFE_GOALS_EN = [
    "Living my best life ✨",
    "Goal: {target}K followers 🔥",
    "Sharing my journey 🌍",
    "Daily content from {country}",
    "Inspiring the next generation 🚀",
    "Education & entertainment 📚🎬",
]


def generate_profession_profile(country_code: str = "_DEFAULT_", language: str = "ar") -> dict:
    """توليد ملف مهني كامل (مهنة + تخصص + جامعة + هدف)"""
    prof_key = random.choice(list(PROFESSIONS.keys()))
    prof = PROFESSIONS[prof_key]

    # اختيار التخصص
    specialty = random.choice(prof["specialties_ar"] if language == "ar" else prof["specialties_en"])

    # اختيار الجامعة
    universities = UNIVERSITIES.get(country_code, UNIVERSITIES["_DEFAULT_"])
    university = random.choice(universities)

    # توليد الهدف
    target_followers = random.choice([50, 100, 200, 500, 1000])
    country_name = country_code  # placeholder
    goals_pool = LIFE_GOALS_AR if language == "ar" else LIFE_GOALS_EN
    goal_template = random.choice(goals_pool)
    goal = goal_template.format(target=target_followers, country=country_name)

    # توليد bio كامل
    if language == "ar":
        bio = f"{prof['emoji']} {prof['ar']} | {specialty}\n🎓 {university}\n{goal}"
    else:
        bio = f"{prof['emoji']} {prof['en']} | {specialty}\n🎓 {university}\n{goal}"

    return {
        "profession_key": prof_key,
        "profession_ar": prof["ar"],
        "profession_en": prof["en"],
        "specialty": specialty,
        "university": university,
        "emoji": prof["emoji"],
        "hashtags": prof["hashtags"],
        "goal": goal,
        "bio": bio,
        "target_followers": f"{target_followers}K",
    }


def get_available_professions() -> list:
    """قائمة المهن المتاحة"""
    return [
        {"key": k, "ar": v["ar"], "en": v["en"], "emoji": v["emoji"]}
        for k, v in PROFESSIONS.items()
    ]


def generate_specific_profession(profession_key: str, country_code: str = "_DEFAULT_", language: str = "ar") -> dict:
    """توليد ملف بمهنة محددة"""
    if profession_key not in PROFESSIONS:
        return generate_profession_profile(country_code, language)

    prof = PROFESSIONS[profession_key]
    specialty = random.choice(prof["specialties_ar"] if language == "ar" else prof["specialties_en"])
    universities = UNIVERSITIES.get(country_code, UNIVERSITIES["_DEFAULT_"])
    university = random.choice(universities)

    target_followers = random.choice([50, 100, 200, 500, 1000])
    goals_pool = LIFE_GOALS_AR if language == "ar" else LIFE_GOALS_EN
    goal = random.choice(goals_pool).format(target=target_followers, country=country_code)

    if language == "ar":
        bio = f"{prof['emoji']} {prof['ar']} | {specialty}\n🎓 {university}\n{goal}"
    else:
        bio = f"{prof['emoji']} {prof['en']} | {specialty}\n🎓 {university}\n{goal}"

    return {
        "profession_key": profession_key,
        "profession_ar": prof["ar"],
        "profession_en": prof["en"],
        "specialty": specialty,
        "university": university,
        "emoji": prof["emoji"],
        "hashtags": prof["hashtags"],
        "goal": goal,
        "bio": bio,
        "target_followers": f"{target_followers}K",
    }
