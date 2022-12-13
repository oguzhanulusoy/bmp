from django.http import JsonResponse
from django.shortcuts import render
from .models import User
import logging
from http import HTTPStatus


is_log = True
response = 'response'
not_found = 'not found'


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
            context[response] = not_found
            status = HTTPStatus.NOT_FOUND
            if is_log:
                logging.error(e)
        return JsonResponse(context, status=status)
    else:
        context[response] = not_found
        status = HTTPStatus.BAD_REQUEST
        if is_log:
            logging.error("Invalid get request")

