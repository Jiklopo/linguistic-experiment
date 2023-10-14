from django.db.models import IntegerChoices


class CorrectSampleChoices(IntegerChoices):
    FIRST = 0, 'First'
    SECONDS = 1, 'Second'
