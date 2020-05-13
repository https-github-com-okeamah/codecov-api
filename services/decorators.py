from shared.torngit.exceptions import TorngitClientError
from rest_framework.exceptions import APIException
from services.billing import BillingException


def torngit_safe(method):
    """
    Translatess torngit exceptions into DRF APIExceptions.
    For use in DRF views.
    """
    def exec_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except TorngitClientError as e:
            exception = APIException(detail=e.message)
            exception.status_code = e.code
            raise exception
    # This is needed to decorate custom DRF viewset actions
    exec_method.__name__ = method.__name__
    return exec_method


def billing_safe(method):
    """
    Translatess billing exceptions into DRF APIExceptions.
    For use in DRF views.
    """
    def exec_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except BillingException as e:
            exception = APIException(detail=e.message)
            exception.status_code = e.http_status
            raise exception
    exec_method.__name__ = method.__name__
    return exec_method
