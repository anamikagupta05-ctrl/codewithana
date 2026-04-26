from unittest import result

from curl_cffi import request
from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from torch import classes

#from sklearn.externals import joblib
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import pickle
#from sklearndatasets import load_iris
import numpy as np
from PIL import Image

from tensorflow import *
from .forms import UploadFileForm
from tensorflow.keras.preprocessing import image
from io import BytesIO
from keras.models import load_model

# prediction/views.py

def predict(request):
    
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
    
        try:

            classes=['acai','cupuacu','graviola','guarana','pupunha','tucuma']
            # Deserialize model
            file_path="E:/AI/Python313/model/model_fruit_classification.h5"
            
           
            model=load_model(file_path) 
                                        
                
            # Extract features from request data
            test_image=request.FILES.get('file')
            if test_image is not None:
                 
                #test_image = test_image.read()

                
                test_image = image.load_img(BytesIO(test_image.read()), target_size=(64, 64))
                test_image=image.img_to_array(test_image)
                test_image=np.expand_dims(test_image,axis=0)
                result=model.predict(test_image)
                
                result1=result[0]

                for i in range(6):
                    if result1[i] ==1.:
                        break;

                prediction=classes[i]
            
                return render(request, 'prediction/result.html', {'prediction': prediction})
            else:
                 raise FileNotFoundError("No image file uploaded.")    
            
        except Exception as e:
                return render(request, 'prediction/result.html', {'error': str(e)})
    
    else:
        prediction=UploadFileForm()

        return render(request, 'prediction/predict.html', {'form': prediction})


def result(request):
    return render(request, 'prediction/result.html')
