from django.db.models import TextChoices


class CorrectSampleChoices(TextChoices):
    FIRST = 'f', 'First'
    SECOND = 's', 'Second'
