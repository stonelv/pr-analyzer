from ..core.config import settings

BASIC_PR_PROMPT = """
You are an AI assistant helping summarize code changes in a Merge Request.
Provide:
1. Overall intent
2. Key modified components
3. Potential risks (list)
4. Suggested reviewer focus points
Return concise bullet points.
""".strip()

def generate_basic_summary(pr_title: str, diff_snippet: str) -> dict:
    # Placeholder: later integrate OpenAI or local LLM.
    # For MVP scaffolding we just template.
    summary_text = f"Intent: {pr_title}\nKey Changes: (placeholder)\nRisks: (placeholder)\nFocus: Review sensitive areas."
    return {"summary": summary_text, "model": settings.LLM_PROVIDER, "version": 1}
