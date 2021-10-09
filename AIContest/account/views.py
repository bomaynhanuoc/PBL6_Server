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
    print(fernet.encrypt(account_data['password'].encode()))
    account_serializer = AccountSerializer(data=account_data)
    if account_serializer.is_valid():
        account_serializer.save()
        return JsonResponse("Added Successfully", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


def updateAccount(request):
    account_data = JSONParser().parse(request)
    try:
        account = Accounts.objects.get(username=account_data['username'])
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
    a = []
    try:
        account_data = JSONParser().parse(request)
        username = account_data['username']
        password = account_data['password']
        accounts = list(Accounts.objects.all().values())

        account = Accounts.objects.get(username=account_data['username'])
        account_serializer = AccountSerializer(account, data=account_data)

        for i, j in enumerate(accounts):
            if j['username'] == username:
                fernet = Fernet(bytes(j['key'], "utf-8"))
                #print(bytes(j['password'], "utf-8"))
                #print(fernet.decrypt(bytes(j['password'], "utf-8")).decode())
                #test = fernet.encrypt(password.encode())
                #check = fernet.decrypt(bytes(j['password'], "utf-8")).decode()
                #print(check)
                #print(bytes(fernet.decrypt(j['password'])).decode())
                if fernet.decrypt(bytes(j['password'], "utf-8")).decode() == password:
                    a = j['token']
                    break
                a = "Password is wrong"
                break
            if accounts[i]['username'] != username:
                a = "Account doesn't existed"
        return JsonResponse(a, safe=False)
    except:
        return JsonResponse("You got error!!!", safe=False)

def logoutAccount(request):
    try:
        account_data = JSONParser().parse(request)
        account = Accounts.objects.get(username=account_data['username'])
        # account_data = account
        account_data['token'] = secrets.token_hex(16)
        account_serializer = AccountSerializer(account, data=account_data)
        # username = account_data['username']
        # accounts = list(Accounts.objects.all().values())
        # for account in accounts:
        #     if account['username'] == username:
        #         account['token'] = secrets.token_hex(16)
        #         account_serializer = AccountSerializer(account_data, data=account)
        if account_serializer.is_valid():
            account_serializer.save()
            return JsonResponse("Logged out Successfully", safe=False)

    except Accounts.DoesNotExist:
        return JsonResponse("Account doesn't existed", safe=False)
    return JsonResponse(account_serializer.errors, safe=False)

