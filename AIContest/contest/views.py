import secrets
from cryptography.fernet import Fernet
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.contest.models import Contests, ContestSerializer


def getContest(request):
    contest_data = JSONParser().parse(request)
    contest = Contests.objects.get(id=contest_data['id'])
    print(contest.partilist)
    contest_serializer = ContestSerializer(contest, data=contest_data)
    if contest_serializer.is_valid():
        return JsonResponse(contest_serializer.data, safe=False)
    return JsonResponse(contest_serializer.errors, safe=False)


def getContests(request):
    contests = list(Contests.objects.all().values())
    contest_serializer = ContestSerializer(data=contests, many=True)
    if contest_serializer.is_valid():
        return JsonResponse(contest_serializer.data, safe=False)
    return JsonResponse(contest_serializer.errors, safe=False)


def createContest(request):
    contest_data = JSONParser().parse(request)
    print(contest_data['partilist'])
    contest_serializer = ContestSerializer(data=contest_data)
    if contest_serializer.is_valid():
        #print(contest_serializer.data)
        contest_serializer.save()
        return JsonResponse("Added Successfully", safe=False)
    return JsonResponse(contest_serializer.errors, safe=False)


def updateContest(request):
    # contest_data = JSONParser().parse(request)
    # try:
    #     contest = Contests.objects.get(username=contest_data['username'])
    #     fernet = Fernet(contest.key)
    #     contest_data['password'] = fernet.encrypt(contest_data['password'].encode()).decode("utf-8")
    #     # print(contest.key)
    #     contest_serializer = ContestSerializer(contest, data=contest_data)
    #     if contest_serializer.is_valid():
    #         contest_serializer.save()
    #         return JsonResponse("Updated Successfully", safe=False)
    # except Contests.DoesNotExist:
    #     return JsonResponse("Contest doesn't existed", safe=False)
    # return JsonResponse(contest_serializer.errors, safe=False)
    return JsonResponse("update", safe=False)


def deleteContest(request):
    # contest_data = JSONParser().parse(request)
    # try:
    #     contest = Contests.objects.get(username=contest_data['username'])
    #     contest.delete()
    #     return JsonResponse("Delete Successfully", safe=False)
    # except Contests.DoesNotExaist:
    #     return JsonResponse("Contest doesn't existed", safe=False)
    return JsonResponse("update", safe=False)