from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

import json
import pandas as pd

import joblib

model = joblib.load('modelPipeline.pkl')


# Create your views here.
def scoreJson(request):
    print(request.body)
    data = json.loads(request.body)
    dataF = pd.DataFrame({'x':data}).transpose()
    print(dataF)
    print("coming here!")
    score=model.predict_proba(dataF)[:,-1][0]
    score = float(score)
    
    return JsonResponse({'score': score})


def scoreFile(request):
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    filePath='.'+filePathName

    data = pd.read_csv(filePath)
    score = model.predict_proba(data)[:,-1]

    scores = {j:k for j,k in zip(data['Loan_ID'], score)}

    score =sorted(scores.items(),key=lambda x: x[1],reverse=True)
    return JsonResponse({'score': score})