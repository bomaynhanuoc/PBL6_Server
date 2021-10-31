import secrets
from cryptography.fernet import Fernet
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import exceptions
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.account.models import Accounts, AccountSerializer
import json


@api_view(['GET'])
def getAccounts(request):
    try:
        data = JSONParser().parse(request)
        if 'token' in data:
            account = Accounts.objects.get(token=data['token'])
            if account.role == "admin":
                accounts = list(Accounts.objects.all().values())
                return JsonResponse(accounts, safe=False)
            else:
                return JsonResponse("Denied access", safe=False)
        else:
            return JsonResponse("Need token to proceed", safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse("Invalid token", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['POST'])
def createAccount(request):
    try:
        account_data = JSONParser().parse(request)
        if 'username' in account_data and 'password' in account_data:
            if checkUsername(account_data['username']):
                account_data['key'] = Fernet.generate_key().decode("utf-8")
                fernet = Fernet(account_data['key'])
                account_data['token'] = secrets.token_hex(16)
                account_data['password'] = fernet.encrypt(account_data['password'].encode()).decode("utf-8")
                account_serializer = AccountSerializer(data=account_data)
                if account_serializer.is_valid():
                    account_serializer.save()
                    return JsonResponse("Added Successfully", safe=False)
                return JsonResponse(account_serializer.errors, safe=False)
            else:
                return JsonResponse("This username is already taken", safe=False)
        else:
            return JsonResponse("Need username and password to proceed", safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['PATCH'])
def updateAccount(request):
    try:
        account_data = JSONParser().parse(request)
        if 'username' in account_data and 'password' in account_data:
            account = Accounts.objects.get(username=account_data['username'])
            fernet = Fernet(account.key)
            account_data['password'] = fernet.encrypt(account_data['password'].encode()).decode("utf-8")
            account_serializer = AccountSerializer(account, data=account_data)
            if account_serializer.is_valid():
                account_serializer.save()
                return JsonResponse("Updated Successfully", safe=False)
        else:
            return JsonResponse("Need username and password to proceed", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['DELETE'])
def deleteAccount(request):
    try:
        account_data = JSONParser().parse(request)
        if 'username' in account_data:
            account = Accounts.objects.get(username=account_data['username'])
            account.delete()
            return JsonResponse("Delete Successfully", safe=False)
        else:
            return JsonResponse("Need username to proceed", safe=False)
    except Accounts.DoesNotExaist:
        return JsonResponse("Account doesn't existed", safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['POST'])
def loginAccount(request):
    try:
        account_data = JSONParser().parse(request)
        if 'username' in account_data and 'password' in account_data:
            account = Accounts.objects.get(username=account_data['username'])
            token = secrets.token_hex(16)
            fernet = Fernet(account.key)
            if account_data['password'] == fernet.decrypt(bytes(account.password, "utf-8")).decode():
                account_data['password'] = account.password
                account_data['token'] = token
                account_serializer = AccountSerializer(account, data=account_data)
                if account_serializer.is_valid():
                    account_serializer.save()
                    return JsonResponse({"username": account.username, "token": token}, safe=False)
                return JsonResponse(account_serializer.errors, safe=False)
            else:
                return JsonResponse("Wrong password", safe=False)
        else:
            return JsonResponse("Need username and password to proceed", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


@api_view(['POST'])
def logoutAccount(request):
    try:
        account_data = JSONParser().parse(request)
        account = Accounts.objects.get(username=account_data['username'])
        account_data['token'] = secrets.token_hex(16)
        account_serializer = AccountSerializer(account, data=account_data)
        if account_serializer.is_valid():
            account_serializer.save()
            return JsonResponse("Logged out Successfully", safe=False)

    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


@api_view(['GET'])
def checkToken(request):
    try:
        data = JSONParser().parse(request)
        if 'token' in data:
            account = Accounts.objects.get(token=data['token'])
            return JsonResponse({"username": account.username}, safe=False)
        else:
            return JsonResponse("Need token to proceed", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, safe=False)
    except exceptions.ParseError:
        return JsonResponse("Invalid request data", safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


def checkUsername(name):
    try:
        account = Accounts.objects.get(username=name)
    except Accounts.DoesNotExist:
        return True
    return False


def getTokenRole(token):
    try:
        account = Accounts.objects.get(token=token)
        res = {
                "username": account.username,
                "role": account.role
        }
        return res
    except Accounts.DoesNotExist:
        return "Invalid token"
