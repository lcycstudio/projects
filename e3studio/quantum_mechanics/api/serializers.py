from rest_framework import serializers

from quantum_mechanics.models import Chapter, Section, Choice, Answer


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'chapter', 'image')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'chapter', 'section')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'chapter', 'section', 'exercise',
                  'choice_1', 'choice_2', 'choice_3', 'answer',
                  'comment_1', 'equation_1', 'comment_2', 'equation_2')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer')


# class CodingSerializer(serializers.Serializer):
#     code = serializers.CharField(style={'base_template': 'textarea.html'})

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Coding` instance, given the validated data.
#         """
#         instance.code = validated_data.get('code', instance.code)
#         instance.save()
#         return instance
