from rest_framework import serializers

from apps_physics.models import AppsPhysics


class CodingSerializer(serializers.Serializer):
    input = serializers.CharField(style={'base_template': 'textarea.html'})

    def update(self, instance, validated_data):
        """
        Update and return an existing `Coding` instance, given the validated data.
        """
        instance.input = validated_data.get('input', instance.input)
        instance.save()
        return instance


class AppsPhysicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppsPhysics
        fields = ('id', 'appname', 'front_image', 'icon',
                  'top_image', 'right_image', 'right_image_web', 'web', 'description')


class OneAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppsPhysics
        fields = ('id', 'appname')


class PMFSerializer(serializers.Serializer):
    mass = serializers.CharField()
    charge = serializers.CharField()
    magnet = serializers.CharField()
    speed = serializers.CharField()
    direction = serializers.CharField()

    def update(self, instance, validated_data):
        """
        Update and return an existing `Coding` instance, given the validated data.
        """
        instance.mass = validated_data.get('mass', instance.mass)
        instance.charge = validated_data.get(
            'charge', instance.charge)
        instance.magnet = validated_data.get(
            'magnet', instance.magnet)
        instance.speed = validated_data.get(
            'speed', instance.speed)
        instance.direction = validated_data.get(
            'direction', instance.direction)
        return instance


class BBSerializer(serializers.Serializer):
    height = serializers.FloatField(min_value=1, max_value=10)
    vertical_v = serializers.FloatField(min_value=-50, max_value=50)
    horizontal_v = serializers.FloatField(min_value=0, max_value=50)
    gravitational = serializers.FloatField(min_value=0.1, max_value=100)
    air_resistance = serializers.FloatField(min_value=0, max_value=99.9)
    restitution = serializers.FloatField(min_value=0, max_value=0.99)
    frequency = serializers.FloatField(min_value=0, max_value=90)
    radius = serializers.FloatField(min_value=0.01, max_value=1.0)
    friction = serializers.FloatField(min_value=1, max_value=200)
    clockwise = serializers.CharField()

    def update(self, instance, validated_data):
        """
        Update and return an existing `Coding` instance, given the validated data.
        """
        instance.height = validated_data.get(
            'height', instance.height)
        instance.vertical_v = validated_data.get(
            'vertical_v', instance.vertical_v)
        instance.horizontal_v = validated_data.get(
            'horizontal_v', instance.horizontal_v)
        instance.gravitational = validated_data.get(
            'gravitational', instance.gravitational)
        instance.air_resistance = validated_data.get(
            'air_resistance', instance.air_resistance)
        instance.restitution = validated_data.get(
            'restitution', instance.restitution)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.radius = validated_data.get(
            'radius', instance.radius)
        instance.friction = validated_data.get(
            'friction', instance.friction)
        instance.clockwise = validated_data.get(
            'clockwise', instance.clockwise)
        return instance


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
