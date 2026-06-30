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
        'title': 'SecureDeal — AI Scam Protection',
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
        'username_title': 'Instagram Username (Optional)',
        'username_desc': 'Enter the seller\'s Instagram username. We\'ll guide you on what to check on their page.',
        'username_placeholder': '@seller_username',
        'username_checklist_title': 'What to check on @{username}\'s page',
        'username_checklist': [
            'Check when their oldest post was uploaded — is the account very new?',
            'Count their posts — did they post 50+ photos in just a few days?',
            'Read the comments — are they real or generic like "Nice!" and "DM me"?',
            'Check if any real customers have tagged them in posts',
            'Look at their bio — is there any address, website or contact info?',
            'Search their phone number on Truecaller before paying',
        ],
        'questions_title': 'Answer 8 Simple Questions',
        'questions_sub': "Help our AI understand the seller's behaviour",
        'analyze_btn': 'Analyze Seller',
        'analyze_sub': 'AI will check and give risk score in seconds',
        'trust_score': 'Risk Score',
        'powered_by': 'Powered by SecureDeal AI Model',
        'image_analysis': 'Image Analysis',
        'red_flags': 'Red Flags Detected',
        'what_to_do': 'What You Should Do',
        'report_btn': '⚠️ Report This Scam at cybercrime.gov.in',
        'check_another': '🔍 Check Another Seller',
        'no_flags': 'No major red flags detected',
        'how_works_title': 'How it works',
        'step1': 'Enter username and answer 8 questions',
        'step2': 'Our AI analyzes the risk',
        'step3': 'Get your risk score instantly',
        'key_insights': 'Key Insights',
        'insight1': 'Always verify the seller',
        'insight2': 'Avoid full payment in advance',
        'insight3': 'Trust your instincts',
        'insight4': 'Use safe payment methods',
        'disclaimer': 'SecureDeal provides risk assessment based on user-provided behaviour patterns. This is not a definitive accusation. Always use your own judgement.',
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
        'about_p1': 'SecureDeal is a free, independent safety tool built to help everyday online shoppers spot fake sellers before they pay — especially on Instagram, where most India-based shopping scams now happen.',
        'about_p2': "We're not affiliated with Instagram, Meta, or any government body. Our AI model looks for common behaviour patterns reported by real scam victims, but it is a guide — not a guarantee. Always trust your own judgement and verify before you pay.",
        'about_helpline': "If you've already been scammed, call India's National Cyber Crime Helpline at 1930 (24x7) or report it at cybercrime.gov.in",
        'analysed_seller': 'Seller Analysed',
        'questions': [
            'Did the seller REFUSE a video call showing the actual product?',
            'Did they ask for FULL PAYMENT before showing any proof the product is real?',
            "Did they REFUSE to write today's date on paper next to the product in a photo?",
            'Are they pressuring you with urgency — "today only", "last piece", "offer ends soon"?',
            'Is their Instagram account LESS THAN A FEW MONTHS old with very few real followers or comments?',
            'Are their prices SIGNIFICANTLY LOWER than every other seller for the same product?',
            "Did the seller's payment QR code or link HIDE who was actually receiving the money?",
            'Is the SAME PRODUCT PHOTO being sold by multiple different Instagram pages at different prices?',
        ],
        'q_icons': ['🎥', '💳', '📸', '⚡', '📅', '💰', '🔍', '🖼️'],
        'flags': [
            'Seller refused video call — genuine sellers always agree to show product live',
            'Demanded payment WITHOUT showing any proof first — primary scam mechanism',
            'Refused date proof photo — suggests product does not exist',
            'Used urgency tactics — designed to stop you from thinking carefully',
            'Account is very new with few real followers — scammers need to act fast and disappear',
            'Prices significantly lower than other sellers — used as bait to attract buyers',
            'Payment QR/link hid the recipient identity — makes the seller untraceable',
            'Same photo found across multiple pages at different prices — likely a stolen/recycled listing',
        ],
        'guidance_high': [
            'Do NOT send any money',
            'Ask for verifiable proof before reconsidering — live video call, dated photo',
            'Block and report this account on Instagram',
            'Report at cybercrime.gov.in if you already paid',
            'Take screenshots of all chats as evidence',
            'Warn your friends and family about this page',
        ],
        'guidance_medium': [
            'Ask seller for a video call showing product RIGHT NOW',
            "Ask seller to photograph product with TODAY'S DATE on paper",
            'Do NOT pay full amount before seeing product',
            'Verify the payment recipient name before paying',
            'Save all chat screenshots before paying',
        ],
        'guidance_low': [
            'Proceed carefully — always verify before final payment',
            'Prefer partial payment first if possible',
            'Save all chat screenshots before paying',
            'Trust your instincts — if something feels wrong it probably is',
        ],
        'img_analysis_title': 'Image Analysis Results',
        'img_flags': {
            'screenshot': '⚠️ Image appears to be a screenshot — original product photos are rarely screenshots',
            'low_quality': '⚠️ Image quality is very low — may be a compressed stolen image',
            'extreme_ratio': '⚠️ Image has unusual dimensions — may be cropped from another listing',
            'very_small': '⚠️ Image resolution is very small — suggests it was downloaded from the internet',
            'flat_colors': '⚠️ Image has very flat or uniform colours — may be digitally generated or heavily edited',
        },
        'img_safe': '✅ No suspicious image patterns detected — image appears to be an original photo',
        'img_note': 'Note: These checks are experimental and can be wrong — e.g. a plain background may trigger a false flag. Treat this as a hint, not proof. Always ask the seller to show the product on a live video call.',
        'img_consistent': '✅ Image appears consistent across devices',
    },
    'te': {
        'title': 'SecureDeal — AI స్కామ్ రక్షణ',
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
        'username_title': 'Instagram యూజర్‌నేమ్ (ఐచ్ఛికం)',
        'username_desc': 'విక్రేత Instagram యూజర్‌నేమ్ నమోదు చేయండి. వారి పేజీలో ఏమి తనిఖీ చేయాలో మేము మీకు మార్గదర్శనం చేస్తాము.',
        'username_placeholder': '@seller_username',
        'username_checklist_title': '@{username} పేజీలో తనిఖీ చేయవలసినవి',
        'username_checklist': [
            'వారి పాత పోస్ట్ ఎప్పుడు అప్‌లోడ్ అయిందో తనిఖీ చేయండి — అకౌంట్ చాలా కొత్తదా?',
            'వారి పోస్ట్‌లు లెక్కించండి — కొన్ని రోజుల్లో 50+ ఫోటోలు పోస్ట్ చేశారా?',
            'కామెంట్లు చదవండి — నిజమైనవా లేదా "Nice!" మరియు "DM me" వంటివా?',
            'నిజమైన కస్టమర్లు వారిని పోస్ట్‌లలో ట్యాగ్ చేశారా తనిఖీ చేయండి',
            'వారి బయోలో చిరునామా, వెబ్‌సైట్ లేదా సంప్రదింపు సమాచారం ఉందా?',
            'చెల్లించే ముందు Truecaller లో వారి ఫోన్ నంబర్ వెతకండి',
        ],
        'questions_title': '8 సాధారణ ప్రశ్నలకు సమాధానం ఇవ్వండి',
        'questions_sub': 'విక్రేత ప్రవర్తనను అర్థం చేసుకోవడానికి సహాయం చేయండి',
        'analyze_btn': 'విక్రేతను విశ్లేషించండి',
        'analyze_sub': 'AI తనిఖీ చేసి సెకన్లలో రిస్క్ స్కోర్ ఇస్తుంది',
        'trust_score': 'రిస్క్ స్కోర్',
        'powered_by': 'SecureDeal AI మోడల్ ద్వారా',
        'image_analysis': 'చిత్ర విశ్లేషణ',
        'red_flags': 'గుర్తించిన హెచ్చరికలు',
        'what_to_do': 'మీరు ఏమి చేయాలి',
        'report_btn': '⚠️ cybercrime.gov.in లో రిపోర్ట్ చేయండి',
        'check_another': '🔍 మరొక విక్రేతను తనిఖీ చేయండి',
        'no_flags': 'పెద్ద హెచ్చరికలు ఏమీ లేవు',
        'how_works_title': 'ఎలా పని చేస్తుంది',
        'step1': 'యూజర్‌నేమ్ నమోదు చేసి 8 ప్రశ్నలకు సమాధానం ఇవ్వండి',
        'step2': 'మా AI రిస్క్ విశ్లేషిస్తుంది',
        'step3': 'వెంటనే రిస్క్ స్కోర్ పొందండి',
        'key_insights': 'ముఖ్య సూచనలు',
        'insight1': 'ఎల్లప్పుడూ విక్రేతను ధృవీకరించండి',
        'insight2': 'ముందుగా పూర్తి చెల్లింపు నివారించండి',
        'insight3': 'మీ అంతర్మనస్సును నమ్మండి',
        'insight4': 'సురక్షిత చెల్లింపు పద్ధతులు వాడండి',
        'disclaimer': 'SecureDeal వినియోగదారు నివేదించిన సంకేతాల ఆధారంగా రిస్క్ అంచనా అందిస్తుంది. ఇది నిర్ధారిత అభియోగం కాదు.',
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
        'about_p1': 'SecureDeal అనేది ఆన్‌లైన్ కొనుగోలుదారులు చెల్లించే ముందు నకిలీ విక్రేతలను గుర్తించడంలో సహాయపడే ఉచిత భద్రతా టూల్.',
        'about_p2': 'మేము Instagram లేదా Meta తో సంబంధం లేదు. మా AI మోడల్ ఒక గైడ్ మాత్రమే — హామీ కాదు.',
        'about_helpline': 'మీరు మోసపోయినట్లయితే, 1930 (24x7) కు కాల్ చేయండి లేదా cybercrime.gov.in లో రిపోర్ట్ చేయండి',
        'analysed_seller': 'విశ్లేషించిన విక్రేత',
        'questions': [
            'విక్రేత ఉత్పత్తిని చూపించే వీడియో కాల్‌ను తిరస్కరించారా?',
            'ఉత్పత్తి నిజమైనదని ఎలాంటి రుజువు చూపకుండానే పూర్తి చెల్లింపు అడిగారా?',
            'నేటి తేదీ కాగితంతో ఫోటో తీయడానికి నిరాకరించారా?',
            '"ఈరోజు మాత్రమే", "చివరి వస్తువు" వంటి అత్యవసరత చూపించారా?',
            'వారి Instagram ఖాతా కొన్ని నెలల కంటే తక్కువ పాతదా, నిజమైన ఫాలోయర్లు తక్కువగా ఉన్నారా?',
            'ఇతర విక్రేతల కంటే వారి ధరలు గణనీయంగా తక్కువగా ఉన్నాయా?',
            'విక్రేత చెల్లింపు QR కోడ్ లేదా లింక్ డబ్బు అందుకునే వారి పేరును దాచిందా?',
            'అదే ఉత్పత్తి ఫోటో వేర్వేరు Instagram పేజీలలో వేర్వేరు ధరలకు అమ్ముడవుతోందా?',
        ],
        'q_icons': ['🎥', '💳', '📸', '⚡', '📅', '💰', '🔍', '🖼️'],
        'flags': [
            'వీడియో కాల్ తిరస్కరించారు — నిజమైన విక్రేతలు ఎప్పుడూ అంగీకరిస్తారు',
            'ఎలాంటి రుజువు చూపకుండానే చెల్లింపు అడిగారు — ప్రధాన మోసం పద్ధతి',
            'నేటి తేదీతో ఫోటో తీయడానికి నిరాకరించారు',
            'అత్యవసరత వ్యూహాలు ఉపయోగించారు',
            'ఖాతా చాలా కొత్తది, నిజమైన ఫాలోయర్లు తక్కువ — స్కామర్లు వేగంగా వెళ్ళిపోవాలి',
            'ఇతర విక్రేతల కంటే ధరలు గణనీయంగా తక్కువ — ఆకర్షించడానికి ఎరగా వాడతారు',
            'చెల్లింపు QR/లింక్ గ్రహీత గుర్తింపును దాచింది — విక్రేతను గుర్తించలేకుండా చేస్తుంది',
            'అదే ఫోటో వేర్వేరు పేజీలలో వేర్వేరు ధరలకు కనిపించింది — దొంగిలించిన లిస్టింగ్ కావచ్చు',
        ],
        'guidance_high': [
            'డబ్బు పంపకండి',
            'పునరాలోచించే ముందు ధృవీకరించదగిన రుజువు అడగండి — లైవ్ వీడియో కాల్, తేదీతో ఫోటో',
            'Instagram లో బ్లాక్ చేసి రిపోర్ట్ చేయండి',
            'cybercrime.gov.in లో రిపోర్ట్ చేయండి',
            'అన్ని చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'స్నేహితులకు హెచ్చరించండి',
        ],
        'guidance_medium': [
            'వీడియో కాల్ అడగండి',
            'నేటి తేదీతో ఫోటో అడగండి',
            'పూర్తి మొత్తం చెల్లించకండి',
            'చెల్లించే ముందు గ్రహీత పేరు ధృవీకరించండి',
            'చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
        ],
        'guidance_low': [
            'జాగ్రత్తగా ముందుకు వెళ్ళండి',
            'పాక్షిక చెల్లింపు చేయండి',
            'స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'అంతర్మనస్సును నమ్మండి',
        ],
        'img_analysis_title': 'చిత్ర విశ్లేషణ ఫలితాలు',
        'img_flags': {
            'screenshot': '⚠️ చిత్రం స్క్రీన్‌షాట్ గా కనిపిస్తోంది — అసలు ఉత్పత్తి ఫోటోలు అరుదుగా స్క్రీన్‌షాట్‌లు అవుతాయి',
            'low_quality': '⚠️ చిత్రం నాణ్యత చాలా తక్కువ — కంప్రెస్ చేసిన దొంగిలించిన చిత్రం కావచ్చు',
            'extreme_ratio': '⚠️ చిత్రం అసాధారణ కొలతలు కలిగి ఉంది — మరొక లిస్టింగ్ నుండి క్రాప్ చేయబడి ఉండవచ్చు',
            'very_small': '⚠️ చిత్రం రిజల్యూషన్ చాలా చిన్నది — ఇంటర్నెట్ నుండి డౌన్‌లోడ్ చేయబడిందని సూచిస్తుంది',
            'flat_colors': '⚠️ చిత్రంలో చాలా సమతుల్య రంగులు ఉన్నాయి — డిజిటల్ గా రూపొందించబడి ఉండవచ్చు',
        },
        'img_safe': '✅ అనుమానాస్పద చిత్ర నమూనాలు గుర్తించబడలేదు — చిత్రం అసలైన ఫోటో గా కనిపిస్తోంది',
        'img_note': 'గమనిక: ఈ తనిఖీలు ప్రయోగాత్మకమైనవి మరియు తప్పుగా ఉండవచ్చు — ఉదాహరణకు సాదా బ్యాక్‌గ్రౌండ్ తప్పుడు హెచ్చరికను ప్రేరేపించవచ్చు. దీన్ని ఆధారంగా కాకుండా సూచనగా మాత్రమే పరిగణించండి.',
        'img_consistent': '✅ చిత్రం అన్ని పరికరాలలో సమానంగా కనిపిస్తోంది',
    },
    'hi': {
        'title': 'SecureDeal — AI स्कैम सुरक्षा',
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
        'username_title': 'Instagram यूज़रनेम (वैकल्पिक)',
        'username_desc': 'विक्रेता का Instagram यूज़रनेम दर्ज करें। हम आपको उनके पेज पर क्या जांचना है इसका मार्गदर्शन करेंगे।',
        'username_placeholder': '@seller_username',
        'username_checklist_title': '@{username} के पेज पर क्या जांचें',
        'username_checklist': [
            'उनकी सबसे पुरानी पोस्ट कब अपलोड हुई — क्या अकाउंट बहुत नया है?',
            'उनकी पोस्ट गिनें — क्या उन्होंने कुछ दिनों में 50+ फोटो पोस्ट किए?',
            'टिप्पणियां पढ़ें — क्या वे असली हैं या "Nice!" और "DM me" जैसी?',
            'जांचें कि क्या असली ग्राहकों ने उन्हें पोस्ट में टैग किया है',
            'उनके बायो में पता, वेबसाइट या संपर्क जानकारी है?',
            'भुगतान से पहले Truecaller पर उनका फोन नंबर खोजें',
        ],
        'questions_title': '8 सरल प्रश्नों का उत्तर दें',
        'questions_sub': 'हमारे AI को विक्रेता के व्यवहार को समझने में मदद करें',
        'analyze_btn': 'विक्रेता का विश्लेषण करें',
        'analyze_sub': 'AI जांच करेगा और सेकंडों में जोखिम स्कोर देगा',
        'trust_score': 'जोखिम स्कोर',
        'powered_by': 'SecureDeal AI मॉडल द्वारा संचालित',
        'image_analysis': 'छवि विश्लेषण',
        'red_flags': 'पहचाने गए खतरे',
        'what_to_do': 'आपको क्या करना चाहिए',
        'report_btn': '⚠️ cybercrime.gov.in पर रिपोर्ट करें',
        'check_another': '🔍 दूसरे विक्रेता की जांच करें',
        'no_flags': 'कोई बड़ा खतरा नहीं',
        'how_works_title': 'कैसे काम करता है',
        'step1': 'यूज़रनेम दर्ज करें और 8 प्रश्नों का उत्तर दें',
        'step2': 'हमारा AI जोखिम का विश्लेषण करता है',
        'step3': 'तुरंत जोखिम स्कोर पाएं',
        'key_insights': 'मुख्य सुझाव',
        'insight1': 'हमेशा विक्रेता को सत्यापित करें',
        'insight2': 'पहले पूरा भुगतान करने से बचें',
        'insight3': 'अपनी अंतरात्मा पर भरोसा करें',
        'insight4': 'सुरक्षित भुगतान विधियां उपयोग करें',
        'disclaimer': 'SecureDeal उपयोगकर्ता द्वारा प्रदान किए गए व्यवहार संकेतों के आधार पर जोखिम मूल्यांकन प्रदान करता है।',
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
            'स्कैमर अक्सर उन खरीदारों को निशाना बनाते हैं जो जल्दी में हों।',
            'ज्यादातर स्कैम में उत्पाद असली होने का सबूत दिए बिना पूरा भुगतान मांगा जाता है।',
            'कुछ सेकंड की जांच आपके पैसे बचा सकती है।',
        ],
        'live_badge': 'लाइव',
        'live_hint': 'जैसे ही आप प्रश्नों के उत्तर देंगे, यह तुरंत अपडेट होगा',
        'answered_label': 'उत्तर दिए गए प्रश्न',
        'about_p1': 'SecureDeal एक मुफ्त सुरक्षा टूल है जो ऑनलाइन खरीदारों को नकली विक्रेताओं को पहचानने में मदद करता है।',
        'about_p2': 'हम Instagram या Meta से संबद्ध नहीं हैं। हमारा AI एक गाइड है — गारंटी नहीं।',
        'about_helpline': 'यदि धोखाधड़ी हुई है तो 1930 (24x7) पर कॉल करें या cybercrime.gov.in पर रिपोर्ट करें',
        'analysed_seller': 'विश्लेषित विक्रेता',
        'questions': [
            'क्या विक्रेता ने उत्पाद दिखाने वाली वीडियो कॉल से मना किया?',
            'क्या उन्होंने उत्पाद असली होने का कोई सबूत दिखाए बिना पूरा भुगतान मांगा?',
            'क्या उन्होंने आज की तारीख वाली फोटो लेने से मना किया?',
            'क्या उन्होंने "आज का ऑफर", "आखिरी सामान" जैसी जल्दबाजी दिखाई?',
            'क्या उनका Instagram अकाउंट कुछ महीनों से कम पुराना है और असली फॉलोअर्स बहुत कम हैं?',
            'क्या उनकी कीमतें अन्य विक्रेताओं की तुलना में काफी कम हैं?',
            'क्या विक्रेता के भुगतान QR कोड या लिंक ने पैसे पाने वाले का नाम छुपाया?',
            'क्या वही उत्पाद फोटो अलग-अलग Instagram पेजों पर अलग-अलग कीमतों पर बिक रहा है?',
        ],
        'q_icons': ['🎥', '💳', '📸', '⚡', '📅', '💰', '🔍', '🖼️'],
        'flags': [
            'वीडियो कॉल से मना किया — असली विक्रेता हमेशा तैयार रहते हैं',
            'कोई सबूत दिखाए बिना भुगतान मांगा — मुख्य धोखाधड़ी तरीका',
            'आज की तारीख वाली फोटो से मना किया',
            'जल्दबाजी की रणनीति इस्तेमाल की',
            'अकाउंट बहुत नया है, असली फॉलोअर्स कम — धोखेबाज जल्दी भागना चाहते हैं',
            'अन्य विक्रेताओं की तुलना में कीमतें काफी कम — फंसाने के लिए चारा',
            'भुगतान QR/लिंक ने प्राप्तकर्ता की पहचान छुपाई — विक्रेता को ट्रेस करना मुश्किल',
            'वही फोटो अलग-अलग पेजों पर अलग कीमतों पर मिली — चोरी की गई लिस्टिंग हो सकती है',
        ],
        'guidance_high': [
            'पैसे न भेजें',
            'दोबारा विचार करने से पहले सत्यापन योग्य सबूत मांगें — लाइव वीडियो कॉल, तारीख वाली फोटो',
            'Instagram पर ब्लॉक करें और रिपोर्ट करें',
            'cybercrime.gov.in पर रिपोर्ट करें',
            'सभी चैट स्क्रीनशॉट सेव करें',
            'दोस्तों और परिवार को चेतावनी दें',
        ],
        'guidance_medium': [
            'वीडियो कॉल मांगें',
            'आज की तारीख वाली फोटो मांगें',
            'पूरा भुगतान न करें',
            'भुगतान से पहले प्राप्तकर्ता का नाम सत्यापित करें',
            'चैट स्क्रीनशॉट सेव करें',
        ],
        'guidance_low': [
            'सावधानी से आगे बढ़ें',
            'पहले आंशिक भुगतान करें',
            'स्क्रीनशॉट सेव करें',
            'अंतरात्मा पर भरोसा करें',
        ],
        'img_analysis_title': 'छवि विश्लेषण परिणाम',
        'img_flags': {
            'screenshot': '⚠️ छवि स्क्रीनशॉट लगती है — असली उत्पाद फोटो शायद ही कभी स्क्रीनशॉट होती हैं',
            'low_quality': '⚠️ छवि की गुणवत्ता बहुत कम है — चोरी की गई संपीड़ित छवि हो सकती है',
            'extreme_ratio': '⚠️ छवि का आकार असामान्य है — किसी अन्य लिस्टिंग से क्रॉप की गई हो सकती है',
            'very_small': '⚠️ छवि रिज़ॉल्यूशन बहुत छोटा है — इंटरनेट से डाउनलोड की गई हो सकती है',
            'flat_colors': '⚠️ छवि में बहुत सपाट रंग हैं — डिजिटल रूप से बनाई गई हो सकती है',
        },
        'img_safe': '✅ कोई संदिग्ध छवि पैटर्न नहीं मिला — छवि मूल फोटो प्रतीत होती है',
        'img_note': 'नोट: ये जांच प्रयोगात्मक हैं और गलत हो सकती हैं — जैसे एक सादा बैकग्राउंड गलत चेतावनी दे सकता है। इसे प्रमाण नहीं, केवल एक संकेत मानें।',
        'img_consistent': '✅ छवि सभी उपकरणों पर समान दिखती है',
    }
}


# ─── Image Analysis ───
def analyse_image(file):
    findings = []
    score_addition = 0
    try:
        file.seek(0)
        img = Image.open(file)
        img.load()
        width, height = img.size
        total_pixels = width * height

        if width < 150 or height < 150:
            findings.append('very_small')
            score_addition += 10

        ratio = width / height if height > 0 else 1
        if ratio > 2.8 or ratio < 0.36:
            findings.append('extreme_ratio')
            score_addition += 8

        if total_pixels < 40000:
            if 'very_small' not in findings:
                findings.append('low_quality')
                score_addition += 7

        if img.mode in ('RGB', 'RGBA') and total_pixels > 1000:
            try:
                rgb_img = img.convert('RGB') if img.mode == 'RGBA' else img
                sample_size = min(100, width, height)
                small = rgb_img.resize((sample_size, sample_size), Image.LANCZOS)
                pixels = list(small.getdata())
                r_vals = [p[0] for p in pixels]
                g_vals = [p[1] for p in pixels]
                b_vals = [p[2] for p in pixels]

                def variance(vals):
                    mean = sum(vals) / len(vals)
                    return sum((v - mean) ** 2 for v in vals) / len(vals)

                avg_variance = (variance(r_vals) + variance(g_vals) + variance(b_vals)) / 3

                if avg_variance < 200:
                    findings.append('flat_colors')
                    score_addition += 8

                top_row = [rgb_img.getpixel((x, 0)) for x in range(0, width, max(1, width // 20))]
                bottom_row = [rgb_img.getpixel((x, height - 1)) for x in range(0, width, max(1, width // 20))]

                def row_brightness(row):
                    return sum(sum(p) / 3 for p in row) / len(row)

                if row_brightness(top_row) > 220 and row_brightness(bottom_row) > 220 and avg_variance > 500:
                    findings.append('screenshot')
                    score_addition += 6

            except Exception as pixel_err:
                print(f"Pixel analysis error: {pixel_err}")

    except Exception as e:
        print(f"Image analysis error: {e}")

    return findings, score_addition


def calculate_risk_score(answers):
    flag_indices = []
    checks = [
        'refused_video_call', 'payment_before_proof', 'refused_date_photo',
        'urgency_tactics', 'account_very_new', 'price_significantly_lower',
        'hidden_payment_recipient', 'photo_reused_elsewhere',
    ]
    for i, key in enumerate(checks):
        if answers.get(key):
            flag_indices.append(i)
    if model is not None:
        try:
            input_data = pd.DataFrame([{
                'refused_video_call': int(answers.get('refused_video_call', False)),
                'payment_before_product': int(answers.get('payment_before_proof', False)),
                'refused_date_photo': int(answers.get('refused_date_photo', False)),
                'urgency_tactics': int(answers.get('urgency_tactics', False)),
                'page_very_new': int(answers.get('account_very_new', False)),
                'unrealistic_price': int(answers.get('price_significantly_lower', False)),
                'blocked_after_payment': int(answers.get('hidden_payment_recipient', False)),
                'extra_charges_after_payment': int(answers.get('photo_reused_elsewhere', False)),
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
        return list(t['guidance_high'])
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
    --bg: #0d0d1a; --sidebar: #090912; --surface: #13132a;
    --surface2: #1a1a35; --surface3: #20203f; --border: #2a2a50;
    --text: #ffffff; --text2: #9090b8; --text3: #606090;
    --accent: #7c5cfc; --accent2: #9b7cff;
    --red: #ff4757; --orange: #ffa502; --green: #2ed573;
    --card-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
:root[data-theme="light"] {
    --bg: #f0f2ff; --sidebar: #ffffff; --surface: #ffffff;
    --surface2: #f5f5ff; --surface3: #ebebff; --border: #e0e0f0;
    --text: #1a1a35; --text2: #505080; --text3: #9090b8;
    --accent: #7c5cfc; --accent2: #6040e0;
    --red: #e0313e; --orange: #e07800; --green: #1a9e48;
    --card-shadow: 0 4px 24px rgba(100,100,200,0.1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',system-ui,sans-serif; background:var(--bg); color:var(--text); min-height:100vh; display:flex; }
.sidebar { width:220px; min-height:100vh; background:var(--sidebar); border-right:1px solid var(--border); display:flex; flex-direction:column; padding:24px 16px; position:fixed; top:0; left:0; bottom:0; z-index:100; transition:transform 0.3s; }
.sidebar-logo { display:flex; align-items:center; gap:10px; margin-bottom:32px; padding:0 8px; }
.sidebar-logo-icon { width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,var(--accent),var(--accent2)); display:flex; align-items:center; justify-content:center; font-size:18px; }
.sidebar-logo-text { font-size:18px; font-weight:800; color:var(--text); }
.sidebar-logo-text span { color:var(--accent); }
.sidebar-sub { font-size:10px; color:var(--text2); margin-top:1px; }
.nav-section { font-size:10px; font-weight:700; color:var(--text3); text-transform:uppercase; letter-spacing:1.2px; padding:0 12px; margin:16px 0 6px; }
.nav-item { display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:10px; color:var(--text2); font-size:13px; font-weight:500; text-decoration:none; margin-bottom:4px; cursor:pointer; border:none; background:none; width:100%; transition:all 0.2s; }
.nav-item:hover { background:var(--surface2); color:var(--text); }
.nav-item.active { background:linear-gradient(135deg,rgba(124,92,252,0.2),rgba(124,92,252,0.1)); color:var(--accent); font-weight:600; }
.nav-icon { font-size:16px; width:20px; text-align:center; }
.nav-badge { margin-left:auto; font-size:10px; background:var(--accent); color:white; padding:2px 7px; border-radius:20px; }
.sidebar-footer { margin-top:auto; padding:16px 12px; background:linear-gradient(135deg,rgba(124,92,252,0.15),rgba(124,92,252,0.05)); border-radius:12px; border:1px solid rgba(124,92,252,0.2); }
.sidebar-footer p { font-size:13px; font-weight:700; color:var(--text); margin-bottom:4px; }
.sidebar-footer span { font-size:11px; color:var(--text2); }
.sidebar-made { font-size:11px; color:var(--text2); text-align:center; margin-top:12px; }
.main { margin-left:220px; flex:1; min-height:100vh; display:flex; flex-direction:column; }
.topbar { height:56px; background:var(--surface); border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; padding:0 24px; position:sticky; top:0; z-index:50; }
.made-badge { font-size:12px; color:var(--text2); background:var(--surface2); padding:4px 10px; border-radius:20px; border:1px solid var(--border); }
.topbar-right { display:flex; align-items:center; gap:8px; }
.lang-dropdown { position:relative; }
.lang-toggle-btn { display:flex; align-items:center; gap:6px; padding:6px 12px; border-radius:8px; border:1px solid var(--border); background:var(--surface2); color:var(--text); font-size:12px; font-weight:700; cursor:pointer; }
.lang-toggle-btn:hover { border-color:var(--accent); }
.lang-caret { font-size:9px; color:var(--text2); transition:transform 0.2s; }
.lang-dropdown.open .lang-caret { transform:rotate(180deg); }
.lang-popup { position:absolute; top:calc(100% + 8px); right:0; background:var(--surface); border:1px solid var(--border); border-radius:12px; box-shadow:var(--card-shadow); padding:6px; min-width:160px; z-index:200; display:none; flex-direction:column; gap:2px; }
.lang-dropdown.open .lang-popup { display:flex; }
.lang-popup-item { display:flex; align-items:center; justify-content:space-between; padding:9px 12px; border-radius:8px; font-size:13px; font-weight:600; text-decoration:none; color:var(--text2); transition:all 0.15s; }
.lang-popup-item:hover { background:var(--surface2); color:var(--text); }
.lang-popup-item.active { background:rgba(124,92,252,0.15); color:var(--accent); }
.lang-popup-check { font-size:12px; color:var(--accent); }
.theme-btn { width:32px; height:32px; border-radius:8px; border:1px solid var(--border); background:var(--surface2); cursor:pointer; font-size:14px; display:flex; align-items:center; justify-content:center; }
.hamburger { display:none; width:36px; height:36px; border-radius:8px; background:var(--surface2); border:1px solid var(--border); cursor:pointer; align-items:center; justify-content:center; font-size:18px; }
.sidebar-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:99; }
.content { padding:24px; flex:1; max-width:1300px; margin:0 auto; width:100%; }
.hero { display:flex; align-items:center; justify-content:space-between; margin-bottom:28px; }
.hero-text h1 { font-size:40px; font-weight:900; line-height:1.15; margin-bottom:12px; }
.hero-text h1 .line2 { color:var(--accent); }
.hero-text p { color:var(--text2); font-size:14px; max-width:380px; margin-bottom:20px; }
.hero-badges { display:flex; gap:12px; flex-wrap:wrap; }
.hero-badge { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--text2); }
.hero-shield { font-size:120px; filter:drop-shadow(0 0 40px rgba(124,92,252,0.4)); }
.card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; box-shadow:var(--card-shadow); }
.card-title { font-size:13px; font-weight:700; color:var(--text); margin-bottom:6px; display:flex; align-items:center; gap:8px; }
.card-sub { font-size:12px; color:var(--text2); margin-bottom:16px; }
.username-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; box-shadow:var(--card-shadow); }
.username-input-wrap { display:flex; align-items:center; gap:10px; margin-bottom:12px; }
.username-input { flex:1; padding:10px 14px; border-radius:10px; border:1.5px solid var(--border); background:var(--surface2); color:var(--text); font-size:14px; font-weight:600; outline:none; transition:border-color 0.2s; }
.username-input:focus { border-color:var(--accent); }
.username-input::placeholder { color:var(--text3); font-weight:400; }
.username-checklist { display:none; margin-top:12px; padding:14px; background:var(--surface2); border-radius:10px; border:1px solid var(--border); }
.username-checklist.visible { display:block; }
.username-checklist-title { font-size:12px; font-weight:700; color:var(--accent); margin-bottom:10px; }
.username-checklist-item { display:flex; align-items:flex-start; gap:8px; padding:6px 0; font-size:12px; color:var(--text2); line-height:1.5; border-bottom:1px solid var(--border); }
.username-checklist-item:last-child { border-bottom:none; }
.username-checklist-num { width:18px; height:18px; border-radius:50%; background:var(--accent); color:white; font-size:9px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.username-note { font-size:10px; color:var(--text3); font-style:italic; margin-top:10px; padding-top:10px; border-top:1px solid var(--border); }
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; align-items:start; }
.upload-zone { border:2px dashed var(--border); border-radius:12px; padding:28px 20px; text-align:center; cursor:pointer; transition:border-color 0.2s; }
.upload-zone:hover { border-color:var(--accent); }
.upload-zone input { display:none; }
.upload-icon { font-size:32px; margin-bottom:10px; color:var(--text2); }
.upload-label-text { font-size:13px; color:var(--text2); margin-bottom:4px; }
.upload-hint { font-size:11px; color:var(--text3); }
#preview-container { margin-top:12px; display:none; }
#preview-container img { max-width:120px; max-height:120px; border-radius:8px; border:1px solid var(--border); }
#file-name { font-size:11px; color:var(--green); margin-top:4px; }
.analyze-card { background:linear-gradient(135deg,var(--accent),var(--accent2)); border-radius:16px; padding:20px; display:flex; align-items:center; justify-content:space-between; cursor:pointer; border:none; width:100%; box-shadow:0 8px 32px rgba(124,92,252,0.35); transition:transform 0.2s, box-shadow 0.2s; }
.analyze-card:hover { transform:translateY(-2px); box-shadow:0 12px 40px rgba(124,92,252,0.45); }
.analyze-card-text h3 { font-size:18px; font-weight:800; color:white; margin-bottom:4px; }
.analyze-card-text p { font-size:12px; color:rgba(255,255,255,0.8); }
.analyze-arrow { width:48px; height:48px; border-radius:50%; background:rgba(255,255,255,0.2); display:flex; align-items:center; justify-content:center; font-size:20px; color:white; flex-shrink:0; }
.questions-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
.q-card { background:var(--surface2); border:1px solid var(--border); border-radius:12px; padding:12px; transition:border-color 0.2s; }
.q-card:hover { border-color:var(--accent); }
.q-icon { font-size:20px; margin-bottom:8px; }
.q-num { font-size:9px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }
.q-text { font-size:11px; color:var(--text); line-height:1.4; margin-bottom:10px; font-weight:500; }
.q-options { display:flex; gap:6px; }
.q-opt { flex:1; padding:6px 4px; border-radius:6px; border:1.5px solid var(--border); font-size:11px; font-weight:600; color:var(--text2); cursor:pointer; display:flex; align-items:center; justify-content:center; gap:4px; background:none; transition:all 0.15s; }
.q-opt input { display:none; }
.q-opt.yes:hover { border-color:var(--red); color:var(--red); background:rgba(255,71,87,0.08); }
.q-opt.no:hover { border-color:var(--green); color:var(--green); background:rgba(46,213,115,0.08); }
.q-opt:has(input:checked).yes { border-color:var(--red); color:var(--red); background:rgba(255,71,87,0.12); }
.q-opt:has(input:checked).no { border-color:var(--green); color:var(--green); background:rgba(46,213,115,0.12); }
.how-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; }
.step { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.step-num { width:28px; height:28px; border-radius:50%; background:var(--accent); color:white; font-size:12px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.step-text { font-size:12px; color:var(--text2); line-height:1.4; }
.risk-panel { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; }
.risk-score-label { font-size:11px; font-weight:700; color:var(--text2); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; display:flex; align-items:center; gap:6px; }
.live-tag { margin-left:auto; font-size:9px; font-weight:800; background:var(--accent); color:white; padding:3px 8px; border-radius:20px; display:inline-flex; align-items:center; gap:4px; }
.live-dot { width:6px; height:6px; border-radius:50%; background:white; display:inline-block; animation:pulse 1.4s infinite; }
@keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.3} }
.score-ring-wrap { display:flex; flex-direction:column; align-items:center; margin-bottom:16px; }
.score-ring { width:120px; height:120px; border-radius:50%; border:8px solid var(--border); display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:10px; transition:border-color 0.3s, box-shadow 0.3s; }
.score-ring.red { border-color:var(--red); box-shadow:0 0 24px rgba(255,71,87,0.3); }
.score-ring.orange { border-color:var(--orange); box-shadow:0 0 24px rgba(255,165,2,0.3); }
.score-ring.green { border-color:var(--green); box-shadow:0 0 24px rgba(46,213,115,0.3); }
.score-num { font-size:40px; font-weight:900; line-height:1; }
.score-num.red { color:var(--red); }
.score-num.orange { color:var(--orange); }
.score-num.green { color:var(--green); }
.score-denom { font-size:12px; color:var(--text2); }
.verdict-pill { padding:6px 16px; border-radius:20px; font-size:13px; font-weight:800; margin-bottom:4px; }
.verdict-pill.red { background:rgba(255,71,87,0.15); color:var(--red); }
.verdict-pill.orange { background:rgba(255,165,2,0.15); color:var(--orange); }
.verdict-pill.green { background:rgba(46,213,115,0.15); color:var(--green); }
.verdict-sub { font-size:11px; color:var(--text2); margin-bottom:12px; text-align:center; }
.powered-badge { font-size:10px; color:var(--text2); display:flex; align-items:center; justify-content:center; gap:4px; }
.progress-row { display:flex; justify-content:space-between; font-size:11px; color:var(--text2); margin-bottom:6px; }
.progress-track { height:6px; background:var(--surface3); border-radius:4px; overflow:hidden; }
.progress-fill { height:100%; width:0%; background:linear-gradient(90deg,var(--accent),var(--accent2)); border-radius:4px; transition:width 0.3s; }
.insights-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:16px; margin-top:16px; }
.insight-item { display:flex; align-items:flex-start; gap:8px; padding:6px 0; font-size:12px; color:var(--text2); line-height:1.5; }
.insight-dot { width:6px; height:6px; border-radius:50%; background:var(--accent); flex-shrink:0; margin-top:5px; }
.result-grid { display:grid; grid-template-columns:320px 1fr; gap:20px; }
.result-left, .result-right { display:flex; flex-direction:column; gap:16px; }
.flag-item { display:flex; align-items:flex-start; gap:10px; padding:10px 0; border-bottom:1px solid var(--border); font-size:12px; color:var(--text2); line-height:1.5; }
.flag-item:last-child { border-bottom:none; }
.flag-x { color:var(--red); font-size:14px; flex-shrink:0; font-weight:700; }
.guidance-item { display:flex; align-items:flex-start; gap:8px; padding:8px 0; border-bottom:1px solid var(--border); font-size:12px; color:var(--text2); line-height:1.5; }
.guidance-item:last-child { border-bottom:none; }
.g-check { color:var(--green); flex-shrink:0; }
.img-finding { display:flex; align-items:flex-start; gap:8px; padding:8px 12px; background:rgba(255,165,2,0.08); border-radius:8px; margin-bottom:8px; font-size:12px; color:var(--text2); }
.img-finding-note { font-size:11px; color:var(--text2); font-style:italic; margin-top:8px; padding:8px; background:var(--surface2); border-radius:6px; line-height:1.5; }
.img-safe { display:flex; align-items:center; gap:8px; padding:10px; background:rgba(46,213,115,0.08); border-radius:8px; font-size:12px; color:var(--green); }
.seller-badge { display:inline-flex; align-items:center; gap:6px; padding:6px 14px; background:rgba(124,92,252,0.12); border:1px solid rgba(124,92,252,0.3); border-radius:20px; font-size:12px; color:var(--accent); font-weight:700; margin-bottom:12px; }
.btn-report { display:flex; align-items:center; justify-content:center; gap:8px; padding:14px; background:var(--red); color:white; border-radius:12px; text-decoration:none; font-weight:700; font-size:14px; border:none; cursor:pointer; box-shadow:0 4px 16px rgba(255,71,87,0.3); }
.btn-report:hover { opacity:0.9; }
.btn-another { display:flex; align-items:center; justify-content:center; gap:8px; padding:14px; background:var(--surface); color:var(--text); border-radius:12px; text-decoration:none; font-weight:700; font-size:14px; border:1px solid var(--border); }
.btn-another:hover { background:var(--surface2); }
.about-card p { font-size:12px; color:var(--text2); line-height:1.7; margin-top:8px; }
.about-helpline { margin-top:14px; padding:12px; background:var(--surface2); border-radius:10px; font-size:12px; color:var(--text2); display:flex; align-items:center; gap:10px; border:1px solid var(--border); }
.about-helpline-icon { font-size:18px; flex-shrink:0; }
.disclaimer { font-size:11px; color:var(--text2); text-align:center; padding:16px; border-top:1px solid var(--border); line-height:1.6; }
@media (max-width:900px) {
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
@media (max-width:480px) {
    .questions-grid { grid-template-columns:repeat(2,1fr); }
    .content { padding:16px; }
    .hero-text h1 { font-size:24px; }
}
</style>
</head>
<body>

<div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>

<nav class="sidebar" id="sidebar">
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🛡️</div>
        <div>
            <div class="sidebar-logo-text">Secure<span>Deal</span></div>
            <div class="sidebar-sub">AI Scam Protection</div>
        </div>
    </div>
    <div class="nav-section">Main</div>
    <a class="nav-item active" href="/?lang={{ lang }}">
        <span class="nav-icon">🏠</span> {{ t.new_check }}
        <span class="nav-badge">AI</span>
    </a>
    <div class="nav-section">Tools</div>
    <a class="nav-item" href="/?lang={{ lang }}#how-it-works" onclick="return navAnchor(event,'how-it-works')">
        <span class="nav-icon">❓</span> {{ t.how_it_works }}
    </a>
    <a class="nav-item" href="/?lang={{ lang }}#safety-tips" onclick="return navAnchor(event,'safety-tips')">
        <span class="nav-icon">🛡️</span> {{ t.safety_tips }}
    </a>
    <a class="nav-item" href="https://cybercrime.gov.in" target="_blank" rel="noopener">
        <span class="nav-icon">🚨</span> Report Scam
    </a>
    <div class="nav-section">Info</div>
    <a class="nav-item" href="/?lang={{ lang }}#about" onclick="return navAnchor(event,'about')">
        <span class="nav-icon">ℹ️</span> {{ t.about }}
    </a>
    <div class="sidebar-footer">
        <p>{{ t.free_forever }}</p>
        <span>{{ t.no_signup }}</span>
    </div>
    <div class="sidebar-made">{{ t.footer }}</div>
</nav>

<div class="main">
    <div class="topbar">
        <div style="display:flex;align-items:center;gap:8px;">
            <button class="hamburger" onclick="toggleSidebar()">☰</button>
            <span class="made-badge">{{ t.made_india }}</span>
        </div>
        <div class="topbar-right">
            <div class="lang-dropdown" id="langDropdown">
                <button class="lang-toggle-btn" onclick="toggleLangMenu(event)" type="button">
                    🌐 <span>{{ lang_label }}</span> <span class="lang-caret">▾</span>
                </button>
                <div class="lang-popup" id="langPopup">
                    <a href="/?lang=en" class="lang-popup-item {% if lang=='en' %}active{% endif %}">
                        English {% if lang=='en' %}<span class="lang-popup-check">✓</span>{% endif %}
                    </a>
                    <a href="/?lang=te" class="lang-popup-item {% if lang=='te' %}active{% endif %}">
                        తెలుగు {% if lang=='te' %}<span class="lang-popup-check">✓</span>{% endif %}
                    </a>
                    <a href="/?lang=hi" class="lang-popup-item {% if lang=='hi' %}active{% endif %}">
                        हिंदी {% if lang=='hi' %}<span class="lang-popup-check">✓</span>{% endif %}
                    </a>
                </div>
            </div>
            <button class="theme-btn" onclick="toggleTheme()" id="themeBtn">🌙</button>
        </div>
    </div>

    <div class="content">

    {% if not result %}

    <div class="hero">
        <div class="hero-text">
            <h1>{{ t.tagline_1 }}<br><span class="line2">{{ t.tagline_2 }}</span><br>{{ t.tagline_3 }}</h1>
            <p>{{ t.subtitle }}</p>
            <div class="hero-badges">
                <div class="hero-badge">✅ {{ t.free }}</div>
                <div class="hero-badge">👤 {{ t.no_reg }}</div>
                <div class="hero-badge">⚡ {{ t.instant }}</div>
            </div>
        </div>
        <div class="hero-shield">🛡️</div>
    </div>

    <form method="POST" action="/check?lang={{ lang }}" enctype="multipart/form-data" id="checkForm">

    <div class="form-grid">

        <div style="display:flex;flex-direction:column;gap:16px;">

            <div class="username-card">
                <div class="card-title">📱 {{ t.username_title }}</div>
                <div class="card-sub">{{ t.username_desc }}</div>
                <div class="username-input-wrap">
                    <input type="text" name="instagram_username" id="usernameInput" class="username-input"
                        placeholder="{{ t.username_placeholder }}" autocomplete="off" oninput="handleUsername(this.value)">
                </div>
                <div class="username-checklist" id="usernameChecklist">
                    <div class="username-checklist-title" id="usernameChecklistTitle"></div>
                    {% for i, item in enumerate(t.username_checklist) %}
                    <div class="username-checklist-item">
                        <div class="username-checklist-num">{{ i+1 }}</div>
                        <span>{{ item }}</span>
                    </div>
                    {% endfor %}
                    <div class="username-note">This is a manual checklist for you to verify yourself — SecureDeal does not access or scan Instagram pages directly.</div>
                </div>
            </div>

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

        <div style="display:flex;flex-direction:column;gap:16px;">

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
                    <label class="q-opt yes"><input type="radio" name="q{{ i }}" value="yes" required> ⚠️ {{ t.yes }}</label>
                    <label class="q-opt no"><input type="radio" name="q{{ i }}" value="no"> ✅ {{ t.no }}</label>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <button type="submit" class="analyze-card" style="margin-bottom:24px;">
        <div class="analyze-card-text">
            <h3>{{ t.analyze_btn }}</h3>
            <p>{{ t.analyze_sub }}</p>
        </div>
        <div class="analyze-arrow">→</div>
    </button>

    </form>

    {% else %}

    <div class="hero" style="margin-bottom:20px;">
        <div class="hero-text">
            <h1>{{ t.tagline_1 }}<br><span class="line2">{{ t.tagline_2 }}</span><br>{{ t.tagline_3 }}</h1>
            <p>{{ t.subtitle }}</p>
        </div>
        <div class="hero-shield">🛡️</div>
    </div>

    <div class="result-grid">
        <div class="result-left">
            <div class="risk-panel">
                <div class="risk-score-label">📈 {{ t.trust_score }}</div>
                {% if seller_username %}
                <div style="text-align:center;">
                    <div class="seller-badge">📱 {{ t.analysed_seller }}: {{ seller_username }}</div>
                </div>
                {% endif %}
                <div class="score-ring-wrap">
                    <div class="score-ring {{ color }}">
                        <div class="score-num {{ color }}">{{ score }}</div>
                        <div class="score-denom">/100</div>
                    </div>
                    <div class="verdict-pill {{ color }}">
                        {% if color=='red' %}🔴{% elif color=='orange' %}🟡{% else %}🟢{% endif %}
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
                    <div class="guidance-item"><span class="g-check">✅</span><span>{{ g }}</span></div>
                    {% endfor %}
                </div>
            </div>

            {% if score >= 70 %}
            <a href="https://cybercrime.gov.in" target="_blank" class="btn-report">{{ t.report_btn }}</a>
            {% endif %}
            <a href="/?lang={{ lang }}" class="btn-another">{{ t.check_another }}</a>
        </div>

        <div class="result-right">

            {% if seller_username %}
            <div class="card">
                <div class="card-title">📱 {{ t.username_checklist_title.replace('{username}', seller_username) }}</div>
                <div style="margin-top:12px;">
                    {% for i, item in enumerate(t.username_checklist) %}
                    <div class="username-checklist-item" style="padding:8px 0; border-bottom:1px solid var(--border);">
                        <div class="username-checklist-num">{{ i+1 }}</div>
                        <span style="font-size:12px; color:var(--text2);">{{ item }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% if image_findings is not none %}
            <div class="card">
                <div class="card-title">🖼️ {{ t.image_analysis }}</div>
                <div style="margin-top:12px;">
                    {% if image_findings %}
                        {% for finding in image_findings %}
                        <div class="img-finding"><span>⚠️</span><span>{{ t.img_flags[finding] }}</span></div>
                        {% endfor %}
                    {% else %}
                        <div class="img-safe">{{ t.img_safe }}</div>
                    {% endif %}
                    <div class="img-finding-note">{{ t.img_note }}</div>
                </div>
            </div>
            {% endif %}

            <div class="card">
                <div class="card-title">
                    {% if flags %}⚠️ {{ t.red_flags }} ({{ flags|length }}){% else %}✅ {{ t.no_flags }}{% endif %}
                </div>
                <div style="margin-top:12px;">
                    {% if flags %}
                        {% for flag in flags %}
                        <div class="flag-item"><span class="flag-x">✕</span><span>{{ flag }}</span></div>
                        {% endfor %}
                    {% else %}
                        <div class="flag-item"><span style="color:var(--green);">✓</span><span>{{ t.no_flags }}</span></div>
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
function toggleLangMenu(e) {
    e.stopPropagation();
    document.getElementById('langDropdown').classList.toggle('open');
}
document.addEventListener('click', function(e) {
    const dd = document.getElementById('langDropdown');
    if (dd && !dd.contains(e.target)) dd.classList.remove('open');
});
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const dd = document.getElementById('langDropdown');
        if (dd) dd.classList.remove('open');
        closeSidebar();
    }
});
function navAnchor(e, id) {
    closeSidebar();
    const el = document.getElementById(id);
    if (el) { e.preventDefault(); el.scrollIntoView({behavior:'smooth',block:'start'}); return false; }
    return true;
}
window.addEventListener('DOMContentLoaded', function() {
    if (location.hash) {
        const id = location.hash.substring(1);
        setTimeout(function() {
            const el = document.getElementById(id);
            if (el) el.scrollIntoView({behavior:'smooth',block:'start'});
        }, 150);
    }
});

const CHECKLIST_TITLE = {{ t.username_checklist_title | tojson }};
function handleUsername(val) {
    const checklist = document.getElementById('usernameChecklist');
    const title = document.getElementById('usernameChecklistTitle');
    val = val.trim();
    if (val.length > 1) {
        const display = val.startsWith('@') ? val : '@' + val;
        title.textContent = CHECKLIST_TITLE.replace('{username}', display);
        checklist.classList.add('visible');
    } else {
        checklist.classList.remove('visible');
    }
}

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
    if (!ring) return;
    const radios = document.querySelectorAll('#checkForm input[type=radio]:checked');
    let score = 0, answered = 0;
    radios.forEach(function(input) {
        answered++;
        if (input.value === 'yes') {
            const qIndex = parseInt(input.name.replace('q',''), 10);
            score += QUESTION_POINTS[qIndex] || 0;
        }
    });
    score = Math.min(score, 100);
    let color, verdictText, verdictSub, emoji;
    if (score >= 70) { color='red'; verdictText=LIVE_T.high; verdictSub=LIVE_T.highSub; emoji='🔴'; }
    else if (score >= 35) { color='orange'; verdictText=LIVE_T.caution; verdictSub=LIVE_T.cautionSub; emoji='🟡'; }
    else { color='green'; verdictText=LIVE_T.low; verdictSub=LIVE_T.lowSub; emoji='🟢'; }
    ['red','orange','green'].forEach(function(c) {
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
document.querySelectorAll('#checkForm input[type=radio]').forEach(function(input) {
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
    return render_template_string(HTML, result=False, t=t, lang=lang, lang_label=LANG_LABELS[lang], enumerate=enumerate)

@app.route("/check", methods=["POST"])
def check():
    lang = request.args.get('lang', 'en')
    if lang not in TRANSLATIONS:
        lang = 'en'
    t = TRANSLATIONS[lang]

    answers = {
        'refused_video_call': request.form.get('q0') == 'yes',
        'payment_before_proof': request.form.get('q1') == 'yes',
        'refused_date_photo': request.form.get('q2') == 'yes',
        'urgency_tactics': request.form.get('q3') == 'yes',
        'account_very_new': request.form.get('q4') == 'yes',
        'price_significantly_lower': request.form.get('q5') == 'yes',
        'hidden_payment_recipient': request.form.get('q6') == 'yes',
        'photo_reused_elsewhere': request.form.get('q7') == 'yes',
    }

    raw_username = request.form.get('instagram_username', '').strip()
    seller_username = None
    if raw_username:
        clean = raw_username.lstrip('@').strip()
        if clean and len(clean) <= 30 and clean.replace('.', '').replace('_', '').isalnum():
            seller_username = '@' + clean

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
        seller_username=seller_username,
        t=t, lang=lang, lang_label=LANG_LABELS[lang], enumerate=enumerate
    )

if __name__ == "__main__":
    app.run()
