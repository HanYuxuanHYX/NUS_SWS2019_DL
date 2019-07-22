import glob
import random
import platform
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from upload_image import upload

# Get endpoint and key from environment variables
def image_captioning():
    endpoint = 'https://imagecaptioning.cognitiveservices.azure.com/'
    key = '0560fbdbb9f94590879780be528c136e'
    hostname = '52.175.54.42'
    username = 'xgxg666'
    password = 'Hilyw131567_'
    image_folder = 'test_images/'

    prefix1 = ['I can see', 'There are', 'I find', 'Aha! I see']
    prefix2 = ["So, I guess it's","Mmm, I think it should be","It's probably","It looks like"]
    answer = ''

    # Set credentials
    credentials = CognitiveServicesCredentials(key)

    # Create client
    client = ComputerVisionClient(endpoint, credentials)

    for image in glob.glob(image_folder+'*'):
        upload(hostname,username,password,image)
        if platform.system()=='Windows':
            url = 'http://52.175.54.42/images/'+image.split('\\')[-1]
        else:
            url = 'http://52.175.54.42/images/'+image.split('/')[-1]
        #url = 'https://cdn.filestackcontent.com/sM8F3qPERK6otQAWJixU'
        language = "en"
        max_descriptions = 1

        image_analysis = client.analyze_image(url,visual_features=[VisualFeatureTypes.tags])

        answer=answer+prefix1[random.randint(0,len(prefix1)-1)]+' '

        for i in range(4):
            if i==3:
                answer=answer+'and '+image_analysis.tags[i].name+'.'
            else:
                answer=answer+image_analysis.tags[i].name+', '

        analysis = client.describe_image(url, max_descriptions, language)

        answer+=prefix2[random.randint(0,len(prefix2)-1)]
        answer=answer+' '+analysis.captions[0].text+'. '
    
    return answer


