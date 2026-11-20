import re
import csv
import os
from datetime import datetime

import streamlit as st
from ollama import chat

# ----------------------------------
# Crochet Knowledge Layer
# ----------------------------------

crochet_terms = {
    "Rnd": "Round",
    "rnd": "round",
    "Ch": "Chain",
    "ch": "chain",
    "sc": "single crochet",
    "dc": "double crochet",
    "hdc": "half double crochet",
    "sl st": "slip stitch",
    "inc": "increase",
    "dec": "decrease",
    "st": "stitch"
}

# ----------------------------------
# Page Setup
# ----------------------------------

st.set_page_config(
    page_title="CraftFlow Pattern Explainer",
    page_icon="🧶",
    layout="wide"
)

# ----------------------------------
# App Header
# ----------------------------------

st.title("🧶 CraftFlow AI : Crochet Pattern Explainer")
st.caption(
    "Powered by Phi3 + CraftFlow Crochet Knowledge Layer"
)

st.subheader(
    "Convert crochet patterns into beginner-friendly instructions"
)

# ----------------------------------
# User Type
# ----------------------------------

user_type = st.selectbox(
    "What best describes you?",
    [
        "Beginner Crocheter",
        "Intermediate Crocheter",
        "Advanced Crocheter",
        "Crochet Instructor"
    ]
)

# ----------------------------------
# Pattern Input
# ----------------------------------

pattern = st.text_area(
    "Paste a crochet pattern",
    height=200,
    placeholder="""
Rnd 1: Ch 2, work 6 sc in 2nd ch from hook.

Rnd 2: Inc in each st around.
"""
)

# ----------------------------------
# Explain Pattern
# ----------------------------------

if st.button("Explain Pattern"):

    if pattern.strip() == "":
        st.warning("Please enter a crochet pattern.")

    else:

        # ----------------------------------
        # Expand Crochet Abbreviations
        # ----------------------------------

        expanded_pattern = pattern

        for short, full in crochet_terms.items():
            expanded_pattern = re.sub(
                rf"\b{re.escape(short)}\b",
                full,
                expanded_pattern
            )

        # ----------------------------------
        # Prompt
        # ----------------------------------

        prompt = f"""
You are a crochet teacher.

Explain ONLY the crochet instructions provided.

Rules:

- Explain only the pattern below.
- Stop after the final instruction.
- Do not add extra rounds.
- Do not add extra stitches.
- Do not create examples.
- Do not create alternative patterns.
- Maximum 4 short steps.
- Maximum 80 words.

Pattern:

{expanded_pattern}
"""

        # ----------------------------------
        # Run Phi3
        # ----------------------------------

        with st.spinner("Analyzing pattern..."):

            response = chat(
                model="phi3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0,
                    "num_predict": 120
                }
            )

            explanation = response["message"]["content"]

        # ----------------------------------
        # Clean Up Rambling
        # ----------------------------------

        stop_phrases = [
            "Instruction 2",
            "More difficult",
            "constraints",
            "advanced crochet technique",
            "Difficulty: Intermediate",
            "Difficulty: Advanced",
            "Difficulty: Expert",
            "Difficulty: Master",
            "Difficulty: Grandmaster",
            "Difficulty: Legend",
            "Pattern:",
            "Round 3:",
            "Round 4:",
            "Round 5:"
        ]

        for phrase in stop_phrases:
            if phrase in explanation:
                explanation = explanation.split(phrase)[0]

        explanation = explanation.strip()

        # ----------------------------------
        # Save Session Data
        # ----------------------------------

        st.session_state["pattern"] = pattern
        st.session_state["expanded_pattern"] = expanded_pattern
        st.session_state["explanation"] = explanation

        # ----------------------------------
        # Show Results
        # ----------------------------------

        st.success("Explanation ready!")

        st.markdown("### Beginner-Friendly Explanation")
        st.write(explanation)

        with st.expander("See Expanded Pattern"):
            st.code(expanded_pattern)

# ----------------------------------
# Feedback Section
# ----------------------------------

if "explanation" in st.session_state:

    st.markdown("---")

    st.subheader("Feedback")

    feedback = st.radio(
        "Was this explanation helpful?",
        [
            "👍 Yes",
            "👎 No"
        ]
    )

    comments = st.text_area(
        "Additional comments (optional)",
        placeholder="Tell us what was helpful or confusing..."
    )

    if st.button("Submit Feedback"):

        feedback_file = "feedback.csv"

        file_exists = os.path.isfile(feedback_file)

        with open(
            feedback_file,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Timestamp",
                    "User Type",
                    "Helpful",
                    "Pattern",
                    "Expanded Pattern",
                    "Explanation",
                    "Comments"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_type,
                feedback,
                st.session_state["pattern"],
                st.session_state["expanded_pattern"],
                st.session_state["explanation"],
                comments
            ])

        st.success(
            "✅ Feedback saved successfully. Thank you!"
        )

