from io import BytesIO
import os
from PIL import Image, ImageDraw
import requests
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials

def Images(_filename):
    ubicacion = r'E:/Documents/Programacion/Python/Work&Party/venv/static/upload/' + _filename
    subscription_key = 'f7534e7c93cd4598aed88d96f2564a77'
    endpoint = 'https://encuestas-dsc.cognitiveservices.azure.com/'
    sentiment_url = endpoint + "/face/v1.0/detect"

    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'emotion',
        'returnFaceId': 'true'
    }
    _img = open(ubicacion, 'rb').read()
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        'Content-Type': 'application/octet-stream'
    }
    response = requests.post(sentiment_url, params=params, headers=headers, data=_img)
    responseJson = response.json()
    if len(responseJson) != 0:
        angerId = responseJson[0]["faceAttributes"]["emotion"]["anger"]
        contemptId = responseJson[0]["faceAttributes"]["emotion"]["contempt"]
        disgustId = responseJson[0]["faceAttributes"]["emotion"]["disgust"]
        fearId = responseJson[0]["faceAttributes"]["emotion"]["fear"]
        happinessId = responseJson[0]["faceAttributes"]["emotion"]["happiness"]
        neutralId = responseJson[0]["faceAttributes"]["emotion"]["neutral"]
        sadnessId = responseJson[0]["faceAttributes"]["emotion"]["sadness"]
        surpriseId = responseJson[0]["faceAttributes"]["emotion"]["surprise"]
        emotionSelect = []
        emotionSelect.append(angerId)
        emotionSelect.append(contemptId)
        emotionSelect.append(disgustId)
        emotionSelect.append(fearId)
        emotionSelect.append(happinessId)
        emotionSelect.append(neutralId)
        emotionSelect.append(sadnessId)
        emotionSelect.append(surpriseId)
        maxemotion = emotionSelect.index(max(emotionSelect))

        def numbers_to_emotions(argument):
            switcher = {
                0: "enojo",
                1: "desprecio",
                2: "disgusto",
                3: "espantado",
                4: "felicidad",
                5: "seriedad",
                6: "tristeza",
                7: "sorprendido"
            }
            return switcher.get(argument, "nothing")
        emotion = numbers_to_emotions(maxemotion)
        return emotion
    return False