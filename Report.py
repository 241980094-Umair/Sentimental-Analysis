HUMAN_INSIGHTS = {
    "pride": {
        "summary": "Expresses genuine satisfaction and personal validation.",
        "tone": "Warm, Affirmative & Supportive",
        "analysis": "The statement carries strong positive reinforcement, aiming to uplift and validate effort or achievement."
    },
    "joy": {
        "summary": "Radiates high positive energy and happiness.",
        "tone": "Upbeat, Energetic & Optimistic",
        "analysis": "The language points to clear enthusiasm and contentment with an underlying feeling of delight."
    },
    "admiration": {
        "summary": "Conveys high respect and appreciation.",
        "tone": "Respectful, Warm & Esteemed",
        "analysis": "Demonstrates clear regard toward an individual, effort, or accomplishment."
    },
    "gratitude": {
        "summary": "Expresses sincere thankfulness and recognition.",
        "tone": "Appreciative & Grounded",
        "analysis": "Focuses on acknowledging support, kindness, or positive circumstances."
    },
    "neutral": {
        "summary": "Maintains an objective and matter-of-fact tone.",
        "tone": "Balanced & Clear",
        "analysis": "Functions as conversational context or factual communication without heavy emotional bias."
    },
    "relief": {
        "summary": "Signals a release of stress or uncertainty.",
        "tone": "Reassuring & Relaxed",
        "analysis": "Reflects emotional ease following the resolution of a prior concern."
    }
}

DEFAULT_INSIGHT = {
    "summary": "Conveys a clear and focused emotional expression.",
    "tone": "Direct & Expressive",
    "analysis": "The statement exhibits clear intent aligned with its primary category."
}

def generate_emotion_report_html(predictions: list, text: str = ""):
    if not predictions:
        return "<div style='padding:15px; border:3px solid var(--text-color, #000);'>No emotions detected.</div>", ""

    primary_label, primary_score = predictions[0]
    primary_key = str(primary_label).lower()
    insight = HUMAN_INSIGHTS.get(primary_key, DEFAULT_INSIGHT)

    secondary_html = ""
    if len(predictions) > 1:
        badges = "".join([
            f"<span style='display:inline-block; border:2px solid var(--text-color, #000); padding:4px 8px; font-weight:700; font-size:0.85rem; margin-right:6px;'>{str(lbl).title()} ({score:.1%})</span>" 
            for lbl, score in predictions[1:]
        ])
        secondary_html = f"<div style='margin-top:15px; border-top:2px solid var(--text-color, #000); padding-top:12px;'><div style='font-weight:900; font-size:0.8rem; opacity:0.75; text-transform:uppercase; margin-bottom:6px;'>SECONDARY UNDERTONES</div><div>{badges}</div></div>"

    html_content = (
        f"<div style='border:4px solid var(--text-color, #000000); box-shadow:6px 6px 0px var(--text-color, #000000); padding:20px; margin-bottom:20px; font-family:sans-serif;'>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; border-bottom:3px solid var(--text-color, #000); padding-bottom:10px; margin-bottom:15px;'>"
        f"<span style='font-weight:900; font-size:1.2rem; background:#FFDE59; color:#000000; padding:4px 10px; border:2px solid #000;'>PRIMARY: {str(primary_label).upper()}</span>"
        f"<span style='font-weight:900; font-size:1.1rem;'>{primary_score:.1%} CONFIDENCE</span>"
        f"</div>"
        f"<div style='margin-bottom:14px;'>"
        f"<div style='font-weight:900; font-size:0.8rem; opacity:0.75; text-transform:uppercase; margin-bottom:2px;'>Summary</div>"
        f"<div style='font-size:1.1rem; font-weight:700;'>{insight['summary']}</div>"
        f"</div>"
        f"<div style='display:grid; grid-template-columns:1fr 1fr; gap:12px; border-top:2px solid var(--text-color, #000); padding-top:12px;'>"
        f"<div><div style='font-weight:900; font-size:0.8rem; opacity:0.75; text-transform:uppercase; margin-bottom:2px;'>DOMINANT TONE</div><div style='font-weight:700; font-size:0.95rem;'>{insight['tone']}</div></div>"
        f"<div><div style='font-weight:900; font-size:0.8rem; opacity:0.75; text-transform:uppercase; margin-bottom:2px;'>DESCRIPTION</div><div style='font-weight:700; font-size:0.95rem;'>{insight['analysis']}</div></div>"
        f"</div>"
        f"{secondary_html}"
        f"</div>"
    )
    
    return html_content, insight["analysis"]