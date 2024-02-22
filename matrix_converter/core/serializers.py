from rest_framework import serializers
from core.models import Matrix


class MatrixSerializer(serializers.ModelSerializer):

    matrix_field = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))
    class Meta:
        model = Matrix
        fields = '__all__'