import json
import typing
from typing import Mapping, NoReturn

from aiohttp.web import (
    HTTPBadRequest,
    HTTPConflict,
    HTTPForbidden,
    HTTPNotFound,
    HTTPUnprocessableEntity,
)
from marshmallow import Schema, ValidationError

if typing.TYPE_CHECKING:
    from app.web.app import Request

REQUIRED = "Missing data for required field."
INVALID_EMAIL = "Not a valid email address."
AT_LEAST_TWO_ANSW = "Question must have at least 2 answers"
AT_LEAST_ONE_CORRECT_ANSW = "At least one correct answer required."
ONLY_ONE_CORRECTS_ANSW = "Only one correct answer allowed."
QUESTION_ALREADY_EXISTS = "Question with this title already exists."


# 400
def handle_bad_request(
    error: ValidationError,
    error_headers: Mapping[str, str] | None = None,
) -> NoReturn:
    raise HTTPBadRequest(
        text=json.dumps(error.messages_dict),
        headers=error_headers,
        content_type="application/json",
    )


# 404
def handle_not_found(
    error: ValidationError,
    error_headers: Mapping[str, str] | None = None,
) -> NoReturn:
    raise HTTPNotFound(
        text=json.dumps(error.messages_dict),
        headers=error_headers,
        content_type="application/json",
    )


def handle_required_error(
    error: ValidationError,
    error_headers: Mapping[str, str] | None = None,
) -> NoReturn:
    raise HTTPUnprocessableEntity(
        text=json.dumps(error.messages_dict),
        headers=error_headers,
        content_type="application/json",
    )


# 403
def handle_invalid_email_error(
    error: ValidationError,
    error_headers: Mapping[str, str] | None = None,
) -> NoReturn:
    raise HTTPForbidden(
        text=json.dumps(error.messages_dict),
        headers=error_headers,
        content_type="application/json",
    )


# 409
def handle_conflict_error(
    error: ValidationError,
    error_headers: Mapping[str, str] | None = None,
) -> NoReturn:
    raise HTTPConflict(
        text=json.dumps(error.messages_dict),
        headers=error_headers,
        content_type="application/json",
    )


ERROR_HANDLERS = {
    REQUIRED: handle_required_error,
    INVALID_EMAIL: handle_invalid_email_error,
    AT_LEAST_ONE_CORRECT_ANSW: handle_bad_request,
    ONLY_ONE_CORRECTS_ANSW: handle_bad_request,
    AT_LEAST_TWO_ANSW: handle_bad_request,
}


def validation_error_handler(
    error: ValidationError,
    req: "Request",
    schema: Schema,
    error_status_code: int | None = None,
    error_headers: Mapping[str, str] | None = None,
) -> NoReturn:
    for errors in error.messages.values():
        for err in errors.values():
            print(err)
            error_type = None
            if err[0] == REQUIRED:
                error_type = REQUIRED
            elif "email" in err[0].lower():
                error_type = INVALID_EMAIL
            elif "at least one correct" in err[0].lower():
                error_type = AT_LEAST_ONE_CORRECT_ANSW
            elif "one correct answer" in err[0].lower():
                error_type = ONLY_ONE_CORRECTS_ANSW
            elif "at least 2 answers" in err[0].lower():
                error_type = AT_LEAST_TWO_ANSW

            if error_type in ERROR_HANDLERS:
                ERROR_HANDLERS[error_type](error, error_headers)

    raise HTTPForbidden(
        text=json.dumps(error.messages_dict),
        headers=error_headers,
        content_type="application/json",
    )
