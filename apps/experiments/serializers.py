from rest_framework import serializers

from apps.experiments.models import SingleChoiceQuestion, SingleChoiceResult, SingleChoiceAnswer


class AnswerSerializer(serializers.Serializer):
    response = serializers.ChoiceField(choices=(0, 1))
    question_id = serializers.PrimaryKeyRelatedField(queryset=SingleChoiceQuestion.objects.all())


class SingleChoiceResultSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)
    raw_json = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        result = SingleChoiceResult.objects.create(raw_json=validated_data['raw_json'])
        answers = []
        for ans in answers_data:
            answers.append(SingleChoiceAnswer(
                result=result,
                question=ans['question_id'],
                selected_sample=ans['response'],
                is_correct=ans['response'] == ans['question_id'].correct_sample
            ))

        SingleChoiceAnswer.objects.bulk_create(answers)
        return result

    class Meta:
        model = SingleChoiceResult
        fields = ['answers', 'raw_json']
