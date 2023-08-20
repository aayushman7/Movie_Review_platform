from django.shortcuts import render
from .serializers import Registerserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from user_app import models
# Create your views here.

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    if request.method=='POST':
        serializer=Registerserializer(data=request.data)

        data={}
        
        if serializer.is_valid():
            account=serializer.save()

            data['username']=account.username
            data['email']=account.email
            
            token=Token.objects.get(user=account).key
            
            data['Token']=token
            data['Response']="Registration Successful"

        else:
            data= serializer.errors

        return Response(data)