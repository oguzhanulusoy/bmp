import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from http import HTTPStatus

from .models import User, UserToken

import logging
import random

is_log = True
response = 'response'
no_context = 'not found'


def get_user_list(request):
    context = {}
    status = 0
    if request.method == 'GET':
        try:
            users = User.objects.all()
            context = {response: [user.serialize() for user in users]}
            status = HTTPStatus.ACCEPTED
            if is_log:
                logging.info("Retrieved all users from database.")
        except Exception as e:
            context[response] = no_context
            status = HTTPStatus.NOT_FOUND
            if is_log:
                logging.error(e)
        return JsonResponse(context, status=status)
    else:
        context[response] = no_context
        status = HTTPStatus.BAD_REQUEST
        if is_log:
            logging.error("Invalid get request")
        return JsonResponse(context, status=status)


def get_user_by_email(request, email):
    context = {}
    status = 0
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
            context = {response: user.serialize()}
            status = HTTPStatus.ACCEPTED
            if is_log:
                logging.info("Retrieved user accordance with e-mail from database.")
        except Exception as e:
            context[response] = no_context
            status = HTTPStatus.NOT_FOUND
            if is_log:
                logging.error(e)
        return JsonResponse(context, status=status)
    else:
        context[response] = no_context
        status = HTTPStatus.BAD_REQUEST
        if is_log:
            logging.error("Invalid get request")
        return JsonResponse(context, status=status)


def get_user_by_pk(request, pk):
    context = {}
    status = 0
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=pk)
            context = {response: user.serialize()}
            status = HTTPStatus.ACCEPTED
            if is_log:
                logging.info("Retrieved user accordance with pk from database.")
        except Exception as e:
            context[response] = no_context
            status = HTTPStatus.NOT_FOUND
            if is_log:
                logging.error(e)
        return JsonResponse(context, status=status)
    else:
        context[response] = no_context
        status = HTTPStatus.BAD_REQUEST
        if is_log:
            logging.error("Invalid get request")
        return JsonResponse(context, status=status)


@csrf_exempt
def log(request):
    context = {}
    status = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data["username"]
        if username is not None:
            user = get_object_or_404(User, username=username)
            try:
                username = data["username"]
                password = data["password"]
                print("burda")
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    user_token = User.objects.create(user=user, token=get_token(), date_expired=datetime.datetime.now().day(1))
                    print(user_token)
                    # context = {response: [user.serialize() for user in users]}
                    status = HTTPStatus.ACCEPTED
                else:
                    context[response] = no_context
                    status = HTTPStatus.NOT_FOUND
            except Exception as e:
                context[response] = no_context
                status = HTTPStatus.NOT_FOUND
                if is_log:
                    logging.error(e)
            return JsonResponse(context, status=status)
        else:
            context[response] = no_context
            status = HTTPStatus.BAD_REQUEST
            if is_log:
                logging.error("Invalid get request")
            return JsonResponse(context, status=status)
    else:
        context[response] = no_context
        status = HTTPStatus.BAD_REQUEST
        if is_log:
            logging.error("Invalid get request")
        return JsonResponse(context, status=status)


def get_token(size=50):
    sys_random = random.SystemRandom()
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    return ''.join(sys_random.choices(letters, k=size))
