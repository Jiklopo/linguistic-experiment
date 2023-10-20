from rest_framework import serializers

from apps.experiments.single_choice_models import SingleChoiceQuestion, SingleChoiceResult, SingleChoiceAnswer


class AnswerSerializer(serializers.Serializer):
    time_elapsed = serializers.IntegerField()
    response = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=SingleChoiceQuestion.objects.all(), required=False)


class SingleChoiceResultSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        result = SingleChoiceResult.objects.create(raw_json=self.initial_data['answers'])
        answers = []
        for i, ans in enumerate(answers_data):
            if 'question_id' not in ans:
                continue

            response_time = ans['time_elapsed'] - answers_data[i - 1]['time_elapsed']
            answers.append(SingleChoiceAnswer(
                result=result,
                question=ans['question_id'],
                selected_sample=ans['response'],
                is_correct=ans['response'] == ans['question_id'].correct_sample,
                response_time_ms=response_time
            ))

        SingleChoiceAnswer.objects.bulk_create(answers)
        return result

    class Meta:
        model = SingleChoiceResult
        fields = ['answers']
