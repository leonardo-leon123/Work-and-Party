import os, requests, uuid
from pprint import pprint

def Texto(_encuesta):
    subscription_key = "249de3f72881453595e0e18323d63ab9"
    endpoint = "https://rg-texta.cognitiveservices.azure.com/"
    sentiment_api_url = endpoint + "/text/analytics/v3.0/sentiment"

    texto = _encuesta
    documents = {"documents": [
        {"id": "1", "text": texto}
    ]}

    headers = {"Ocp-Apim-Subscription-Key": subscription_key,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
    }
    response = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()
    return sentiments