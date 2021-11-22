import secrets
from cryptography.fernet import Fernet
from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from AIContest.contest.models import Contests, ContestSerializer
from AIContest.account.models import Accounts
from AIContest.account.views import getTokenRole
from datetime import datetime
import json
import base64
import os
import os.path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
CONTEST_DIR = BASE_DIR / "contest" / "file"


@api_view(['POST'])
def getContest(request):
    data = JSONParser().parse(request)
    try:
        jsondec = json.decoder.JSONDecoder()
        contest = Contests.objects.get(id=data['id'])
        list_participants = json.loads(contest.participants)
        list_language = jsondec.decode(contest.language)
        jsonres = {
            "id": contest.id,
            "creator": contest.creator,
            "participants": list_participants,
            "title": contest.title,
            "description": contest.description,
            "time_regist": convertDateTimetoString(contest.time_regist),
            "time_start": convertDateTimetoString(contest.time_start),
            "time_end": convertDateTimetoString(contest.time_end),
            "language": list_language,
            "time_out": contest.time_out
        }
        account = getTokenRole(data['token'])
        if account.__class__ is str:
            return Response("FORBIDDEN")
        else:
            if account['username'] == contest.creator:
                jsonres['link_contest'] = base64.b64encode(open(CONTEST_DIR / contest.link_contest / "contest.pdf", 'rb').read()).decode('utf-8')
                jsonres['link_datatrain'] = open(CONTEST_DIR / contest.link_datatrain, 'r').read()
                jsonres['link_datatest'] = open(CONTEST_DIR / contest.link_datatest, 'r').read()
                jsonres['link_tester'] = open(CONTEST_DIR / contest.link_tester, 'r').read()
            elif account['username'] in list_participants:
                jsonres['link_contest'] = base64.b64encode(open(CONTEST_DIR / contest.link_contest / "contest.pdf", 'rb').read()).decode('utf-8')
                jsonres['link_datatrain'] = open(CONTEST_DIR / contest.link_datatrain, 'r').read()
        return Response(jsonres)
    except Contests.DoesNotExist:
        return Response("Contest does not exist")
    except Exception as e:
        return Response(e)


@api_view(['GET'])
def getContests(request):
    contests = list(Contests.objects.all().values('id', 'title', 'time_regist', 'time_start', 'time_end'))
    for i in contests:
        i['time_regist'] = convertDateTimetoString(i['time_regist'])
        i['time_start'] = convertDateTimetoString(i['time_start'])
        i['time_end'] = convertDateTimetoString(i['time_end'])
    return JsonResponse(contests, safe=False)


@api_view(['POST'])
def createContest(request):
    try:
        contest_detail = request.data['contest']
        data_train = request.data['data_train']
        data_test = request.data['data_test']
        tester = request.data['tester']
        name = secrets.token_hex(16)
        save_path = CONTEST_DIR / name
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        fs = FileSystemStorage(location=save_path)
        fs.save("contest.pdf", contest_detail)
        fs.save("data_train.txt", data_train)
        fs.save("data_test.txt", data_test)
        fs.save("tester.py", tester)
        filenames = ['data_train.txt', 'data_test.txt']
        with open(CONTEST_DIR / name / 'input.txt', 'w') as outfile:
            for f in filenames:
                with open(CONTEST_DIR / name / f) as infile:
                    for line in infile:
                        outfile.write(line)
        contest_data = {"creator": request.data['creator'],
                        "participants": "{}",
                        "title": request.data['title'],
                        "description": request.data['description'],
                        "link_contest": name,
                        "link_datatrain": name + "/data_train.txt",
                        "link_datatest": name + "/data_test.txt",
                        "link_tester": name + "/tester.py",
                        "time_regist": convertStringtoDateTime(request.data['time_regist']),
                        "time_start": convertStringtoDateTime(request.data['time_start']),
                        "time_end": convertStringtoDateTime(request.data['time_end']),
                        "language": request.data['language'],
                        "time_out": request.data['time_out']
                        }
        contest_serializer = ContestSerializer(data=contest_data)
        if contest_serializer.is_valid():
            contest_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(contest_serializer.errors, safe=False)

    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['POST'])
def addParticipant(request):
    request_data = JSONParser().parse(request)
    try:
        contest = Contests.objects.get(id=request_data['id'])
        participant = json.loads(contest.participants)
        if request_data['username'] in participant:
            return JsonResponse("Username had been added in Contest", safe=False)
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


@api_view(['PATCH'])
def updateContest(request):
    try:
        request_data = {}
        for key in request:
            print(key)
        request_data = JSONParser().parse(request)
        contest = Contests.objects.get(id=request_data['id'])
        check = False
        if 'token' in request_data:
            account = getTokenRole(request_data.pop('token'))
            if account is not str:
                if account['role'] == 'admin':
                    check = True
                elif account['role'] == 'creator' and account['username'] == contest.creator:
                    check = True
        if not check:
            return Response("No authorization")
        if 'time_regist' in request_data:
            request.data['time_regist'] = convertStringtoDateTime(request.data['time_regist'])
        if 'time_start' in request_data:
            request.data['time_end'] = convertStringtoDateTime(request.data['time_start'])
        if 'time_regist' in request_data:
            request.data['time_end'] = convertStringtoDateTime(request.data['time_end'])
        contest_serializer = ContestSerializer(contest, data=request_data)
        if contest_serializer.is_valid():
            contest_serializer.save()
            return Response("Updated Successfully")
        else:
            return JsonResponse(contest_serializer.errors, safe=False)
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Contests.DoesNotExist:
        return Response("Contest doesn't existed")


@api_view(['DELETE'])
def deleteContest(request):
    try:
        request_data = JSONParser().parse(request)
        contest = Contests.objects.get(id=request_data['id'])
        check = False
        if 'token' in request_data:
            account = getTokenRole(request_data.pop('token'))
            if account is not str:
                if account['role'] == 'admin':
                    check = True
                elif account['role'] == 'creator' and account['username'] == contest.creator:
                    check = True
        if not check:
            return Response("No authorization")
        contest.delete()
        return Response("Deleted Successfully")
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Contests.DoesNotExist:
        return Response("Contest doesn't existed")


def updateRanking(id, username, point):
    contest_data = Contests.objects.get(id=id)
    participants = json.loads(contest_data.participants)
    if participants[username] < point:
        participants[username] = point
    participants = dict(sorted(participants.items(), key=lambda x: x[1], reverse=True))
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


def findContest(id):
    contest = Contests.objects.get(id=id)
    return contest
