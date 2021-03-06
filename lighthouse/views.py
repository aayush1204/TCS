from django.shortcuts import render

# Create your views here.
from nltk.tokenize import RegexpTokenizer
import nltk

# stopwords = nltk.corpus.stopwords.words('english')
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re

import textstat

from .models import Laws, Score

import requests

# Importing all the necessary libraries
import nltk, re, numpy as np
import urllib

from nltk import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import string
from gensim.summarization import summarize
from nltk.probability import FreqDist

def summarizeAlgo(_text): 

    tos_text_paras = _text.split("\n")
    
    # Classifying using common words used under labels 
    copyright = ['collective work',\
    'compilation',\
    'compulsory license',\
    'copyright',\
    'copyright holder/copyright owner',\
    'copyright notice',\
    'derivative work',\
    'exclusive right',\
    'expression',\
    'fair use',\
    'first sale doctrine',\
    'fixation',\
    'idea',\
    'infringement',\
    'intellectual property',\
    'license',\
    'master use license',\
    'mechanical license',\
    'medium',\
    'moral rights',\
    'musical composition',\
    'parody',\
    'patent',\
    'performing rights',\
    'permission',\
    'public domain',\
    'publication/publish',\
    'right of publicity',\
    'royalty',\
    'service mark',\
    'sound recording',\
    'statutory damages',\
    'synchronization license',\
    'tangible form of expression',\
    'term',\
    'title',\
    'trademark',\
    'trade secret',\
    'work for hire']

    privacy = ['access',\
    'account',\
    'activity',\
    'advertising',\
    'confidentiality',\
    'content',\
    'cookie',\
    'legal',\
    'preferences',\
    'privacy',\
    'protect',\
    'religion',\
    'security',\
    'settings',\
    'personal data',\
    'personal information',\
    'track']

    termination = ['cease',\
    'terminate',\
    'remove',\
    'inactive',\
    'suspend',\
    'account',\
    'discontinue',\
    'revoke',\
    'retain']

    content_sharing = ['share']

    modification_or_pricing = ['modification',\
         'pricing']

    copyright_all,privacy_all,termination_all, sharing_all, modification_or_pricing_all = [],[],[],[],[]


    for para in tos_text_paras:
        check = 0
        for word in para.split(" "):
            word = word.lower()
            if word in copyright:
                copyright_all.append(para)
                check = 1
            if word in privacy:
                privacy_all.append(para)
                check = 1
            if word in termination:
                termination_all.append(para)
                check = 1
            if word in content_sharing:
                sharing_all.append(para)
                check = 1  
            if word in modification_or_pricing:
                modification_or_pricing_all.append(para)
                check = 1        
            if check != 0:
                break
    
    #Removing sentences that contain less than 5 words under all the labels
    
    copyright_all = [sent for sent in copyright_all if len(word_tokenize(sent)) > 5]

    privacy_all = [sent for sent in privacy_all if len(word_tokenize(sent)) > 5]

    termination_all = [sent for sent in termination_all if len(word_tokenize(sent)) > 5]

    sharing_all = [sent for sent in sharing_all if len(word_tokenize(sent)) > 5]

    modification_or_pricing_all = [sent for sent in modification_or_pricing_all if len(word_tokenize(sent)) > 5]

    categoryDict = {}
    
    #Summarizing each labelled text

    if (len(copyright_all) != 0):
        if (len(copyright_all) != 1):
            copyright_text = ' '.join(copyright_all)
            copyright_all = summarize(copyright_text, split=True, ratio=.2)
        categoryDict["Copyright"] = copyright_all


    if (len(privacy_all) != 0):
        if (len(privacy_all) != 1):
            privacy_text = ' '.join(privacy_all)
            privacy_all = summarize(privacy_text, split=True, ratio=.1)
        categoryDict["Privacy"] = privacy_all


    if (len(termination_all) != 0):
        if (len(termination_all) != 1):
            termination_text = ' '.join(termination_all)
            termination_all = summarize(termination_text, split=True, ratio=.2)
        categoryDict["Termination"] = termination_all

    if (len(sharing_all) != 0):
        if (len(sharing_all) != 1):
            sharing_text = ' '.join(sharing_all)
            sharing_all = summarize(sharing_text, split=True, ratio=.2)
        categoryDict["Sharing"] = sharing_all    
    

    
    if (len(modification_or_pricing_all) != 0):
        if (len(modification_or_pricing_all) != 1):
            modification_text = ' '.join(modification_or_pricing_all)
            modification_or_pricing_all = summarize(modification_text, split=True, ratio=.2)
        categoryDict["Modification"] = modification_or_pricing_all   
    print(type(categoryDict))
    print(categoryDict['Privacy'])

    for keys , values in categoryDict.items():
        print(keys)
        print(values)

    return categoryDict

#loadText
def loadText(text):

    # file = open(file_path, 'r', encoding="utf8")
    # doc = file.read()

    f = open(text,'r',encoding="utf8")
    raw = f.read()
    return raw
 
def index2(request):
    if request.method == "POST":
          

        tos_text = request.POST['toctext']

        summary = summarizeAlgo(tos_text)
        # for key in summary:
        #     print(key)
        #     print(summary[key])
        #     print()
        
        read_score = textstat.flesch_reading_ease(tos_text)
        summ = ""
        for key , values in summary.items():
            for i in values:
                summ = summ + i
        
        #  = textstat.flesch_reading_ease(summ)

    # from gensim.summarization import keywords

    # print 'Keywords:'
    # print keywords(text, ratio=0.15)

    # Uses Cookies - privacy
    # Uses and shares Personal data - privacy
    # store data anywhere around the world - privacy
    # does not track you - privacy


        q1 = 1
        q2 = 0
        q3 = 0
        q4 = 0
        q5 = 0
        # for i in summary['Copyright']:
        #     if(('name'and'use'and'information'and'show') in i):
        #         print(i)
        #         print("eewe")
        #         q1 = q1+1
        for i in summary['Privacy']:
            if(('cookies' in i) and ('collect' in i)):
                print(i)
                print("collects cookies")    
                q2 = q2 + 1

            if(('personal data' in i) and ('use' in i)):
                print(i)
                print("collects and Uses personal data")      
                q3 = q3 + 1
            if(('data' in i) and ('store' in i) and ('world' in i)):
                print(i)
                print("stores data anywhere in the world personal data")  
                q4 = q4 + 1

            if(('does not track' in i)):
                print("this service does not track you")
                q5 = q5 + 1
                print("track")      

        overall_score = q1 + q2 + q3 + q4 + q5 
        overall_score = 5 - overall_score

        ab = {}
        temp = ""
        for key, value in summary.items():
            temp = ""
            for i in value:
                temp = temp + i
            ab[key] = temp

        Score.objects.create(q1 = q2, q2 = q3, q3=q4, q4=q5, read_score = read_score, overall_score = overall_score)

        return render(request, 'summary.html',{'summary_list':ab, 'x':read_score, 'y':summ, 'overall_score':overall_score})

    return render(request, 'index.html',)
def countrylaws(request):
    data = Laws.objects.all()
    ls = []
    for i in data:
        ls.append(i.country)
    print(ls)    
    return render(request, 'mainlaws.html',{'data':data})

def laws(request):
    data = Laws.objects.all()
    ls = []
    for i in data:
        ls.append(i.country)
    print(ls)    
    return render(request, 'laws.html',{'data':data})

def sitebreach(request):

    if request.method == "POST":
        domain = request.POST['domain']
        url = "https://haveibeenpwned.com/api/v2/breaches?domain=" + domain 
        response = requests.get(url).json()
        print(response)

        desc = response[0]['Description']
        dataclasses = response[0]['DataClasses']
        date = response[0]['BreachDate']

        return render(request, 'news.html', {'response':response, 'desc':desc, 'dataclasses':dataclasses,
                                                'date': date})
    return render(request, 'news.html')

def analysis(request):
    data = Score.objects.all().last()
    return render(request, 'analysis.html', {'data':data})

