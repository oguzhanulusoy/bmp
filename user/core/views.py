from django.http import JsonResponse
from django.shortcuts import render
from .models import User
import logging
from http import HTTPStatus


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