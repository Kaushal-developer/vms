from django.utils.translation import gettext_lazy as _
'''
This is constant file which contains allt the constant required in this project
'''

class Action:
    CREATE = "create"
    DESTROY = "destroy"
    LIST = "list"
    PARTIAL_UPDATE = "partial_update"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    VIEW = "view"
    SELECT = "select"


class FieldConstants:
    PHONE_NUMBER_LENGTH = 12
    PHONE_CODE_LENGTH = 5
    DEFAULT_PHONE_CODE = "91"
    ADDRESS_LENGTH = 200
    NAME_LENGTH = 200
    DATE_TIME_FORMATS = ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S")
    DATE_FORMAT = "%Y-%m-%d"

    TIME_FORMAT = "%H:%M"
    MULTIPLE_DATE_FORMATS = ("%m/%d/%Y", "%m-%d-%Y",
                             "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d")
    
class DateTimeFormat:
    DATE = "%d-%m-%Y"
    DATE_TIME = "%d-%m-%Y %H:%M"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    FULL_DATE_TIME = "%d-%m-%Y %H:%M:%S"
    MULTIPLE_DATE_FORMATS = ("%m/%d/%Y", "%m-%d-%Y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d")
    TIME = "%H:%M"



class Method:
    GET = "get"
    HEAD = "head"
    OPTIONS = "options"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class OrderConstants:
    PENDING,COMPLETED, CANCELLED = ('Pending','Completed', 'Cancelled',)


    @classmethod
    def get_order_status_choices(cls):
        ORDER_STATUS_CHOICES = [(cls.PENDING, 'Pending'), (cls.COMPLETED, 'Completed'), (cls.CANCELLED, 'Cancelled')]
        return ORDER_STATUS_CHOICES

