
class EndPoints:
    BASE_URL = "https://api.adviceslip.com"
    ADVICE_ENDPOINT = f"{BASE_URL}/advice"
    ADVICE_SEARCH_ENDPOINT = f"{ADVICE_ENDPOINT}/search"

class SlipId:
    INVALID = "999"

class ErrorMessage:
    ERROR_TYPE = "error"
    ADVICE_SLIP_NOT_FOUND = "Advice slip not found."