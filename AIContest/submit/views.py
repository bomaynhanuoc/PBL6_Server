from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from AIContest.submit.models import Submits, SubmitSerializer
from AIContest.contest.models import Contests
from AIContest.contest.views import findContest, updateRanking
import secrets
import json
from pathlib import Path
import threading
import os
import os.path
import subprocess
from subprocess import PIPE, STDOUT
BASE_DIR = Path(__file__).resolve().parent.parent
SUBMIT_DIR = BASE_DIR / "submit" / "file"
CONTEST_DIR = BASE_DIR / "contest" / "file"


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
                "time_submit": submit.time_submit.strftime("%Y-%m-%d %H:%M:%S")
            }
            return Response(json_res)
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Submits.DoesNotExist:
        return Response("id does not exist")
    except Exception as e:
        return Response(e)


@api_view(['GET'])
def viewSubmit(request):
    try:
        data = JSONParser().parse(request)
        if 'id' in data:
            submit = Submits.objects.get(id=data['id'])
            file = open(SUBMIT_DIR / submit.link_submit.split(".")[0] / submit.link_submit, 'r')
            data = file.read()
            return HttpResponse(data)
        else:
            return Response("Need id to proceed")
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Submits.DoesNotExist:
        return Response("id does not exist")
    except Exception as e:
        return Response(e)


@api_view(['GET'])
def getSubmits(request):
    try:
        data = JSONParser().parse(request)
        if 'id_contest' in data and 'username' in data:
            submits = list(Submits.objects.filter(id_contest=data['id_contest'], username=data['username']).values())
            # remove link_submit
            res = [{k: v for k, v in d.items() if k != 'link_submit'} for d in submits]
            # change time format
            for item in res:
                item['time_submit'] = item['time_submit'].strftime("%d-%m-%Y %H:%M:%S")
            return Response(res)
        else:
            return Response("Need id_contest and username to proceed")
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Exception as e:
        return Response(e)


@api_view(['POST'])
def createSubmit(request):
    try:
        submit_data = {
            "id_contest": int(request.data['id_contest']),
            "username": request.data['username'],
            "language": request.data['language']
        }
        contest = findContest(submit_data["id_contest"])
        jsondec = json.decoder.JSONDecoder()
        languages = jsondec.decode(contest.language)
        if submit_data["language"] not in languages:
            return Response("Invalid language for this contest")
        code = request.data['code']
        type = code.name.split('.')[1]
        if checkType(submit_data["language"], type):
            name = secrets.token_hex(16) + '.' + type
            save_path = SUBMIT_DIR / name.split(".")[0]
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            fs = FileSystemStorage(location=save_path)
            fs.save(name, code)
            submit_data["link_submit"] = name
            submit_serializer = SubmitSerializer(data=submit_data)
            if submit_serializer.is_valid():
                submit_serializer.save()
                try:
                    t1 = threading.Thread(target=checkSubmit, args=(name, save_path, CONTEST_DIR / contest.link_contest / 'input.txt',
                                                                    submit_data['language'], contest.time_out, CONTEST_DIR / contest.link_contest,
                                                                    submit_data["id_contest"], submit_data["username"],))
                    t1.start()
                except:
                    return Response("Error when check submit")
                return Response("Added Successfully")
            return Response(submit_serializer.errors)
        else:
            return Response("Invalid type for " + submit_data["language"])
    except exceptions.ParseError:
        return Response("Invalid request data")
    except Exception as e:
        return Response(e)


def checkType(language, type):
    if language == "Python" and type == "py":
        return True
    elif language == "C" and type == "c":
        return True
    elif language == "C++" and type == "cpp":
        return True
    return False


def checkSubmit(name, path, input_path, language, time_out, file_path, id_contest, username):
    if language == "C" or language == "C++":
        status = c_run(name, path, input_path, time_out)
    elif language == "Python":
        status = py_run(name, path, input_path, time_out)
    else:
        status = "Error"
    submit_id = findSubmit(name)
    if status == "Error" or status == "Time Limit Exceed" or status == "Compile Error" or status == "Runtime Error":
        saveStatus(submit_id, status)
        return
    with open(path / "output.txt", 'w') as f:
        f.write(status)
    subprocess.call(["cp", file_path / "tester.py", path / "tester.py"])
    subprocess.call(["cp", file_path / "data_train.txt", path / "data_train.txt"])
    subprocess.call(["cp", file_path / "data_test.txt", path / "data_test.txt"])
    try:
        tmp = subprocess.run(["python", path / "tester.py"], stdout=PIPE, stderr=PIPE, encoding="utf-8")
        status = tmp.stdout
    except:
        return
    os.remove(path / "tester.py")
    os.remove(path / "data_train.txt")
    os.remove(path / "data_test.txt")
    saveStatus(submit_id, status)
    updateRanking(id_contest, username, float(status))


def saveStatus(id, status):
    submit = Submits.objects.get(id=id)
    submit_data = {
        "id": id,
        "status": status
    }
    submit_serializer = SubmitSerializer(submit, data=submit_data)
    if submit_serializer.is_valid():
        submit_serializer.save()


def findSubmit(name):
    submit = Submits.objects.get(link_submit=name)
    return submit.id


def c_run(name, path, input_path, time_out):
    try:
        build_path = path / name.split(".")[0]
        subprocess.run(["g++", path / name, "-o", build_path], check=True)
    except subprocess.CalledProcessError:
        return "Compile Error"
    try:
        tmp = subprocess.run(str(build_path), stdin=open(input_path, 'r'), stdout=PIPE, stderr=PIPE, timeout=time_out, check=True, encoding="utf-8")
        result = tmp.stdout
    except subprocess.TimeoutExpired:
        result = "Time Limit Exceed"
    except subprocess.CalledProcessError:
        result = "Runtime Error"
    return result


def py_run(name, model_path, input_path, time_out):
    try:
        tmp = subprocess.run(["python", model_path / name], stdin=open(input_path, 'r'), stdout=PIPE, stderr=PIPE, timeout=time_out, check=True, encoding="utf-8")
        result = tmp.stdout
    except subprocess.TimeoutExpired:
        result = "Time Limit Exceed"
    except subprocess.CalledProcessError:
        result = "Runtime Error"
    return result
