from datetime import datetime

from mongoengine import DateTimeField, Document


class TimeLoggingDocument:
    created_at = DateTimeField(default=datetime.utcnow, required=True)
    updated_at = DateTimeField(default=datetime.utcnow, required=True)
