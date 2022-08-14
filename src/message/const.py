class MessageTemplate:
    MANGA_RELEASE = {
        "TITLE": "Manga Release - {manga_name}",
        "DESCRIPTION": "Chapter {chapter_number} has been released. Check it out.",
    }
    EXPENSE_ADDED = "Thanks, I've noted the expenses for {date}"
    EXPENSE_MISSING = "Please provide the expenses"
    TECHNICAL_ISSUE = "A technical issue happens, please contact the engineering team"


class AppName:
    EXPENSE = "expense"
    REPORT = "report"
    UNCATEGORIZED = "uncategorized"
