from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AIContest.user.models import Users, UserSerializer


def getUsers(request, id=0):
    users = Users.objects.all().values()
    return JsonResponse(list(users), safe=False)
    #serializ list = error
    #user_serializer = UserSerializer(data=users, many=True)
    #if user_serializer.is_valid():
    #    return JsonResponse(user_serializer.data, safe=False)
    #return JsonResponse("Fail to Get", safe=False)


def createUser(request, id=0):
    user_data = JSONParser().parse(request)
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse("Added Successfully", safe=False)
    return JsonResponse("Fail to Add", safe=False)


def updateUser(request, id=0):
    user_data = JSONParser().parse(request)
    user = Users.objects.filter(username=user_data['username']).values()[0]
    user_serializer = UserSerializer(data=user)
    print(user_serializer)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse("Updated Successfully", safe=False)
    print(user_serializer.errors)
    return JsonResponse("Fail to Update", safe=False)


def deleteUser(request, id=0):
    user = Users.objects.get(userid=id)
    user.delete()
    return JsonResponse("Fail to Update", safe=False)
