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
    try:
        account_data = JSONParser().parse(request)
        username = account_data['username']
        password = account_data['password']
        token = secrets.token_hex(16)
        account_data['token'] = token
        accounts = list(Accounts.objects.all().values())
        res = "Account doesn't existed"
        for account in accounts:
            if account['username'] == username:
                fernet = Fernet(bytes(account['key'], "utf-8"))
                if fernet.decrypt(bytes(account['password'], "utf-8")).decode() == password:
                    res = token
                    account_save = Accounts.objects.get(username=account_data['username'])
                    account_save_data = account_data
                    account_save_data['password'] = account['password']
                    account_save_data['token'] = token
                    account_serializer = AccountSerializer(account_save, data=account_save_data)
                    if account_serializer.is_valid():
                        account_serializer.save()
                    print(account_serializer.errors)
                    break
                res = "Wrong password"
                break
        return JsonResponse(res, safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)


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

