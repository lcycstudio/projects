from rest_framework import serializers

from apps_math.models import AppsMath, Function


class CodingSerializer(serializers.Serializer):
    input = serializers.CharField(style={'base_template': 'textarea.html'})

    def update(self, instance, validated_data):
        """
        Update and return an existing `Coding` instance, given the validated data.
        """
        instance.input = validated_data.get('input', instance.input)
        instance.save()
        return instance


class AppsMathSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppsMath
        fields = ('id', 'appname', 'front_image', 'icon',
                  'top_image', 'right_image', 'right_image_web', 'web', 'description')


class OneAppMathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ('id', 'appname', 'name', 'note', 'latex')


class CFSerializer(serializers.Serializer):
    function = serializers.CharField()
    parameter = serializers.CharField()
    left_bound = serializers.CharField()
    right_bound = serializers.CharField()
    title = serializers.CharField()
    hlabel = serializers.CharField()
    vlabel = serializers.CharField()
    option = serializers.CharField()
    forxvalue = serializers.CharField()
    foryvalue = serializers.CharField()

    def update(self, instance, validated_data):
        """
        Update and return an existing `Coding` instance, given the validated data.
        """
        instance.function = validated_data.get('function', instance.function)
        instance.parameter = validated_data.get(
            'parameter', instance.parameter)
        instance.left_bound = validated_data.get(
            'left_bound', instance.left_bound)
        instance.right_bound = validated_data.get(
            'right_bound', instance.right_bound)
        instance.title = validated_data.get('title', instance.title)
        instance.hlabel = validated_data.get('hlabel', instance.hlabel)
        instance.vlabel = validated_data.get('vlabel', instance.vlabel)
        instance.option = validated_data.get('option', instance.option)
        instance.forxvalue = validated_data.get(
            'forxvalue', instance.forxvalue)
        instance.foryvalue = validated_data.get(
            'foryvalue', instance.foryvalue)
        instance.save()
        return instance


class ODESerializer(serializers.Serializer):
    equation = serializers.CharField()
    parameter = serializers.CharField()
    ifv = serializers.CharField()
    idv = serializers.CharField()
    left_bound = serializers.CharField()
    right_bound = serializers.CharField()
    title = serializers.CharField()
    hlabel = serializers.CharField()
    vlabel = serializers.CharField()
    option = serializers.CharField()
    forxvalue = serializers.CharField()
    foryvalue = serializers.CharField()

    def update(self, instance, validated_data):
        """
        Update and return an existing `Coding` instance, given the validated data.
        """
        instance.equation = validated_data.get('equation', instance.equation)
        instance.parameter = validated_data.get(
            'parameter', instance.parameter)
        instance.ifv = validated_data.get(
            'ifv', instance.ifv)
        instance.idv = validated_data.get(
            'idv', instance.idv)
        instance.left_bound = validated_data.get(
            'left_bound', instance.left_bound)
        instance.right_bound = validated_data.get(
            'right_bound', instance.right_bound)
        instance.title = validated_data.get('title', instance.title)
        instance.hlabel = validated_data.get('hlabel', instance.hlabel)
        instance.vlabel = validated_data.get('vlabel', instance.vlabel)
        instance.option = validated_data.get('option', instance.option)
        instance.forxvalue = validated_data.get(
            'forxvalue', instance.forxvalue)
        instance.foryvalue = validated_data.get(
            'foryvalue', instance.foryvalue)
        instance.save()
        return instance
