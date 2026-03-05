import pandas as pd
import os
from rag_llama_auditor import rag_audit
from llama_scoring import llm_score


def combine_scores(transcript):
    """
    Combines:
    - Soft skill LLM scoring
    - RAG-based compliance auditing
    Returns structured unified result.
    """

    # -----------------------
    # Soft Skill LLM Scoring
    # -----------------------
    try:
        soft_result = llm_score(transcript)
    except Exception as e:
        soft_result = {}

    empathy = soft_result.get("empathy") or 0
    urgency = soft_result.get("urgency") or 0
    politeness = soft_result.get("politeness") or 0

    soft_total = empathy + urgency + politeness

    # -----------------------
    # RAG Compliance Audit
    # -----------------------
    try:
        compliance_result = rag_audit(transcript)
    except Exception as e:
        compliance_result = {}

    compliance_score = compliance_result.get("compliance_score")
    if compliance_score is None:
        compliance_score = 0

    violations = compliance_result.get("violations", [])
    recommendation = compliance_result.get("recommendation", "")

    # -----------------------
    # Final Tag Logic
    # -----------------------
    if soft_total >= 8 and compliance_score >= 4:
        final_tag = "Excellent"
    elif soft_total >= 5 and compliance_score >= 3:
        final_tag = "Acceptable"
    else:
        final_tag = "Needs Improvement"

    return {
        "empathy": empathy,
        "urgency": urgency,
        "politeness": politeness,
        "soft_skill_score": soft_total,
        "compliance_score": compliance_score,
        "violations": violations,
        "recommendation": recommendation,
        "final_tag": final_tag
    }


# ------------------------------------
# MAIN EXECUTION BLOCK
# ------------------------------------
if __name__ == "__main__":

    print("Running Hybrid AI Auditor...\n")

    # Load dataset
    df = pd.read_csv("preprocessed_calls.csv")

    # ⚠️ Always test small first
    subset = df.head(3)

    results = subset["clean_transcript"].apply(combine_scores)

    results_df = pd.json_normalize(results)

    final_df = pd.concat([subset.reset_index(drop=True), results_df], axis=1)

    # Create output folder if not exists
    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/hybrid_ai_scored_calls.csv"
    final_df.to_csv(output_path, index=False)

    print(f"\n✅ Hybrid AI scoring completed successfully!")
    print(f"Saved to: {output_path}")
