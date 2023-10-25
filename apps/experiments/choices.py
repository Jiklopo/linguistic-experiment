from django.db.models import TextChoices


class CorrectSampleChoices(TextChoices):
    FIRST = 'f', 'First'
    SECOND = 'j', 'Second'

    @classmethod
    def to_number(cls, value) -> int:
        if value == cls.FIRST:
            return 1
        elif value == cls.SECOND:
            return 2
        raise ValueError(f'{value} is not among allowed values')
