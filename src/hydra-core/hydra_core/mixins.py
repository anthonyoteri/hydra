from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, List

from django.core.exceptions import ValidationError as DjangoValidationError
import pydantic
from rest_framework.exceptions import (
    APIException,
    ErrorDetail,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from hydra_core.exceptions import Http409

__all__ = ("ExceptionHandlerMixin",)


ConflictDetail = DefaultDict[str, List[ErrorDetail]]


class ExceptionHandlerMixin:
    """Mixin that transforms Django and Python exceptions into exceptions
    handled by Django REST Framework.

    Without this a generic "500 Internal Server Error" will be returned.
    """

    expected_exceptions = {
        ValueError: ValidationError,
        DjangoValidationError: ValidationError,
        PermissionError: PermissionDenied,
        pydantic.ValidationError: ValidationError,
    }

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            exc = drf_exception_class(_get_error_message(exc))

        if isinstance(exc, ValidationError):
            exc = self.__handle_conflict_exception(exc)

        return APIView.handle_exception(self, exc)

    def __handle_conflict_exception(
        self, exc: ValidationError
    ) -> APIException:
        """Conditionally remap generic validation error to ``Conflict``.

        Looks through a validation error instance for an error detail with the
        code "unique". If it finds one it creates a new exception that produces
        a "409 Conflict" response with the correct error message(s).
        """
        conflict_detail: ConflictDetail = defaultdict(list)

        if isinstance(exc.detail, dict):
            for field, details in exc.detail.items():
                # Ignore nested resources when search for conflict error(s).
                if isinstance(details, dict):
                    continue

                if not isinstance(details, list):
                    details = [details]

                for detail in details:
                    if isinstance(detail, dict):
                        continue
                    if detail.code == "unique":
                        conflict_detail[field].append(detail)

        if conflict_detail:
            return Http409(conflict_detail)

        return exc


def _get_first_matching_attr(obj, *attrs, default=None):
    """Return the value of the attribute that's first found in obj.

    If no attribute was found, return the default value.
    """
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def _get_error_message(exc):
    """Extract error message(s) from Django and Python exceptions."""
    if isinstance(exc, pydantic.ValidationError):
        return _format_pydantic_exception(exc)
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    error_msg = _get_first_matching_attr(exc, "message", "messages")

    if isinstance(error_msg, list):
        error_msg = ", ".join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


def _format_pydantic_exception(exc: pydantic.ValidationError):
    return {
        e["loc"][0]: ErrorDetail(e["msg"], e["type"]) for e in exc.errors()
    }
