import secrets
from cryptography.fernet import Fernet
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.contest.models import Contests, ContestSerializer
from datetime import datetime
import json


def getContest(request):
    contest_data = JSONParser().parse(request)
    try:
        jsondec = json.decoder.JSONDecoder()
        contest = Contests.objects.get(id=contest_data['id'])
        list_participants = json.loads(contest.participants)
        list_participants = dict(sorted(list_participants.items(), key=lambda item: item[1], reverse=True))
        list_language = jsondec.decode(contest.language)

        jsonres = {
            "id": contest.id,
            "creator": contest.creator,
            "participants": list_participants,
            "title": contest.title,
            "description": contest.description,
            "link_contest": contest.link_contest,
            "link_datatrain": contest.link_datatrain,
            "link_datatest": contest.link_datatest,
            "link_tester": contest.link_tester,
            "time_regist": convertDateTimetoString(contest.time_regist),
            "time_start": convertDateTimetoString(contest.time_start),
            "time_end": convertDateTimetoString(contest.time_end),
            "language": list_language,
            "time_out": contest.time_out
        }
        return JsonResponse(jsonres, safe=False)
    except Contests.DoesNotExist:
        return JsonResponse("Contest does not exist", safe=False)
    # except Exception as e:


def getContests(request):
    contests = list(Contests.objects.all().values('id', 'title', 'time_regist', 'time_start', 'time_end'))
    for i in contests:
        i['time_regist'] = convertDateTimetoString(i['time_regist'])
        i['time_start'] = convertDateTimetoString(i['time_start'])
        i['time_end'] = convertDateTimetoString(i['time_end'])
    # contest_serializer = ContestSerializer(data=contests, many=True)
    if len(contests) != 0:
        return JsonResponse(contests, safe=False)
    return JsonResponse("no contest", safe=False)


def createContest(request):
    contest_data = JSONParser().parse(request)
    try:
        # contest_data['participants']
        if 'participants' in contest_data:
            participants_str = json.dumps(contest_data['participants'])
        else:
            participants_str = "{}"
        if 'language' in contest_data:
            language_str = '["' + '", "'.join(contest_data['language']) + '"]'
        else:
            language_str = "[]"
        contest_data['participants'] = participants_str
        contest_data['language'] = language_str
        contest_data['time_regist'] = convertStringtoDateTime(contest_data['time_regist'])
        contest_data['time_start'] = convertStringtoDateTime(contest_data['time_start'])
        contest_data['time_end'] = convertStringtoDateTime(contest_data['time_end'])
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
        participant = json.loads(contest.participants)
        if request_data['username'] in participant:
            return JsonResponse("User name had been added in Contest", safe=False)
        participant[request_data['username']] = 0
        contest_data = {
            "id": contest.id,
            "participants": json.dumps(participant)
        }
        contest_serializer = ContestSerializer(contest, data=contest_data)
        if contest_serializer.is_valid():
            contest_serializer.save()
            return JsonResponse("Joint Contest Successfully", safe=False)
        return JsonResponse(contest_serializer.errors, safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


def updateContest(request):
    request_data = JSONParser().parse(request)
    try:
        contest = Contests.objects.get(id=request_data['id'])
        updateRanking(request_data['id'], "Long", 10)
        contest_serializer = ContestSerializer(contest, data=request_data)
        # participant = json.loads(contest.participants)
        if contest_serializer.is_valid():
            contest_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
    except Contests.DoesNotExist:
        return JsonResponse("Contest doesn't existed", safe=False)
    return JsonResponse(contest_serializer.errors, safe=False)
    # return JsonResponse("update", safe=False)


def deleteContest(request):
    # contest_data = JSONParser().parse(request)
    # try:
    #     contest = Contests.objects.get(username=contest_data['username'])
    #     contest.delete()
    #     return JsonResponse("Delete Successfully", safe=False)
    # except Contests.DoesNotExist:
    #     return JsonResponse("Contest doesn't existed", safe=False)
    return JsonResponse("update", safe=False)

def updateRanking(id , username, point):

    contest_data = Contests.objects.get(id=id)
    participants = json.loads(contest_data.participants)
    print(participants)
    if participants[username] < point:
        participants[username] = point
    print(participants)
    contest_update = {
        "id": id,
        "participants": json.dumps(participants)
    }
    contest_serializer = ContestSerializer(contest_data, data=contest_update)
    if contest_serializer.is_valid():
        contest_serializer.save()

def convertDateTimetoString(time):
    time_parse = time.strftime('%d-%m-%Y %H:%M:%S')
    return time_parse

def convertStringtoDateTime(time):
    time_parse = time.replace(" ", "T")
    return time_parse
