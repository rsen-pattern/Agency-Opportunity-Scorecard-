import streamlit as st

st.set_page_config(page_title="Agency Opportunity Scorecard", page_icon="🎯", layout="centered")

st.markdown("""
<style>
    .verdict-box { border-radius: 12px; padding: 24px; text-align: center; margin-top: 24px; }
    .strong { background-color: #d4edda; border: 2px solid #28a745; }
    .possible { background-color: #fff3cd; border: 2px solid #ffc107; }
    .longshot { background-color: #f8d7da; border: 2px solid #dc3545; }
    .score-big { font-size: 64px; font-weight: 800; line-height: 1; }
    .verdict-label { font-size: 22px; font-weight: 600; margin-top: 8px; }
    .section-header { font-size: 17px; font-weight: 700; color: #1a1a2e; border-left: 4px solid #4361ee; padding-left: 10px; margin-top: 28px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Agency Opportunity Scorecard")
st.caption("Evaluate whether a new business opportunity is worth pursuing.")

QUESTIONS = {
    "Competitive Landscape": [
        {"id": "Q1", "label": "Number of competing agencies", "hint": "Fewer competitors = higher score",
         "options": [("1–2 agencies", 20), ("3–4 agencies", 6), ("5–6 agencies", 2), ("7+ agencies", 0)]},
        {"id": "Q2", "label": "Incumbent status", "hint": "Are we defending or challenging?",
         "options": [("We are the incumbent", 8), ("Challenger — incumbent is weak", 5), ("No incumbent / unknown", 4), ("Challenger — incumbent is strong", 2)]},
        {"id": "Q3", "label": "Do you know who the other agencies are?", "hint": "Known competitors allow better strategy",
         "options": [("Yes — all known & we compare well", 4), ("Yes — but competition is strong", 2), ("No — mostly unknown", 1)]},
    ],
    "Relationship & History": [
        {"id": "Q4", "label": "Prior relationship with client", "hint": "Existing relationships increase win rate",
         "options": [("Previous client — positive history", 8), ("Met them but never worked together", 4), ("No prior relationship", 1)]},
        {"id": "Q5", "label": "Pitch origin", "hint": "Inbound pitches signal stronger intent",
         "options": [("Inbound — they approached us", 6), ("Outbound — we approached them", 2)]},
        {"id": "Q6", "label": "Internal champion / sponsor", "hint": "An advocate inside the brand is a strong signal",
         "options": [("Yes — identified & engaged", 6), ("Possible but unconfirmed", 3), ("No internal champion", 0)]},
        {"id": "Q7", "label": "LinkedIn connections at the brand", "hint": "Network depth at the client",
         "options": [("5+ connections", 4), ("2–4 connections", 2), ("1 connection", 1), ("None", 0)]},
    ],
    "Brief & Process": [
        {"id": "Q8", "label": "Brief quality & alignment", "hint": "How well does it match our strengths?",
         "options": [("Detailed brief — strong fit", 6), ("Good brief — partial fit", 4), ("Vague brief or weak fit", 1)]},
        {"id": "Q9", "label": "Access to decision-maker", "hint": "Chemistry meeting or direct contact",
         "options": [("Yes — chemistry meeting held", 4), ("Some contact but no formal meeting", 2), ("No access to decision-maker", 0)]},
        {"id": "Q10", "label": "Time given to prepare", "hint": "More time benefits challengers",
         "options": [("3+ weeks", 3), ("1–3 weeks", 2), ("Under 1 week", 0)]},
    ],
    "Commercial Opportunity": [
        {"id": "Q11", "label": "Overall $ value of the opportunity", "hint": "Larger accounts justify more investment",
         "options": [("$500k+", 5), ("$200k–$500k", 4), ("$100k–$200k", 3), ("Under $100k", 1)]},
        {"id": "Q12", "label": "Growth potential beyond initial brief", "hint": "Can this account expand over time?",
         "options": [("High — clear expansion opportunity", 3), ("Medium — some potential", 2), ("Low — likely stays as scoped", 1)]},
        {"id": "Q13", "label": "Budget realism", "hint": "Does the budget match the scope?",
         "options": [("Budget is realistic for scope", 3), ("Slightly underfunded but workable", 2), ("Budget too low for scope", 0)]},
    ],
    "Scope & Category": [
        {"id": "Q14", "label": "Number of channels pitched for", "hint": "More channels = more value & stickiness",
         "options": [("5+ channels", 5), ("3–4 channels", 4), ("2 channels", 2), ("1 channel", 1)]},
        {"id": "Q15", "label": "Client category", "hint": "How strong is your category expertise?",
         "options": [("Core category (fashion / beauty)", 5), ("Adjacent category", 3), ("New/unfamiliar category (automotive)", 1)]},
        {"id": "Q16", "label": "Strategic fit for agency portfolio", "hint": "Does winning help your agency's story?",
         "options": [("Trophy client or new category win", 3), ("Good fit — not transformational", 2), ("Limited strategic value", 1)]},
    ],
}

MAX_PER_CATEGORY = {
    "Competitive Landscape": 32,
    "Relationship & History": 24,
    "Brief & Process": 13,
    "Commercial Opportunity": 11,
    "Scope & Category": 13,
}

answers = {}
total_questions = sum(len(qs) for qs in QUESTIONS.values())

for category, questions in QUESTIONS.items():
    max_pts = MAX_PER_CATEGORY[category]
    st.markdown(f'<div class="section-header">{category} &nbsp;<span style="font-weight:400;font-size:13px;color:#888">Max {max_pts} pts</span></div>', unsafe_allow_html=True)
    for q in questions:
        option_labels = [o[0] for o in q["options"]]
        choice = st.selectbox(
            f"{q['label']} — *{q['hint']}*",
            options=["— Select —"] + option_labels,
            key=q["id"],
        )
        answers[q["id"]] = dict(q["options"]).get(choice)

st.divider()

answered = [v for v in answers.values() if v is not None]
total_answered = len(answered)
score = sum(answered)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**Progress:** {total_answered} / {total_questions} questions answered")
    st.progress(total_answered / total_questions)
with col2:
    if total_answered > 0:
        st.metric("Score so far", f"{score}")

if total_answered == total_questions:
    if score >= 70:
        css_class, verdict = "strong", "✅ Strong Chance"
        description = "This opportunity is worth a full pursuit. Prioritise resources and go all in."
        color = "#28a745"
    elif score >= 45:
        css_class, verdict = "possible", "⚠️ Possible"
        description = "Proceed with caution. Identify your gaps and address them before committing fully."
        color = "#856404"
    else:
        css_class, verdict = "longshot", "❌ Long Shot"
        description = "Significant barriers exist. Consider whether the investment is justified."
        color = "#721c24"

    st.markdown(f"""
    <div class="verdict-box {css_class}">
        <div class="score-big" style="color:{color}">{score}</div>
        <div style="color:#777;font-size:14px">out of 100 points</div>
        <div class="verdict-label" style="color:{color}">{verdict}</div>
        <div style="margin-top:10px;font-size:15px;color:#333">{description}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Score Breakdown by Category")
    for category, questions in QUESTIONS.items():
        q_ids = [q["id"] for q in questions]
        cat_score = sum(answers[qid] for qid in q_ids if answers.get(qid) is not None)
        cat_max = MAX_PER_CATEGORY[category]
        st.markdown(f"**{category}** — {cat_score} / {cat_max}")
        st.progress(cat_score / cat_max)

elif total_answered > 0:
    st.info(f"Answer all {total_questions} questions to see your final verdict.")
else:
    st.info("Answer the questions above to score this opportunity.")
