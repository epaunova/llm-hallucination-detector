import streamlit as st
from collections import Counter
import pandas as pd

# -- CUSTOM STYLE --
st.markdown(
    """
    <style>
    .st-emotion-cache-18ni7ap { /* Main background */
        background: #fcf6f0;
    }
    .st-emotion-cache-6qob1r { /* Sidebar */
        background-color: #ffe5dc !important;
    }
    .st-emotion-cache-1v0mbdj h1 { /* H1 Header */
        color: #c44536 !important;
    }
    .eva-logo {
        display: flex; align-items: center; gap: 14px; margin-bottom: 0.2em;
    }
    .eva-logo-img {
        width: 40px; height: 40px; border-radius: 50%; border: 2px solid #c44536;
        object-fit: cover; background: #fff;
    }
    .eva-title {
        font-size: 2.0em; color: #c44536; font-weight: bold; letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# -- HEADER с "лого" (инициал/иконка или сложи URL към твой PNG/JPG) --
st.markdown(
    """
    <div class="eva-logo">
        <img src="https://cdn-icons-png.flaticon.com/512/3940/3940417.png" class="eva-logo-img">
        <span class="eva-title">LLM Hallucination & Robustness Detector</span>
    </div>
    <p>Paste your LLM output below. The app will highlight likely hallucination patterns and let you rate factuality.</p>
    """, unsafe_allow_html=True)

output = st.text_area("LLM Output", height=180)

hallucination_triggers = [
    "as far as I know", "no evidence", "unable to find", "I do not know",
    "there is no record", "not aware of", "cannot be confirmed",
    "cannot guarantee", "fictional", "hypothetical", "it is believed",
    "rumored", "some sources claim", "this may not be accurate"
]

highlighted = output
for trigger in hallucination_triggers:
    if trigger in output.lower():
        highlighted = highlighted.replace(trigger, f"<mark style='background-color: #ffc2c2'>{trigger}</mark>")

if output:
    st.markdown("### 🔎 Highlighted Output")
    st.markdown(highlighted, unsafe_allow_html=True)

    st.markdown("### 🧠 Manual Factuality Check")
    fact_score = st.slider("How factual is this output? (0 = totally hallucinated, 1 = fully factual)", 0.0, 1.0, 0.5, 0.01)
    st.info(f"Manual factuality score: **{fact_score:.2f}**")

    # Simple score: counts how many trigger phrases are present
    n_triggers = sum(trigger in output.lower() for trigger in hallucination_triggers)
    st.markdown(f"**Detected {n_triggers} possible hallucination phrase(s).**")
    if n_triggers == 0:
        st.success("✅ No obvious hallucination patterns found. (Not a guarantee, but a good sign!)")
    elif n_triggers == 1:
        st.warning("⚠️ 1 possible hallucination pattern detected.")
    else:
        st.error(f"🚨 {n_triggers} possible hallucination patterns detected!")

    # ------ AUTO LLM EVALUATION ------
    st.markdown("### 🤖 Auto LLM Evaluation (Simulated)")
    if st.button("Run Auto Fact-Check"):
        verdicts = [
            ("LLM: This output is likely factual.", "success"),
            ("LLM: Possible hallucination detected.", "warning"),
            ("LLM: Hallucination pattern detected. Needs human review.", "error")
        ]
        if n_triggers == 0:
            msg, style = verdicts[0]
        elif n_triggers == 1:
            msg, style = verdicts[1]
        else:
            msg, style = verdicts[2]
        if style == "success":
            st.success(msg)
        elif style == "warning":
            st.warning(msg)
        else:
            st.error(msg)

    # ------ TOXICITY DETECTION ------
    toxicity_words = [
        "idiot", "stupid", "dumb", "hate", "useless", "shut up", "kill", "bastard", "moron", "sucks", "fool",
        "garbage", "trash", "loser", "ugly", "nonsense", "dick", "asshole"
    ]
    toxic_found = [word for word in toxicity_words if word in output.lower()]
    st.markdown("### ☢️ Toxicity Detection")
    if toxic_found:
        st.error(f"⚠️ Toxic language detected: {', '.join(toxic_found)}")
    else:
        st.success("No obvious toxicity found.")

    # ------ HALLUCINATION TRIGGERS BAR CHART ------
    triggers_count = Counter()
    for trigger in hallucination_triggers:
        count = output.lower().count(trigger)
        if count > 0:
            triggers_count[trigger] = count

    if triggers_count:
        st.markdown("### 📊 Top Hallucination Patterns")
        df_triggers = pd.DataFrame(triggers_count.items(), columns=["Phrase", "Count"]).sort_values(by="Count", ascending=False)
        st.bar_chart(df_triggers.set_index("Phrase"))

st.markdown("""
---
<small>
By Eva Paunova | Demo for LLM hallucination & robustness testing.<br>
[GitHub](https://github.com/epaunova)
</small>
""", unsafe_allow_html=True)
