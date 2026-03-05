import streamlit as st
from rag_llama_auditor import rag_audit

st.set_page_config(
    page_title="AI Compliance Auditor",
    layout="wide"
)

st.title("📞 AI Customer Support Compliance Auditor")

st.markdown("Evaluate customer support calls using RAG + Pinecone + Llama")

# -----------------------------
# Transcript Input
# -----------------------------
st.subheader("📝 Enter Call Transcript")

transcript = st.text_area(
    "Paste transcript here:",
    height=200
)

# -----------------------------
# Run Audit Button
# -----------------------------
if st.button("Run AI Audit"):

    if transcript.strip() == "":
        st.warning("Please enter a transcript.")
    else:
        with st.spinner("Running AI Auditor..."):

            result = rag_audit(transcript)

        st.subheader("📊 Audit Results")

        st.metric("Compliance Score", result.get("compliance_score", "N/A"))

        st.write("### Violations")
        violations = result.get("violations", [])

        if violations:
            for v in violations:
                st.write(f"- {v}")
        else:
            st.write("No violations detected.")

        st.write("### Recommendation")
        st.info(result.get("recommendation", "No recommendation available"))
