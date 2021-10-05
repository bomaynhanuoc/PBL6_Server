from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.user.models import Users, UserSerializer


def getUsers(request):
    users = list(Users.objects.all().values())
    user_serializer = UserSerializer(data=users, many=True)
    if user_serializer.is_valid():
        return JsonResponse(user_serializer.data, safe=False)
    return JsonResponse(user_serializer.errors, safe=False)


def createUser(request):
    user_data = JSONParser().parse(request)
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse("Added Successfully", safe=False)
    return JsonResponse(user_serializer.errors, safe=False)


def updateUser(request):
    user_data = JSONParser().parse(request)
    try:
        user = Users.objects.get(username=user_data['username'])
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
    except Users.DoesNotExist:
        return JsonResponse("User doesn't existed", safe=False)
    return JsonResponse(user_serializer.errors, safe=False)


def deleteUser(request):
    user_data = JSONParser().parse(request)
    try:
        user = Users.objects.get(username=user_data['username'])
        user.delete()
        return JsonResponse("Delete Successfully", safe=False)
    except Users.DoesNotExist:
        return JsonResponse("User doesn't existed", safe=False)
