# Rest framework package
from rest_framework import serializers

# Model import
from app.models import *


# Data serializer for CardDetails model 
class CardDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardDetails
		fields = ["card_last_digit",
                "cardholder_name",
                "expiry_month",
                "expiry_year"]


# Serializer for create card details
class CardCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardDetails
		fields = '__all__'


class TransactionLogsReadSerializer(serializers.ModelSerializer):
	card = CardDetailsSerializer(many=False, read_only=True)
	class Meta:
		model = TransactionLogs
		fields = '__all__'


class TransactionLogsWriteSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = TransactionLogs
		fields = '__all__'