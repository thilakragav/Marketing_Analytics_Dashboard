def route_question(question: str, current_page: str) -> str:

    question_lower = question.lower().strip()

    if "highest roas" in question_lower and "campaign" in question_lower:
        return "CMO Executive Summary"

    if "traffic decline" in question_lower:
        return "GA4 Analytics"

    if "keyword" in question_lower or "keywords" in question_lower:
        return "SEO Performance"

    return current_page