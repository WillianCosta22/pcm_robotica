"""API Views e Serializers do app Robots"""
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Robot


class RobotSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_operacional_display', read_only=True)

    class Meta:
        model = Robot
        fields = '__all__'
        extra_fields = ['status_display']


class RobotViewSet(viewsets.ModelViewSet):
    """API ViewSet para Robôs"""
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    permission_classes = [IsAuthenticated]
