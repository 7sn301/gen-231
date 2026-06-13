"""
مولد حسابات وسائل التواصل الاجتماعي - الإصدار النهائي
Worldwide Social Accounts Generator v3.0
- 231 دولة
- IP حقيقي
- 12 مهنة + جامعات
- Bio احترافي
"""

import streamlit as st
import random
import string
import json
from datetime import datetime, timedelta
from ip_engine import (
    generate_ip_for_country,
    get_available_countries,
    to_dict,
    get_stats,
)
from countries_data import COUNTRIES_META
from profession_data import (
    generate_specific_profession,
    generate_profession_profile,
    get_available_professions,
    PROFESSIONS,
)

# ===========================
# إعدادات الصفحة
# ===========================
st.set_page_config(
    page_title="gen-231 — مولد عالمي",
    page_icon="🌍",
    layout="wide",
)

# RTL + Noto Sans Arabic
st.markdown(
    """
    <div dir="rtl" lang="ar">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp, .stMarkdown, .stText, .stButton,
    .stSelectbox, .stTextInput, .stRadio, .stNumberInput,
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        font-family: 'Noto Sans Arabic', 'Segoe UI', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(102,126,234,0.3);
    }
    .account-card {
        background: #f8f9fa;
        padding: 22px;
        border-radius: 14px;
        border-right: 5px solid #667eea;
        margin: 18px 0;
        direction: rtl;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .bio-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #ff9800;
        margin: 10px 0;
        white-space: pre-line;
        direction: rtl;
        font-weight: 500;
    }
    .ip-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 18px;
        border-radius: 12px;
        border-right: 5px solid #4caf50;
        font-family: 'Courier New', 'Noto Sans Arabic', monospace;
        direction: ltr;
        text-align: left;
        margin-top: 10px;
    }
    .field-label { color: #555; font-weight: 600; font-size: 0.9em; }
    .field-value { color: #222; font-size: 1.05em; font-weight: 500; }
    </style>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===========================
# Flag emoji
# ===========================
def cc_to_flag(cc: str) -> str:
    if len(cc) != 2:
        return "🌍"
    return chr(ord(cc[0]) + 127397) + chr(ord(cc[1]) + 127397)


# ===========================
# الأسماء حسب الجنسية
# ===========================
NATIONALITY_NAMES = {
    "EG": {"m": ["محمد", "أحمد", "علي", "حسن", "كريم", "عمر", "يوسف", "خالد"], "f": ["فاطمة", "مريم", "ياسمين", "سارة", "نور", "هدى"], "ln": ["السيد", "حسن", "محمود", "عبدالله", "إبراهيم"]},
    "SA": {"m": ["عبدالله", "محمد", "فهد", "سعود", "خالد", "ناصر"], "f": ["نورة", "ريم", "هيا", "سارة", "العنود"], "ln": ["السبيعي", "العتيبي", "الدوسري", "الشهري"]},
    "AE": {"m": ["راشد", "حمدان", "زايد", "محمد", "خليفة"], "f": ["شمسة", "موزة", "ميثاء"], "ln": ["المكتوم", "النهيان", "القاسمي"]},
    "IQ": {"m": ["غيث", "علي", "حسين", "محمد", "كرار", "مصطفى"], "f": ["زينب", "فاطمة", "نور", "زهراء"], "ln": ["العراقي", "البصري", "الموصلي", "البغدادي"]},
    "MA": {"m": ["يوسف", "محمد", "أمين", "حمزة"], "f": ["فاطمة", "خديجة", "ليلى"], "ln": ["العلوي", "الإدريسي", "بنعلي"]},
    "DZ": {"m": ["محمد", "عبدالقادر", "أمين"], "f": ["أمينة", "نسرين"], "ln": ["بن علي", "بومدين"]},
    "JO": {"m": ["عبدالله", "حسين", "محمد"], "f": ["رانيا", "هيا"], "ln": ["العلي", "الزعبي"]},
    "LB": {"m": ["جورج", "إلياس", "كريم"], "f": ["ميرنا", "ريما"], "ln": ["حداد", "خوري"]},
    "SY": {"m": ["محمد", "أحمد", "علي"], "f": ["رانيا", "سمر"], "ln": ["الحلبي", "الدمشقي"]},
    "PS": {"m": ["محمد", "أحمد", "كريم"], "f": ["فاطمة", "نور"], "ln": ["العلي", "النابلسي"]},
    "TN": {"m": ["محمد", "أمين"], "f": ["أميرة"], "ln": ["بن علي", "التونسي"]},
    "LY": {"m": ["محمد", "علي"], "f": ["فاطمة"], "ln": ["القذافي", "الليبي"]},
    "SD": {"m": ["محمد", "عمر"], "f": ["مريم"], "ln": ["البشير", "السوداني"]},
    "KW": {"m": ["عبدالله", "ناصر"], "f": ["نورة"], "ln": ["الصباح", "الكويتي"]},
    "QA": {"m": ["محمد", "حمد"], "f": ["موزا"], "ln": ["آل ثاني", "القطري"]},
    "BH": {"m": ["حمد", "عيسى"], "f": ["لطيفة"], "ln": ["آل خليفة"]},
    "OM": {"m": ["سعيد", "هيثم"], "f": ["مزون"], "ln": ["آل سعيد", "العماني"]},
    "YE": {"m": ["علي", "محمد"], "f": ["فاطمة"], "ln": ["الصنعاني", "الحضرمي"]},
    "US": {"m": ["John", "Michael", "David"], "f": ["Mary", "Jennifer"], "ln": ["Smith", "Johnson", "Williams"]},
    "GB": {"m": ["Oliver", "Harry"], "f": ["Olivia", "Amelia"], "ln": ["Smith", "Jones", "Taylor"]},
    "DE": {"m": ["Lukas", "Maximilian"], "f": ["Mia", "Emma"], "ln": ["Müller", "Schmidt"]},
    "FR": {"m": ["Lucas", "Hugo"], "f": ["Emma", "Jade"], "ln": ["Martin", "Bernard"]},
    "IT": {"m": ["Leonardo", "Francesco"], "f": ["Sofia", "Giulia"], "ln": ["Rossi", "Russo"]},
    "ES": {"m": ["Hugo", "Mateo"], "f": ["Lucía", "Sofía"], "ln": ["García", "Rodríguez"]},
    "RU": {"m": ["Ivan", "Alexander"], "f": ["Anna", "Maria"], "ln": ["Ivanov", "Smirnov"]},
    "CN": {"m": ["Wei", "Lei"], "f": ["Li", "Mei"], "ln": ["Wang", "Li", "Zhang"]},
    "JP": {"m": ["Haruto", "Yuto"], "f": ["Yui", "Aoi"], "ln": ["Sato", "Suzuki"]},
    "KR": {"m": ["Min-jun"], "f": ["Seo-yeon"], "ln": ["Kim", "Lee", "Park"]},
    "IN": {"m": ["Aarav"], "f": ["Saanvi"], "ln": ["Sharma", "Patel", "Singh"]},
    "TR": {"m": ["Mehmet"], "f": ["Ayşe"], "ln": ["Yılmaz", "Kaya"]},
    "BR": {"m": ["Miguel"], "f": ["Helena"], "ln": ["Silva", "Santos"]},
    "MX": {"m": ["Santiago"], "f": ["Sofía"], "ln": ["Hernández", "García"]},
    "_DEFAULT_": {"m": ["Alex", "Chris"], "f": ["Maria", "Anna"], "ln": ["Smith", "Brown"]},
}

PLATFORMS = ["TikTok", "Instagram", "Twitter/X", "Facebook", "Snapchat", "YouTube", "Telegram", "LinkedIn"]
PHONE_PREFIXES = {
    "EG": "+20", "SA": "+966", "AE": "+971", "MA": "+212", "DZ": "+213",
    "IQ": "+964", "JO": "+962", "LB": "+961", "SY": "+963", "YE": "+967",
    "PS": "+970", "TN": "+216", "LY": "+218", "SD": "+249", "KW": "+965",
    "QA": "+974", "BH": "+973", "OM": "+968", "US": "+1", "GB": "+44",
    "DE": "+49", "FR": "+33", "IT": "+39", "ES": "+34", "RU": "+7",
    "CN": "+86", "JP": "+81", "KR": "+82", "IN": "+91", "TR": "+90",
    "BR": "+55", "MX": "+52",
}


def random_username(name: str) -> str:
    base = "".join(c for c in name.lower() if c.isalnum())
    suffix = "".join(random.choices(string.digits, k=random.randint(3, 5)))
    sep = random.choice(["_", ".", ""])
    return f"{base}{sep}{suffix}"


def random_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(random.choices(chars, k=length))


def random_email(username: str) -> str:
    return f"{username}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'proton.me'])}"


def random_phone(prefix: str) -> str:
    return f"{prefix}{''.join(random.choices(string.digits, k=9))}"


def random_birthdate() -> str:
    today = datetime.now()
    start = today - timedelta(days=365 * 35)
    end = today - timedelta(days=365 * 18)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")


def get_names_for_country(cc: str) -> dict:
    return NATIONALITY_NAMES.get(cc, NATIONALITY_NAMES["_DEFAULT_"])


def generate_account(nationality_cc, residence_cc, platform, gender, proxy_type, profession_key=None, language="ar"):
    names = get_names_for_country(nationality_cc)
    first = random.choice(names["m"] if gender == "ذكر" else names["f"])
    last = random.choice(names["ln"])
    full_name = f"{first} {last}"
    username = random_username(first + last)
    phone_prefix = PHONE_PREFIXES.get(nationality_cc, "+1")

    ip_loc = generate_ip_for_country(residence_cc, proxy_type=proxy_type)

    # توليد ملف مهني (مهنة محددة أو عشوائية)
    if profession_key and profession_key != "عشوائي":
        prof = generate_specific_profession(profession_key, residence_cc, language)
    else:
        prof = generate_profession_profile(residence_cc, language)

    return {
        "platform": platform,
        "full_name": full_name,
        "username": username,
        "email": random_email(username),
        "password": random_password(),
        "phone": random_phone(phone_prefix),
        "gender": gender,
        "birthdate": random_birthdate(),
        "nationality_code": nationality_cc,
        "nationality_ar": COUNTRIES_META[nationality_cc]["ar"],
        "nationality_en": COUNTRIES_META[nationality_cc]["en"],
        "profession": prof,
        "residence": to_dict(ip_loc),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ===========================
# الواجهة الرئيسية
# ===========================
stats = get_stats()
st.markdown(
    f"""
    <div dir="rtl" lang="ar">
    <div class="main-header">
        <h1>🌍 مولد حسابات وسائل التواصل + IP عالمي v3.0</h1>
        <p style="font-size:1.1em; margin:10px 0;">
            🌐 <b>{stats['countries']} دولة</b> •
            📡 <b>{stats['ip_ranges']:,}</b> نطاق IP •
            💼 <b>{len(PROFESSIONS)}</b> مهنة •
            🎓 جامعات حقيقية
        </p>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

all_countries = get_available_countries()
country_options = [c["code"] for c in all_countries]

def fmt_country(cc):
    meta = COUNTRIES_META.get(cc, {})
    return f"{cc_to_flag(cc)} {meta.get('ar', cc)} — {meta.get('en', cc)}"


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 توليد حساب",
    "🌐 توليد IP",
    "💼 المهن",
    "📊 الدول",
    "ℹ️ شرح",
])

# ===========================
# تبويب 1: توليد حساب
# ===========================
with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div dir="rtl"><h3>👤 الهوية</h3></div>', unsafe_allow_html=True)
        nat_pool = ["EG", "SA", "AE", "IQ", "MA", "DZ", "JO", "LB", "SY", "PS", "TN", "LY", "SD",
                    "KW", "QA", "BH", "OM", "YE", "US", "GB", "DE", "FR", "IT", "ES", "RU", "CN",
                    "JP", "KR", "IN", "TR", "BR", "MX"]
        nat_pool = [c for c in nat_pool if c in country_options]
        nationality = st.selectbox("الجنسية", nat_pool, format_func=fmt_country,
                                   index=nat_pool.index("IQ") if "IQ" in nat_pool else 0)
        gender = st.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)
        platform = st.selectbox("المنصة", PLATFORMS)

    with col2:
        st.markdown('<div dir="rtl"><h3>📍 الإقامة</h3></div>', unsafe_allow_html=True)
        residence = st.selectbox("دولة الإقامة (IP)", country_options, format_func=fmt_country,
                                 index=country_options.index("RU") if "RU" in country_options else 0)
        proxy_type = st.selectbox("نوع الاتصال", ["Residential", "ISP", "Mobile (4G/5G)", "Datacenter", "VPN"])
        count = st.number_input("عدد الحسابات", 1, 100, 1)

    with col3:
        st.markdown('<div dir="rtl"><h3>💼 المهنة</h3></div>', unsafe_allow_html=True)
        prof_options = ["عشوائي"] + [p["key"] for p in get_available_professions()]
        def fmt_prof(k):
            if k == "عشوائي": return "🎲 عشوائي"
            p = PROFESSIONS[k]
            return f"{p['emoji']} {p['ar']}"
        profession_key = st.selectbox("اختر المهنة", prof_options, format_func=fmt_prof)
        bio_lang = st.radio("لغة البايو", ["ar", "en"], horizontal=True,
                            format_func=lambda x: "🇸🇦 عربي" if x == "ar" else "🇬🇧 إنجليزي")

    st.markdown("---")

    if st.button("🚀 توليد الحسابات", use_container_width=True, type="primary"):
        accounts = [
            generate_account(nationality, residence, platform, gender, proxy_type, profession_key, bio_lang)
            for _ in range(count)
        ]

        for i, acc in enumerate(accounts, 1):
            res = acc["residence"]
            prof = acc["profession"]
            flag_nat = cc_to_flag(acc["nationality_code"])
            flag_res = cc_to_flag(res["country_code"])

            st.markdown(
                f"""
                <div dir="rtl" lang="ar">
                <div class="account-card">
                    <h3>#{i} — {acc['platform']} {prof['emoji']}</h3>
                    <hr>
                    <p><span class="field-label">👤 الاسم:</span> <span class="field-value">{acc['full_name']}</span></p>
                    <p><span class="field-label">🆔 المستخدم:</span> <span class="field-value">@{acc['username']}</span></p>
                    <p><span class="field-label">📧 الإيميل:</span> <span class="field-value">{acc['email']}</span></p>
                    <p><span class="field-label">🔑 الباسورد:</span> <span class="field-value">{acc['password']}</span></p>
                    <p><span class="field-label">📱 الهاتف:</span> <span class="field-value">{acc['phone']}</span></p>
                    <p><span class="field-label">🎂 الميلاد:</span> <span class="field-value">{acc['birthdate']}</span></p>
                    <p><span class="field-label">🌏 الجنسية:</span> <span class="field-value">{flag_nat} {acc['nationality_ar']}</span></p>
                    <p><span class="field-label">🏠 الإقامة:</span> <span class="field-value">{flag_res} {res['country_ar']}</span></p>
                    <p><span class="field-label">💼 المهنة:</span> <span class="field-value">{prof['emoji']} {prof['profession_ar']} — {prof['specialty']}</span></p>
                    <p><span class="field-label">🎓 الجامعة:</span> <span class="field-value">{prof['university']}</span></p>
                    <p><span class="field-label">🎯 الهدف:</span> <span class="field-value">{prof['goal']}</span></p>
                </div>
                <div class="bio-box">
<b>📝 البايو الكامل (انسخه مباشرة للحساب):</b>

{prof['bio']}

{' '.join(prof['hashtags'])}
                </div>
                </div>
                <div class="ip-box">
                    <b>📍 IP & Geolocation Details</b><br>
                    IP Address: <b>{res['ip_address']}</b><br>
                    Country: {res['country_en']} ({res['country_code']}) {flag_res}<br>
                    City: {res['city']}<br>
                    Coordinates: {res['latitude']}, {res['longitude']}<br>
                    Timezone: {res['timezone']}<br>
                    ISP: {res['isp']}<br>
                    Type: {res['proxy_type']}<br>
                    Language: {res['language']} | Currency: {res['currency']}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div dir="rtl">🗺️ <a href="https://www.google.com/maps?q={res["latitude"]},{res["longitude"]}" target="_blank">عرض الموقع على الخريطة</a></div>',
                unsafe_allow_html=True,
            )
            st.markdown("---")

        st.download_button(
            "📥 تحميل الحسابات (JSON)",
            data=json.dumps(accounts, ensure_ascii=False, indent=2),
            file_name=f"accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )


# ===========================
# تبويب 2: توليد IP فقط
# ===========================
with tab2:
    st.markdown('<div dir="rtl"><h3>🌐 مولد IP مستقل</h3></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ip_country = st.selectbox("الدولة", country_options, format_func=fmt_country, key="ip_only")
    with c2:
        ip_count = st.number_input("العدد", 1, 200, 10, key="ipc")

    if st.button("🎲 توليد IPs", type="primary"):
        ips = [generate_ip_for_country(ip_country) for _ in range(ip_count)]
        for i, ip in enumerate(ips, 1):
            flag = cc_to_flag(ip.country_code)
            st.markdown(
                f"""<div class="ip-box">
                <b>#{i}</b> — IP: <b>{ip.ip_address}</b> | {flag} {ip.country_en} → {ip.city} |
                📍 {ip.latitude}, {ip.longitude} | 🕐 {ip.timezone} | 🏢 {ip.isp}
                </div>""",
                unsafe_allow_html=True,
            )

        st.download_button(
            "📥 تحميل IPs",
            data=json.dumps([to_dict(ip) for ip in ips], ensure_ascii=False, indent=2),
            file_name=f"ips_{ip_country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )


# ===========================
# تبويب 3: المهن
# ===========================
with tab3:
    st.markdown(
        f'<div dir="rtl"><h3>💼 المهن المتاحة ({len(get_available_professions())} مهنة)</h3></div>',
        unsafe_allow_html=True,
    )
    profs = get_available_professions()
    cols = st.columns(3)
    for idx, p in enumerate(profs):
        with cols[idx % 3]:
            prof_data = PROFESSIONS[p["key"]]
            specialties = " • ".join(prof_data["specialties_ar"][:3])
            st.markdown(
                f"""
                <div dir="rtl" style="background:#f1f3f9; padding:15px; border-radius:12px; margin:8px 0; border-right:4px solid #667eea;">
                    <h4 style="margin:0;">{p['emoji']} {p['ar']}</h4>
                    <p style="color:#666; font-size:0.85em; margin:5px 0;">{p['en']}</p>
                    <p style="color:#444; font-size:0.85em;">📋 {specialties}...</p>
                    <p style="color:#888; font-size:0.8em;">{' '.join(prof_data['hashtags'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ===========================
# تبويب 4: قائمة الدول
# ===========================
with tab4:
    st.markdown(
        f'<div dir="rtl"><h3>📊 جميع الدول ({len(all_countries)} دولة)</h3></div>',
        unsafe_allow_html=True,
    )
    search = st.text_input("🔍 ابحث (عربي / إنجليزي / كود)")
    filtered = all_countries
    if search:
        q = search.lower()
        filtered = [c for c in all_countries if q in c["ar"].lower() or q in c["en"].lower() or q in c["code"].lower()]

    cols_per_row = 4
    for row_start in range(0, len(filtered), cols_per_row):
        cols = st.columns(cols_per_row)
        for idx, country in enumerate(filtered[row_start:row_start + cols_per_row]):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div dir="rtl" style="background:#f1f3f9; padding:12px; border-radius:10px; margin:5px 0; text-align:center;">
                        <div style="font-size:2em;">{cc_to_flag(country['code'])}</div>
                        <div style="font-weight:600;">{country['ar']}</div>
                        <div style="color:#666; font-size:0.85em;">{country['en']} ({country['code']})</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ===========================
# تبويب 5: شرح
# ===========================
with tab5:
    st.markdown(
        """
        <div dir="rtl" lang="ar">

        ### 🆕 ما الجديد في v3.0؟

        - ✅ **12 مهنة** كاملة مع تخصصات
        - ✅ **جامعات حقيقية** لـ 15 دولة
        - ✅ **بايو احترافي** جاهز للنسخ
        - ✅ **هدف شخصي** متغير لكل حساب
        - ✅ **هاشتاقات** متخصصة حسب المهنة

        ### 💼 المهن المدعومة

        | المهنة | التخصصات | الإيموجي |
        |---|---|---|
        | طبيب | طب أسنان، طب عام، جراحة، أطفال... | 🩺 |
        | طالب طب | طب بشري، طب أسنان، صيدلة... | 🎓 |
        | مهندس | مدني، كهربائي، ميكانيكي... | 👷 |
        | مطور برامج | Full Stack، Backend، Mobile... | 💻 |
        | رجل أعمال | تجارة، استثمار، عقارات... | 💼 |
        | طالب جامعي | إدارة، حاسوب، اقتصاد... | 🎓 |
        | صانع محتوى | سفر، طعام، موضة، ألعاب... | 🎬 |
        | مصور | سفر، منتجات، زفاف... | 📸 |
        | شيف | شرقي، إيطالي، حلويات... | 👨‍🍳 |
        | معلم | عربية، رياضيات، علوم... | 👨‍🏫 |
        | رياضي | كرة قدم، كمال أجسام... | 💪 |
        | مصمم | جرافيك، داخلي، UX/UI... | 🎨 |

        ### 🎯 مثال على الواقعية (محاكاة @go97g)

        ```
        🩺 طبيب | طب أسنان
        🎓 جامعة تشوفاش الحكومية ЧГУ
        هدفي نوصل 200K متابع 🔥
        #طب #أطباء #صحة #medical
        ```

        ### ⚠️ ملاحظات
        - الأداة **للاختبار والتطوير فقط** (Pentest / QA)
        - IP حقيقي ضمن نطاقات الدولة، لكن يحتاج Proxy/VPN لتفعيله
        - لا تستخدم البيانات في انتحال هوية أو أنشطة ضارة

        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div dir="rtl" style='text-align:center; color:#888; margin-top:30px;'>
        ⚡ مولد الحسابات + IP العالمي v3.0 • 231 دولة • 12 مهنة • للاختبار والتطوير
    </div>
    """,
    unsafe_allow_html=True,
)
