# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from custom_auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

@api_view(['POST'])
@permission_classes((AllowAny, ))
@parser_classes((JSONParser,))
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'id': user.id,
                'created': user.date_joined,
                'modified': user.modified,
                'last_login': user.last_login,
                'token': user.profile.token
            }
            return JsonResponse(response_data, status=200)
        return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes((AllowAny, ))
@parser_classes((JSONParser,))
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            user.last_login = timezone.now()
            user.save()
            response_data = {
                'id': user.id,
                'created': user.date_joined,
                'modified': user.modified,
                'last_login': user.last_login,
                'token': user.profile.token
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'message': 'Usuário e/ou senha inválidos'}, status=400)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@parser_classes((JSONParser,))
def profile(request):
    if request.method == 'GET':
        if request.query_params.get('id') is not None:
            user = User.objects.get(pk=request.query_params.get('id'))
            if(request.auth.decode('utf-8') == user.profile.token):
                response_data = {
                    'id': user.id,
                    'created': user.date_joined,
                    'modified': user.modified,
                    'last_login': user.last_login,
                    'token': user.profile.token
                }
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({'message': 'Não autorizado'}, status=400)
        else:
            return JsonResponse({'message': 'Não autorizado'}, status=400)
    else:
        return JsonResponse({'message': 'Não autorizado'}, status=400)