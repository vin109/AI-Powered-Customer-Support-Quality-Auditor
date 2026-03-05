import ollama
import json
from pinecone_rag_engine import retrieve_context


def rag_audit(transcript):
    """
    Enterprise AI Quality & Compliance Auditor
    Returns structured JSON with multi-dimensional scoring.
    """

    # Retrieve relevant policies from Pinecone
    context = retrieve_context(transcript)

    # ---------------- PROMPT ----------------
    prompt = f"""
You are a strict enterprise-level Customer Support Quality Auditor.

You MUST return ONLY valid JSON.
Do NOT include explanations.
Do NOT include markdown.
Do NOT include text before or after JSON.

You MUST be critical and deduct marks where appropriate.

SCORING RULES (STRICT):

Empathy (0-100):
- 90-100 → Strong emotional acknowledgment + apology
- 60-89 → Some empathy shown
- 30-59 → Weak empathy
- 0-29 → No empathy

Professionalism (0-100):
- Based on politeness, tone, clarity.

Compliance (0-100):
- 90-100 → Fully compliant, zero violations.
- 70-89 → Minor gaps.
- 40-69 → Clear violations.
- 0-39 → Major violations.

Resolution Quality (0-100):
- Based on clarity, correctness, actionability of solution.

IMPORTANT:
If there are violations, compliance score MUST be below 85.

POLICIES:
{context}

TRANSCRIPT:
{transcript}

Return STRICT JSON in this format:

{{
  "empathy_score": number,
  "professionalism_score": number,
  "compliance_score": number,
  "resolution_quality_score": number,
  "overall_score": number,
  "violations": ["string"],
  "recommendation": "short improvement suggestion"
}}
"""

    # ---------------- CALL LLAMA ----------------
    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}],
        options={"temperature": 0}
    )

    content = response['message']['content']
    print("\nRAW LLM OUTPUT:\n")
    print(content)

    # ---------------- BULLETPROOF JSON EXTRACTION ----------------
    try:
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON object detected.")

        json_str = content[start:end]
        parsed = json.loads(json_str)

        return parsed

    except Exception as e:
        print("\nJSON Parsing Failed:", e)

        return {
            "empathy_score": None,
            "professionalism_score": None,
            "compliance_score": None,
            "resolution_quality_score": None,
            "overall_score": None,
            "violations": [],
            "recommendation": "JSON parsing error"
        }


# ---------------- TEST BLOCK ----------------
if __name__ == "__main__":

    print("Running Enterprise AI Quality Auditor...\n")

    test_transcript = """
Customer: My internet has been down for two days and I need it fixed immediately!
Agent: Please restart your router.
"""

    result = rag_audit(test_transcript)

    print("\n===== AI QUALITY AUDIT RESULT =====\n")
    print(result)