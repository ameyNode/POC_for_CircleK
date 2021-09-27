# python packages
import string
import random

# Django packages
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.db.models import Q as queue

# Rest Framework packages
from rest_framework.views import APIView


# Model and serializers
from app.serializers import CardDetailsSerializer, TransactionLogsReadSerializer, CardCreateSerializer, TransactionLogsWriteSerializer
from app.models import CardDetails, TransactionLogs




# Card details search API
class CardDetailsApiView(APIView):
	'''
		Card API
		Method get : Get searched logs in response
		Method post : Create Card
	'''
	# TODO :  Authentication decorators
	def get(self, request):
		# Get search query from Query String
		query = request.GET.get('query')
		# If query has some data then proceed to search in database
		if query:
			card_logs = CardDetails.objects.filter(cardholder_name__icontains=query).all()
			
			if card_logs:
				# resulted query string pass to serializer to serialize data into readable format
				card_logs_serialized = CardDetailsSerializer(card_logs, many=True).data
				# many=True, pasameter is to know queryset has multiple records

				# return result to client in JSON Format
				return JsonResponse({'message':'Card details found.', 'status':True, 'status_code':200, 'result':card_logs_serialized}, status=200)
			else:
				# return empty card details response
				return JsonResponse({'message':'Card details not found.', 'status':False, 'status_code':404}, status=404)
		return JsonResponse({'message':'Bad Request! Please insert characters.', 'status':False, 'status_code':400}, status=400)


	# Save card details API
	# TODO :  Authentication decorators
	def post(self, request):
		if request.data:
			# get data in varibales
			card_number = request.data.get('card_number')
			card_expiry_month = request.data.get('card_expiry_month')
			card_expiry_year = request.data.get('card_expiry_year')
			card_holder_name = request.data.get('card_holder_name')
			card_cvv = request.data.get('card_cvv')

			# Check if all data present
			if card_number and card_cvv and card_holder_name and card_expiry_year and card_expiry_month:
				# Check card number is valid!
				if len(card_number) == 16:
					# Prepare object to store
					card_object = {
						"card_last_digit" : card_number[-6:],
						"cardholder_name" : card_holder_name,
						"expiry_month" : card_expiry_month,
						"expiry_year" : card_expiry_year
					}

					serializer = CardCreateSerializer(data=card_object)
					# check if data is valid!
					if serializer.is_valid():
						serializer.save()
						return JsonResponse({'message':'Card details saved successfully.', 'status':True, 'status_code':201}, status=201)
					else:
						return JsonResponse({'message':'Invalid data. Please check details.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
				return JsonResponse({'message':'Invalid card number.', 'status':False, 'status_code':400}, status=400)
			return JsonResponse({'message':'Insufficient data. Card Number, CVV, Card holder name and Expiry Month/Year required', 'status':False, 'status_code':200}, status=400)



class TransactionLogsApiView(APIView):
	'''
		Transaction Logs API
		Method get : Get searched logs in response
		Method post : Create transaction log
	'''
	# TODO :  Authentication decorators
	def get(self, request):
		# Get key from querystring
		query = request.GET.get('query')

		if query:
			# Filter query against transaction logs
			transaction_logs = TransactionLogs.objects.filter(queue(card__cardholder_name__icontains=query) | queue(card__card_last_digit__icontains=query))
			
			if transaction_logs:
				# resulted query string pass to serializer to serialize data into readable format
				transaction_logs_serialized = TransactionLogsReadSerializer(transaction_logs, many=True).data
				# many=True, pasameter is to know queryset has multiple records

				# return result to client in JSON Format
				return JsonResponse({'message':'Transaction Logs.', 'status':True, 'status_code':200, 'result':transaction_logs_serialized}, status=200)
			else:
				# return empty card details response
				return JsonResponse({'message':'Transaction log not found.', 'status':False, 'status_code':404}, status=404)
		return JsonResponse({'message':'Bad Request! Please insert characters.', 'status':False, 'status_code':400}, status=400)


	# TODO :  Authentication decorators
	def post(self, request):
		if request.data:
			card_number = request.data.get('card_number')
			card_expiry_month = request.data.get('card_expiry_month')
			card_expiry_year = request.data.get('card_expiry_year')
			card_holder_name = request.data.get('card_holder_name')
			card_cvv = request.data.get('card_cvv')
			amount = request.data.get('amount')
			tax = request.data.get('tax', 0)

			if card_number and card_cvv and card_holder_name and card_expiry_year and card_expiry_month and amount:
				# Check if card is valid !
				if len(card_number) == 16:
					# Check if card already exist

					card_exist = CardDetails.objects.filter(card_last_digit=card_number[-6:], cardholder_name=card_holder_name, expiry_month=card_expiry_month, expiry_year=card_expiry_year).last()
					# If exists dont create card 
					if card_exist:
						transaction_object = {
							"transaction_id" : 'transaction_'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
							"invoice_number" : 'invoice_'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
							"amount" : amount,
							"tax" : tax,
							"card" : card_exist.id
						}

						serializer = TransactionLogsWriteSerializer(data=transaction_object)

						if serializer.is_valid():
							serializer.save()
							return JsonResponse({'message':'Transaction log saved successfully.', 'status':True, 'status_code':201}, status=201)
						else:
							return JsonResponse({'message':'Error during saving transaction details.', 'status':False, 'status_code':400, 'errors':serializer.errors}, status=400)

					# If not exists create card and save transaction log 
					else:
						# Prepare object to store
						card_object = {
							"card_last_digit" : card_number[-6:],
							"cardholder_name" : card_holder_name,
							"expiry_month" : card_expiry_month,
							"expiry_year" : card_expiry_year,
						}

						serializer = CardCreateSerializer(data=card_object)

						# check if data is valid!
						if serializer.is_valid():
							serializer.save()
							transaction_object = {
								"transaction_id" : 'transaction_'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
								"invoice_number" : 'invoice_'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
								"amount" : amount,
								"tax" : tax,
								"card" : serializer.data.get('id')
							}
							transaction_serializer = TransactionLogsWriteSerializer(data=transaction_object)
							if transaction_serializer.is_valid():
								transaction_serializer.save()
								return JsonResponse({'message':'Transaction log saved successfully.', 'status':True, 'status_code':201}, status=201)
							else:
								return JsonResponse({'message':'Error during saving transaction details.', 'status':False, 'status_code':400, 'errors':transaction_serializer.errors}, status=400)
						else:
							return JsonResponse({'message':'Invalid data. Please check details.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
				return JsonResponse({'message':'Invalid card number.', 'status':False, 'status_code':400}, status=400)
			return JsonResponse({'message':'Insufficient data. Card Number, CVV, Card holder name and Expiry Month/Year required', 'status':False, 'status_code':200}, status=400)