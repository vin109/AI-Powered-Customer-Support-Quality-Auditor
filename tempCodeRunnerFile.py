import ollama
import json
import re
from pinecone_rag_engine import retrieve_context



def rag_audit(transcript):
    """
    Audits a transcript using RAG + Local Llama
    Returns structured JSON output.
    """

    context = retrieve_context(transcript)

    prompt = f"""
You are a JSON-only compliance evaluation engine.

You MUST return ONLY valid JSON.

If you output anything other than JSON, the response is invalid.

Do NOT include:
- explanations
- markdown
- text before JSON
- text after JSON

Use the policies to evaluate compliance.

POLICIES:
{context}

TRANSCRIPT:
{transcript}

Return strictly this format:

{{
  "compliance_score": 0-5,
  "violations": ["string", "string"],
  "recommendation": "short sentence"
}}
"""


    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}],
        options={"temperature": 0}
    )

    content = response['message']['content']
    print("\nRAW LLM OUTPUT:\n")
    print(content)


    # 🔥 Bulletproof JSON extraction
    json_match = re.search(r'\{.*\}', content, re.DOTALL)

    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            return {
                "compliance_score": None,
                "violations": [],
                "recommendation": "JSON parsing error"
            }
    else:
        return {
            "compliance_score": None,
            "violations": [],
            "recommendation": "No JSON returned"
        }


# ✅ TEST BLOCK (VERY IMPORTANT)
if __name__ == "__main__":

    print("Running AI RAG Auditor...\n")

    test_transcript = """
Customer: My internet has been down for two days and I need it fixed immediately!
Agent: Please restart your router.
"""

    result = rag_audit(test_transcript)

    print("===== AI AUDIT RESULT =====\n")
    print(result)
