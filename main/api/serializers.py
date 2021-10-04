from rest_framework import serializers

from main.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude=()
