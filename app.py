from flask import Flask, render_template_string, request
import pickle
import os
import pandas as pd
from PIL import Image

app = Flask(__name__)

# ─── Load ML Model ───
model = None
model_path = os.path.join(os.path.dirname(__file__), 'buyshield_model.pkl')
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("✅ ML model loaded!")
except Exception as e:
    print(f"⚠️ Model not found: {e}")

LANG_LABELS = {
    'en': 'English',
    'te': 'తెలుగు',
    'hi': 'हिंदी',
}

TRANSLATIONS = {
    'en': {
        'title': 'BuyShield — AI Scam Protection',
        'tagline_1': "Don't Trust.",
        'tagline_2': 'Verify.',
        'tagline_3': 'Pay Safely.',
        'subtitle': 'AI-Powered protection against fake Instagram sellers.',
        'free': '100% Free',
        'no_reg': 'No Registration',
        'instant': 'Instant Result',
        'free_forever': '100% Free Forever',
        'no_signup': 'No sign up. No limits.',
        'made_india': '🛡️ Made for India',
        'new_check': 'New Check',
        'history': 'History',
        'analytics': 'Analytics',
        'how_it_works': 'How it Works',
        'safety_tips': 'Safety Tips',
        'about': 'About Us',
        'image_title': 'Upload Product Image (Optional)',
        'image_desc': "Upload a product photo the seller sent you. We'll analyse it for red flags.",
        'image_label': 'Drag & drop or click to upload',
        'image_hint': 'JPG, PNG, WEBP — Max 5MB',
        'questions_title': 'Answer 8 Simple Questions',
        'questions_sub': "Help our AI understand the seller's behaviour",
        'analyze_btn': 'Analyze Seller',
        'analyze_sub': 'AI will check and give risk score in seconds',
        'trust_score': 'Trust Score',
        'powered_by': 'Powered by BuyShield AI Model',
        'image_analysis': 'Image Analysis',
        'red_flags': 'Red Flags Detected',
        'what_to_do': 'What You Should Do',
        'report_btn': '⚠️ Report This Scam at cybercrime.gov.in',
        'check_another': '🔍 Check Another Seller',
        'no_flags': 'No major red flags detected',
        'how_works_title': 'How it works',
        'step1': 'Answer 8 simple questions',
        'step2': 'Our AI analyzes the risk',
        'step3': 'Get your trust score instantly',
        'key_insights': 'Key Insights',
        'insight1': 'Always verify the seller',
        'insight2': 'Avoid full payment in advance',
        'insight3': 'Trust your instincts',
        'insight4': 'Use safe payment methods',
        'disclaimer': 'BuyShield provides risk assessment based on user-provided behaviour patterns. This is not a definitive assurance. Always use your own judgement.',
        'footer': 'Made with ❤️ in India 🇮🇳',
        'yes': 'Yes',
        'no': 'No',
        'high_risk': 'HIGH RISK',
        'high_risk_sub': 'DO NOT pay this seller',
        'caution': 'MODERATE RISK',
        'caution_sub': 'Verify before paying',
        'low_risk': 'LOW RISK',
        'low_risk_sub': 'Proceed carefully',
        'why_title': 'Why This Matters',
        'why_items': [
            'Scammers often target buyers who feel rushed or excited about a deal.',
            'Most scams ask for full payment before any proof the product is real.',
            'A few seconds of checking can save you from losing your money.',
        ],
        'live_badge': 'LIVE',
        'live_hint': 'Updates instantly as you answer the questions below',
        'answered_label': 'Questions Answered',
        'about_p1': 'BuyShield is a free, independent safety tool built to help everyday online shoppers spot fake sellers before they pay — especially on Instagram, where most India-based shopping scams now happen.',
        'about_p2': "We're not affiliated with Instagram, Meta, or any government body. Our AI model looks for common behaviour patterns reported by real scam victims, but it is a guide — not a guarantee. Always trust your own judgement and verify before you pay.",
        'about_helpline': "If you've already been scammed, call India's National Cyber Crime Helpline at 1930 (24x7) or report it at cybercrime.gov.in",
        'questions': [
            'Did the seller REFUSE a video call showing the product?',
            'Did they demand FULL PAYMENT before showing the actual product?',
            "Did they REFUSE to photograph the product with today's date on paper?",
            'Did they use urgency like "today only offer" or "last piece left"?',
            'Is their Instagram page LESS THAN 1 MONTH old?',
            'Are their prices UNREALISTICALLY CHEAP compared to market?',
            'Did they BLOCK YOU or go silent after payment?',
            'After payment, did they ask for EXTRA MONEY like shipping fee?',
        ],
        'q_icons': ['🎥', '💳', '📸', '⚡', '📅', '💰', '🚫', '💸'],
        'flags': [
            'Seller refused video call — genuine sellers always agree to show product live',
            'Demanded payment WITHOUT showing product first — primary scam mechanism',
            'Refused date proof photo — suggests product does not exist',
            'Used urgency tactics — designed to stop you from thinking carefully',
            'Page less than 1 month old — scammers need to act fast and disappear',
            'Prices unrealistically low — scammers use low prices as bait',
            'Blocked after payment — confirmed scam behaviour',
            'Asked for extra charges after payment — this is Advance Fee Fraud',
        ],
        'guidance_high': [
            'Do NOT send any more money',
            'STOP paying extra charges — every new charge is another trap',
            'Block and report this account on Instagram',
            'Report at cybercrime.gov.in if you already paid',
            'Take screenshots of all chats as evidence',
            'Warn your friends and family about this page',
        ],
        'guidance_medium': [
            'Ask seller for a video call showing product RIGHT NOW',
            "Ask seller to photograph product with TODAY'S DATE on paper",
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
        'img_flags': {
            'too_small': 'Image is very small — may be a low quality stolen image',
            'no_exif': 'Image has no camera metadata — may not be an original photo',
            'ai_uniform': 'Image appears too uniform — could be AI generated or heavily edited',
            'suspicious_ratio': 'Image dimensions look unusual — may be a screenshot of another listing',
        },
        'img_safe': 'Image appears to be an original photo — no suspicious patterns detected',
        'img_note': 'Note: Image analysis is one signal only. Ask the seller to show the product on a live video call to be certain.',
    },
    'te': {
        'title': 'BuyShield — AI స్కామ్ రక్షణ',
        'tagline_1': 'నమ్మకండి.',
        'tagline_2': 'ధృవీకరించండి.',
        'tagline_3': 'సురక్షితంగా చెల్లించండి.',
        'subtitle': 'నకిలీ Instagram విక్రేతలకు వ్యతిరేకంగా AI రక్షణ.',
        'free': '100% ఉచితం',
        'no_reg': 'రిజిస్ట్రేషన్ లేదు',
        'instant': 'తక్షణ ఫలితం',
        'free_forever': '100% ఎల్లప్పుడూ ఉచితం',
        'no_signup': 'సైన్ అప్ లేదు. పరిమితులు లేవు.',
        'made_india': '🇮🇳 భారతదేశంలో తయారైంది',
        'new_check': 'కొత్త తనిఖీ',
        'history': 'చరిత్ర',
        'analytics': 'విశ్లేషణ',
        'how_it_works': 'ఎలా పని చేస్తుంది',
        'safety_tips': 'భద్రతా చిట్కాలు',
        'about': 'మా గురించి',
        'image_title': 'ఉత్పత్తి చిత్రం అప్‌లోడ్ చేయండి (ఐచ్ఛికం)',
        'image_desc': 'ఉత్పత్తి ఫోటో అప్‌లోడ్ చేయండి. మేము దాన్ని విశ్లేషిస్తాము.',
        'image_label': 'డ్రాగ్ & డ్రాప్ లేదా క్లిక్ చేయండి',
        'image_hint': 'JPG, PNG, WEBP — గరిష్టంగా 5MB',
        'questions_title': '8 సాధారణ ప్రశ్నలకు సమాధానం ఇవ్వండి',
        'questions_sub': 'విక్రేత ప్రవర్తనను అర్థం చేసుకోవడానికి సహాయం చేయండి',
        'analyze_btn': 'విక్రేతను విశ్లేషించండి',
        'analyze_sub': 'AI తనిఖీ చేసి సెకన్లలో రిస్క్ స్కోర్ ఇస్తుంది',
        'trust_score': 'ట్రస్ట్ స్కోర్',
        'powered_by': 'BuyShield AI మోడల్ ద్వారా',
        'image_analysis': 'చిత్ర విశ్లేషణ',
        'red_flags': 'గుర్తించిన హెచ్చరికలు',
        'what_to_do': 'మీరు ఏమి చేయాలి',
        'report_btn': '⚠️ cybercrime.gov.in లో రిపోర్ట్ చేయండి',
        'check_another': '🔍 మరొక విక్రేతను తనిఖీ చేయండి',
        'no_flags': 'పెద్ద హెచ్చరికలు ఏమీ లేవు',
        'how_works_title': 'ఎలా పని చేస్తుంది',
        'step1': '8 సాధారణ ప్రశ్నలకు సమాధానం',
        'step2': 'మా AI రిస్క్ విశ్లేషిస్తుంది',
        'step3': 'వెంటనే ట్రస్ట్ స్కోర్ పొందండి',
        'key_insights': 'ముఖ్య సూచనలు',
        'insight1': 'ఎల్లప్పుడూ విక్రేతను ధృవీకరించండి',
        'insight2': 'ముందుగా పూర్తి చెల్లింపు నివారించండి',
        'insight3': 'మీ అంతర్మనస్సును నమ్మండి',
        'insight4': 'సురక్షిత చెల్లింపు పద్ధతులు వాడండి',
        'disclaimer': 'BuyShield వినియోగదారు నివేదించిన సంకేతాల ఆధారంగా రిస్క్ అంచనా అందిస్తుంది. ఇది నిర్ధారిత అభియోగం కాదు.',
        'footer': '❤️ తో భారతదేశంలో తయారైంది 🇮🇳',
        'yes': 'అవును',
        'no': 'కాదు',
        'high_risk': 'అధిక ప్రమాదం',
        'high_risk_sub': 'చెల్లించకండి',
        'caution': 'మధ్యస్థ ప్రమాదం',
        'caution_sub': 'చెల్లించే ముందు ధృవీకరించండి',
        'low_risk': 'తక్కువ ప్రమాదం',
        'low_risk_sub': 'జాగ్రత్తగా ముందుకు వెళ్ళండి',
        'why_title': 'ఇది ఎందుకు ముఖ్యం',
        'why_items': [
            'తొందరపడేలా లేదా ఆఫర్‌తో ఉత్సాహపరిచే కొనుగోలుదారులను స్కామర్లు లక్ష్యంగా చేసుకుంటారు.',
            'చాలా స్కామ్‌లు ఉత్పత్తి నిజమైనదని రుజువు చూపకుండానే పూర్తి చెల్లింపు అడుగుతాయి.',
            'కొన్ని సెకన్ల తనిఖీ మీ డబ్బును కాపాడగలదు.',
        ],
        'live_badge': 'లైవ్',
        'live_hint': 'మీరు దిగువ ప్రశ్నలకు సమాధానం ఇస్తున్నప్పుడు తక్షణమే అప్‌డేట్ అవుతుంది',
        'answered_label': 'సమాధానం ఇచ్చిన ప్రశ్నలు',
        'about_p1': 'BuyShield అనేది ఆన్‌లైన్ కొనుగోలుదారులు చెల్లించే ముందు నకిలీ విక్రేతలను గుర్తించడంలో సహాయపడే ఉచిత, స్వతంత్ర భద్రతా టూల్ — ప్రత్యేకించి Instagram లో, ఇప్పుడు భారతదేశంలో ఎక్కువ షాపింగ్ స్కామ్‌లు జరుగుతున్నాయి.',
        'about_p2': 'మేము Instagram, Meta లేదా ఏ ప్రభుత్వ సంస్థతో సంబంధం లేదు. మా AI మోడల్ నిజమైన బాధితులు నివేదించిన సాధారణ ప్రవర్తన నమూనాలను చూస్తుంది, కానీ ఇది ఒక గైడ్ మాత్రమే — హామీ కాదు. ఎల్లప్పుడూ మీ స్వంత తీర్పును నమ్మండి మరియు చెల్లించే ముందు ధృవీకరించండి.',
        'about_helpline': 'మీరు ఇప్పటికే మోసపోయినట్లయితే, భారతదేశ నేషనల్ సైబర్ క్రైమ్ హెల్ప్‌లైన్ 1930 (24x7) కు కాల్ చేయండి లేదా cybercrime.gov.in లో రిపోర్ట్ చేయండి',
        'questions': [
            'విక్రేత వీడియో కాల్‌ను తిరస్కరించారా?',
            'ఉత్పత్తి చూపించే ముందే పూర్తి చెల్లింపు డిమాండ్ చేశారా?',
            'నేటి తేదీ కాగితంతో ఫోటో తీయడానికి నిరాకరించారా?',
            '"ఈరోజు మాత్రమే" వంటి అత్యవసరత చూపించారా?',
            'వారి Instagram పేజీ 1 నెల కంటే తక్కువ పాతదా?',
            'ధరలు అసాధారణంగా తక్కువగా ఉన్నాయా?',
            'చెల్లింపు తర్వాత బ్లాక్ చేశారా?',
            'చెల్లింపు తర్వాత అదనపు డబ్బు అడిగారా?',
        ],
        'q_icons': ['🎥', '💳', '📸', '⚡', '📅', '💰', '🚫', '💸'],
        'flags': [
            'వీడియో కాల్ తిరస్కరించారు — నిజమైన విక్రేతలు ఎప్పుడూ అంగీకరిస్తారు',
            'ఉత్పత్తి చూపించే ముందే చెల్లింపు అడిగారు — ప్రధాన మోసం పద్ధతి',
            'నేటి తేదీతో ఫోటో తీయడానికి నిరాకరించారు',
            'అత్యవసరత వ్యూహాలు ఉపయోగించారు',
            'పేజీ 1 నెల కంటే తక్కువ పాతది',
            'ధరలు అసాధారణంగా తక్కువ — స్కామర్లు ఆకర్షించడానికి',
            'చెల్లింపు తర్వాత బ్లాక్ చేశారు — నిర్ధారిత మోసం',
            'చెల్లింపు తర్వాత అదనపు చార్జీలు అడిగారు — అడ్వాన్స్ ఫీ మోసం',
        ],
        'guidance_high': [
            'ఇంకా డబ్బు పంపకండి',
            'అదనపు చార్జీలు చెల్లించడం ఆపండి',
            'Instagram లో బ్లాక్ చేసి రిపోర్ట్ చేయండి',
            'cybercrime.gov.in లో రిపోర్ట్ చేయండి',
            'అన్ని చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'స్నేహితులకు హెచ్చరించండి',
        ],
        'guidance_medium': [
            'వీడియో కాల్ అడగండి',
            'నేటి తేదీతో ఫోటో అడగండి',
            'పూర్తి మొత్తం చెల్లించకండి',
            'Truecaller లో నంబర్ వెతకండి',
            'చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
        ],
        'guidance_low': [
            'జాగ్రత్తగా ముందుకు వెళ్ళండి',
            'పాక్షిక చెల్లింపు చేయండి',
            'స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'అంతర్మనస్సును నమ్మండి',
        ],
        'img_flags': {
            'too_small': 'చిత్రం చాలా చిన్నది — దొంగిలించిన చిత్రం కావచ్చు',
            'no_exif': 'చిత్రంలో కెమెరా సమాచారం లేదు — అసలు ఫోటో కాకపోవచ్చు',
            'ai_uniform': 'చిత్రం చాలా సమానంగా ఉంది — AI జనరేటెడ్ కావచ్చు',
            'suspicious_ratio': 'చిత్రం కొలతలు అనుమానాస్పదంగా ఉన్నాయి',
        },
        'img_safe': 'చిత్రం అసలైనదిగా కనిపిస్తోంది',
        'img_note': 'గమనిక: నిర్ధారణకు వీడియో కాల్ అడగండి.',
    },
    'hi': {
        'title': 'BuyShield — AI स्कैम सुरक्षा',
        'tagline_1': 'भरोसा मत करो।',
        'tagline_2': 'सत्यापित करो।',
        'tagline_3': 'सुरक्षित भुगतान करो।',
        'subtitle': 'नकली Instagram विक्रेताओं के खिलाफ AI सुरक्षा।',
        'free': '100% मुफ्त',
        'no_reg': 'कोई पंजीकरण नहीं',
        'instant': 'तुरंत परिणाम',
        'free_forever': '100% हमेशा मुफ्त',
        'no_signup': 'कोई साइन अप नहीं। कोई सीमा नहीं।',
        'made_india': '🇮🇳 भारत में बना',
        'new_check': 'नई जांच',
        'history': 'इतिहास',
        'analytics': 'विश्लेषण',
        'how_it_works': 'कैसे काम करता है',
        'safety_tips': 'सुरक्षा टिप्स',
        'about': 'हमारे बारे में',
        'image_title': 'उत्पाद छवि अपलोड करें (वैकल्पिक)',
        'image_desc': 'विक्रेता द्वारा भेजी गई उत्पाद फोटो अपलोड करें।',
        'image_label': 'ड्रैग & ड्रॉप या क्लिक करें',
        'image_hint': 'JPG, PNG, WEBP — अधिकतम 5MB',
        'questions_title': '8 सरल प्रश्नों का उत्तर दें',
        'questions_sub': 'हमारे AI को विक्रेता के व्यवहार को समझने में मदद करें',
        'analyze_btn': 'विक्रेता का विश्लेषण करें',
        'analyze_sub': 'AI जांच करेगा और सेकंडों में जोखिम स्कोर देगा',
        'trust_score': 'ट्रस्ट स्कोर',
        'powered_by': 'BuyShield AI मॉडल द्वारा संचालित',
        'image_analysis': 'छवि विश्लेषण',
        'red_flags': 'पहचाने गए खतरे',
        'what_to_do': 'आपको क्या करना चाहिए',
        'report_btn': '⚠️ cybercrime.gov.in पर रिपोर्ट करें',
        'check_another': '🔍 दूसरे विक्रेता की जांच करें',
        'no_flags': 'कोई बड़ा खतरा नहीं',
        'how_works_title': 'कैसे काम करता है',
        'step1': '8 सरल प्रश्नों का उत्तर दें',
        'step2': 'हमारा AI जोखिम का विश्लेषण करता है',
        'step3': 'तुरंत ट्रस्ट स्कोर पाएं',
        'key_insights': 'मुख्य सुझाव',
        'insight1': 'हमेशा विक्रेता को सत्यापित करें',
        'insight2': 'पहले पूरा भुगतान करने से बचें',
        'insight3': 'अपनी अंतरात्मा पर भरोसा करें',
        'insight4': 'सुरक्षित भुगतान विधियां उपयोग करें',
        'disclaimer': 'BuyShield उपयोगकर्ता द्वारा प्रदान किए गए व्यवहार संकेतों के आधार पर जोखिम मूल्यांकन प्रदान करता है।',
        'footer': '❤️ के साथ भारत में बना 🇮🇳',
        'yes': 'हाँ',
        'no': 'नहीं',
        'high_risk': 'उच्च जोखिम',
        'high_risk_sub': 'भुगतान न करें',
        'caution': 'मध्यम जोखिम',
        'caution_sub': 'भुगतान से पहले सत्यापित करें',
        'low_risk': 'कम जोखिम',
        'low_risk_sub': 'सावधानी से आगे बढ़ें',
        'why_title': 'यह क्यों ज़रूरी है',
        'why_items': [
            'स्कैमर अक्सर उन खरीदारों को निशाना बनाते हैं जो जल्दी में हों या ऑफर से उत्साहित हों।',
            'ज्यादातर स्कैम में उत्पाद असली होने का सबूत दिए बिना पूरा भुगतान मांगा जाता है।',
            'कुछ सेकंड की जांच आपके पैसे बचा सकती है।',
        ],
        'live_badge': 'लाइव',
        'live_hint': 'जैसे ही आप नीचे प्रश्नों के उत्तर देंगे, यह तुरंत अपडेट होगा',
        'answered_label': 'उत्तर दिए गए प्रश्न',
        'about_p1': 'BuyShield एक मुफ्त, स्वतंत्र सुरक्षा टूल है जो ऑनलाइन खरीदारों को भुगतान करने से पहले नकली विक्रेताओं को पहचानने में मदद करता है — खासकर Instagram पर, जहां अब भारत में ज्यादातर शॉपिंग स्कैम होते हैं।',
        'about_p2': 'हम Instagram, Meta या किसी सरकारी संस्था से संबद्ध नहीं हैं। हमारा AI मॉडल असली पीड़ितों द्वारा रिपोर्ट किए गए सामान्य व्यवहार पैटर्न देखता है, लेकिन यह एक गाइड है — गारंटी नहीं। हमेशा अपने विवेक पर भरोसा करें और भुगतान से पहले सत्यापित करें।',
        'about_helpline': 'यदि आपके साथ पहले ही धोखाधड़ी हो चुकी है, तो भारत की नेशनल साइबर क्राइम हेल्पलाइन 1930 (24x7) पर कॉल करें या cybercrime.gov.in पर रिपोर्ट करें',
        'questions': [
            'क्या विक्रेता ने वीडियो कॉल से मना किया?',
            'क्या उन्होंने उत्पाद दिखाने से पहले पूरा भुगतान मांगा?',
            'क्या उन्होंने आज की तारीख वाली फोटो लेने से मना किया?',
            'क्या उन्होंने "आज का ऑफर" जैसी जल्दबाजी दिखाई?',
            'क्या उनका Instagram पेज 1 महीने से कम पुराना है?',
            'क्या उनकी कीमतें असामान्य रूप से कम हैं?',
            'क्या भुगतान के बाद उन्होंने ब्लॉक किया?',
            'क्या भुगतान के बाद अतिरिक्त पैसे मांगे?',
        ],
        'q_icons': ['🎥', '💳', '📸', '⚡', '📅', '💰', '🚫', '💸'],
        'flags': [
            'वीडियो कॉल से मना किया — असली विक्रेता हमेशा तैयार रहते हैं',
            'उत्पाद दिखाए बिना भुगतान मांगा — मुख्य धोखाधड़ी तरीका',
            'आज की तारीख वाली फोटो से मना किया',
            'जल्दबाजी की रणनीति इस्तेमाल की',
            'पेज 1 महीने से कम पुराना',
            'कीमतें असामान्य रूप से कम — धोखेबाज सस्ती कीमत से फंसाते हैं',
            'भुगतान के बाद ब्लॉक किया — पुष्टि हुई धोखाधड़ी',
            'भुगतान के बाद अतिरिक्त शुल्क मांगा — एडवांस फी धोखाधड़ी',
        ],
        'guidance_high': [
            'अब और पैसे न भेजें',
            'अतिरिक्त शुल्क देना बंद करें',
            'Instagram पर ब्लॉक करें और रिपोर्ट करें',
            'cybercrime.gov.in पर रिपोर्ट करें',
            'सभी चैट स्क्रीनशॉट सेव करें',
            'दोस्तों और परिवार को चेतावनी दें',
        ],
        'guidance_medium': [
            'वीडियो कॉल मांगें',
            'आज की तारीख वाली फोटो मांगें',
            'उत्पाद देखे बिना पूरा भुगतान न करें',
            'Truecaller पर नंबर खोजें',
            'सभी चैट स्क्रीनशॉट सेव करें',
        ],
        'guidance_low': [
            'सावधानी से आगे बढ़ें',
            'पहले आंशिक भुगतान करें',
            'स्क्रीनशॉट सेव करें',
            'अंतरात्मा पर भरोसा करें',
        ],
        'img_flags': {
            'too_small': 'छवि बहुत छोटी है — चोरी की गई हो सकती है',
            'no_exif': 'छवि में कैमरा डेटा नहीं है — मूल फोटो नहीं हो सकती',
            'ai_uniform': 'छवि बहुत एकसमान दिखती है — AI जनरेटेड हो सकती है',
            'suspicious_ratio': 'छवि का आकार संदिग्ध है',
        },
        'img_safe': 'छवि मूल प्रतीत होती है',
        'img_note': 'नोट: पुष्टि के लिए वीडियो कॉल मांगें।',
    }
}

def analyse_image(file):
    findings = []
    score_addition = 0
    try:
        img = Image.open(file)
        width, height = img.size
        if width < 200 or height < 200:
            findings.append('too_small')
            score_addition += 8
        exif_data = img._getexif() if hasattr(img, '_getexif') else None
        if exif_data is None:
            findings.append('no_exif')
            score_addition += 5
        if img.mode in ('RGB', 'RGBA'):
            img_small = img.resize((50, 50))
            pixels = list(img_small.getdata())
            if img.mode == 'RGBA':
                pixels = [(r, g, b) for r, g, b, a in pixels]
            r_vals = [p[0] for p in pixels]
            g_vals = [p[1] for p in pixels]
            b_vals = [p[2] for p in pixels]
            if (max(r_vals) - min(r_vals) < 30 and
                max(g_vals) - min(g_vals) < 30 and
                max(b_vals) - min(b_vals) < 30):
                findings.append('ai_uniform')
                score_addition += 10
        ratio = width / height if height > 0 else 1
        if ratio > 3.0 or ratio < 0.3:
            findings.append('suspicious_ratio')
            score_addition += 5
    except Exception as e:
        print(f"Image error: {e}")
    return findings, score_addition

def calculate_risk_score(answers):
    flag_indices = []
    checks = [
        'refused_video_call', 'payment_before_product', 'refused_date_photo',
        'urgency_tactics', 'page_very_new', 'unrealistic_price',
        'blocked_after_payment', 'extra_charges_after_payment',
    ]
    for i, key in enumerate(checks):
        if answers.get(key):
            flag_indices.append(i)
    if model is not None:
        try:
            input_data = pd.DataFrame([{
                'refused_video_call': int(answers.get('refused_video_call', False)),
                'payment_before_product': int(answers.get('payment_before_product', False)),
                'refused_date_photo': int(answers.get('refused_date_photo', False)),
                'urgency_tactics': int(answers.get('urgency_tactics', False)),
                'page_very_new': int(answers.get('page_very_new', False)),
                'unrealistic_price': int(answers.get('unrealistic_price', False)),
                'blocked_after_payment': int(answers.get('blocked_after_payment', False)),
                'extra_charges_after_payment': int(answers.get('extra_charges_after_payment', False)),
            }])
            prob = model.predict_proba(input_data)[0][1]
            return int(prob * 100), flag_indices
        except Exception as e:
            print(f"Model error: {e}")
    points = [25, 20, 15, 15, 10, 10, 20, 25]
    score = sum(points[i] for i in flag_indices)
    return min(score, 100), flag_indices

def get_verdict(score, t):
    if score >= 70:
        return t['high_risk'], t['high_risk_sub'], 'red'
    elif score >= 35:
        return t['caution'], t['caution_sub'], 'orange'
    else:
        return t['low_risk'], t['low_risk_sub'], 'green'

def get_guidance(score, answers, t):
    if score >= 70:
        guidance = list(t['guidance_high'])
        if answers.get('extra_charges_after_payment') and len(guidance) > 1:
            # Already included stop paying extra charges at index 1
            pass
        return guidance
    elif score >= 35:
        return t['guidance_medium']
    else:
        return t['guidance_low']


HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ t.title }}</title>
<style>
:root[data-theme="dark"] {
    --bg: #0d0d1a;
    --sidebar: #090912;
    --surface: #13132a;
    --surface2: #1a1a35;
    --surface3: #20203f;
    --border: #2a2a50;
    --text: #ffffff;
    --text2: #9090b8;
    --text3: #606090;
    --accent: #7c5cfc;
    --accent2: #9b7cff;
    --red: #ff4757;
    --orange: #ffa502;
    --green: #2ed573;
    --blue: #1e90ff;
    --card-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
:root[data-theme="light"] {
    --bg: #f0f2ff;
    --sidebar: #ffffff;
    --surface: #ffffff;
    --surface2: #f5f5ff;
    --surface3: #ebebff;
    --border: #e0e0f0;
    --text: #1a1a35;
    --text2: #505080;
    --text3: #9090b8;
    --accent: #7c5cfc;
    --accent2: #6040e0;
    --red: #e0313e;
    --orange: #e07800;
    --green: #1a9e48;
    --blue: #1060cc;
    --card-shadow: 0 4px 24px rgba(100,100,200,0.1);
}

* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; display: flex; }

/* ── SIDEBAR ── */
.sidebar {
    width: 220px; min-height: 100vh; background: var(--sidebar);
    border-right: 1px solid var(--border); display: flex; flex-direction: column;
    padding: 24px 16px; position: fixed; top:0; left:0; bottom:0; z-index:100;
    transition: transform 0.3s;
}
.sidebar-logo { display:flex; align-items:center; gap:10px; margin-bottom:32px; padding:0 8px; }
.sidebar-logo-icon {
    width:36px; height:36px; border-radius:10px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display:flex; align-items:center; justify-content:center; font-size:18px;
}
.sidebar-logo-text { font-size:18px; font-weight:800; color:var(--text); }
.sidebar-logo-text span { color:var(--accent); }
.sidebar-sub { font-size:10px; color:var(--text2); margin-top:1px; }

.nav-section { font-size:10px; font-weight:700; color:var(--text3); text-transform:uppercase; letter-spacing:1.2px; padding:0 12px; margin:16px 0 6px; }

.nav-item {
    display:flex; align-items:center; gap:10px; padding:10px 12px;
    border-radius:10px; color:var(--text2); font-size:13px; font-weight:500;
    text-decoration:none; margin-bottom:4px; cursor:pointer; border:none; background:none; width:100%;
    transition: all 0.2s;
}
.nav-item:hover { background:var(--surface2); color:var(--text); }
.nav-item.active { background:linear-gradient(135deg, rgba(124,92,252,0.2), rgba(124,92,252,0.1)); color:var(--accent); font-weight:600; }
.nav-item.active .nav-icon { color:var(--accent); }
.nav-icon { font-size:16px; width:20px; text-align:center; }
.nav-badge { margin-left:auto; font-size:10px; background:var(--accent); color:white; padding:2px 7px; border-radius:20px; }

.sidebar-footer { margin-top:auto; padding:16px 12px; background:linear-gradient(135deg, rgba(124,92,252,0.15), rgba(124,92,252,0.05)); border-radius:12px; border:1px solid rgba(124,92,252,0.2); }
.sidebar-footer p { font-size:13px; font-weight:700; color:var(--text); margin-bottom:4px; }
.sidebar-footer span { font-size:11px; color:var(--text2); }
.sidebar-made { font-size:11px; color:var(--text2); text-align:center; margin-top:12px; }

/* ── MAIN ── */
.main { margin-left:220px; flex:1; min-height:100vh; display:flex; flex-direction:column; }

/* ── TOP BAR ── */
.topbar {
    height:56px; background:var(--surface); border-bottom:1px solid var(--border);
    display:flex; align-items:center; justify-content:space-between;
    padding:0 24px; position:sticky; top:0; z-index:50;
}
.topbar-left { display:flex; align-items:center; gap:8px; }
.made-badge {
    font-size:12px; color:var(--text2); background:var(--surface2);
    padding:4px 10px; border-radius:20px; border:1px solid var(--border);
}
.topbar-right { display:flex; align-items:center; gap:8px; }

/* ── LANGUAGE POPUP ── */
.lang-dropdown { position:relative; }
.lang-toggle-btn {
    display:flex; align-items:center; gap:6px;
    padding:6px 12px; border-radius:8px; border:1px solid var(--border);
    background:var(--surface2); color:var(--text); font-size:12px; font-weight:700;
    cursor:pointer; transition:border-color 0.15s;
}
.lang-toggle-btn:hover { border-color:var(--accent); }
.lang-toggle-icon { font-size:14px; }
.lang-caret { font-size:9px; color:var(--text2); transition:transform 0.2s; margin-left:2px; }
.lang-dropdown.open .lang-caret { transform:rotate(180deg); }
.lang-popup {
    position:absolute; top:calc(100% + 8px); right:0; left:auto;
    background:var(--surface); border:1px solid var(--border); border-radius:12px;
    box-shadow:var(--card-shadow); padding:6px; min-width:160px; z-index:200;
    display:none; flex-direction:column; gap:2px;
}
.lang-dropdown.open .lang-popup { display:flex; }
.lang-popup-item {
    display:flex; align-items:center; justify-content:space-between;
    padding:9px 12px; border-radius:8px; font-size:13px; font-weight:600;
    text-decoration:none; color:var(--text2); transition:all 0.15s;
}
.lang-popup-item:hover { background:var(--surface2); color:var(--text); }
.lang-popup-item.active { background:rgba(124,92,252,0.15); color:var(--accent); }
.lang-popup-check { font-size:12px; color:var(--accent); }
.theme-btn {
    width:32px; height:32px; border-radius:8px; border:1px solid var(--border);
    background:var(--surface2); cursor:pointer; font-size:14px;
    display:flex; align-items:center; justify-content:center; color:var(--text2);
}

/* ── CONTENT ── */
.content { padding:24px; flex:1; max-width:1300px; margin:0 auto; width:100%; }

/* ── HERO ── */
.hero { display:flex; align-items:center; justify-content:space-between; margin-bottom:28px; }
.hero-text h1 { font-size:40px; font-weight:900; line-height:1.15; margin-bottom:12px; }
.hero-text h1 .line2 { color:var(--accent); }
.hero-text p { color:var(--text2); font-size:14px; max-width:380px; margin-bottom:20px; }
.hero-badges { display:flex; gap:12px; flex-wrap:wrap; }
.hero-badge { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--text2); }
.hero-badge-icon { font-size:14px; }
.hero-shield { font-size:120px; opacity:0.9; filter:drop-shadow(0 0 40px rgba(124,92,252,0.4)); }

/* ── FORM GRID ── */
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; align-items:start; }

/* ── CARDS ── */
.card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:16px; padding:20px;
    box-shadow: var(--card-shadow);
}
.card-title { font-size:13px; font-weight:700; color:var(--text); margin-bottom:6px; display:flex; align-items:center; gap:8px; }
.card-sub { font-size:12px; color:var(--text2); margin-bottom:16px; }

/* ── UPLOAD ── */
.upload-zone {
    border:2px dashed var(--border); border-radius:12px; padding:28px 20px;
    text-align:center; cursor:pointer; transition:border-color 0.2s;
}
.upload-zone:hover { border-color:var(--accent); }
.upload-zone input { display:none; }
.upload-icon { font-size:32px; margin-bottom:10px; color:var(--text2); }
.upload-label-text { font-size:13px; color:var(--text2); margin-bottom:4px; }
.upload-hint { font-size:11px; color:var(--text3); }
#preview-container { margin-top:12px; display:none; }
#preview-container img { max-width:120px; max-height:120px; border-radius:8px; border:1px solid var(--border); }
#file-name { font-size:11px; color:var(--green); margin-top:4px; }

/* ── ANALYZE BUTTON ── */
.analyze-card {
    background:linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius:16px; padding:20px; display:flex; align-items:center;
    justify-content:space-between; cursor:pointer; border:none; width:100%;
    box-shadow:0 8px 32px rgba(124,92,252,0.35);
}
.analyze-card:hover { transform:translateY(-2px); box-shadow:0 12px 40px rgba(124,92,252,0.45); }
.analyze-card-text { text-align:left; }
.analyze-card-text h3 { font-size:18px; font-weight:800; color:white; margin-bottom:4px; }
.analyze-card-text p { font-size:12px; color:rgba(255,255,255,0.8); }
.analyze-arrow { width:48px; height:48px; border-radius:50%; background:rgba(255,255,255,0.2); display:flex; align-items:center; justify-content:center; font-size:20px; color:white; flex-shrink:0; }

/* ── QUESTIONS GRID ── */
.questions-grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; }
.q-card {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:12px; padding:12px; transition:border-color 0.2s;
}
.q-card:hover { border-color:var(--accent); }
.q-icon { font-size:20px; margin-bottom:8px; }
.q-num { font-size:9px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }
.q-text { font-size:11px; color:var(--text); line-height:1.4; margin-bottom:10px; font-weight:500; }
.q-options { display:flex; gap:6px; }
.q-opt {
    flex:1; padding:6px 4px; border-radius:6px; border:1.5px solid var(--border);
    font-size:11px; font-weight:600; color:var(--text2); cursor:pointer;
    display:flex; align-items:center; justify-content:center; gap:4px;
    background:none; transition:all 0.15s;
}
.q-opt input { display:none; }
.q-opt.yes:hover { border-color:var(--red); color:var(--red); background:rgba(255,71,87,0.08); }
.q-opt.no:hover { border-color:var(--green); color:var(--green); background:rgba(46,213,115,0.08); }
.q-opt:has(input:checked).yes { border-color:var(--red); color:var(--red); background:rgba(255,71,87,0.12); }
.q-opt:has(input:checked).no { border-color:var(--green); color:var(--green); background:rgba(46,213,115,0.12); }

/* ── HOW IT WORKS ── */
.how-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; }
.step { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.step-num { width:28px; height:28px; border-radius:50%; background:var(--accent); color:white; font-size:12px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.step-text { font-size:12px; color:var(--text2); line-height:1.4; }

/* ── RISK PANEL (right side) ── */
.risk-panel { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; }
.risk-score-label { font-size:11px; font-weight:700; color:var(--text2); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; display:flex; align-items:center; gap:6px; }
.live-tag { margin-left:auto; font-size:9px; font-weight:800; letter-spacing:0.5px; background:var(--accent); color:white; padding:3px 8px; border-radius:20px; display:inline-flex; align-items:center; gap:4px; }
.live-dot { width:6px; height:6px; border-radius:50%; background:white; display:inline-block; animation:pulse 1.4s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.score-ring-wrap { display:flex; flex-direction:column; align-items:center; margin-bottom:16px; }
.score-ring {
    width:120px; height:120px; border-radius:50%; border:8px solid var(--border);
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    margin-bottom:10px; position:relative; transition:border-color 0.3s, box-shadow 0.3s;
}
.score-ring.red { border-color:var(--red); box-shadow:0 0 24px rgba(255,71,87,0.3); }
.score-ring.orange { border-color:var(--orange); box-shadow:0 0 24px rgba(255,165,2,0.3); }
.score-ring.green { border-color:var(--green); box-shadow:0 0 24px rgba(46,213,115,0.3); }
.score-num { font-size:40px; font-weight:900; line-height:1; transition:color 0.3s; }
.score-num.red { color:var(--red); }
.score-num.orange { color:var(--orange); }
.score-num.green { color:var(--green); }
.score-denom { font-size:12px; color:var(--text2); }
.verdict-pill {
    padding:6px 16px; border-radius:20px; font-size:13px; font-weight:800;
    margin-bottom:4px; transition:background 0.3s, color 0.3s;
}
.verdict-pill.red { background:rgba(255,71,87,0.15); color:var(--red); }
.verdict-pill.orange { background:rgba(255,165,2,0.15); color:var(--orange); }
.verdict-pill.green { background:rgba(46,213,115,0.15); color:var(--green); }
.verdict-sub { font-size:11px; color:var(--text2); margin-bottom:12px; text-align:center; }
.powered-badge { font-size:10px; color:var(--text2); display:flex; align-items:center; justify-content:center; gap:4px; }

.progress-row { display:flex; justify-content:space-between; font-size:11px; color:var(--text2); margin-bottom:6px; }
.progress-track { height:6px; background:var(--surface3); border-radius:4px; overflow:hidden; }
.progress-fill { height:100%; width:0%; background:linear-gradient(90deg, var(--accent), var(--accent2)); border-radius:4px; transition:width 0.3s; }

.risk-stat { display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid var(--border); }
.risk-stat:last-child { border-bottom:none; }
.risk-stat-label { font-size:11px; color:var(--text2); display:flex; align-items:center; gap:6px; }
.risk-stat-value { font-size:11px; font-weight:700; }
.risk-stat-value.good { color:var(--green); }
.risk-stat-value.bad { color:var(--red); }
.risk-stat-value.neutral { color:var(--text2); }

/* ── INSIGHTS / WHY ── */
.insights-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:16px; margin-top:16px; }
.insight-item { display:flex; align-items:flex-start; gap:8px; padding:6px 0; font-size:12px; color:var(--text2); line-height:1.5; }
.insight-dot { width:6px; height:6px; border-radius:50%; background:var(--accent); flex-shrink:0; margin-top:5px; }

/* ── ABOUT ── */
.about-card p { font-size:12px; color:var(--text2); line-height:1.7; margin-top:8px; }
.about-helpline { margin-top:14px; padding:12px; background:var(--surface2); border-radius:10px; font-size:12px; color:var(--text2); display:flex; align-items:center; gap:10px; border:1px solid var(--border); }
.about-helpline-icon { font-size:18px; flex-shrink:0; }

/* ── RESULT PAGE ── */
.result-grid { display:grid; grid-template-columns:320px 1fr; gap:20px; }
.result-left { display:flex; flex-direction:column; gap:16px; }
.result-right { display:flex; flex-direction:column; gap:16px; }

.flag-item { display:flex; align-items:flex-start; gap:10px; padding:10px 0; border-bottom:1px solid var(--border); font-size:12px; color:var(--text2); line-height:1.5; }
.flag-item:last-child { border-bottom:none; }
.flag-x { color:var(--red); font-size:14px; flex-shrink:0; font-weight:700; }
.flag-check { color:var(--green); font-size:14px; flex-shrink:0; }

.guidance-item { display:flex; align-items:flex-start; gap:8px; padding:8px 0; border-bottom:1px solid var(--border); font-size:12px; color:var(--text2); line-height:1.5; }
.guidance-item:last-child { border-bottom:none; }
.g-check { color:var(--green); flex-shrink:0; }

.img-finding { display:flex; align-items:flex-start; gap:8px; padding:8px 12px; background:rgba(255,165,2,0.08); border-radius:8px; margin-bottom:8px; font-size:12px; color:var(--text2); }
.img-finding-icon { font-size:14px; flex-shrink:0; }
.img-finding-note { font-size:11px; color:var(--text2); font-style:italic; margin-top:8px; padding:8px; background:var(--surface2); border-radius:6px; line-height:1.5; }
.img-safe { display:flex; align-items:center; gap:8px; padding:10px; background:rgba(46,213,115,0.08); border-radius:8px; font-size:12px; color:var(--green); }

.btn-report {
    display:flex; align-items:center; justify-content:center; gap:8px;
    padding:14px; background:var(--red); color:white; border-radius:12px;
    text-decoration:none; font-weight:700; font-size:14px; border:none; cursor:pointer;
    box-shadow:0 4px 16px rgba(255,71,87,0.3);
}
.btn-report:hover { background:#e0313e; }
.btn-another {
    display:flex; align-items:center; justify-content:center; gap:8px;
    padding:14px; background:var(--surface); color:var(--text); border-radius:12px;
    text-decoration:none; font-weight:700; font-size:14px;
    border:1px solid var(--border);
}
.btn-another:hover { background:var(--surface2); }

.disclaimer { font-size:11px; color:var(--text2); text-align:center; padding:16px; border-top:1px solid var(--border); line-height:1.6; }

/* ── HAMBURGER ── */
.hamburger { display:none; width:36px; height:36px; border-radius:8px; background:var(--surface2); border:1px solid var(--border); cursor:pointer; align-items:center; justify-content:center; font-size:18px; }
.sidebar-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:99; }

/* ── RESPONSIVE ── */
@media (max-width: 900px) {
    .sidebar { transform:translateX(-220px); }
    .sidebar.open { transform:translateX(0); }
    .sidebar-overlay.open { display:block; }
    .hamburger { display:flex; }
    .main { margin-left:0; }
    .questions-grid { grid-template-columns:repeat(2,1fr); }
    .form-grid { grid-template-columns:1fr; }
    .result-grid { grid-template-columns:1fr; }
    .hero { flex-direction:column; text-align:center; }
    .hero-shield { font-size:80px; }
    .hero-text h1 { font-size:28px; }
}
@media (max-width: 480px) {
    .questions-grid { grid-template-columns:repeat(2,1fr); }
    .content { padding:16px; }
    .hero-text h1 { font-size:24px; }
}
</style>
</head>
<body>

<!-- SIDEBAR OVERLAY (mobile) -->
<div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>

<!-- SIDEBAR -->
<nav class="sidebar" id="sidebar">
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🛡️</div>
        <div>
            <div class="sidebar-logo-text">Buy<span>Shield</span></div>
            <div class="sidebar-sub">AI Scam Protection</div>
        </div>
    </div>

    <div class="nav-section">Main</div>
    <a class="nav-item {% if not result %}active{% endif %}" href="/?lang={{ lang }}">
        <span class="nav-icon">🏠</span> {{ t.new_check }}
        <span class="nav-badge">AI</span>
    </a>

    <div class="nav-section">Tools</div>
    <a class="nav-item" href="/?lang={{ lang }}#how-it-works" onclick="return navAnchor(event, 'how-it-works')">
        <span class="nav-icon">❓</span> {{ t.how_it_works }}
    </a>
    <a class="nav-item" href="/?lang={{ lang }}#safety-tips" onclick="return navAnchor(event, 'safety-tips')">
        <span class="nav-icon">🛡️</span> {{ t.safety_tips }}
    </a>
    <a class="nav-item" href="https://cybercrime.gov.in" target="_blank" rel="noopener">
        <span class="nav-icon">🚨</span> Report Scam
    </a>

    <div class="nav-section">Info</div>
    <a class="nav-item" href="/?lang={{ lang }}#about" onclick="return navAnchor(event, 'about')">
        <span class="nav-icon">ℹ️</span> {{ t.about }}
    </a>

    <div class="sidebar-footer">
        <p>{{ t.free_forever }}</p>
        <span>{{ t.no_signup }}</span>
    </div>
    <div class="sidebar-made">{{ t.footer }}</div>
</nav>

<!-- MAIN -->
<div class="main">

    <!-- TOPBAR -->
    <div class="topbar">
        <div class="topbar-left">
            <button class="hamburger" onclick="toggleSidebar()">☰</button>
            <span class="made-badge">{{ t.made_india }}</span>
        </div>
        <div class="topbar-right">
            <div class="lang-dropdown" id="langDropdown">
                <button class="lang-toggle-btn" onclick="toggleLangMenu(event)" type="button">
                    <span class="lang-toggle-icon">🌐</span>
                    <span>{{ lang_label }}</span>
                    <span class="lang-caret">▾</span>
                </button>
                <div class="lang-popup" id="langPopup">
                    <a href="/?lang=en" class="lang-popup-item {% if lang == 'en' %}active{% endif %}">
                        English {% if lang == 'en' %}<span class="lang-popup-check">✓</span>{% endif %}
                    </a>
                    <a href="/?lang=te" class="lang-popup-item {% if lang == 'te' %}active{% endif %}">
                        తెలుగు {% if lang == 'te' %}<span class="lang-popup-check">✓</span>{% endif %}
                    </a>
                    <a href="/?lang=hi" class="lang-popup-item {% if lang == 'hi' %}active{% endif %}">
                        हिंदी {% if lang == 'hi' %}<span class="lang-popup-check">✓</span>{% endif %}
                    </a>
                </div>
            </div>
            <button class="theme-btn" onclick="toggleTheme()" id="themeBtn">🌙</button>
        </div>
    </div>

    <div class="content">

    {% if not result %}

    <!-- HERO -->
    <div class="hero">
        <div class="hero-text">
            <h1>
                {{ t.tagline_1 }}<br>
                <span class="line2">{{ t.tagline_2 }}</span><br>
                {{ t.tagline_3 }}
            </h1>
            <p>{{ t.subtitle }}</p>
            <div class="hero-badges">
                <div class="hero-badge"><span class="hero-badge-icon">✅</span> {{ t.free }}</div>
                <div class="hero-badge"><span class="hero-badge-icon">👤</span> {{ t.no_reg }}</div>
                <div class="hero-badge"><span class="hero-badge-icon">⚡</span> {{ t.instant }}</div>
            </div>
        </div>
        <div class="hero-shield">🛡️</div>
    </div>

    <form method="POST" action="/check?lang={{ lang }}" enctype="multipart/form-data" id="checkForm">

    <!-- FORM GRID: Upload + Right panel -->
    <div class="form-grid">

        <!-- LEFT COL: Image Upload + Why It Matters -->
        <div style="display:flex; flex-direction:column; gap:16px;">
            <div class="card">
                <div class="card-title">🖼️ {{ t.image_title }}</div>
                <div class="card-sub">{{ t.image_desc }}</div>
                <div class="upload-zone" onclick="document.getElementById('imgInput').click()">
                    <input type="file" id="imgInput" name="product_image" accept="image/*" onchange="previewImg(this)">
                    <div class="upload-icon">☁️</div>
                    <div class="upload-label-text">{{ t.image_label }}</div>
                    <div class="upload-hint">{{ t.image_hint }}</div>
                    <div id="preview-container">
                        <img id="preview-img" src="" alt="preview">
                        <div id="file-name"></div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">💡 {{ t.why_title }}</div>
                <div style="margin-top:8px;">
                    {% for item in t.why_items %}
                    <div class="insight-item"><div class="insight-dot"></div>{{ item }}</div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- RIGHT COL: How it works + Live score preview -->
        <div style="display:flex; flex-direction:column; gap:16px;">

            <div class="how-card" id="how-it-works">
                <div class="card-title">{{ t.how_works_title }}</div>
                <div style="margin-top:12px;">
                    <div class="step"><div class="step-num">1</div><div class="step-text">{{ t.step1 }}</div></div>
                    <div class="step"><div class="step-num">2</div><div class="step-text">{{ t.step2 }}</div></div>
                    <div class="step" style="margin-bottom:0;"><div class="step-num">3</div><div class="step-text">{{ t.step3 }}</div></div>
                </div>
            </div>

            <div class="risk-panel">
                <div class="risk-score-label">
                    📈 {{ t.trust_score }}
                    <span class="live-tag"><span class="live-dot"></span>{{ t.live_badge }}</span>
                </div>
                <div class="score-ring-wrap">
                    <div class="score-ring green" id="liveRing">
                        <div class="score-num green" id="liveScoreNum">0</div>
                        <div class="score-denom">/100</div>
                    </div>
                    <div class="verdict-pill green" id="liveVerdictPill">🟢 {{ t.low_risk }}</div>
                    <div class="verdict-sub" id="liveVerdictSub">{{ t.live_hint }}</div>
                </div>
                <div class="progress-row">
                    <span>{{ t.answered_label }}</span>
                    <span id="answeredCount">0/8</span>
                </div>
                <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
            </div>

            <div class="insights-card" id="safety-tips">
                <div class="card-title" style="margin-bottom:10px;">💡 {{ t.key_insights }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight1 }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight2 }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight3 }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight4 }}</div>
            </div>

        </div>
    </div>

    <!-- QUESTIONS (full width, after the grid) -->
    <div class="card" style="margin-bottom:20px;">
        <div class="card-title">🤖 {{ t.questions_title }}</div>
        <div class="card-sub">{{ t.questions_sub }}</div>
        <div class="questions-grid">
            {% for i in range(8) %}
            <div class="q-card">
                <div class="q-icon">{{ t.q_icons[i] }}</div>
                <div class="q-num">Q{{ i+1 }}</div>
                <div class="q-text">{{ t.questions[i] }}</div>
                <div class="q-options">
                    <label class="q-opt yes">
                        <input type="radio" name="q{{ i }}" value="yes" required>
                        ⚠️ {{ t.yes }}
                    </label>
                    <label class="q-opt no">
                        <input type="radio" name="q{{ i }}" value="no">
                        ✅ {{ t.no }}
                    </label>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- ANALYZE BUTTON (after questions) -->
    <button type="submit" class="analyze-card" style="margin-bottom:24px;">
        <div class="analyze-card-text">
            <h3>{{ t.analyze_btn }}</h3>
            <p>{{ t.analyze_sub }}</p>
        </div>
        <div class="analyze-arrow">→</div>
    </button>

    </form>

    {% else %}

    <!-- RESULT PAGE -->
    <div class="hero" style="margin-bottom:20px;">
        <div class="hero-text">
            <h1>
                {{ t.tagline_1 }}<br>
                <span class="line2">{{ t.tagline_2 }}</span><br>
                {{ t.tagline_3 }}
            </h1>
            <p>{{ t.subtitle }}</p>
        </div>
        <div class="hero-shield">🛡️</div>
    </div>

    <div class="result-grid">

        <!-- LEFT — Score + Guidance -->
        <div class="result-left">

            <div class="risk-panel">
                <div class="risk-score-label">📈 {{ t.trust_score }}</div>
                <div class="score-ring-wrap">
                    <div class="score-ring {{ color }}">
                        <div class="score-num {{ color }}">{{ score }}</div>
                        <div class="score-denom">/100</div>
                    </div>
                    <div class="verdict-pill {{ color }}">
                        {% if color == 'red' %}🔴{% elif color == 'orange' %}🟡{% else %}🟢{% endif %}
                        {{ verdict }}
                    </div>
                    <div class="verdict-sub">{{ verdict_sub }}</div>
                    <div class="powered-badge">🤖 {{ t.powered_by }}</div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">🛡️ {{ t.what_to_do }}</div>
                <div style="margin-top:12px;">
                    {% for g in guidance %}
                    <div class="guidance-item">
                        <span class="g-check">✅</span>
                        <span>{{ g }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

            {% if score >= 70 %}
            <a href="https://cybercrime.gov.in" target="_blank" class="btn-report">{{ t.report_btn }}</a>
            {% endif %}
            <a href="/?lang={{ lang }}" class="btn-another">{{ t.check_another }}</a>

        </div>

        <!-- RIGHT — Analysis -->
        <div class="result-right">

            {% if image_findings is not none %}
            <div class="card">
                <div class="card-title">🖼️ {{ t.image_analysis }}</div>
                <div style="margin-top:12px;">
                    {% if image_findings %}
                        {% for finding in image_findings %}
                        <div class="img-finding">
                            <span class="img-finding-icon">⚠️</span>
                            <span>{{ t.img_flags[finding] }}</span>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="img-safe">✅ {{ t.img_safe }}</div>
                    {% endif %}
                    <div class="img-finding-note">{{ t.img_note }}</div>
                </div>
            </div>
            {% endif %}

            <div class="card">
                <div class="card-title">
                    {% if flags %}⚠️ {{ t.red_flags }} ({{ flags|length }})
                    {% else %}✅ {{ t.no_flags }}{% endif %}
                </div>
                <div style="margin-top:12px;">
                    {% if flags %}
                        {% for flag in flags %}
                        <div class="flag-item">
                            <span class="flag-x">✕</span>
                            <span>{{ flag }}</span>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="flag-item">
                            <span class="flag-check">✓</span>
                            <span>{{ t.no_flags }}</span>
                        </div>
                    {% endif %}
                </div>
            </div>

            <div class="insights-card">
                <div class="card-title" style="margin-bottom:10px;">💡 {{ t.key_insights }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight1 }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight2 }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight3 }}</div>
                <div class="insight-item"><div class="insight-dot"></div>{{ t.insight4 }}</div>
            </div>

        </div>
    </div>

    {% endif %}

    <!-- ABOUT (always available, regardless of page) -->
    <div class="card about-card" id="about" style="margin-top:20px;">
        <div class="card-title">🛡️ {{ t.about }}</div>
        <p>{{ t.about_p1 }}</p>
        <p>{{ t.about_p2 }}</p>
        <div class="about-helpline">
            <span class="about-helpline-icon">📞</span>
            <span>{{ t.about_helpline }}</span>
        </div>
    </div>

    <div class="disclaimer">{{ t.disclaimer }}</div>

    </div>
</div>

<script>
function toggleTheme() {
    const html = document.documentElement;
    const btn = document.getElementById('themeBtn');
    const isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
    btn.textContent = isDark ? '🌙' : '☀️';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}
const saved = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', saved);
document.getElementById('themeBtn').textContent = saved === 'dark' ? '☀️' : '🌙';

function previewImg(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
            document.getElementById('preview-img').src = e.target.result;
            document.getElementById('preview-container').style.display = 'block';
            document.getElementById('file-name').textContent = '✅ ' + input.files[0].name;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('open');
}
function closeSidebar() {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('sidebarOverlay').classList.remove('open');
}

/* ── LANGUAGE POPUP ── */
function toggleLangMenu(e) {
    e.stopPropagation();
    document.getElementById('langDropdown').classList.toggle('open');
}
document.addEventListener('click', function (e) {
    const dd = document.getElementById('langDropdown');
    if (dd && !dd.contains(e.target)) dd.classList.remove('open');
});
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        const dd = document.getElementById('langDropdown');
        if (dd) dd.classList.remove('open');
    }
});

function scrollToId(id) {
    const el = document.getElementById(id);
    if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
}
// Sidebar anchor links: smooth-scroll if the section exists on this page,
// otherwise fall back to a normal navigation to the home page + hash.
function navAnchor(e, id) {
    closeSidebar();
    const el = document.getElementById(id);
    if (el) {
        e.preventDefault();
        scrollToId(id);
        return false;
    }
    return true;
}
window.addEventListener('DOMContentLoaded', function () {
    if (location.hash) {
        const id = location.hash.substring(1);
        setTimeout(function () { scrollToId(id); }, 150);
    }
});

/* ── LIVE TRUST SCORE PREVIEW ──
   Mirrors the server-side fallback scoring weights so the user gets an
   instant, evolving estimate while answering — final score (and the
   image analysis) is always calculated server-side by the AI model. */
const QUESTION_POINTS = [25, 20, 15, 15, 10, 10, 20, 25];
const LIVE_T = {
    high: {{ t.high_risk | tojson }},
    highSub: {{ t.high_risk_sub | tojson }},
    caution: {{ t.caution | tojson }},
    cautionSub: {{ t.caution_sub | tojson }},
    low: {{ t.low_risk | tojson }},
    lowSub: {{ t.low_risk_sub | tojson }},
    hint: {{ t.live_hint | tojson }}
};

function updateLiveScore() {
    const ring = document.getElementById('liveRing');
    if (!ring) return; // not on the form page

    const radios = document.querySelectorAll('#checkForm input[type=radio]:checked');
    let score = 0, answered = 0;
    radios.forEach(function (input) {
        answered++;
        if (input.value === 'yes') {
            const qIndex = parseInt(input.name.replace('q', ''), 10);
            score += QUESTION_POINTS[qIndex] || 0;
        }
    });
    score = Math.min(score, 100);

    let color, verdictText, verdictSub, emoji;
    if (score >= 70) { color = 'red'; verdictText = LIVE_T.high; verdictSub = LIVE_T.highSub; emoji = '🔴'; }
    else if (score >= 35) { color = 'orange'; verdictText = LIVE_T.caution; verdictSub = LIVE_T.cautionSub; emoji = '🟡'; }
    else { color = 'green'; verdictText = LIVE_T.low; verdictSub = LIVE_T.lowSub; emoji = '🟢'; }

    ['red', 'orange', 'green'].forEach(function (c) {
        ring.classList.remove(c);
        document.getElementById('liveScoreNum').classList.remove(c);
        document.getElementById('liveVerdictPill').classList.remove(c);
    });
    ring.classList.add(color);
    document.getElementById('liveScoreNum').classList.add(color);
    document.getElementById('liveVerdictPill').classList.add(color);

    document.getElementById('liveScoreNum').textContent = score;
    document.getElementById('liveVerdictPill').textContent = emoji + ' ' + verdictText;
    document.getElementById('liveVerdictSub').textContent = answered === 0 ? LIVE_T.hint : verdictSub;
    document.getElementById('answeredCount').textContent = answered + '/8';
    document.getElementById('progressFill').style.width = (answered / 8 * 100) + '%';
}
document.querySelectorAll('#checkForm input[type=radio]').forEach(function (input) {
    input.addEventListener('change', updateLiveScore);
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    lang = request.args.get('lang', 'en')
    if lang not in TRANSLATIONS:
        lang = 'en'
    t = TRANSLATIONS[lang]
    return render_template_string(HTML, result=False, t=t, lang=lang, lang_label=LANG_LABELS[lang])

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

    image_findings = None
    if 'product_image' in request.files:
        file = request.files['product_image']
        if file and file.filename != '':
            image_findings, img_score = analyse_image(file)
            score = min(score + img_score, 100)

    verdict, verdict_sub, color = get_verdict(score, t)
    flags = [t['flags'][i] for i in flag_indices]
    guidance = get_guidance(score, answers, t)

    return render_template_string(HTML,
        result=True, score=score, flags=flags,
        verdict=verdict, verdict_sub=verdict_sub,
        color=color, guidance=guidance,
        image_findings=image_findings,
        t=t, lang=lang, lang_label=LANG_LABELS[lang]
    )

if __name__ == "__main__":
    app.run()
