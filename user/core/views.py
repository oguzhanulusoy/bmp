from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from http import HTTPStatus
from datetime import timedelta

from .models import User, UserToken

import json
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
def auth(request):
    context = {}
    status = 0
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data["username"]
        if username is not None:
            # TODO: Check whether user is already authenticated, or not
            try:
                username = data["username"]
                password = data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    user = User.objects.get(username=username)
                    expiration_time = timezone.now().date() + timedelta(days=1)
                    user_token = UserToken.objects.create(user=user, token=get_token(), date_expired=expiration_time)
                    context = {response: user_token.serialize()}
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
