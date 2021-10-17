from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from AIContest.submit.models import Submits, SubmitSerializer
import secrets
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SUBMIT_DIR = BASE_DIR / "submit" / "file"


@api_view(['GET'])
def getSubmit(request):
    try:
        data = JSONParser().parse(request)
        if 'id' in data:
            submit = Submits.objects.get(id=data['id'])
            json_res = {
                "id": submit.id,
                "username": submit.username,
                "language": submit.language,
                "status": submit.status,
                "time_submit": submit.time_submit.strftime("%d-%m-%Y %H:%M:%S"),
                "time_execute": submit.time_execute
            }
            return Response(json_res)
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Submits.DoesNotExist:
        return Response("SubmitID does not exist")
    except Exception as e:
        return Response(e)


@api_view(['GET'])
def viewSubmit(request):
    try:
        data = JSONParser().parse(request)
        if 'id' in data:
            submit = Submits.objects.get(id=data['id'])
            print(data['id'])
            file = open(SUBMIT_DIR / submit.link_submit, 'r')
            data = file.read()
            return HttpResponse(data)
        else:
            return Response("Need submitID to proceed")
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Submits.DoesNotExist:
        return Response("SubmitID does not exist")
    except Exception as e:
        return Response(e)


@api_view(['GET'])
def getSubmits(request):
    submits = list(Submits.objects.all().values())
    # remove link_submit
    res = [{k: v for k, v in d.items() if k != 'link_submit'} for d in submits]
    # change time format
    for item in res:
        item['time_submit'] = item['time_submit'].strftime("%d-%m-%Y %H:%M:%S")
    return Response(res)


@api_view(['POST'])
def createSubmit(request):
    try:
        submit_data = {
            "id_contest": int(request.data['id_contest']),
            "username": request.data['username'],
            "language": request.data['language']
        }
        code = request.data['code']
        type = code.name.split('.')[1]
        name = secrets.token_hex(16) + '.' + type
        fs = FileSystemStorage(location=SUBMIT_DIR)
        fs.save(name, code)
        submit_data["link_submit"] = name
        submit_serializer = SubmitSerializer(data=submit_data)
        if submit_serializer.is_valid():
            submit_serializer.save()
            return Response("Added Successfully")
        return Response(submit_serializer.errors)
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Exception as e:
        return Response(e)
