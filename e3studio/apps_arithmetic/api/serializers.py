from rest_framework import serializers

from apps_arithmetic.models import AppsArithmetic, Grade


class InputSerializer(serializers.Serializer):
    input_0 = serializers.CharField()
    input_1 = serializers.CharField()
    input_2 = serializers.CharField()
    input_3 = serializers.CharField()
    input_4 = serializers.CharField()
    input_5 = serializers.CharField()
    input_6 = serializers.CharField()
    input_7 = serializers.CharField()
    input_8 = serializers.CharField()
    input_9 = serializers.CharField()

    def update(self, instance, validated_data):
        """
        Update and return an existing `Input` instance, given the validated data.
        """
        instance.input_0 = validated_data.get('input_0', instance.input_0)
        instance.input_1 = validated_data.get('input_1', instance.input_1)
        instance.input_2 = validated_data.get('input_2', instance.input_2)
        instance.input_3 = validated_data.get('input_3', instance.input_3)
        instance.input_4 = validated_data.get('input_4', instance.input_4)
        instance.input_5 = validated_data.get('input_5', instance.input_5)
        instance.input_6 = validated_data.get('input_6', instance.input_6)
        instance.input_7 = validated_data.get('input_7', instance.input_7)
        instance.input_8 = validated_data.get('input_8', instance.input_8)
        instance.input_9 = validated_data.get('input_9', instance.input_9)
        instance.save()
        return instance


class AppsArithmeticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppsArithmetic
        fields = ('id', 'appname', 'front_image', 'icon',
                  'top_image', 'right_image', 'right_image_web', 'web', 'description')


class OneAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppsArithmetic
        fields = ('id', 'appname')


class OneGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'appname', 'grade', 'web')

    # list = serializers.CharField()

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `List` instance, given the validated data.
    #     """
    #     instance.list = validated_data.get('list', instance.list)
    #     instance.save()
    #     return instance
