from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import PredResults
from django.http import JsonResponse
import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Create your views here.
@login_required(login_url='login')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Passwords don't match")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')


def Encrypt(digitarr):
    key = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(os.urandom(16)), backend=default_backend())
    enc = []
    cip = []
    for n in digitarr:
        plaintext = bytes([n])
        padding_length = 16 - len(plaintext) % 16
        plaintext += bytes([padding_length] * padding_length)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        cip.append(ciphertext)
        enc.append(ciphertext.hex())
    return enc,cip

# def Decrypt(cip):
#     dec = []
#     for c in cip:
#         decryptor = cipher.decryptor()
#         decrypted_data = decryptor.update(c) + decryptor.finalize()

#         padding_length = decrypted_data[-1]
#         decrypted_data = decrypted_data[:-padding_length]

#         digit = int.from_bytes(decrypted_data, byteorder='big')
#         dec.append(digit)
#     return dec

def HomePage(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Patient_Blood_Pressure = int(request.POST.get('Patient_Blood_Pressure'))
        Patient_Heartrate = int(request.POST.get('Patient_Heartrate'))
        
        vals,val_cip = Encrypt([Patient_ID, Patient_Age, Patient_Gender, Patient_Blood_Pressure, Patient_Heartrate])
        print(vals)
        # Unpickle model
        model = pd.read_pickle(r"new_model.pickle")
        # Make prediction
        result = model.predict([[Patient_ID, Patient_Age, Patient_Gender, Patient_Blood_Pressure, Patient_Heartrate]])

        Heart_Disease = result[0]

        PredResults.objects.create(Patient_ID=vals[0], Patient_Age=vals[1], Patient_Gender=vals[2],Patient_Blood_Pressure=vals[3], Patient_Heartrate=vals[4], Heart_Disease=Heart_Disease)

        return JsonResponse({'result': Heart_Disease, 'Patient_ID': Patient_ID,'Patient_Age': Patient_Age, 'Patient_Gender': Patient_Gender, 'Patient_Blood_Pressure': Patient_Blood_Pressure, 'Patient_Heartrate': Patient_Heartrate},safe=False)
    
    return render(request,'home.html')

def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)