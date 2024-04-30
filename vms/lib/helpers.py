import logging
import os
from datetime import date, timedelta
from django.core.exceptions import FieldDoesNotExist
from . import constants

logger = logging.getLogger(__name__)

'''
Check the empty fields validation
'''
def check_empty_fields_for_validation(fields_to_check: dict):
    error_dict = {}
    required_error_message = "This field is required"
    for field_name, value in fields_to_check.items():
        if not value:
            error_dict[field_name] = [required_error_message]
    return error_dict

'''
Get Response Message
'''
def get_response_message(data, model, action="create"):
    model_name = model._meta.verbose_name.title()
    obj_response_message = data.get('response_message', model_name)
    response_message = f"{obj_response_message} {action}d successfully"
    return response_message

'''
Format date and time objects to default
'''
def format_date_time(input_date):
    if input_date:
        return input_date.strftime(constants.DateTimeFormat.DATE_TIME)
    return None

'''
Format date to required format
'''
def format_date(input_date, date_format=constants.DateTimeFormat.DATE):
    if input_date:
        return input_date.strftime(date_format)
    return None

'''
Formate time to required format
'''
def format_time(input_time):
    if input_time:
        return input_time.strftime(constants.DateTimeFormat.TIME)
    return None

'''
Removes keys from dict where values are in None, "","N/A"
'''
def remove_null_key_value_pair(dictionary):
    return {k: v for k, v in dictionary.items() if v not in [None, "", "N/A"]}

'''
To get action user name
'''
def get_log_added_by(user):
    return user.full_name


