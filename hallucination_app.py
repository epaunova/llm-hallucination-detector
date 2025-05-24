
import streamlit as st

st.markdown(
    """
    <h1 style='color:#c44536;'>🤖 LLM Hallucination & Robustness Detector</h1>
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

    # ------ ТУК ДОБАВЯМЕ АВТОМАТИЧНАТА LLM ПРОВЕРКА -------
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
    # ------ КРАЙ НА LLM ПРОВЕРКАТА ------

st.markdown("""
---
<small>
By Eva Paunova | Demo for LLM hallucination & robustness testing.<br>
[GitHub](https://github.com/epaunova)
</small>
""", unsafe_allow_html=True)
