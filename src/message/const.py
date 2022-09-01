class MessageTemplate:
    MANGA_RELEASE = {
        "TITLE": "Manga Release - {manga_name}",
        "DESCRIPTION": "Chapter {chapter_number} has been released. Check it out.",
    }
    EXPENSE_ADDED = "Thanks, I've noted the expenses for {date}."
    EXPENSE_MISSING = "Please provide the expenses."
    EXPENSE_REPORTED = "Here is your report:"
    EXPENSE_REPORTED_FAILED = "I can't generate the report, maybe you haven't spent anything yet."
    TECHNICAL_ISSUE = "A technical issue happens, please contact the engineering team."


class AppName:
    EXPENSE = "expense"
    REPORT = "report"
    UNCATEGORIZED = "uncategorized"
