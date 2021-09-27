from django.urls import path, re_path
from django.conf.urls import url

from app.views import *

urlpatterns = [
	# Card Details URLs
	url(r'^card/details$', CardDetailsApiView.as_view(), name='card_details'),

	# Transaction Logs
	url(r'^transaction/logs$', TransactionLogsApiView.as_view(), name='transaction_logs'),
	
]