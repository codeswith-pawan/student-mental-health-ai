import streamlit as st
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Mental Health AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# API  (do not change URL, method, or payload keys)
# =========================================================

API_URL = st.secrets["API_URL"]

# =========================================================
# ML CATEGORY VALUES  (sent to backend — never Hindi)
# =========================================================

GENDER_OPTIONS = ["Male", "Female", "Other"]

COUNTRY_OPTIONS = [
    "India", "USA", "Canada", "Australia", "UK",
    "Germany", "Mexico", "Turkey", "France", "Other"
]

ACADEMIC_OPTIONS = ["High School", "Undergraduate", "Graduate"]

PLATFORM_OPTIONS = [
    "Instagram", "YouTube", "TikTok", "Facebook",
    "Twitter", "Snapchat", "Reddit", "LinkedIn", "Other"
]

PURPOSE_OPTIONS = [
    "Entertainment", "Education", "Social Interaction",
    "Work", "News", "Other"
]

STRESS_OPTIONS = ["Low", "Medium", "High", "Very High"]

# =========================================================
# TRANSLATIONS  (UI only)
# =========================================================

OPTION_LABELS = {
    "en": {
        "gender": {"Male": "Male", "Female": "Female", "Other": "Other"},
        "country": {
            "India": "India", "USA": "USA", "Canada": "Canada",
            "Australia": "Australia", "UK": "UK", "Germany": "Germany",
            "Mexico": "Mexico", "Turkey": "Turkey", "France": "France",
            "Other": "Other",
        },
        "academic": {
            "High School": "High School",
            "Undergraduate": "Undergraduate",
            "Graduate": "Graduate",
        },
        "platform": {p: p for p in PLATFORM_OPTIONS},
        "purpose": {
            "Entertainment": "Entertainment",
            "Education": "Education",
            "Social Interaction": "Social Interaction",
            "Work": "Work",
            "News": "News",
            "Other": "Other",
        },
        "stress": {
            "Low": "Low",
            "Medium": "Medium",
            "High": "High",
            "Very High": "Very High",
        },
    },
    "hi": {
        "gender": {"Male": "पुरुष", "Female": "महिला", "Other": "अन्य"},
        "country": {
            "India": "भारत", "USA": "अमेरिका", "Canada": "कनाडा",
            "Australia": "ऑस्ट्रेलिया", "UK": "यूनाइटेड किंगडम",
            "Germany": "जर्मनी", "Mexico": "मेक्सिको", "Turkey": "तुर्की",
            "France": "फ्रांस", "Other": "अन्य",
        },
        "academic": {
            "High School": "हाई स्कूल",
            "Undergraduate": "स्नातक",
            "Graduate": "परास्नातक",
        },
        "platform": {p: p for p in PLATFORM_OPTIONS},
        "purpose": {
            "Entertainment": "मनोरंजन",
            "Education": "शिक्षा",
            "Social Interaction": "सामाजिक संपर्क",
            "Work": "कार्य",
            "News": "समाचार",
            "Other": "अन्य",
        },
        "stress": {
            "Low": "कम",
            "Medium": "मध्यम",
            "High": "अधिक",
            "Very High": "बहुत अधिक",
        },
    },
}

TRANSLATIONS = {
    "en": {
        "lang_title": "🌐 Select Language",
        "lang_subtitle": "Choose a language to continue. You can switch anytime without losing your answers.",
        "btn_english": "🇬🇧  English",
        "btn_hindi": "🇮🇳  हिन्दी",
        "app_title": "🧠 Student Mental Health AI",
        "app_subtitle": "Model-based wellness estimate for students",
        "hero_text": (
            "This tool uses student academic, lifestyle and digital-behaviour information "
            "to generate a model-based mental health score."
        ),
        "hero_notice": "Educational prediction tool — not a medical diagnosis.",
        "profile_title": "👤 Student Profile",
        "profile_desc": "Basic information about the student",
        "digital_title": "📱 Digital Behaviour",
        "digital_desc": "Daily social-media usage patterns",
        "lifestyle_title": "🌙 Lifestyle & Wellbeing",
        "lifestyle_desc": "Study, physical activity, sleep and stress",
        "label_age": "Age",
        "label_gender": "Gender",
        "label_country": "Country",
        "label_academic": "Academic Level",
        "label_platform": "Most Used Platform",
        "label_purpose": "Purpose Of Use",
        "label_usage": "Average Daily Usage (hours)",
        "label_unlocks": "Daily Phone Unlocks",
        "label_study": "Study Hours / Day",
        "label_activity": "Physical Activity (hours)",
        "label_sleep": "Sleep Hours / Night",
        "label_stress": "Stress Level",
        "predict_button": "🧠 Predict Mental Health Score",
        "loading": "Generating model-based score…",
        "result_label": "Predicted Mental Health Score",
        "score_description": "Model-based estimate from the information provided. Consider reviewing the factors below.",
        "category_strong": "🟢 Strong predicted mental health",
        "category_moderate_good": "🔵 Moderate-to-good predicted mental health",
        "category_moderate": "🟠 Moderate predicted mental health",
        "category_lower": "🔴 Lower predicted mental health",
        "suggestions_title": "💡 Personalized Suggestions",
        "sugg_stress_title": "🧘 Stress",
        "sugg_activity_title": "🏃 Physical Activity",
        "sugg_screen_title": "📱 Screen Time",
        "sugg_sleep_title": "😴 Sleep",
        "sugg_study_title": "📚 Study",
        "stress_low": "Your reported stress level is low. Continue maintaining a balanced daily routine.",
        "stress_medium": "Your stress level is moderate. Try taking regular breaks, maintaining a consistent sleep schedule and including relaxing activities in your routine.",
        "stress_high": "Your stress level is high. Consider reducing avoidable workload, taking regular breaks, improving sleep consistency and talking with someone you trust if stress persists.",
        "stress_very_high": "Your reported stress level is very high. Prioritize rest, reduce avoidable pressure and consider speaking with a qualified mental-health professional or trusted person if this continues.",
        "activity_low": "Your physical activity is relatively low. Try adding a short walk, stretching or another comfortable physical activity to your daily routine.",
        "activity_mid": "Your activity level is reasonable. Keep it consistent and gradually increase movement when comfortable.",
        "activity_high": "You are maintaining a good amount of physical activity. Continue balancing exercise with adequate recovery.",
        "screen_high": "Your social-media usage is high. Consider setting screen-free periods during the day and avoiding unnecessary late-night usage.",
        "screen_mid": "Your social-media usage is moderate to high. Try keeping some parts of the day completely screen-free.",
        "screen_ok": "Your reported social-media usage is relatively moderate. Continue maintaining boundaries around screen time.",
        "sleep_low": "Your sleep duration is low. Try establishing a consistent sleep schedule and reducing screen exposure before bedtime.",
        "sleep_slightly_low": "Your sleep duration is slightly below the commonly recommended range. Try improving sleep consistency and giving yourself enough time to rest.",
        "sleep_ok": "Your reported sleep duration is in a healthy range. Continue maintaining a consistent sleep routine.",
        "sleep_high": "You are reporting a relatively high amount of sleep. Focus on sleep quality and consistency as well as duration.",
        "study_low": "Your study time is relatively low. Try creating a manageable study routine with short focused sessions and regular breaks.",
        "study_mid": "You have a study routine in place. Keep a balance between study, rest and recreation.",
        "study_high": "Your study hours are relatively high. Make sure you are taking sufficient breaks and protecting your sleep and recovery time.",
        "disclaimer": (
            "<strong>Disclaimer:</strong> This prediction is generated by a machine-learning "
            "model for educational purposes. It is not a medical diagnosis or a substitute "
            "for professional advice."
        ),
        "footer": "Student Mental Health AI • Machine Learning Prediction System",
        "err_connection": "❌ Could not connect to the FastAPI server. Start your backend with: `python3 -m uvicorn main:app --reload`",
        "err_timeout": "⏳ The prediction server took too long to respond.",
        "err_request": "❌ API request failed: {error}",
        "err_generic": "❌ Something went wrong: {error}",
    },
    "hi": {
        "lang_title": "🌐 भाषा चुनें",
        "lang_subtitle": "जारी रखने के लिए भाषा चुनें। आपके भरे हुए उत्तर भाषा बदलने पर भी सुरक्षित रहेंगे।",
        "btn_english": "🇬🇧  English",
        "btn_hindi": "🇮🇳  हिन्दी",
        "app_title": "🧠 छात्र मानसिक स्वास्थ्य एआई",
        "app_subtitle": "छात्रों के लिए मॉडल आधारित कल्याण अनुमान",
        "hero_text": (
            "यह अनुप्रयोग छात्र की शैक्षणिक जानकारी, जीवनशैली और डिजिटल व्यवहार के आधार पर "
            "एक मॉडल-आधारित मानसिक स्वास्थ्य स्कोर तैयार करता है।"
        ),
        "hero_notice": "शैक्षणिक पूर्वानुमान उपकरण — यह चिकित्सकीय निदान नहीं है।",
        "profile_title": "👤 छात्र प्रोफ़ाइल",
        "profile_desc": "छात्र की मूल जानकारी",
        "digital_title": "📱 डिजिटल व्यवहार",
        "digital_desc": "दैनिक सोशल-मीडिया उपयोग के पैटर्न",
        "lifestyle_title": "🌙 जीवनशैली और स्वास्थ्य",
        "lifestyle_desc": "अध्ययन, शारीरिक गतिविधि, नींद और तनाव",
        "label_age": "आयु",
        "label_gender": "लिंग",
        "label_country": "देश",
        "label_academic": "शैक्षणिक स्तर",
        "label_platform": "सबसे अधिक उपयोग किया गया प्लेटफ़ॉर्म",
        "label_purpose": "उपयोग का उद्देश्य",
        "label_usage": "औसत दैनिक उपयोग (घंटे)",
        "label_unlocks": "दैनिक फ़ोन अनलॉक",
        "label_study": "अध्ययन घंटे / दिन",
        "label_activity": "शारीरिक गतिविधि (घंटे)",
        "label_sleep": "नींद के घंटे / रात",
        "label_stress": "तनाव स्तर",
        "predict_button": "🧠 मानसिक स्वास्थ्य स्कोर का अनुमान लगाएँ",
        "loading": "मॉडल-आधारित स्कोर तैयार किया जा रहा है…",
        "result_label": "अनुमानित मानसिक स्वास्थ्य स्कोर",
        "score_description": "दी गई जानकारी पर आधारित मॉडल अनुमान। नीचे दिए गए कारकों पर विचार करें।",
        "category_strong": "🟢 मजबूत अनुमानित मानसिक स्वास्थ्य",
        "category_moderate_good": "🔵 मध्यम-से-अच्छा अनुमानित मानसिक स्वास्थ्य",
        "category_moderate": "🟠 मध्यम अनुमानित मानसिक स्वास्थ्य",
        "category_lower": "🔴 अपेक्षाकृत कम अनुमानित मानसिक स्वास्थ्य",
        "suggestions_title": "💡 व्यक्तिगत सुझाव",
        "sugg_stress_title": "🧘 तनाव",
        "sugg_activity_title": "🏃 शारीरिक गतिविधि",
        "sugg_screen_title": "📱 स्क्रीन समय",
        "sugg_sleep_title": "😴 नींद",
        "sugg_study_title": "📚 अध्ययन",
        "stress_low": "आपका बताया गया तनाव स्तर कम है। संतुलित दैनिक दिनचर्या बनाए रखें।",
        "stress_medium": "आपका तनाव स्तर मध्यम है। नियमित विश्राम लें, नींद का समय स्थिर रखें और दिनचर्या में आरामदायक गतिविधियाँ शामिल करें।",
        "stress_high": "आपका तनाव स्तर अधिक है। अनावश्यक कार्यभार कम करने, नियमित विश्राम लेने, नींद सुधारने और यदि तनाव बना रहे तो किसी विश्वसनीय व्यक्ति से बात करने पर विचार करें।",
        "stress_very_high": "आपका बताया गया तनाव स्तर बहुत अधिक है। आराम को प्राथमिकता दें, अनावश्यक दबाव कम करें और यदि यह स्थिति बनी रहे तो योग्य मानसिक-स्वास्थ्य विशेषज्ञ या किसी विश्वसनीय व्यक्ति से बात करने पर विचार करें।",
        "activity_low": "आपकी शारीरिक गतिविधि अपेक्षाकृत कम है। दैनिक दिनचर्या में छोटी सैर, स्ट्रेचिंग या कोई आरामदायक शारीरिक गतिविधि जोड़ने का प्रयास करें।",
        "activity_mid": "आपकी गतिविधि का स्तर उचित है। इसे नियमित रखें और जब सहज लगे तब धीरे-धीरे गतिविधि बढ़ाएँ।",
        "activity_high": "आप पर्याप्त शारीरिक गतिविधि बनाए रख रहे हैं। व्यायाम के साथ पर्याप्त आराम का संतुलन जारी रखें।",
        "screen_high": "आपका सोशल-मीडिया उपयोग अधिक है। दिन में स्क्रीन-मुक्त समय निर्धारित करें और रात में अनावश्यक उपयोग से बचें।",
        "screen_mid": "आपका सोशल-मीडिया उपयोग मध्यम से अधिक है। दिन के कुछ हिस्से पूरी तरह स्क्रीन-मुक्त रखने का प्रयास करें।",
        "screen_ok": "आपका बताया गया सोशल-मीडिया उपयोग अपेक्षाकृत मध्यम है। स्क्रीन समय की सीमाएँ बनाए रखें।",
        "sleep_low": "आपकी नींद की अवधि कम है। नियमित सोने का समय तय करें और सोने से पहले स्क्रीन का उपयोग कम करें।",
        "sleep_slightly_low": "आपकी नींद की अवधि सामान्यतः सुझाई गई सीमा से थोड़ी कम है। नींद की नियमितता सुधारें और पर्याप्त आराम का समय दें।",
        "sleep_ok": "आपकी बताई गई नींद की अवधि स्वस्थ सीमा में है। नियमित नींद की दिनचर्या बनाए रखें।",
        "sleep_high": "आप अपेक्षाकृत अधिक नींद बता रहे हैं। अवधि के साथ-साथ नींद की गुणवत्ता और नियमितता पर भी ध्यान दें।",
        "study_low": "आपका अध्ययन समय अपेक्षाकृत कम है। छोटे केंद्रित सत्रों और नियमित विश्राम के साथ एक सहज अध्ययन दिनचर्या बनाएँ।",
        "study_mid": "आपकी अध्ययन दिनचर्या बनी हुई है। अध्ययन, आराम और मनोरंजन के बीच संतुलन बनाए रखें।",
        "study_high": "आपके अध्ययन घंटे अपेक्षाकृत अधिक हैं। पर्याप्त विश्राम लें और अपनी नींद व रिकवरी के समय की रक्षा करें।",
        "disclaimer": (
            "<strong>अस्वीकरण:</strong> यह अनुमान एक मशीन-लर्निंग मॉडल द्वारा शैक्षणिक उद्देश्यों "
            "के लिए तैयार किया गया है। यह चिकित्सकीय निदान नहीं है और पेशेवर सलाह का विकल्प नहीं है।"
        ),
        "footer": "छात्र मानसिक स्वास्थ्य एआई • मशीन लर्निंग पूर्वानुमान प्रणाली",
        "err_connection": "❌ FastAPI सर्वर से कनेक्ट नहीं हो सका। बैकएंड इस आदेश से शुरू करें: `python3 -m uvicorn main:app --reload`",
        "err_timeout": "⏳ पूर्वानुमान सर्वर ने उत्तर देने में बहुत समय लिया।",
        "err_request": "❌ एपीआई अनुरोध असफल रहा: {error}",
        "err_generic": "❌ कुछ गलत हो गया: {error}",
    },
}


def t(key):
    lang = st.session_state.get("lang") or "en"
    return TRANSLATIONS[lang][key]


def option_label(group, value):
    lang = st.session_state.get("lang") or "en"
    return OPTION_LABELS[lang][group][value]


def format_gender(value):
    return option_label("gender", value)


def format_country(value):
    return option_label("country", value)


def format_academic(value):
    return option_label("academic", value)


def format_platform(value):
    return option_label("platform", value)


def format_purpose(value):
    return option_label("purpose", value)


def format_stress(value):
    return option_label("stress", value)


def set_lang_en():
    st.session_state.lang = "en"


def set_lang_hi():
    st.session_state.lang = "hi"


def category_key(prediction):
    if prediction >= 8:
        return "category_strong"
    if prediction >= 6:
        return "category_moderate_good"
    if prediction >= 4:
        return "category_moderate"
    return "category_lower"


def suggestion_keys(stress_level, physical_activity, avg_daily_usage, sleep_hours, study_hours):
    if stress_level == "Low":
        stress_class, stress_key = "stress-low", "stress_low"
    elif stress_level == "Medium":
        stress_class, stress_key = "stress-medium", "stress_medium"
    elif stress_level == "High":
        stress_class, stress_key = "stress-high", "stress_high"
    else:
        stress_class, stress_key = "stress-very-high", "stress_very_high"

    if physical_activity < 1:
        activity_key = "activity_low"
    elif physical_activity < 2:
        activity_key = "activity_mid"
    else:
        activity_key = "activity_high"

    if avg_daily_usage >= 8:
        screen_key = "screen_high"
    elif avg_daily_usage >= 5:
        screen_key = "screen_mid"
    else:
        screen_key = "screen_ok"

    if sleep_hours < 6:
        sleep_key = "sleep_low"
    elif sleep_hours < 7:
        sleep_key = "sleep_slightly_low"
    elif sleep_hours <= 9:
        sleep_key = "sleep_ok"
    else:
        sleep_key = "sleep_high"

    if study_hours < 2:
        study_key = "study_low"
    elif study_hours <= 6:
        study_key = "study_mid"
    else:
        study_key = "study_high"

    return {
        "stress_class": stress_class,
        "stress": stress_key,
        "activity": activity_key,
        "screen": screen_key,
        "sleep": sleep_key,
        "study": study_key,
    }


def init_session_state():
    defaults = {
        "age": 20,
        "gender": "Male",
        "country": "India",
        "academic_level": "High School",
        "platform": "Instagram",
        "purpose": "Entertainment",
        "avg_daily_usage": 4.0,
        "daily_unlocks": 50.0,
        "study_hours": 4.0,
        "physical_activity": 1.0,
        "sleep_hours": 7.0,
        "stress_level": "Low",
        "last_result": None,
        "api_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
"""
<style>
:root {
    color-scheme: light dark;
    --card-bg: rgba(127, 127, 127, 0.08);
    --card-border: rgba(127, 127, 127, 0.20);
    --accent: #4f46e5;
}

.stApp {
    font-family: "Noto Sans Devanagari", "Segoe UI", system-ui, sans-serif;
    overflow: visible;
}

.block-container {
    max-width: 1120px;
    padding-top: 3.5rem !important;
    padding-bottom: 2.4rem;
}

.lang-screen {
    max-width: 640px;
    margin: 1.5rem auto 0 auto;
    padding: 40px 32px;
    border-radius: 24px;
    text-align: center;
    background: linear-gradient(160deg, rgba(99, 102, 241, 0.16), rgba(14, 165, 233, 0.08));
    border: 1px solid rgba(99, 102, 241, 0.28);
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.lang-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 10px;
}

.lang-subtitle {
    font-size: 15px;
    line-height: 1.6;
    opacity: 0.72;
    margin-bottom: 8px;
}

.app-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 18px;
}

.header-title {
    font-size: 30px;
    font-weight: 800;
    line-height: 1.35;
    margin: 0 0 6px 0;
    overflow: visible;
}

.header-subtitle {
    font-size: 14px;
    opacity: 0.68;
}

.hero {
    padding: 28px 30px;
    border-radius: 22px;
    margin-bottom: 22px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(59, 130, 246, 0.10));
    border: 1px solid rgba(99, 102, 241, 0.30);
    box-shadow: 0 12px 30px rgba(79, 70, 229, 0.08);
}

.hero-text {
    font-size: 16px;
    line-height: 1.65;
    opacity: 0.86;
    max-width: 860px;
}

.hero-notice {
    display: inline-block;
    margin-top: 14px;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    background: rgba(245, 158, 11, 0.16);
    border: 1px solid rgba(245, 158, 11, 0.35);
}

.section-card {
    padding: 18px 22px;
    border-radius: 18px;
    margin-top: 18px;
    margin-bottom: 14px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

.section-title {
    font-size: 22px;
    font-weight: 750;
    margin-bottom: 4px;
}

.section-subtitle {
    font-size: 14px;
    opacity: 0.65;
}

.result-card {
    margin-top: 28px;
    padding: 32px;
    border-radius: 24px;
    text-align: center;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.16), rgba(99, 102, 241, 0.10));
    border: 1px solid rgba(99, 102, 241, 0.30);
    box-shadow: 0 16px 36px rgba(59, 130, 246, 0.10);
}

.result-label {
    font-size: 16px;
    font-weight: 650;
    opacity: 0.75;
}

.score {
    font-size: 58px;
    font-weight: 850;
    margin: 8px 0 14px 0;
    line-height: 1.1;
}

.score-track {
    width: min(420px, 100%);
    height: 10px;
    margin: 0 auto 14px auto;
    border-radius: 999px;
    background: rgba(127, 127, 127, 0.18);
    overflow: hidden;
}

.score-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6366f1, #0ea5e9);
}

.score-description {
    font-size: 14px;
    opacity: 0.68;
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.55;
}

.category {
    display: inline-block;
    margin-top: 16px;
    padding: 9px 16px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.30);
}

.suggestions-title {
    font-size: 24px;
    font-weight: 750;
    margin-top: 32px;
    margin-bottom: 16px;
}

.suggestion-card {
    padding: 18px 20px;
    border-radius: 16px;
    margin-bottom: 12px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

.suggestion-title {
    font-size: 15px;
    font-weight: 750;
    margin-bottom: 5px;
}

.suggestion-text {
    font-size: 14px;
    line-height: 1.55;
    opacity: 0.82;
}

.stress-low {
    background: rgba(22, 163, 74, 0.14);
    border: 1px solid rgba(22, 163, 74, 0.35);
}

.stress-medium {
    background: rgba(234, 138, 0, 0.15);
    border: 1px solid rgba(234, 138, 0, 0.38);
}

.stress-high {
    background: rgba(220, 38, 38, 0.14);
    border: 1px solid rgba(220, 38, 38, 0.38);
}

.stress-very-high {
    background: rgba(153, 27, 27, 0.18);
    border: 1px solid rgba(153, 27, 27, 0.45);
}

.disclaimer {
    margin-top: 28px;
    padding: 16px 18px;
    border-radius: 14px;
    background: rgba(127, 127, 127, 0.07);
    border: 1px solid rgba(127, 127, 127, 0.16);
    font-size: 12px;
    line-height: 1.55;
    opacity: 0.72;
}

.footer {
    text-align: center;
    margin-top: 28px;
    padding-top: 18px;
    font-size: 13px;
    opacity: 0.55;
    border-top: 1px solid rgba(127, 127, 127, 0.15);
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    font-size: 16px;
}

.predict-wrap div.stButton > button {
    min-height: 56px;
    font-size: 17px;
    border: 0;
}

@media (max-width: 768px) {
    .block-container { padding-top: 3.75rem !important; }
    .lang-screen { padding: 28px 20px; margin-top: 0.75rem; }
    .lang-title { font-size: 26px; }
    .header-title { font-size: 24px; line-height: 1.4; }
    .hero { padding: 22px 18px; }
    .hero-text { font-size: 15px; }
    .score { font-size: 44px; }
    .section-title { font-size: 19px; }
    .app-header { flex-direction: column; }
}
</style>
""",
unsafe_allow_html=True
)

init_session_state()

# =========================================================
# LANGUAGE SELECTION SCREEN
# =========================================================

if "lang" not in st.session_state:
    st.session_state.lang = None

if st.session_state.lang is None:
    st.markdown(
        f"""
        <div class="lang-screen">
            <div class="lang-title">{TRANSLATIONS["en"]["lang_title"]}</div>
            <div class="lang-subtitle">{TRANSLATIONS["en"]["lang_subtitle"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_en, col_hi = st.columns(2)
    with col_en:
        st.button(
            TRANSLATIONS["en"]["btn_english"],
            key="pick_en",
            use_container_width=True,
            on_click=set_lang_en,
        )
    with col_hi:
        st.button(
            TRANSLATIONS["hi"]["btn_hindi"],
            key="pick_hi",
            use_container_width=True,
            on_click=set_lang_hi,
        )
    st.stop()

# =========================================================
# HEADER
# =========================================================

head_left, head_right = st.columns([3.2, 1.4])

with head_left:
    st.markdown(
        f"""
        <div class="header-title">{t("app_title")}</div>
        <div class="header-subtitle">{t("app_subtitle")}</div>
        """,
        unsafe_allow_html=True,
    )

with head_right:
    sw_en, sw_hi = st.columns(2)
    with sw_en:
        st.button(
            "🇬🇧 English",
            key="hdr_lang_en",
            use_container_width=True,
            on_click=set_lang_en,
        )
    with sw_hi:
        st.button(
            "🇮🇳 हिन्दी",
            key="hdr_lang_hi",
            use_container_width=True,
            on_click=set_lang_hi,
        )

# =========================================================
# HERO / INTRO
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-text">{t("hero_text")}</div>
        <div class="hero-notice">{t("hero_notice")}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# STUDENT PROFILE
# =========================================================

st.markdown(
    f"""
    <div class="section-card">
        <div class="section-title">{t("profile_title")}</div>
        <div class="section-subtitle">{t("profile_desc")}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.number_input(t("label_age"), min_value=1, max_value=100, value=20, step=1, key="age")

with col2:
    st.selectbox(
        t("label_gender"),
        GENDER_OPTIONS,
        format_func=format_gender,
        key="gender",
    )

with col3:
    st.selectbox(
        t("label_country"),
        COUNTRY_OPTIONS,
        format_func=format_country,
        key="country",
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.selectbox(
        t("label_academic"),
        ACADEMIC_OPTIONS,
        format_func=format_academic,
        key="academic_level",
    )

with col5:
    st.selectbox(
        t("label_platform"),
        PLATFORM_OPTIONS,
        format_func=format_platform,
        key="platform",
    )

with col6:
    st.selectbox(
        t("label_purpose"),
        PURPOSE_OPTIONS,
        format_func=format_purpose,
        key="purpose",
    )

# =========================================================
# DIGITAL BEHAVIOUR
# =========================================================

st.markdown(
    f"""
    <div class="section-card">
        <div class="section-title">{t("digital_title")}</div>
        <div class="section-subtitle">{t("digital_desc")}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.number_input(
        t("label_usage"),
        min_value=0.0,
        max_value=24.0,
        value=4.0,
        step=0.5,
        key="avg_daily_usage",
    )

with col2:
    st.number_input(
        t("label_unlocks"),
        min_value=0.0,
        max_value=500.0,
        value=50.0,
        step=1.0,
        key="daily_unlocks",
    )

# =========================================================
# LIFESTYLE
# =========================================================

st.markdown(
    f"""
    <div class="section-card">
        <div class="section-title">{t("lifestyle_title")}</div>
        <div class="section-subtitle">{t("lifestyle_desc")}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.number_input(
        t("label_study"),
        min_value=0.0,
        max_value=24.0,
        value=4.0,
        step=0.5,
        key="study_hours",
    )

with col2:
    st.number_input(
        t("label_activity"),
        min_value=0.0,
        max_value=24.0,
        value=1.0,
        step=0.5,
        key="physical_activity",
    )

with col3:
    st.number_input(
        t("label_sleep"),
        min_value=0.0,
        max_value=24.0,
        value=7.0,
        step=0.5,
        key="sleep_hours",
    )

st.selectbox(
    t("label_stress"),
    STRESS_OPTIONS,
    format_func=format_stress,
    key="stress_level",
)

# Values stored in session_state are the original ML categories
age = st.session_state.age
gender = st.session_state.gender
country = st.session_state.country
academic_level = st.session_state.academic_level
platform = st.session_state.platform
purpose = st.session_state.purpose
avg_daily_usage = st.session_state.avg_daily_usage
daily_unlocks = st.session_state.daily_unlocks
study_hours = st.session_state.study_hours
physical_activity = st.session_state.physical_activity
sleep_hours = st.session_state.sleep_hours
stress_level = st.session_state.stress_level

# =========================================================
# PREDICT BUTTON  (API is called only here)
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="predict-wrap">', unsafe_allow_html=True)
predict_button = st.button(t("predict_button"), use_container_width=True, key="predict_btn")
st.markdown("</div>", unsafe_allow_html=True)

if predict_button:
    top10_country = {
        "India", "USA", "Canada", "Australia", "UK",
        "Germany", "Mexico", "Turkey", "France"
    }
    group_country = country if country in top10_country else "Other"

    payload = {
        "Age": age,
        "Gender": gender,
        "Country": group_country,
        "Academic_Level": academic_level,
        "Most_Used_Platform": platform,
        "Purpose_Of_Use": purpose,
        "Avg_Daily_Usage_Hours": avg_daily_usage,
        "Daily_Unlocks": daily_unlocks,
        "Study_Hours": study_hours,
        "Physical_Activity_Hours": physical_activity,
        "Sleep_Hours_Per_Night": sleep_hours,
        "Stress_Level": stress_level
    }

    try:
        with st.spinner(t("loading")):
            response = requests.post(API_URL, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

        prediction = float(result["predicted_mental_health_score"])
        prediction = max(0.0, min(10.0, prediction))

        st.session_state.api_error = None
        st.session_state.last_result = {
            "prediction": prediction,
            "stress_level": stress_level,
            "physical_activity": physical_activity,
            "avg_daily_usage": avg_daily_usage,
            "sleep_hours": sleep_hours,
            "study_hours": study_hours,
        }

    except requests.exceptions.ConnectionError:
        st.session_state.api_error = "connection"
    except requests.exceptions.Timeout:
        st.session_state.api_error = "timeout"
    except requests.exceptions.RequestException as e:
        st.session_state.api_error = ("request", str(e))
    except Exception as e:
        st.session_state.api_error = ("generic", str(e))

# Language switching never enters the predict_button block.

if st.session_state.api_error == "connection":
    st.error(t("err_connection"))
elif st.session_state.api_error == "timeout":
    st.error(t("err_timeout"))
elif isinstance(st.session_state.api_error, tuple) and st.session_state.api_error[0] == "request":
    st.error(t("err_request").format(error=st.session_state.api_error[1]))
elif isinstance(st.session_state.api_error, tuple) and st.session_state.api_error[0] == "generic":
    st.error(t("err_generic").format(error=st.session_state.api_error[1]))

# =========================================================
# RESULT + SUGGESTIONS  (from stored snapshot; no extra API call)
# =========================================================

last = st.session_state.last_result

if last is not None:
    prediction = last["prediction"]
    score_pct = max(0.0, min(100.0, (prediction / 10.0) * 100.0))
    cat = category_key(prediction)
    keys = suggestion_keys(
        last["stress_level"],
        last["physical_activity"],
        last["avg_daily_usage"],
        last["sleep_hours"],
        last["study_hours"],
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">{t("result_label")}</div>
            <div class="score">{prediction:.2f} / 10</div>
            <div class="score-track"><div class="score-fill" style="width:{score_pct:.1f}%"></div></div>
            <div class="score-description">{t("score_description")}</div>
            <div class="category">{t(cat)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""<div class="suggestions-title">{t("suggestions_title")}</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="suggestion-card {keys["stress_class"]}">
            <div class="suggestion-title">{t("sugg_stress_title")}</div>
            <div class="suggestion-text">{t(keys["stress"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="suggestion-card">
            <div class="suggestion-title">{t("sugg_activity_title")}</div>
            <div class="suggestion-text">{t(keys["activity"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="suggestion-card">
            <div class="suggestion-title">{t("sugg_screen_title")}</div>
            <div class="suggestion-text">{t(keys["screen"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="suggestion-card">
            <div class="suggestion-title">{t("sugg_sleep_title")}</div>
            <div class="suggestion-text">{t(keys["sleep"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="suggestion-card">
            <div class="suggestion-title">{t("sugg_study_title")}</div>
            <div class="suggestion-text">{t(keys["study"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# DISCLAIMER & FOOTER
# =========================================================

st.markdown(
    f"""<div class="disclaimer">{t("disclaimer")}</div>""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""<div class="footer">{t("footer")}</div>""",
    unsafe_allow_html=True,
)
