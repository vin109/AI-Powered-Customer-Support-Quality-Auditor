import streamlit as st
from rag_llama_auditor import rag_audit
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import io
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Quality & Compliance Auditor",
    page_icon="📞",
    layout="wide"
)

# ---------------- SESSION STATE INIT ----------------
if "audit_result" not in st.session_state:
    st.session_state.audit_result = None

if "audit_transcript" not in st.session_state:
    st.session_state.audit_transcript = ""

# ---------------- STYLING ----------------
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #3b82f6, #9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    font-size: 18px;
    color: #9ca3af;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="big-title">AI Customer Support Quality Auditor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Cloud RAG (Pinecone) + Local Llama • Enterprise Report System</div>', unsafe_allow_html=True)

st.divider()

# ---------------- PDF GENERATOR ----------------
def generate_pdf(transcript, result):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("AI Customer Support Quality Audit Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Transcript:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(transcript, styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    score_data = [
        ["Metric", "Score"],
        ["Empathy", result.get("empathy_score", 0)],
        ["Professionalism", result.get("professionalism_score", 0)],
        ["Compliance", result.get("compliance_score", 0)],
        ["Resolution Quality", result.get("resolution_quality_score", 0)],
        ["Overall", result.get("overall_score", 0)]
    ]

    table = Table(score_data, colWidths=[3 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Policy Violations:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))

    violations = result.get("violations", [])

    if violations:
        violation_list = [ListItem(Paragraph(v, styles["Normal"])) for v in violations]
        elements.append(ListFlowable(violation_list, bulletType='bullet'))
    else:
        elements.append(Paragraph("No violations detected.", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>AI Recommendation:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(result.get("recommendation", ""), styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- EMAIL FUNCTION ----------------
def send_email_with_pdf(receiver_email, pdf_buffer):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        st.error("Email credentials not configured in .env file.")
        return False

    msg = EmailMessage()
    msg["Subject"] = "AI Quality Audit Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find attached the AI-generated Quality Audit Report.")

    msg.add_attachment(
        pdf_buffer.getvalue(),
        maintype="application",
        subtype="pdf",
        filename="AI_Quality_Audit_Report.pdf"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    return True

# ---------------- INPUT ----------------
st.subheader("📝 Enter Call Transcript")

transcript = st.text_area(
    "",
    height=220,
    placeholder="Customer: ...\nAgent: ...",
    value=st.session_state.audit_transcript
)

st.divider()

# ---------------- RUN BUTTON ----------------
if st.button("🚀 Run AI Audit", use_container_width=True):

    if transcript.strip() == "":
        st.warning("Please enter a transcript.")
        st.stop()

    with st.spinner("Analyzing transcript with AI..."):
        result = rag_audit(transcript)

    # SAVE TO SESSION STATE
    st.session_state.audit_result = result
    st.session_state.audit_transcript = transcript

# ---------------- DISPLAY RESULTS IF EXISTS ----------------
if st.session_state.audit_result:

    result = st.session_state.audit_result
    transcript = st.session_state.audit_transcript

    empathy = result.get("empathy_score", 0)
    professionalism = result.get("professionalism_score", 0)
    compliance = result.get("compliance_score", 0)
    resolution = result.get("resolution_quality_score", 0)
    overall = result.get("overall_score", 0)
    violations = result.get("violations", [])
    recommendation = result.get("recommendation", "")

    st.divider()
    st.subheader("📊 Quality Breakdown (0–100)")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Empathy", empathy)
    col2.metric("Professionalism", professionalism)
    col3.metric("Compliance", compliance)
    col4.metric("Resolution", resolution)
    col5.metric("Overall", overall)

    st.divider()

    st.subheader("📈 Score Visualization")

    st.write("Empathy")
    st.progress(empathy / 100)

    st.write("Professionalism")
    st.progress(professionalism / 100)

    st.write("Compliance")
    st.progress(compliance / 100)

    st.write("Resolution Quality")
    st.progress(resolution / 100)

    st.write("Overall Score")
    st.progress(overall / 100)

    st.divider()

    st.subheader("🚨 Policy Violations")
    if violations:
        for v in violations:
            st.error(v)
    else:
        st.success("No violations detected.")

    st.divider()

    st.subheader("💡 AI Recommendation")
    st.info(recommendation)

    st.divider()

    # ---------------- PDF DOWNLOAD ----------------
    pdf_file = generate_pdf(transcript, result)

    st.download_button(
        label="📄 Download Audit Report (PDF)",
        data=pdf_file,
        file_name="AI_Quality_Audit_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.divider()

    # ---------------- EMAIL SECTION ----------------
    st.subheader("📧 Send Report via Email")

    receiver = st.text_input("Enter recipient email")

    if st.button("Send Email"):
        if receiver:
            if send_email_with_pdf(receiver, pdf_file):
                st.success("Report sent successfully!")
        else:
            st.warning("Please enter an email address.")

st.divider()
st.caption("Built with Streamlit • Pinecone • Ollama • Llama3")