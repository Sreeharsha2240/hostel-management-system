from .http import api_error


def validation_response(error):
    code = getattr(error, "code", None) or "VALIDATION_ERROR"
    if code == "NOT_FOUND":
        status = 404
    elif code in {
        "BED_OCCUPIED",
        "ALREADY_ALLOCATED",
        "ALREADY_RELEASED",
        "HAS_ACTIVE_ALLOCATION",
    }:
        status = 409
    elif code in {
        "GENDER_MISMATCH",
        "IMMUTABLE_FIELD",
        "INACTIVE_STUDENT",
        "INACTIVE_HOSTEL",
    }:
        status = 422
    else:
        status = 400
    return api_error("; ".join(error.messages), code=code, status=status)
