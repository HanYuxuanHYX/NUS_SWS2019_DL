from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


def keyword_extraction(txt):
    subscription_key = "6d9746eaedd2463b8e8a55b314b32f29"
    credentials = CognitiveServicesCredentials(subscription_key)

    text_analytics_url = "https://eastasia.api.cognitive.microsoft.com/"
    text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)

    documents = [{
        "id": "1",
	"language": "en",
	"text": txt}]

    response = text_analytics.key_phrases(documents=documents)
    
    key_phrases = []
    for document in response.documents:
        key_phrases.append(document.key_phrases)

    return key_phrases
