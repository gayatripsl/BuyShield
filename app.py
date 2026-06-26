from flask import Flask, render_template_string, request

app = Flask(__name__)

# ─── Translations ───
TRANSLATIONS = {
    'en': {
        'title': 'BuyShield — Fake Seller Detector',
        'header': '🛡️ BuyShield',
        'subtitle': 'AI-Powered Fake Instagram Seller Detector — Check Before You Pay',
        'intro': 'Before paying any Instagram seller, answer these 8 simple questions. BuyShield will analyse the seller behaviour and give you a risk score in seconds. Free. No registration needed.',
        'form_title': 'Answer about the seller',
        'submit': '🛡️ Check Now',
        'check_again': '🔄 Check Another Seller',
        'report': '🚨 Report This Scam at cybercrime.gov.in',
        'red_flags': 'Red Flags Detected',
        'no_flags': '✅ No major red flags detected',
        'what_to_do': 'What You Should Do',
        'footer': 'BuyShield — Protecting innocent Indian buyers 🛡️\nWhen in doubt — don\'t pay. Stay safe.',
        'questions': [
            'Did the seller REFUSE a video call showing the product?',
            'Did they demand FULL PAYMENT before showing you the actual product?',
            'Did they REFUSE to photograph the product with today\'s date written on paper?',
            'Did they use urgency like "today only offer" or "last piece left"?',
            'Is their Instagram page LESS THAN 1 MONTH old?',
            'Are their prices UNREALISTICALLY CHEAP compared to market rate?',
            'Did they BLOCK YOU or go silent immediately after payment?',
            'After payment, did they ask for EXTRA MONEY like shipping fee or customs charge?',
        ],
        'yes': 'Yes',
        'no': 'No',
        'high_risk': 'HIGH RISK — Do NOT pay this seller',
        'caution': 'CAUTION — Multiple red flags. Verify before paying.',
        'low_risk': 'LOWER RISK — Fewer red flags. Still verify carefully.',
        'flags': [
            'Seller refused video call — genuine sellers always agree to show product live',
            'Demanded payment WITHOUT showing product first — this is the primary scam mechanism',
            'Refused to photograph product with today\'s date — suggests product does not exist',
            'Used urgency tactics like today only or last piece — designed to stop you from thinking',
            'Instagram page is less than 1 month old — scammers need to act fast and disappear',
            'Prices are unrealistically low — scammers use low prices as bait',
            'Seller blocked or went silent after payment — confirmed scam behaviour',
            'Seller asked for extra charges AFTER payment — this is Advance Fee Fraud. Stop paying immediately.',
        ],
        'guidance_high': [
            'Do NOT send any more money',
            'Block and report this account on Instagram',
            'Report at cybercrime.gov.in if you already paid',
            'Take screenshots of all chats as evidence',
            'Warn your friends and family about this page',
        ],
        'guidance_high_extra': 'STOP paying extra charges — every new charge is another theft',
        'guidance_medium': [
            'Ask seller for a video call showing product RIGHT NOW',
            'Ask seller to photograph product with TODAY\'S DATE on paper',
            'Do NOT pay full amount before seeing product',
            'Search seller phone number on Truecaller',
            'Save all chat screenshots before paying',
        ],
        'guidance_low': [
            'Proceed carefully — always verify before final payment',
            'Prefer partial payment first if possible',
            'Save all chat screenshots before paying',
            'Trust your instincts — if something feels wrong it probably is',
        ],
    },
    'te': {
        'title': 'BuyShield — నకిలీ విక్రేత గుర్తింపు',
        'header': '🛡️ BuyShield',
        'subtitle': 'AI ఆధారిత నకిలీ Instagram విక్రేత గుర్తింపు — చెల్లించే ముందు తనిఖీ చేయండి',
        'intro': 'ఏదైనా Instagram విక్రేతకు చెల్లించే ముందు ఈ 8 సాధారణ ప్రశ్నలకు సమాధానం ఇవ్వండి. BuyShield విక్రేత ప్రవర్తనను విశ్లేషించి మీకు రిస్క్ స్కోర్ ఇస్తుంది. ఉచితం. రిజిస్ట్రేషన్ అవసరం లేదు.',
        'form_title': 'విక్రేత గురించి సమాధానం ఇవ్వండి',
        'submit': '🛡️ ఇప్పుడు తనిఖీ చేయండి',
        'check_again': '🔄 మరొక విక్రేతను తనిఖీ చేయండి',
        'report': '🚨 cybercrime.gov.in లో ఈ మోసాన్ని రిపోర్ట్ చేయండి',
        'red_flags': 'గుర్తించిన హెచ్చరికలు',
        'no_flags': '✅ పెద్ద హెచ్చరికలు ఏమీ గుర్తించబడలేదు',
        'what_to_do': 'మీరు ఏమి చేయాలి',
        'footer': 'BuyShield — అమాయక భారతీయ కొనుగోలుదారులను రక్షిస్తోంది 🛡️\nసందేహం ఉంటే — చెల్లించకండి. సురక్షితంగా ఉండండి.',
        'questions': [
            'విక్రేత ఉత్పత్తిని చూపించే వీడియో కాల్‌ను తిరస్కరించారా?',
            'ఉత్పత్తిని చూపించే ముందే పూర్తి చెల్లింపు డిమాండ్ చేశారా?',
            'నేటి తేదీ కాగితంతో ఉత్పత్తి ఫోటో తీయడానికి తిరస్కరించారా?',
            '"ఈరోజు మాత్రమే ఆఫర్" లేదా "చివరి వస్తువు" వంటి అత్యవసరత చూపించారా?',
            'వారి Instagram పేజీ 1 నెల కంటే తక్కువ పాతదా?',
            'వారి ధరలు మార్కెట్ రేటుతో పోలిస్తే అసాధారణంగా తక్కువగా ఉన్నాయా?',
            'చెల్లింపు తర్వాత వారు మిమ్మల్ని బ్లాక్ చేశారా లేదా మౌనంగా ఉన్నారా?',
            'చెల్లింపు తర్వాత షిప్పింగ్ ఫీజు లేదా కస్టమ్స్ చార్జ్ వంటి అదనపు డబ్బు అడిగారా?',
        ],
        'yes': 'అవును',
        'no': 'కాదు',
        'high_risk': 'అధిక ప్రమాదం — ఈ విక్రేతకు చెల్లించకండి',
        'caution': 'జాగ్రత్త — అనేక హెచ్చరికలు. చెల్లించే ముందు ధృవీకరించండి.',
        'low_risk': 'తక్కువ ప్రమాదం — తక్కువ హెచ్చరికలు. అయినా జాగ్రత్తగా ధృవీకరించండి.',
        'flags': [
            'విక్రేత వీడియో కాల్ తిరస్కరించారు — నిజమైన విక్రేతలు ఎప్పుడూ ఉత్పత్తి చూపించడానికి అంగీకరిస్తారు',
            'ఉత్పత్తి చూపించే ముందే చెల్లింపు డిమాండ్ చేశారు — ఇది ప్రధాన మోసం పద్ధతి',
            'నేటి తేదీతో ఉత్పత్తి ఫోటో తీయడానికి నిరాకరించారు — ఉత్పత్తి అస్తిత్వంలో లేదని సూచిస్తుంది',
            'అత్యవసరత వ్యూహాలు ఉపయోగించారు — మీరు జాగ్రత్తగా ఆలోచించకుండా చేయడానికి',
            'Instagram పేజీ 1 నెల కంటే తక్కువ పాతది — మోసగాళ్ళు వేగంగా వెళ్ళిపోవాలి',
            'ధరలు అసాధారణంగా తక్కువగా ఉన్నాయి — మోసగాళ్ళు ఆకర్షణకు తక్కువ ధరలు వాడతారు',
            'చెల్లింపు తర్వాత విక్రేత బ్లాక్ చేశారు — నిర్ధారిత మోసం ప్రవర్తన',
            'చెల్లింపు తర్వాత అదనపు చార్జీలు అడిగారు — ఇది అడ్వాన్స్ ఫీ మోసం. వెంటనే చెల్లించడం ఆపండి.',
        ],
        'guidance_high': [
            'ఇంకా డబ్బు పంపకండి',
            'Instagram లో ఈ అకౌంట్‌ను బ్లాక్ చేసి రిపోర్ట్ చేయండి',
            'ఇప్పటికే చెల్లించి ఉంటే cybercrime.gov.in లో రిపోర్ట్ చేయండి',
            'అన్ని చాట్ స్క్రీన్‌షాట్‌లు సాక్ష్యంగా తీసుకోండి',
            'మీ స్నేహితులకు మరియు కుటుంబానికి హెచ్చరించండి',
        ],
        'guidance_high_extra': 'అదనపు చార్జీలు చెల్లించడం ఆపండి — ప్రతి కొత్త చార్జ్ మరొక దోపిడీ',
        'guidance_medium': [
            'విక్రేతను ఇప్పుడే ఉత్పత్తి చూపించే వీడియో కాల్ అడగండి',
            'నేటి తేదీ కాగితంతో ఉత్పత్తి ఫోటో అడగండి',
            'ఉత్పత్తి చూడకుండా పూర్తి మొత్తం చెల్లించకండి',
            'విక్రేత ఫోన్ నంబర్‌ను Truecaller లో వెతకండి',
            'చెల్లించే ముందు అన్ని చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
        ],
        'guidance_low': [
            'జాగ్రత్తగా ముందుకు వెళ్ళండి — చివరి చెల్లింపు ముందు ధృవీకరించండి',
            'వీలైతే ముందు పాక్షిక చెల్లింపు చేయండి',
            'చెల్లించే ముందు అన్ని చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'మీ అంతర్మనస్సును నమ్మండి — తప్పు అనిపిస్తే అది తప్పే',
        ],
    },
    'hi': {
        'title': 'BuyShield — नकली विक्रेता पहचानकर्ता',
        'header': '🛡️ BuyShield',
        'subtitle': 'AI-संचालित नकली Instagram विक्रेता पहचान — भुगतान से पहले जांचें',
        'intro': 'किसी भी Instagram विक्रेता को भुगतान करने से पहले इन 8 सरल प्रश्नों का उत्तर दें। BuyShield विक्रेता के व्यवहार का विश्लेषण करके आपको सेकंडों में जोखिम स्कोर देगा। मुफ्त। कोई पंजीकरण नहीं।',
        'form_title': 'विक्रेता के बारे में उत्तर दें',
        'submit': '🛡️ अभी जांचें',
        'check_again': '🔄 दूसरे विक्रेता की जांच करें',
        'report': '🚨 cybercrime.gov.in पर इस धोखाधड़ी की रिपोर्ट करें',
        'red_flags': 'पहचाने गए खतरे',
        'no_flags': '✅ कोई बड़ा खतरा नहीं पाया गया',
        'what_to_do': 'आपको क्या करना चाहिए',
        'footer': 'BuyShield — निर्दोष भारतीय खरीदारों की रक्षा करता है 🛡️\nसंदेह हो तो — भुगतान न करें। सुरक्षित रहें।',
        'questions': [
            'क्या विक्रेता ने उत्पाद दिखाने वाली वीडियो कॉल से मना किया?',
            'क्या उन्होंने उत्पाद दिखाने से पहले पूरा भुगतान मांगा?',
            'क्या उन्होंने आज की तारीख वाले कागज के साथ उत्पाद की फोटो लेने से मना किया?',
            'क्या उन्होंने "आज का ऑफर" या "आखिरी सामान" जैसी जल्दबाजी दिखाई?',
            'क्या उनका Instagram पेज 1 महीने से कम पुराना है?',
            'क्या उनकी कीमतें बाजार भाव से असामान्य रूप से कम हैं?',
            'क्या भुगतान के बाद उन्होंने आपको ब्लॉक किया या चुप हो गए?',
            'क्या भुगतान के बाद उन्होंने शिपिंग फीस या कस्टम चार्ज जैसे अतिरिक्त पैसे मांगे?',
        ],
        'yes': 'हाँ',
        'no': 'नहीं',
        'high_risk': 'उच्च जोखिम — इस विक्रेता को भुगतान न करें',
        'caution': 'सावधानी — कई खतरे मिले। भुगतान से पहले सत्यापित करें।',
        'low_risk': 'कम जोखिम — कम खतरे। फिर भी सावधानी से जांचें।',
        'flags': [
            'विक्रेता ने वीडियो कॉल से मना किया — असली विक्रेता हमेशा उत्पाद दिखाने को तैयार रहते हैं',
            'उत्पाद दिखाए बिना भुगतान मांगा — यह मुख्य धोखाधड़ी तरीका है',
            'आज की तारीख के साथ फोटो लेने से मना किया — उत्पाद का अस्तित्व नहीं है',
            'जल्दबाजी की रणनीति इस्तेमाल की — आपको सोचने से रोकने के लिए',
            'Instagram पेज 1 महीने से कम पुराना — धोखेबाज जल्दी भागना चाहते हैं',
            'कीमतें असामान्य रूप से कम — धोखेबाज लालच देने के लिए कम कीमत रखते हैं',
            'भुगतान के बाद ब्लॉक किया — पुष्टि की गई धोखाधड़ी',
            'भुगतान के बाद अतिरिक्त शुल्क मांगा — यह एडवांस फी धोखाधड़ी है। तुरंत भुगतान बंद करें।',
        ],
        'guidance_high': [
            'अब और पैसे न भेजें',
            'Instagram पर इस अकाउंट को ब्लॉक करें और रिपोर्ट करें',
            'अगर पहले ही भुगतान किया है तो cybercrime.gov.in पर रिपोर्ट करें',
            'सबूत के तौर पर सभी चैट स्क्रीनशॉट लें',
            'अपने दोस्तों और परिवार को इस पेज के बारे में चेतावनी दें',
        ],
        'guidance_high_extra': 'अतिरिक्त शुल्क देना बंद करें — हर नया शुल्क एक और चोरी है',
        'guidance_medium': [
            'विक्रेता से अभी उत्पाद दिखाने वाली वीडियो कॉल मांगें',
            'आज की तारीख वाले कागज के साथ उत्पाद की फोटो मांगें',
            'उत्पाद देखे बिना पूरा भुगतान न करें',
            'विक्रेता का फोन नंबर Truecaller पर खोजें',
            'भुगतान से पहले सभी चैट स्क्रीनशॉट सेव करें',
        ],
        'guidance_low': [
            'सावधानी से आगे बढ़ें — अंतिम भुगतान से पहले सत्यापित करें',
            'हो सके तो पहले आंशिक भुगतान करें',
            'भुगतान से पहले सभी चैट स्क्रीनशॉट सेव करें',
            'अपनी अंतरात्मा पर भरोसा करें — गलत लगे तो गलत ही है',
        ],
    }
}

# ─── Scoring Engine ───
def calculate_risk_score(answers):
    score = 0
    flag_indices = []

    checks = [
        ('refused_video_call', 25),
        ('payment_before_product', 20),
        ('refused_date_photo', 15),
        ('urgency_tactics', 15),
        ('page_very_new', 10),
        ('unrealistic_price', 10),
        ('blocked_after_payment', 20),
        ('extra_charges_after_payment', 25),
    ]

    for i, (key, points) in enumerate(checks):
        if answers.get(key):
            score += points
            flag_indices.append(i)

    score = min(score, 100)
    return score, flag_indices


def get_verdict_key(score):
    if score >= 70:
        return 'high_risk', 'red'
    elif score >= 35:
        return 'caution', 'orange'
    else:
        return 'low_risk', 'green'


def get_guidance(score, answers, lang):
    t = TRANSLATIONS[lang]
    if score >= 70:
        guidance = list(t['guidance_high'])
        if answers.get('extra_charges_after_payment'):
            guidance.insert(1, t['guidance_high_extra'])
        return guidance
    elif score >= 35:
        return t['guidance_medium']
    else:
        return t['guidance_low']


# ─── HTML Template ───
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #0f0f1a; color: #ffffff; min-height: 100vh; }

        .header { background: #1a1a2e; padding: 20px; text-align: center; border-bottom: 3px solid #e94560; }
        .header h1 { font-size: 28px; color: #e94560; }
        .header p { color: #cccccc; margin-top: 6px; font-size: 14px; }

        .lang-bar { background: #16213e; padding: 12px; text-align: center; }
        .lang-btn { display: inline-block; margin: 0 6px; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-size: 13px; font-weight: bold; border: 2px solid #e94560; color: #e94560; background: transparent; cursor: pointer; }
        .lang-btn.active { background: #e94560; color: white; }
        .lang-btn:hover { background: #e94560; color: white; }

        .container { max-width: 700px; margin: 30px auto; padding: 0 20px; }

        .intro-card { background: #1a1a2e; border-radius: 12px; padding: 20px; margin-bottom: 25px; border-left: 4px solid #e94560; }
        .intro-card p { color: #cccccc; line-height: 1.6; font-size: 14px; }

        .form-card { background: #1a1a2e; border-radius: 12px; padding: 25px; margin-bottom: 25px; }
        .form-card h2 { color: #e94560; margin-bottom: 20px; font-size: 18px; }

        .question { margin-bottom: 20px; padding: 15px; background: #16213e; border-radius: 10px; }
        .question p { font-size: 14px; color: #ffffff; margin-bottom: 12px; line-height: 1.5; }
        .question label { display: inline-flex; align-items: center; margin-right: 20px; cursor: pointer; font-size: 14px; color: #cccccc; }
        .question input[type=radio] { margin-right: 6px; accent-color: #e94560; width: 16px; height: 16px; }

        .submit-btn { width: 100%; padding: 16px; background: #e94560; color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .submit-btn:hover { background: #c73652; }

        .result-card { border-radius: 12px; padding: 25px; margin-bottom: 20px; }
        .result-red { background: #2d0a0a; border: 2px solid #cc2936; }
        .result-orange { background: #2d1a00; border: 2px solid #f5a623; }
        .result-green { background: #0a2d1a; border: 2px solid #02a676; }

        .score-display { text-align: center; margin-bottom: 20px; }
        .score-number { font-size: 64px; font-weight: bold; }
        .score-red { color: #cc2936; }
        .score-orange { color: #f5a623; }
        .score-green { color: #02a676; }
        .verdict { font-size: 20px; font-weight: bold; margin-top: 8px; }

        .flags-section { margin-top: 20px; }
        .flags-section h3 { margin-bottom: 12px; color: #ffffff; font-size: 16px; }
        .flag-item { background: rgba(204,41,54,0.15); border-left: 3px solid #cc2936; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; font-size: 13px; color: #ffcccc; line-height: 1.5; }

        .guidance-section { margin-top: 20px; }
        .guidance-section h3 { margin-bottom: 12px; color: #ffffff; font-size: 16px; }
        .guidance-item { background: #16213e; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; font-size: 13px; color: #cccccc; line-height: 1.5; }
        .guidance-item::before { content: "✅ "; }

        .report-link { display: block; text-align: center; margin-top: 20px; padding: 14px; background: #e94560; color: white; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 15px; }
        .check-again { display: block; text-align: center; margin-top: 12px; padding: 14px; background: #16213e; color: #e94560; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 15px; border: 2px solid #e94560; }

        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; margin-top: 20px; }
    </style>
</head>
<body>

<div class="header">
    <h1>{{ t.header }}</h1>
    <p>{{ t.subtitle }}</p>
</div>

<div class="lang-bar">
    <a href="/?lang=en" class="lang-btn {% if lang == 'en' %}active{% endif %}">English</a>
    <a href="/?lang=te" class="lang-btn {% if lang == 'te' %}active{% endif %}">తెలుగు</a>
    <a href="/?lang=hi" class="lang-btn {% if lang == 'hi' %}active{% endif %}">हिंदी</a>
</div>

<div class="container">

{% if not result %}
<div class="intro-card">
    <p>{{ t.intro }}</p>
</div>

<form method="POST" action="/check?lang={{ lang }}">
<div class="form-card">
    <h2>{{ t.form_title }}</h2>

    {% for i in range(8) %}
    <div class="question">
        <p>{{ i+1 }}. {{ t.questions[i] }}</p>
        <label><input type="radio" name="q{{ i }}" value="yes" required> {{ t.yes }}</label>
        <label><input type="radio" name="q{{ i }}" value="no"> {{ t.no }}</label>
    </div>
    {% endfor %}

    <button type="submit" class="submit-btn">{{ t.submit }}</button>
</div>
</form>

{% else %}
<div class="result-card result-{{ color }}">
    <div class="score-display">
        <div class="score-number score-{{ color }}">{{ score }}<span style="font-size:28px">/100</span></div>
        <div class="verdict" style="color: {% if color == 'red' %}#cc2936{% elif color == 'orange' %}#f5a623{% else %}#02a676{% endif %}">
            {{ verdict }}
        </div>
    </div>

    {% if flags %}
    <div class="flags-section">
        <h3>⚠️ {{ t.red_flags }} ({{ flags|length }})</h3>
        {% for flag in flags %}
        <div class="flag-item">{{ flag }}</div>
        {% endfor %}
    </div>
    {% else %}
    <div class="flags-section">
        <h3>{{ t.no_flags }}</h3>
    </div>
    {% endif %}

    <div class="guidance-section">
        <h3>{{ t.what_to_do }}</h3>
        {% for g in guidance %}
        <div class="guidance-item">{{ g }}</div>
        {% endfor %}
    </div>

    {% if score >= 70 %}
    <a href="https://cybercrime.gov.in" target="_blank" class="report-link">{{ t.report }}</a>
    {% endif %}

    <a href="/?lang={{ lang }}" class="check-again">{{ t.check_again }}</a>
</div>
{% endif %}

<div class="footer">
    {{ t.footer }}
</div>

</div>
</body>
</html>
"""

# ─── Routes ───
@app.route("/")
def home():
    lang = request.args.get('lang', 'en')
    if lang not in TRANSLATIONS:
        lang = 'en'
    t = TRANSLATIONS[lang]
    return render_template_string(HTML, result=False, t=t, lang=lang)


@app.route("/check", methods=["POST"])
def check():
    lang = request.args.get('lang', 'en')
    if lang not in TRANSLATIONS:
        lang = 'en'
    t = TRANSLATIONS[lang]

    answers = {
        'refused_video_call': request.form.get('q0') == 'yes',
        'payment_before_product': request.form.get('q1') == 'yes',
        'refused_date_photo': request.form.get('q2') == 'yes',
        'urgency_tactics': request.form.get('q3') == 'yes',
        'page_very_new': request.form.get('q4') == 'yes',
        'unrealistic_price': request.form.get('q5') == 'yes',
        'blocked_after_payment': request.form.get('q6') == 'yes',
        'extra_charges_after_payment': request.form.get('q7') == 'yes',
    }

    score, flag_indices = calculate_risk_score(answers)
    verdict_key, color = get_verdict_key(score)
    verdict = t[verdict_key]
    flags = [t['flags'][i] for i in flag_indices]
    guidance = get_guidance(score, answers, lang)

    return render_template_string(HTML,
        result=True,
        score=score,
        flags=flags,
        verdict=verdict,
        color=color,
        guidance=guidance,
        t=t,
        lang=lang
    )


if __name__ == "__main__":
    app.run()
