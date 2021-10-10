import secrets
from cryptography.fernet import Fernet
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.contest.models import Contests, ContestSerializer
import simplejson as json #import json datatype


def getContest(request):
    contest_data = JSONParser().parse(request)
    try:
        jsondec = json.decoder.JSONDecoder()
        contest = Contests.objects.get(id=contest_data['id'])
        list_partilist = jsondec.decode(contest.partilist)
        list_language = jsondec.decode(contest.language)
        jsonRes = {
            "id": contest.id,
            "creator": contest.creator,
            "partilist": list_partilist,
            "title": contest.title,
            "description": contest.description,
            "linkcontest": contest.linkcontest,
            "linkdatatrain": contest.linkdatatrain,
            "linkdatatest": contest.linkdatatest,
            "linktester": contest.linktester,
            "timeregist": contest.timeregist,
            "timestart": contest.timestart,
            "timeend": contest.timeend,
            "language": list_language,

        }
        return JsonResponse(jsonRes, safe=False)
    except Contests.DoesNotExist:
        return JsonResponse("Contest does not exist", safe=False)
    # except Exception as e:




def getContests(request):
    contests = list(Contests.objects.all().values())
    contest_serializer = ContestSerializer(data=contests, many=True)
    if contest_serializer.is_valid():
        return JsonResponse(contest_serializer.data, safe=False)
    return JsonResponse(contest_serializer.errors, safe=False)


def createContest(request):
    contest_data = JSONParser().parse(request)
    try:
        # print(contest_data['partilist'])
        if 'partilist' in contest_data:
            partilist_str = '["' + '", "'.join(contest_data['partilist']) + '"]'
        else:
            partilist_str = "[]"
        if 'language' in contest_data:
            language_str = '["' + '", "'.join(contest_data['language']) + '"]'
        else:
            language_str = "[]"
        contest_data['partilist'] = partilist_str
        contest_data['language'] = language_str
        contest_serializer = ContestSerializer(data=contest_data)
        if contest_serializer.is_valid():
            contest_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(contest_serializer.errors, safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)

def addParticipant(request):
    request_data = JSONParser().parse(request)
    try:
        contest = Contests.objects.get(id=request_data['id'])
        contest_data = {
            "id": contest.id,
            "partilist": contest.partilist[:-1] + ', "' + request_data['username'] + '"]'
        }

        contest_serializer = ContestSerializer(contest, data=contest_data)
        if contest_serializer.is_valid():
            contest_serializer.save()
            return JsonResponse("Joint Contest Successfully", safe=False)
        return JsonResponse(contest_serializer.errors, safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)




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