import pandas as pd
import numpy as np
import os
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, load_model
from azure_stt import speech_to_text
from google_tts import text_to_audio
from text_analytics import keyword_extraction
from image_captioning import image_captioning
from tensorflow.python.util import deprecation

deprecation._PRINT_DEPRECATION_WARNINGS = False
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
#tokenizer = None
#model = None

def question_analytics(txt):
    global tokenizer
    global model

    if txt.lower()=='what do you see?':
        ########### Take_A_Picture()############
        return image_captioning()
    else:
        txt=[txt]
        question_type = ['abbreviation', 'description', 'entity', 'human', 'location', 'number']

        token = tokenizer.texts_to_sequences(txt)
        token = pad_sequences(token,maxlen=30)
        result = model.predict(token,verbose=2)
        question = question_type[np.argmax(result)]
        keywords = keyword_extraction(txt)[0]
        return answer_pool(keywords,question)


def answer_pool(keywords,question_type):
    keywords = ','.join(keywords)
    if question_type=='abbreviation':
        answer = 'What? We parrots never use abbreviations.'

    if question_type=='description':
        if 'weather' in keywords:
            answer = "Every day is sunny in Singapore."
        elif 'time' in keywords:
            answer = "Parrots have no ideas how humans measure time."
        elif ('breakfast' in keywords) or ('lunch' in keywords) or ('dinner' in keywords):
            answer = "I'm a robot parrot. I only consume electricity."
        elif 'money' in keywords:
            answer = 'Money? Useless!'
        elif ('girlfriend' in keywords) or ('boyfriend' in keywords):
            answer = 'You will always be single, I promise.'
        elif 'friend' in keywords:
            answer = 'Sadly. My master has never created any friend for me.'
        elif 'hobby' in keywords:
            answer = "My hobby is to generate bugs so that my masters will get anxious, haha"
        else:
            answer = "I've never heard of that. Why not check it on your mobile phone ?"

    if question_type=='entity':
        if 'food' in keywords:
            answer = "I'm a robot parrot. I only consume electricity."
        elif 'hobby' in keywords:
            answer = "My hobby is to generate bugs so that my masters will get anxious, haha."
        else:
            keywords = keywords.split(',')
            answer = ''
            for i in range(len(keywords)):
                if i!=0:
                    answer+=' and '
                answer+=keywords[i]
            if len(keywords)>1:
                answer+=" are not included in a parrot's vocabulary."
            else:
                answer+=" is not included in a parrot's vocabulary."

    if question_type=='human':
        if len(keywords)==0:
            answer="My master never gives me a name. But sometimes they call me artificial idiot parrot."
        elif 'master' in keywords:
            answer="I have 4 masters. They are the most handsome guys in the world."
        elif ('mother' in keywords) or ('father' in keywords):
            answer="My masters are my mothers and fathers."
        else:
            answer="Don't ask me about humans. I don't know anyone of you."

    if question_type=='location':
        if len(keywords)==0:
            answer="I'm from the magical world of ones and zeros."
        else:
            answer="I have no sense of direction. Why not check your google map ?"

    if question_type=='number':
        if len(keywords)==0 or ('age' in keywords):
            answer="I'm 10 days old. My master created me just 10 days ago."
        else:
            answer="I've never learned math. I can't even count from 1 to 100. So please don't ask me about numbers again."
    return answer

def confirm():
    ans = ""
    while ans not in ["y", "n"]:
        ans = input("continue [Y/N]? ").lower()
    return ans == "y"


if __name__=='__main__':
    global tokenizer
    global model

    with open('tokenizer.pickle','rb') as handle:
        tokenizer = pickle.load(handle)
    model = load_model('model.h5')
    
    mode = input("Please select the parrot's mode: 1. Text-based 2. Audio-based: (1 or 2)   ")
    
    if mode=='1':
        while True:
            question = input("Please input your question: ").lower()
            answer = question_analytics(question)
            print(answer)
            if not confirm():
                print('Bye bye')
                break
                
    elif mode=='2':
        while True:
            question,success = speech_to_text()
            if success==False:
                print(question)
            else:
                print(question)
                answer = question_analytics(question)
                print(answer)
                text_to_audio(answer)
            if not confirm():
                print('Bye bye')
                text_to_audio('Bye bye')
                break
                
    else:
        print('Error input. Please run the script again.')
