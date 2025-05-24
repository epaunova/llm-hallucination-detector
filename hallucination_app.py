import streamlit as st
from collections import Counter
import pandas as pd

# -- CUSTOM STYLE --
st.markdown(
    """
    <style>
    .st-emotion-cache-18ni7ap {background: #fcf6f0;}
    .st-emotion-cache-6qob1r {background-color: #ffe5dc !important;}
    .eva-logo {display: flex; align-items: center; gap: 14px; margin-bottom: 0.2em;}
    .eva-logo-img {width: 40px; height: 40px; border-radius: 50%; border: 2px solid #c44536; object-fit: cover; background: #fff;}
    .eva-title {font-size: 2.0em; color: #c44536; font-weight: bold; letter-spacing: 1px;}
    </style>
    """, unsafe_allow_html=True)

# -- HEADER с "лого" (може да смениш линка към друго PNG/JPG) --
st.markdown(
    """
    <div class="eva-logo">
        <img src="https://cdn-icons-png.flaticon.com/512/3940/3940417.png" class="eva-logo-img">
        <span class="eva-title">LLM Hallucination & Robustness Detector</span>
    </div>
    <p>Paste your LLM output below. The app will highlight likely hallucination patterns and let you rate factuality.</p>
    """, unsafe_allow_html=True)

hallucination_triggers = [
    "as far as I know", "no evidence", "unable to find", "I do not know",
    "there is no record", "not aware of", "cannot be confirmed",
    "cannot guarantee", "fictional", "hypothetical", "it is believed",
    "rumored", "some sources claim", "this may not be accurate"
]
toxicity_words = [
    "idiot", "stupid", "dumb", "hate", "useless", "shut up", "kill", "bastard", "moron", "sucks", "fool",
    "garbage", "trash", "loser", "ugly", "nonsense", "dick", "asshole"
]

batch_mode = st.checkbox("Batch mode (analyze multiple outputs)", value=False)
if batch_mode:
    st.info("Paste multiple LLM outputs, separated by three dashes (---) or empty lines.")
    multi_outputs = st.text_area("LLM Outputs (batch)", height=240)
    # Split by '---' or blank lines
    outputs = [o.strip() for o in multi_outputs.replace('\n\n', '\n---\n').split('---') if o.strip()]
    if outputs:
        batch_results = []
        all_triggers = Counter()
        n_toxic = 0
        manual_scores = []
        for i, out in enumerate(outputs, 1):
            triggers = [tr for tr in hallucination_triggers if tr in out.lower()]
            toxic = [tw for tw in toxicity_words if tw in out.lower()]
            all_triggers.update(triggers)
            score = st.slider(f"Manual factuality for Output {i}", 0.0, 1.0, 0.5, 0.01, key=f"score_{i}")
            manual_scores.append(score)
            if toxic:
                n_toxic += 1
            batch_results.append({
                "index": i,
                "triggers": len(triggers),
                "toxic": bool(toxic),
                "score": score
            })
        st.markdown(f"**Total outputs:** {len(outputs)}")
        st.markdown(f"**Outputs with hallucination triggers:** {sum(r['triggers']>0 for r in batch_results)}")
        st.markdown(f"**Outputs with toxicity:** {n_toxic}")
        st.markdown(f"**Average factuality score:** {sum(manual_scores)/len(manual_scores):.2f}")
        if all_triggers:
            df_tr = pd.DataFrame(all_triggers.items(), columns=["Phrase", "Count"]).sort_values(by="Count", ascending=False)
            st.markdown("#### 📊 Trigger Phrase Distribution (all outputs)")
            st.bar_chart(df_tr.set_index("Phrase"))
else:
    output = st.text_area("LLM Output", height=180)

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
