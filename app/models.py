from django.db import models
from django.contrib.auth.models import User


class CardDetails(models.Model):
	'''
		Card information model to store data
	'''
	card_last_digit = models.CharField(max_length=6, null=False, blank=False)
	cardholder_name = models.CharField(max_length=50, null=False, blank=False)
	expiry_month = models.CharField(max_length=2, null=False, blank=False)
	expiry_year = models.CharField(max_length=4, null=False, blank=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		db_table = 'card_information'
		indexes = [
			models.Index(fields=['cardholder_name']),
		]

	def __str__(self):
		return self.cardholder_name


class TransactionLogs(models.Model):
	'''
	 	Transaction Logs
	'''
	transaction_id = models.CharField(max_length=100, null=False, blank=False)
	invoice_number = models.CharField(max_length=100, null=False, blank=False)
	amount = models.FloatField(null=False)
	tax = models.FloatField(null=False)
	card = models.ForeignKey(CardDetails, null=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'transaction_logs'
		indexes = [
			models.Index(fields=['card']),
			models.Index(fields=['transaction_id']),
			models.Index(fields=['invoice_number']),
		]

	def __str__(self):
		return self.transaction_id