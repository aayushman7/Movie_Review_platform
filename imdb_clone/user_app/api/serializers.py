from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError

class Registerserializer(serializers.ModelSerializer):
    password_conf=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','password_conf']
        extra_kwargs = {
            'password': {'write_only': True},
            }
        
    def save(self):
        password=self.validated_data['password']
        password_conf=self.validated_data['password_conf']

        if password!=password_conf:
            raise ValidationError({'error':"Password doesn't match Password_Conf"})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise ValidationError({'error':'Email already exist'})
        
        account=User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account