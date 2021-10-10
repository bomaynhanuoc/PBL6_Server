import secrets
from cryptography.fernet import  Fernet
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.account.models import Accounts, AccountSerializer

#key = Fernet.generate_key()


def getAccounts(request):
    accounts = list(Accounts.objects.all().values())
    account_serializer = AccountSerializer(data=accounts, many=True)
    if account_serializer.is_valid():
        return JsonResponse(account_serializer.data, safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


def createAccount(request):
    account_data = JSONParser().parse(request)
    account_data['key'] = Fernet.generate_key().decode("utf-8")
    fernet = Fernet(account_data['key'])
    account_data['token'] = secrets.token_hex(16)
    account_data['password'] = fernet.encrypt(account_data['password'].encode()).decode("utf-8")
    account_serializer = AccountSerializer(data=account_data)
    if account_serializer.is_valid():
        account_serializer.save()
        return JsonResponse("Added Successfully", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


def updateAccount(request):
    account_data = JSONParser().parse(request)
    try:
        account = Accounts.objects.get(username=account_data['username'])
        fernet = Fernet(account.key)
        account_data['password'] = fernet.encrypt(account_data['password'].encode()).decode("utf-8")
        # print(account.key)
        account_serializer = AccountSerializer(account, data=account_data)
        if account_serializer.is_valid():
            account_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


def deleteAccount(request):
    account_data = JSONParser().parse(request)
    try:
        account = Accounts.objects.get(username=account_data['username'])
        account.delete()
        return JsonResponse("Delete Successfully", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)


def loginAccount(request):
    account_data = JSONParser().parse(request)
    try:
        account = Accounts.objects.get(username=account_data['username'])
        token = secrets.token_hex(16)
        fernet = Fernet(account.key)
        # print(account.key)
        if account_data['password'] == fernet.decrypt(bytes(account.password, "utf-8")).decode():
            account_data['password'] = account.password
            account_data['token'] = token
            account_serializer = AccountSerializer(account, data=account_data)
            if account_serializer.is_valid():
                account_serializer.save()
                return JsonResponse(token, safe=False)
        else:
            return JsonResponse("Wrong password", safe=False)
    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


def logoutAccount(request):
    try:
        account_data = JSONParser().parse(request)
        account = Accounts.objects.get(username=account_data['username'])
        account_data['token'] = ""
        account_serializer = AccountSerializer(account, data=account_data)
        if account_serializer.is_valid():
            account_serializer.save()
            return JsonResponse("Logged out Successfully", safe=False)

    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)

