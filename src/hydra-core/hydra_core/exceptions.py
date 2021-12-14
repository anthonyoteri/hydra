from __future__ import annotations

from django.utils.translation import gettext_lazy as __
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler


class Http409(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = __("Resource already exist.")
    default_code = "conflict"


class Http503(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = __("Service unavailable.")
    default_code = "error"


class ErrorsFormatter:
    """
    The current formatter gets invalid serializer errors,
    uses DRF standart for code and messaging
    and then parses it to the following format:
    {
        "errors": [
            {
                "message": "Error message",
                "code": "Some code",
                "field": "field_name"
            },
            {
                "message": "Error message",
                "code": "Some code",
                "field": "nested.field_name"
            },
            ...
        ]
    }
    """

    FIELD = "field"
    MESSAGE = "message"
    CODE = "code"
    ERRORS = "errors"

    def __init__(self, exception):
        self.exception = exception

    def __call__(self):
        if hasattr(self.exception, "get_full_details"):
            formatted_errors = self._get_response_json_from_drf_errors(
                serializer_errors=self.exception.get_full_details()
            )
        else:
            formatted_errors = self._get_response_json_from_error_message(
                message=str(self.exception)
            )

        return formatted_errors

    def _get_response_json_from_drf_errors(self, serializer_errors=None):
        if serializer_errors is None:
            serializer_errors = {}

        if isinstance(serializer_errors, list):
            serializer_errors = {
                api_settings.NON_FIELD_ERRORS_KEY: serializer_errors
            }

        list_of_errors = self._get_list_of_errors(
            errors_dict=serializer_errors
        )

        response_data = {self.ERRORS: list_of_errors}

        return response_data

    def _get_response_json_from_error_message(
        self, *, message="", field=None, code="error"
    ):
        error = {self.MESSAGE: message, self.CODE: code}
        if field:
            error[self.FIELD] = field

        return {self.ERRORS: [error]}

    def _unpack(self, obj):
        if isinstance(obj, list) and len(obj) == 1:
            return obj[0]

        return obj

    def _get_list_of_errors(self, field_path="", errors_dict=None):
        """
        Error_dict is in the following format:
        {
            'field1': {
                'message': 'some message..'
                'code' 'some code...'
            },
            'field2: ...'
        }
        """
        if errors_dict is None:
            return []

        message_value = errors_dict.get(self.MESSAGE, None)

        if message_value is not None and (
            isinstance(message_value, (str, exceptions.ErrorDetail))
        ):
            if field_path:
                errors_dict[self.FIELD] = field_path
            return [errors_dict]

        errors_list: list[object] = []
        for key, value in errors_dict.items():
            new_field_path = f"{field_path}.{key}" if field_path else key
            key_is_non_field_errors = key == api_settings.NON_FIELD_ERRORS_KEY

            if isinstance(value, list):
                current_level_error_list = []
                new_value = value

                for error in new_value:
                    # if the type of field_error is list we need to unpack it
                    field_error = self._unpack(error)

                    if not key_is_non_field_errors:
                        field_error[self.FIELD] = new_field_path

                    current_level_error_list.append(field_error)
            else:
                path = (
                    field_path if key_is_non_field_errors else new_field_path
                )

                current_level_error_list = self._get_list_of_errors(
                    field_path=path, errors_dict=value
                )

            errors_list += current_level_error_list

        return errors_list


def _exception_errors_format_handler(exc, context):
    response = exception_handler(exc, context)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    formatter = ErrorsFormatter(exc)

    response.data = formatter()

    return response
