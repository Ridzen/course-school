from rest_framework import serializers

from apps.request.models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ('id', 'full_name', 'phone_number', 'email')

    def create(self, validated_data):
        new_questionnaire = Questionnaire.objects.create(**validated_data)
        return new_questionnaire

