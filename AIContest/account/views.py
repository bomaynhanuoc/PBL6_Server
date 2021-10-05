from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from AIContest.account.models import Accounts, AccountSerializer


def getAccounts(request):
    accounts = list(Accounts.objects.all().values())
    account_serializer = AccountSerializer(data=accounts, many=True)
    if account_serializer.is_valid():
        return JsonResponse(account_serializer.data, safe=False)
    return JsonResponse(account_serializer.errors, safe=False)


def createAccount(request):
    account_data = JSONParser().parse(request)
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
    a = ""
    try:
        account_data = JSONParser().parse(request)
        username = account_data['username']
        password = account_data['password']
        accounts = list(Accounts.objects.all().values())
        for i, j in enumerate(accounts):
            if j['username'] == username:
                if j['password'] == password:
                    a = "Successfully"
                    break
                a = "Password is wrong"
                break
            if accounts[i]['username'] != username:
                a = "Account doesn't existed"
        return JsonResponse(a, safe=False)
    except:
        return JsonResponse("You got error!!!", safe=False)

