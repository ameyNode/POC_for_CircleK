# Paython Packages
import json

# DRF Packages
from rest_framework import status

# Django packages
from django.test import TestCase, Client
from django.urls import reverse

# Models and Serializers
from app.serializers import CardDetailsSerializer, TransactionLogsReadSerializer, CardCreateSerializer, TransactionLogsWriteSerializer
from app.models import CardDetails, TransactionLogs

# initialize the APIClient app
client = Client()

class CardTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
		"card_number" : "4111111111111115",
		"card_expiry_month" : "08",
		"card_expiry_year" :  "2024",
		"card_holder_name" : "Amey Patil",
		"card_cvv" : "123"
		}

        self.invalid_payload = {
		"card_number" : "41111111111111",
		"card_expiry_month" : "08",
		"card_expiry_year" :  "2024",
		"card_holder_name" : "Amey Patil",
		"card_cvv" : "123"
		}

    def test_create_valid_card(self):
    	# create valid record
        response = client.post(
            '/api/card/details',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_get_card_details(self):
    	# Create record in 
    	response_create = client.post(
            '/api/card/details',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
    	# Compare response code
    	self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

    	response = client.get('/api/card/details', {'query': 'patil'},
            content_type='application/json')
    	
    	self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_invalid_card(self):
    	# create invalid record
        response = client.post(
            '/api/card/details',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TransactionLogsTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
			"card_number" : "4111111111111130",
			"card_expiry_month" : "08",
			"card_expiry_year" :  "2024",
			"card_holder_name" : "Mayur Patil",
			"card_cvv" : "123",
			"amount":12.09,
			"tax":3.08
			}

        self.invalid_payload = {
			"card_number" : "41111111111111",
			"card_expiry_month" : "08",
			"card_expiry_year" :  "2024",
			"card_holder_name" : "Mayur Patil",
			"card_cvv" : "123",
			"amount":12.09,
			"tax":3.08
			}

    def test_create_valid_transaction_log(self):
    	# create valid record
        response = client.post(
            '/api/transaction/logs',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_get_transaction_logs(self):
    	# Create record in 
    	response_create = client.post(
            '/api/transaction/logs',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
    	# Compare response code
    	self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

    	response = client.get('/api/transaction/logs', {'query': 'mayur'},
            content_type='application/json')
    	
    	self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_invalid_transaction_log(self):
    	# create invalid record
        response = client.post(
            '/api/transaction/logs',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




