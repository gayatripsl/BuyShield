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

# ─── Translations ───
TRANSLATIONS = {
    'en': {
        'title': 'BuyShield — Fake Seller Detector',
        'header': 'BuyShield',
        'tagline': 'Check Before You Pay',
        'subtitle': 'AI-Powered Protection Against Fake Instagram Sellers',
        'intro': 'Before paying any Instagram seller, answer these 8 simple questions and optionally upload a product image. BuyShield analyses seller behaviour and gives you a risk score in seconds.',
        'free': '100% Free',
        'no_reg': 'No Registration',
        'instant': 'Instant Result',
        'form_title': 'Answer About The Seller',
        'image_title': 'Upload Product Image (Optional)',
        'image_desc': 'Upload a product photo the seller sent you. BuyShield will analyse if it looks suspicious.',
        'image_label': 'Choose Image',
        'submit': '🛡️ Check Now',
        'check_again': '🔄 Check Another Seller',
        'report': '🚨 Report This Scam at cybercrime.gov.in',
        'red_flags': 'Red Flags Detected',
        'no_flags': 'No major red flags detected',
        'what_to_do': 'What You Should Do',
        'image_analysis': 'Image Analysis',
        'footer_tagline': 'Protecting innocent Indian buyers',
        'footer_note': "When in doubt — don't pay. Stay safe.",
        'disclaimer': 'BuyShield provides risk assessment based on user-reported behaviour patterns. This is not a definitive accusation. Always use your own judgement.',
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
        'yes': 'Yes',
        'no': 'No',
        'high_risk': 'HIGH RISK',
        'high_risk_sub': 'Do NOT pay this seller',
        'caution': 'CAUTION',
        'caution_sub': 'Verify before paying',
        'low_risk': 'LOWER RISK',
        'low_risk_sub': 'Still verify carefully',
        'flags': [
            'Seller refused video call — genuine sellers always agree to show product live',
            'Demanded payment WITHOUT showing product first — primary scam mechanism',
            "Refused date paper photo — suggests product does not exist",
            'Used urgency tactics — designed to stop you from thinking carefully',
            'Page less than 1 month old — scammers need to act fast and disappear',
            'Prices unrealistically low — scammers use low prices as bait',
            'Blocked after payment — confirmed scam behaviour',
            'Asked for extra charges after payment — this is Advance Fee Fraud',
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
            'too_small': '⚠️ Image is very small — may be a low quality stolen image',
            'no_exif': '⚠️ Image has no camera metadata — may not be an original photo',
            'ai_uniform': '⚠️ Image appears too uniform — could be AI generated or heavily edited',
            'suspicious_ratio': '⚠️ Image dimensions look unusual — may be a screenshot of another listing',
        },
        'img_safe': '✅ Image appears to be an original photo — no major suspicious patterns detected',
        'img_note': 'Note: Image analysis is one signal only. Ask the seller to show the product on a live video call to be certain.',
    },
    'te': {
        'title': 'BuyShield — నకిలీ విక్రేత గుర్తింపు',
        'header': 'BuyShield',
        'tagline': 'చెల్లించే ముందు తనిఖీ చేయండి',
        'subtitle': 'నకిలీ Instagram విక్రేతలకు వ్యతిరేకంగా AI రక్షణ',
        'intro': 'ఏదైనా Instagram విక్రేతకు చెల్లించే ముందు ఈ 8 సాధారణ ప్రశ్నలకు సమాధానం ఇవ్వండి.',
        'free': '100% ఉచితం',
        'no_reg': 'రిజిస్ట్రేషన్ లేదు',
        'instant': 'తక్షణ ఫలితం',
        'form_title': 'విక్రేత గురించి సమాధానం ఇవ్వండి',
        'image_title': 'ఉత్పత్తి చిత్రాన్ని అప్‌లోడ్ చేయండి (ఐచ్ఛికం)',
        'image_desc': 'విక్రేత పంపిన ఉత్పత్తి ఫోటోను అప్‌లోడ్ చేయండి.',
        'image_label': 'చిత్రాన్ని ఎంచుకోండి',
        'submit': '🛡️ ఇప్పుడు తనిఖీ చేయండి',
        'check_again': '🔄 మరొక విక్రేతను తనిఖీ చేయండి',
        'report': '🚨 cybercrime.gov.in లో రిపోర్ట్ చేయండి',
        'red_flags': 'గుర్తించిన హెచ్చరికలు',
        'no_flags': 'పెద్ద హెచ్చరికలు ఏమీ లేవు',
        'what_to_do': 'మీరు ఏమి చేయాలి',
        'image_analysis': 'చిత్ర విశ్లేషణ',
        'footer_tagline': 'అమాయక భారతీయ కొనుగోలుదారులను రక్షిస్తోంది',
        'footer_note': 'సందేహం ఉంటే — చెల్లించకండి.',
        'disclaimer': 'BuyShield వినియోగదారు నివేదించిన సంకేతాల ఆధారంగా రిస్క్ అంచనా అందిస్తుంది. ఇది నిర్ధారిత అభియోగం కాదు.',
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
        'yes': 'అవును',
        'no': 'కాదు',
        'high_risk': 'అధిక ప్రమాదం',
        'high_risk_sub': 'చెల్లించకండి',
        'caution': 'జాగ్రత్త',
        'caution_sub': 'చెల్లించే ముందు ధృవీకరించండి',
        'low_risk': 'తక్కువ ప్రమాదం',
        'low_risk_sub': 'అయినా జాగ్రత్తగా ధృవీకరించండి',
        'flags': [
            'వీడియో కాల్ తిరస్కరించారు — నిజమైన విక్రేతలు ఎప్పుడూ అంగీకరిస్తారు',
            'ఉత్పత్తి చూపించే ముందే చెల్లింపు అడిగారు — ప్రధాన మోసం పద్ధతి',
            'నేటి తేదీతో ఫోటో తీయడానికి నిరాకరించారు',
            'అత్యవసరత వ్యూహాలు ఉపయోగించారు',
            'పేజీ 1 నెల కంటే తక్కువ పాతది',
            'ధరలు అసాధారణంగా తక్కువ',
            'చెల్లింపు తర్వాత బ్లాక్ చేశారు',
            'చెల్లింపు తర్వాత అదనపు చార్జీలు అడిగారు — అడ్వాన్స్ ఫీ మోసం',
        ],
        'guidance_high': [
            'ఇంకా డబ్బు పంపకండి',
            'Instagram లో బ్లాక్ చేసి రిపోర్ట్ చేయండి',
            'cybercrime.gov.in లో రిపోర్ట్ చేయండి',
            'అన్ని చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'స్నేహితులకు మరియు కుటుంబానికి హెచ్చరించండి',
        ],
        'guidance_high_extra': 'అదనపు చార్జీలు చెల్లించడం ఆపండి',
        'guidance_medium': [
            'వీడియో కాల్ అడగండి',
            'నేటి తేదీతో ఫోటో అడగండి',
            'ఉత్పత్తి చూడకుండా పూర్తి మొత్తం చెల్లించకండి',
            'Truecaller లో నంబర్ వెతకండి',
            'అన్ని చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
        ],
        'guidance_low': [
            'జాగ్రత్తగా ముందుకు వెళ్ళండి',
            'వీలైతే పాక్షిక చెల్లింపు చేయండి',
            'చాట్ స్క్రీన్‌షాట్‌లు సేవ్ చేయండి',
            'అంతర్మనస్సును నమ్మండి',
        ],
        'img_flags': {
            'too_small': '⚠️ చిత్రం చాలా చిన్నది — దొంగిలించిన చిత్రం కావచ్చు',
            'no_exif': '⚠️ చిత్రంలో కెమెరా సమాచారం లేదు — అసలు ఫోటో కాకపోవచ్చు',
            'ai_uniform': '⚠️ చిత్రం చాలా సమానంగా ఉంది — AI జనరేటెడ్ కావచ్చు',
            'suspicious_ratio': '⚠️ చిత్రం కొలతలు అనుమానాస్పదంగా ఉన్నాయి',
        },
        'img_safe': '✅ చిత్రం అసలైనదిగా కనిపిస్తోంది',
        'img_note': 'గమనిక: చిత్ర విశ్లేషణ ఒక సంకేతం మాత్రమే. నిర్ధారణకు వీడియో కాల్ అడగండి.',
    },
    'hi': {
        'title': 'BuyShield — नकली विक्रेता पहचानकर्ता',
        'header': 'BuyShield',
        'tagline': 'भुगतान से पहले जांचें',
        'subtitle': 'नकली Instagram विक्रेताओं के खिलाफ AI सुरक्षा',
        'intro': 'किसी भी Instagram विक्रेता को भुगतान करने से पहले इन 8 सरल प्रश्नों का उत्तर दें।',
        'free': '100% मुफ्त',
        'no_reg': 'कोई पंजीकरण नहीं',
        'instant': 'तुरंत परिणाम',
        'form_title': 'विक्रेता के बारे में उत्तर दें',
        'image_title': 'उत्पाद छवि अपलोड करें (वैकल्पिक)',
        'image_desc': 'विक्रेता द्वारा भेजी गई उत्पाद फोटो अपलोड करें।',
        'image_label': 'छवि चुनें',
        'submit': '🛡️ अभी जांचें',
        'check_again': '🔄 दूसरे विक्रेता की जांच करें',
        'report': '🚨 cybercrime.gov.in पर रिपोर्ट करें',
        'red_flags': 'पहचाने गए खतरे',
        'no_flags': 'कोई बड़ा खतरा नहीं',
        'what_to_do': 'आपको क्या करना चाहिए',
        'image_analysis': 'छवि विश्लेषण',
        'footer_tagline': 'निर्दोष भारतीय खरीदारों की रक्षा करता है',
        'footer_note': 'संदेह हो तो — भुगतान न करें।',
        'disclaimer': 'BuyShield उपयोगकर्ता द्वारा रिपोर्ट किए गए संकेतों के आधार पर जोखिम मूल्यांकन प्रदान करता है।',
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
        'yes': 'हाँ',
        'no': 'नहीं',
        'high_risk': 'उच्च जोखिम',
        'high_risk_sub': 'भुगतान न करें',
        'caution': 'सावधानी',
        'caution_sub': 'भुगतान से पहले सत्यापित करें',
        'low_risk': 'कम जोखिम',
        'low_risk_sub': 'फिर भी सावधानी से जांचें',
        'flags': [
            'वीडियो कॉल से मना किया — असली विक्रेता हमेशा तैयार रहते हैं',
            'उत्पाद दिखाए बिना भुगतान मांगा — मुख्य धोखाधड़ी तरीका',
            'आज की तारीख वाली फोटो से मना किया',
            'जल्दबाजी की रणनीति इस्तेमाल की',
            'पेज 1 महीने से कम पुराना',
            'कीमतें असामान्य रूप से कम',
            'भुगतान के बाद ब्लॉक किया',
            'भुगतान के बाद अतिरिक्त शुल्क मांगा — एडवांस फी धोखाधड़ी',
        ],
        'guidance_high': [
            'अब और पैसे न भेजें',
            'Instagram पर ब्लॉक करें और रिपोर्ट करें',
            'cybercrime.gov.in पर रिपोर्ट करें',
            'सभी चैट स्क्रीनशॉट सेव करें',
            'दोस्तों और परिवार को चेतावनी दें',
        ],
        'guidance_high_extra': 'अतिरिक्त शुल्क देना बंद करें',
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
            'चैट स्क्रीनशॉट सेव करें',
            'अंतरात्मा पर भरोसा करें',
        ],
        'img_flags': {
            'too_small': '⚠️ छवि बहुत छोटी है — चोरी की गई हो सकती है',
            'no_exif': '⚠️ छवि में कैमरा डेटा नहीं है — मूल फोटो नहीं हो सकती',
            'ai_uniform': '⚠️ छवि बहुत एकसमान दिखती है — AI जनरेटेड हो सकती है',
            'suspicious_ratio': '⚠️ छवि का आकार संदिग्ध है',
        },
        'img_safe': '✅ छवि मूल प्रतीत होती है',
        'img_note': 'नोट: छवि विश्लेषण एक संकेत मात्र है। पुष्टि के लिए वीडियो कॉल मांगें।',
    }
}

# ─── Image Analysis ───
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
        print(f"Image analysis error: {e}")

    return findings, score_addition


# ─── Scoring Engine ───
def calculate_risk_score(answers):
    flag_indices = []
    checks = [
        'refused_video_call',
        'payment_before_product',
        'refused_date_photo',
        'urgency_tactics',
        'page_very_new',
        'unrealistic_price',
        'blocked_after_payment',
        'extra_charges_after_payment',
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


def get_verdict_key(score):
    if score >= 70:
        return 'high_risk', 'high_risk_sub', 'red'
    elif score >= 35:
        return 'caution', 'caution_sub', 'orange'
    else:
        return 'low_risk', 'low_risk_sub', 'green'


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


HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.title }}</title>
    <style>
        :root[data-theme="dark"] {
            --bg: #0a0a14; --surface: #12122a; --surface2: #1a1a3a;
            --border: #2a2a5a; --text: #ffffff; --text2: #a0a0c0;
            --text3: #6060a0; --accent: #e94560; --accent2: #ff6b6b;
            --green: #00d4a0; --orange: #ffa500; --red: #ff4444;
        }
        :root[data-theme="light"] {
            --bg: #f0f2f8; --surface: #ffffff; --surface2: #f5f7ff;
            --border: #dde2f0; --text: #1a1a3a; --text2: #4a4a7a;
            --text3: #8888aa; --accent: #e94560; --accent2: #cc3355;
            --green: #00a87a; --orange: #e08800; --red: #cc2222;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; transition: background 0.3s, color 0.3s; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

        /* HEADER */
        .header {
            background: var(--surface); border-bottom: 1px solid var(--border);
            padding: 0 24px; height: 64px;
            display: flex; align-items: center; justify-content: space-between;
            position: sticky; top: 0; z-index: 100;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        .logo { display: flex; align-items: center; gap: 10px; }
        .logo-icon {
            width: 36px; height: 36px;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;
        }
        .logo-text { font-size: 20px; font-weight: 800; color: var(--text); }
        .logo-text span { color: var(--accent); }
        .header-right { display: flex; align-items: center; gap: 12px; }
        .lang-group { display: flex; gap: 4px; background: var(--surface2); padding: 4px; border-radius: 8px; }
        .lang-btn {
            padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;
            text-decoration: none; color: var(--text2); border: none; background: transparent; cursor: pointer;
        }
        .lang-btn.active { background: var(--accent); color: white; }
        .lang-btn:hover:not(.active) { background: var(--border); color: var(--text); }
        .theme-toggle {
            width: 40px; height: 40px; border-radius: 10px;
            background: var(--surface2); border: 1px solid var(--border);
            cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px;
        }

        /* MOBILE LANGUAGE BAR */
        .mobile-lang {
            display: none; justify-content: center; gap: 8px;
            padding: 12px; background: var(--surface); border-bottom: 1px solid var(--border);
        }
        .mobile-lang-btn {
            padding: 8px 20px; border-radius: 8px; font-size: 14px; font-weight: 700;
            text-decoration: none; border: 1px solid var(--border);
            background: var(--surface2); color: var(--text2);
        }
        .mobile-lang-btn.active { background: var(--accent); color: white; border-color: var(--accent); }

        /* HERO */
        .hero {
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
            border-bottom: 1px solid var(--border); padding: 48px 24px; text-align: center;
        }
        .hero-badge {
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(233,69,96,0.1); border: 1px solid rgba(233,69,96,0.3);
            color: var(--accent); padding: 6px 14px; border-radius: 20px;
            font-size: 12px; font-weight: 600; margin-bottom: 20px;
        }
        .hero h1 { font-size: 36px; font-weight: 900; margin-bottom: 12px; }
        .hero h1 span { color: var(--accent); }
        .hero p { color: var(--text2); font-size: 16px; max-width: 520px; margin: 0 auto 28px; }
        .hero-stats { display: flex; justify-content: center; gap: 32px; flex-wrap: wrap; }
        .stat { display: flex; align-items: center; gap: 8px; color: var(--text2); font-size: 13px; }
        .stat-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); }

        /* CONTAINER */
        .container { max-width: 680px; margin: 0 auto; padding: 32px 20px; }

        /* CARDS */
        .form-card {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 20px; padding: 28px; margin-bottom: 20px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        }
        .form-card h2 {
            font-size: 16px; font-weight: 700; color: var(--text);
            margin-bottom: 24px; padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
            display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
        }

        /* QUESTIONS */
        .question {
            padding: 16px; background: var(--surface2);
            border-radius: 12px; margin-bottom: 12px;
            border: 1px solid var(--border);
        }
        .question:hover { border-color: var(--accent); }
        .question-num { font-size: 10px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
        .question p { font-size: 14px; color: var(--text); line-height: 1.5; margin-bottom: 14px; font-weight: 500; }
        .radio-group { display: flex; gap: 10px; }
        .radio-option {
            flex: 1; padding: 10px; border-radius: 8px;
            border: 2px solid var(--border); cursor: pointer;
            display: flex; align-items: center; justify-content: center; gap: 6px;
            font-size: 13px; font-weight: 600; color: var(--text2); transition: all 0.2s;
        }
        .radio-option input { display: none; }
        .radio-option.yes-opt:hover { background: rgba(233,69,96,0.08); border-color: var(--accent); color: var(--accent); }
        .radio-option.no-opt:hover { background: rgba(0,212,160,0.08); border-color: var(--green); color: var(--green); }
        .radio-option:has(input:checked).yes-opt { border-color: var(--accent); background: rgba(233,69,96,0.12); color: var(--accent); }
        .radio-option:has(input:checked).no-opt { border-color: var(--green); background: rgba(0,212,160,0.12); color: var(--green); }

        /* IMAGE UPLOAD */
        .image-upload-card {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 20px; padding: 24px; margin-bottom: 20px;
        }
        .image-upload-card h3 { font-size: 15px; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
        .image-upload-card h3::before { content: '🖼️'; }
        .image-upload-card p { font-size: 13px; color: var(--text2); margin-bottom: 16px; line-height: 1.5; }
        .upload-area { border: 2px dashed var(--border); border-radius: 12px; padding: 24px; text-align: center; }
        .upload-area:hover { border-color: var(--accent); }
        .upload-area input { display: none; }
        .upload-label {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 20px; background: var(--surface2);
            border: 1px solid var(--border); border-radius: 8px;
            cursor: pointer; font-size: 13px; font-weight: 600; color: var(--text2);
        }
        .upload-label:hover { border-color: var(--accent); color: var(--accent); }
        .upload-hint { font-size: 11px; color: var(--text3); margin-top: 8px; }
        #preview-container { margin-top: 12px; display: none; }
        #preview-container img { max-width: 200px; max-height: 200px; border-radius: 8px; border: 1px solid var(--border); }
        #file-name { font-size: 12px; color: var(--green); margin-top: 6px; }

        /* SUBMIT */
        .submit-btn {
            width: 100%; padding: 16px;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            color: white; border: none; border-radius: 14px;
            font-size: 17px; font-weight: 700; cursor: pointer;
            box-shadow: 0 4px 20px rgba(233,69,96,0.35); transition: transform 0.2s;
        }
        .submit-btn:hover { transform: translateY(-2px); }

        /* RESULT */
        .result-hero { border-radius: 20px; padding: 32px; text-align: center; margin-bottom: 20px; border: 1px solid var(--border); }
        .result-red { background: linear-gradient(135deg, rgba(255,68,68,0.08), rgba(255,68,68,0.03)); border-color: rgba(255,68,68,0.3); }
        .result-orange { background: linear-gradient(135deg, rgba(255,165,0,0.08), rgba(255,165,0,0.03)); border-color: rgba(255,165,0,0.3); }
        .result-green { background: linear-gradient(135deg, rgba(0,212,160,0.08), rgba(0,212,160,0.03)); border-color: rgba(0,212,160,0.3); }

        .score-ring {
            width: 140px; height: 140px; border-radius: 50%;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            margin: 0 auto 20px; border: 6px solid var(--border);
        }
        .score-ring.red { border-color: var(--red); box-shadow: 0 0 30px rgba(255,68,68,0.25); }
        .score-ring.orange { border-color: var(--orange); box-shadow: 0 0 30px rgba(255,165,0,0.25); }
        .score-ring.green { border-color: var(--green); box-shadow: 0 0 30px rgba(0,212,160,0.25); }

        .score-num { font-size: 48px; font-weight: 900; line-height: 1; }
        .score-num.red { color: var(--red); }
        .score-num.orange { color: var(--orange); }
        .score-num.green { color: var(--green); }
        .score-label { font-size: 12px; color: var(--text3); }

        .verdict-badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 24px; border-radius: 30px; font-size: 18px; font-weight: 800; margin-bottom: 8px;
        }
        .verdict-badge.red { background: rgba(255,68,68,0.15); color: var(--red); }
        .verdict-badge.orange { background: rgba(255,165,0,0.15); color: var(--orange); }
        .verdict-badge.green { background: rgba(0,212,160,0.15); color: var(--green); }
        .verdict-sub { color: var(--text2); font-size: 14px; }

        .ai-badge {
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(74,144,226,0.1); border: 1px solid rgba(74,144,226,0.3);
            color: #4a90e2; padding: 4px 10px; border-radius: 12px;
            font-size: 11px; font-weight: 600; margin-top: 10px;
        }

        /* SECTIONS */
        .section-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 22px; margin-bottom: 16px; }
        .section-title { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 14px; }
        .flag-item { padding: 12px 14px; margin-bottom: 8px; background: rgba(255,68,68,0.06); border-left: 3px solid var(--red); border-radius: 0 8px 8px 0; font-size: 13px; color: var(--text2); line-height: 1.5; }
        .img-flag-item { padding: 12px 14px; margin-bottom: 8px; background: rgba(255,165,0,0.06); border-left: 3px solid var(--orange); border-radius: 0 8px 8px 0; font-size: 13px; color: var(--text2); line-height: 1.5; }
        .img-safe-item { padding: 12px 14px; margin-bottom: 8px; background: rgba(0,212,160,0.06); border-left: 3px solid var(--green); border-radius: 0 8px 8px 0; font-size: 13px; color: var(--text2); line-height: 1.5; }
        .img-note { font-size: 11px; color: var(--text3); font-style: italic; margin-top: 10px; padding: 8px; background: var(--surface2); border-radius: 6px; }
        .guidance-item { padding: 12px 14px; margin-bottom: 8px; background: var(--surface2); border-radius: 8px; font-size: 13px; color: var(--text2); line-height: 1.5; display: flex; align-items: flex-start; gap: 8px; }
        .guidance-item::before { content: "✅"; flex-shrink: 0; }

        /* BUTTONS */
        .btn-report { display: block; text-align: center; padding: 14px; background: linear-gradient(135deg, var(--accent), var(--accent2)); color: white; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 15px; margin-bottom: 12px; }
        .btn-check-again { display: block; text-align: center; padding: 14px; background: var(--surface); color: var(--accent); border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 15px; border: 2px solid var(--accent); }

        .disclaimer { text-align: center; padding: 16px; color: var(--text3); font-size: 11px; line-height: 1.6; border-top: 1px solid var(--border); margin-top: 20px; }
        .footer { text-align: center; padding: 24px; border-top: 1px solid var(--border); color: var(--text3); font-size: 12px; background: var(--surface); }
        .footer strong { color: var(--accent); }

        /* MOBILE */
        @media (max-width: 480px) {
            .hero h1 { font-size: 24px; }
            .lang-group { display: none; }
            .mobile-lang { display: flex; }
            .container { padding: 20px 14px; }
            .score-ring { width: 110px; height: 110px; }
            .score-num { font-size: 36px; }
            .hero { padding: 32px 16px; }
        }
    </style>
</head>
<body>

<!-- HEADER -->
<header class="header">
    <div class="logo">
        <div class="logo-icon">🛡️</div>
        <span class="logo-text">Buy<span>Shield</span></span>
    </div>
    <div class="header-right">
        <div class="lang-group">
            <a href="/?lang=en" class="lang-btn {% if lang == 'en' %}active{% endif %}">EN</a>
            <a href="/?lang=te" class="lang-btn {% if lang == 'te' %}active{% endif %}">తెలుగు</a>
            <a href="/?lang=hi" class="lang-btn {% if lang == 'hi' %}active{% endif %}">हिंदी</a>
        </div>
        <button class="theme-toggle" onclick="toggleTheme()" id="themeBtn">☀️</button>
    </div>
</header>

<!-- MOBILE LANGUAGE BAR -->
<div class="mobile-lang">
    <a href="/?lang=en" class="mobile-lang-btn {% if lang == 'en' %}active{% endif %}">English</a>
    <a href="/?lang=te" class="mobile-lang-btn {% if lang == 'te' %}active{% endif %}">తెలుగు</a>
    <a href="/?lang=hi" class="mobile-lang-btn {% if lang == 'hi' %}active{% endif %}">हिंदी</a>
</div>

<!-- HERO -->
<div class="hero">
    <div class="hero-badge">🛡️ Made for India</div>
    <h1>{{ t.header }} — <span>{{ t.tagline }}</span></h1>
    <p>{{ t.subtitle }}</p>
    <div class="hero-stats">
        <div class="stat"><div class="stat-dot"></div>{{ t.free }}</div>
        <div class="stat"><div class="stat-dot"></div>{{ t.no_reg }}</div>
        <div class="stat"><div class="stat-dot"></div>{{ t.instant }}</div>
    </div>
</div>

<div class="container">

{% if not result %}

<div class="form-card" style="margin-bottom:20px; padding:20px;">
    <p style="color:var(--text2); font-size:14px; line-height:1.7;">{{ t.intro }}</p>
</div>

<form method="POST" action="/check?lang={{ lang }}" enctype="multipart/form-data">

<!-- Image Upload -->
<div class="image-upload-card">
    <h3>{{ t.image_title }}</h3>
    <p>{{ t.image_desc }}</p>
    <div class="upload-area">
        <input type="file" name="product_image" id="imageInput" accept="image/*" onchange="previewImage(this)">
        <label for="imageInput" class="upload-label">📷 {{ t.image_label }}</label>
        <div class="upload-hint">JPG, PNG, WEBP — Max 5MB</div>
        <div id="preview-container">
            <img id="preview-img" src="" alt="Preview">
            <div id="file-name"></div>
        </div>
    </div>
</div>

<!-- Questions -->
<div class="form-card">
    <h2>📋 {{ t.form_title }} <span style="font-size:11px; background:rgba(74,144,226,0.1); border:1px solid rgba(74,144,226,0.3); color:#4a90e2; padding:3px 8px; border-radius:10px; margin-left:4px;">🤖 AI Powered</span></h2>

    {% for i in range(8) %}
    <div class="question">
        <div class="question-num">Question {{ i+1 }} of 8</div>
        <p>{{ t.questions[i] }}</p>
        <div class="radio-group">
            <label class="radio-option yes-opt">
                <input type="radio" name="q{{ i }}" value="yes" required>
                <span>⚠️ {{ t.yes }}</span>
            </label>
            <label class="radio-option no-opt">
                <input type="radio" name="q{{ i }}" value="no">
                <span>✅ {{ t.no }}</span>
            </label>
        </div>
    </div>
    {% endfor %}

    <button type="submit" class="submit-btn">{{ t.submit }}</button>
</div>
</form>

{% else %}

<!-- Result -->
<div class="result-hero result-{{ color }}">
    <div class="score-ring {{ color }}">
        <div class="score-num {{ color }}">{{ score }}</div>
        <div class="score-label">/100</div>
    </div>
    <div class="verdict-badge {{ color }}">
        {% if color == 'red' %}🔴{% elif color == 'orange' %}🟡{% else %}🟢{% endif %}
        {{ verdict }}
    </div>
    <div class="verdict-sub">{{ verdict_sub }}</div>
    <div><span class="ai-badge">🤖 Powered by Random Forest ML Model</span></div>
</div>

{% if image_findings is not none %}
<div class="section-card">
    <div class="section-title">🖼️ {{ t.image_analysis }}</div>
    {% if image_findings %}
        {% for finding in image_findings %}
        <div class="img-flag-item">{{ t.img_flags[finding] }}</div>
        {% endfor %}
    {% else %}
        <div class="img-safe-item">{{ t.img_safe }}</div>
    {% endif %}
    <div class="img-note">{{ t.img_note }}</div>
</div>
{% endif %}

{% if flags %}
<div class="section-card">
    <div class="section-title">⚠️ {{ t.red_flags }} ({{ flags|length }})</div>
    {% for flag in flags %}
    <div class="flag-item">{{ flag }}</div>
    {% endfor %}
</div>
{% else %}
<div class="section-card">
    <div class="section-title">✅ {{ t.no_flags }}</div>
</div>
{% endif %}

<div class="section-card">
    <div class="section-title">💡 {{ t.what_to_do }}</div>
    {% for g in guidance %}
    <div class="guidance-item">{{ g }}</div>
    {% endfor %}
</div>

{% if score >= 70 %}
<a href="https://cybercrime.gov.in" target="_blank" class="btn-report">{{ t.report }}</a>
{% endif %}
<a href="/?lang={{ lang }}" class="btn-check-again">{{ t.check_again }}</a>

{% endif %}

<div class="disclaimer">{{ t.disclaimer }}</div>
</div>

<footer class="footer">
    <strong>BuyShield</strong> — {{ t.footer_tagline }}<br>{{ t.footer_note }}
</footer>

<script>
    function toggleTheme() {
        const html = document.documentElement;
        const btn = document.getElementById('themeBtn');
        if (html.getAttribute('data-theme') === 'dark') {
            html.setAttribute('data-theme', 'light');
            btn.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        } else {
            html.setAttribute('data-theme', 'dark');
            btn.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        }
    }
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.getElementById('themeBtn').textContent = savedTheme === 'dark' ? '☀️' : '🌙';

    function previewImage(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('preview-img').src = e.target.result;
                document.getElementById('preview-container').style.display = 'block';
                document.getElementById('file-name').textContent = '✅ ' + input.files[0].name;
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
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

    image_findings = None
    image_score = 0
    if 'product_image' in request.files:
        file = request.files['product_image']
        if file and file.filename != '':
            image_findings, image_score = analyse_image(file)
            score = min(score + image_score, 100)

    verdict_key, verdict_sub_key, color = get_verdict_key(score)
    verdict = t[verdict_key]
    verdict_sub = t[verdict_sub_key]
    flags = [t['flags'][i] for i in flag_indices]
    guidance = get_guidance(score, answers, lang)

    return render_template_string(HTML,
        result=True,
        score=score,
        flags=flags,
        verdict=verdict,
        verdict_sub=verdict_sub,
        color=color,
        guidance=guidance,
        image_findings=image_findings,
        t=t,
        lang=lang
    )


if __name__ == "__main__":
    app.run()
