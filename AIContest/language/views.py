from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from AIContest.language.models import Languages, LanguageSerializer
from AIContest.account.views import getTokenRole
import json


@api_view(['POST'])
def getLanguages(request):
    try:
        languages = list(Languages.objects.all().values())
        return JsonResponse(languages, safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['POST'])
def createLanguage(request):
    try:
        data = JSONParser().parse(request)
        if 'token' in data:
            account = getTokenRole(data['token'])
            if account is not str and account['role'] == "admin":
                if 'name' in data and 'type' in data:
                    language_serializer = LanguageSerializer(data=data)
                    if language_serializer.is_valid():
                        language_serializer.save()
                        return JsonResponse("Added Successfully", safe=False)
                    return JsonResponse(language_serializer.errors, safe=False)
                else:
                    return Response("Invalid request data")
            else:
                return Response("Denied access")
        else:
            return Response("Need token to proceed")
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Exception as e:
        return Response(e)


@api_view(['PATCH'])
def updateLanguage(request):
    try:
        data = JSONParser().parse(request)
        if 'token' in data:
            account = getTokenRole(data['token'])
            data.pop('token')
            if account.__class__ is not str and account['role'] == "admin":
                language = Languages.objects.get(name=data['name'])
                language_serializer = LanguageSerializer(language, data=data)
                if language_serializer.is_valid():
                    language_serializer.save()
                    return Response("Updated Successfully")
                return Response(language_serializer.errors)
            return Response("Denied access")
        else:
            return Response("Need token to proceed")
    except Languages.DoesNotExist:
        return Response("Language doesn't existed")
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Exception as e:
        return Response(e)


@api_view(['DELETE'])
def deleteLanguage(request):
    try:
        data = JSONParser().parse(request)
        if 'token' in data:
            account = getTokenRole(data['token'])
            if account.__class__ is not str and account['role'] == "admin":
                data.pop('token')
                language = Languages.objects.get(name=data['name'])
                language.delete()
                return Response("Delete Successfully")
            else:
                return Response("Denied access")
        else:
            return JsonResponse("Need token to proceed", safe=False)
    except Languages.DoesNotExist:
        return JsonResponse("Language doesn't existed", safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)
    