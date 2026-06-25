from flask import Flask, render_template_string, request

app = Flask(__name__)

# ─── Scoring Engine ───
def calculate_risk_score(answers):
    score = 0
    flags = []

    if answers.get("refused_video_call"):
        score += 25
        flags.append("Seller refused video call — genuine sellers always agree to show product live")

    if answers.get("payment_before_product"):
        score += 20
        flags.append("Demanded payment WITHOUT showing product first — this is the primary scam mechanism")

    if answers.get("refused_date_photo"):
        score += 15
        flags.append("Refused to photograph product with today's date — suggests product does not exist")

    if answers.get("urgency_tactics"):
        score += 15
        flags.append("Used urgency tactics like today only or last piece — designed to stop you from thinking")

    if answers.get("page_very_new"):
        score += 10
        flags.append("Instagram page is less than 1 month old — scammers need to act fast and disappear")

    if answers.get("unrealistic_price"):
        score += 10
        flags.append("Prices are unrealistically low — scammers use low prices as bait")

    if answers.get("blocked_after_payment"):
        score += 20
        flags.append("Seller blocked or went silent after payment — confirmed scam behaviour")

    if answers.get("extra_charges_after_payment"):
        score += 25
        flags.append("Seller asked for extra charges AFTER payment — this is Advance Fee Fraud. Stop paying immediately.")

    score = min(score, 100)
    return score, flags


def get_verdict(score):
    if score >= 70:
        return "HIGH RISK", "red"
    elif score >= 35:
        return "CAUTION", "orange"
    else:
        return "LOWER RISK", "green"


def get_guidance(score, answers):
    if score >= 70:
        guidance = [
            "Do NOT send any more money",
            "Block and report this account on Instagram",
            "Report at cybercrime.gov.in if you already paid",
            "Take screenshots of all chats as evidence",
            "Warn your friends and family about this page",
        ]
        if answers.get("extra_charges_after_payment"):
            guidance.insert(1, "STOP paying extra charges — every new charge is another theft")
        return guidance
    elif score >= 35:
        return [
            "Ask seller for a video call showing product RIGHT NOW",
            "Ask seller to photograph product with TODAY'S DATE on paper",
            "Do NOT pay full amount before seeing product",
            "Search seller phone number on Truecaller",
            "Save all chat screenshots before paying",
        ]
    else:
        return [
            "Proceed carefully — always verify before final payment",
            "Prefer partial payment first if possible",
            "Save all chat screenshots before paying",
            "Trust your instincts — if something feels wrong it probably is",
        ]


# ─── HTML Template ───
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BuyShield — Fake Seller Detector</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #0f0f1a; color: #ffffff; min-height: 100vh; }

        .header { background: #1a1a2e; padding: 20px; text-align: center; border-bottom: 3px solid #e94560; }
        .header h1 { font-size: 28px; color: #e94560; }
        .header p { color: #cccccc; margin-top: 6px; font-size: 14px; }

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
        .verdict { font-size: 22px; font-weight: bold; margin-top: 8px; }

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
    <h1>🛡️ BuyShield</h1>
    <p>AI-Powered Fake Instagram Seller Detector — Check Before You Pay</p>
</div>

<div class="container">

{% if not result %}
<div class="intro-card">
    <p>Before paying any Instagram seller, answer these 8 simple questions. BuyShield will analyse the seller behaviour and give you a risk score in seconds. Free. No registration needed.</p>
</div>

<form method="POST" action="/check">
<div class="form-card">
    <h2>Answer about the seller</h2>

    <div class="question">
        <p>1. Did the seller REFUSE a video call showing the product?</p>
        <label><input type="radio" name="refused_video_call" value="yes" required> Yes</label>
        <label><input type="radio" name="refused_video_call" value="no"> No</label>
    </div>

    <div class="question">
        <p>2. Did they demand FULL PAYMENT before showing you the actual product?</p>
        <label><input type="radio" name="payment_before_product" value="yes" required> Yes</label>
        <label><input type="radio" name="payment_before_product" value="no"> No</label>
    </div>

    <div class="question">
        <p>3. Did they REFUSE to photograph the product with today's date written on paper?</p>
        <label><input type="radio" name="refused_date_photo" value="yes" required> Yes</label>
        <label><input type="radio" name="refused_date_photo" value="no"> No</label>
    </div>

    <div class="question">
        <p>4. Did they use urgency like "today only offer" or "last piece left"?</p>
        <label><input type="radio" name="urgency_tactics" value="yes" required> Yes</label>
        <label><input type="radio" name="urgency_tactics" value="no"> No</label>
    </div>

    <div class="question">
        <p>5. Is their Instagram page LESS THAN 1 MONTH old?</p>
        <label><input type="radio" name="page_very_new" value="yes" required> Yes</label>
        <label><input type="radio" name="page_very_new" value="no"> No</label>
    </div>

    <div class="question">
        <p>6. Are their prices UNREALISTICALLY CHEAP compared to market rate?</p>
        <label><input type="radio" name="unrealistic_price" value="yes" required> Yes</label>
        <label><input type="radio" name="unrealistic_price" value="no"> No</label>
    </div>

    <div class="question">
        <p>7. Did they BLOCK YOU or go silent immediately after payment?</p>
        <label><input type="radio" name="blocked_after_payment" value="yes" required> Yes</label>
        <label><input type="radio" name="blocked_after_payment" value="no"> No</label>
    </div>

    <div class="question">
        <p>8. After payment, did they ask for EXTRA MONEY like shipping fee or customs charge?</p>
        <label><input type="radio" name="extra_charges_after_payment" value="yes" required> Yes</label>
        <label><input type="radio" name="extra_charges_after_payment" value="no"> No</label>
    </div>

    <button type="submit" class="submit-btn">🛡️ Check Now</button>
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
        <h3>⚠️ Red Flags Detected ({{ flags|length }})</h3>
        {% for flag in flags %}
        <div class="flag-item">{{ flag }}</div>
        {% endfor %}
    </div>
    {% else %}
    <div class="flags-section">
        <h3>✅ No major red flags detected</h3>
    </div>
    {% endif %}

    <div class="guidance-section">
        <h3>What You Should Do</h3>
        {% for g in guidance %}
        <div class="guidance-item">{{ g }}</div>
        {% endfor %}
    </div>

    {% if score >= 70 %}
    <a href="https://cybercrime.gov.in" target="_blank" class="report-link">🚨 Report This Scam at cybercrime.gov.in</a>
    {% endif %}

    <a href="/" class="check-again">🔄 Check Another Seller</a>
</div>
{% endif %}

<div class="footer">
    BuyShield — Protecting innocent Indian buyers 🛡️<br>
    When in doubt — don't pay. Stay safe.
</div>

</div>
</body>
</html>
"""

# ─── Routes ───
@app.route("/")
def home():
    return render_template_string(HTML, result=False)

@app.route("/check", methods=["POST"])
def check():
    answers = {
        "refused_video_call": request.form.get("refused_video_call") == "yes",
        "payment_before_product": request.form.get("payment_before_product") == "yes",
        "refused_date_photo": request.form.get("refused_date_photo") == "yes",
        "urgency_tactics": request.form.get("urgency_tactics") == "yes",
        "page_very_new": request.form.get("page_very_new") == "yes",
        "unrealistic_price": request.form.get("unrealistic_price") == "yes",
        "blocked_after_payment": request.form.get("blocked_after_payment") == "yes",
        "extra_charges_after_payment": request.form.get("extra_charges_after_payment") == "yes",
    }

    score, flags = calculate_risk_score(answers)
    verdict, color = get_verdict(score)
    guidance = get_guidance(score, answers)

    return render_template_string(HTML,
        result=True,
        score=score,
        flags=flags,
        verdict=verdict,
        color=color,
        guidance=guidance
    )

if __name__ == "__main__":
    app.run()