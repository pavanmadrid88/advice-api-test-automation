import pytest
import data.constants
from models.response.advice_model import AdviceResponse, SearchResponse, ErrorResponse
from utils.api_utils import validate_schema, parse_model


def test_get_advice_random(api_client,get_advice_endpoint, get_logger):
    response = api_client.get(get_advice_endpoint)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    # validate response schema
    assert validate_schema(AdviceResponse, response.json()), "Response schema mismatch"
    advice_response_model = parse_model(AdviceResponse, response.json())
    assert advice_response_model.slip.id > 0, "Slip ID must be positive"
    assert advice_response_model.slip.advice.strip(), "Advice must be non-empty"
    get_logger.info(f"Advice returned for id {advice_response_model.slip.id}:{advice_response_model.slip.advice}")


@pytest.mark.parametrize("slip_id", [1, 2, 3, 4, 5])
def test_get_advice_by_id(api_client,get_advice_endpoint, get_logger, slip_id):
    response = api_client.get(f"{get_advice_endpoint}/{slip_id}")
    assert response.status_code == 200, "Response status code should be 200"
    # validate response schema
    assert validate_schema(AdviceResponse, response.json()), "Response schema mismatch"
    advice_response_model = parse_model(AdviceResponse, response.json())
    # validate response slip_id
    assert int(slip_id) == int(advice_response_model.slip.id), (f"Slip ID in response {advice_response_model.slip.id} should match the path "
                                                 f"parameter : {slip_id}")
    get_logger.info(f"Advice returned for id {slip_id}:{advice_response_model.slip.advice}")



@pytest.mark.parametrize("search_query", ["happy", "life"])
def test_search_advice(api_client,get_advice_search_endpoint, get_logger, search_query):
    response = api_client.get(f"{get_advice_search_endpoint}/{search_query}")
    assert response.status_code == 200, "Response status code should be 200"

    # validate response schema
    assert validate_schema(SearchResponse, response.json()), "Response schema mismatch"
    search_advice_response_model = parse_model(SearchResponse, response.json())
    total_search_results = search_advice_response_model.total_results
    assert int(total_search_results) >= 1, f"No search results returned for query : {search_query}"

    # Iterate over slips and ensure search_query appears in advice text
    for slip in search_advice_response_model.slips:
        advice_text = slip.advice
        # Assert that each advice text contains the search query
        assert search_query.lower() in advice_text.lower(), (f"Expected search term '{search_query}' "
                                                             f"to be present in advice text: '{slip.advice}'")

    get_logger.info(f"All {len(search_advice_response_model.slips)} advice(s) contain the search term '{search_query}'.")


def test_invalid_advice(api_client,get_advice_endpoint, get_logger):
    invalid_slip_id = data.constants.SlipId.INVALID
    response = api_client.get(f"{get_advice_endpoint}/{invalid_slip_id}")
    assert response.status_code == 200, "Response status code should be 200"

    # validate response schema
    assert validate_schema(ErrorResponse,response.json()),"Response schema validation failed"

    # validate error response type and message text
    error_response_model = parse_model(ErrorResponse,response.json())
    error_response_type = error_response_model.message.type
    error_response_message_text = error_response_model.message.text
    assert str(error_response_type).upper().strip() == str(data.constants.ErrorMessage.ERROR_TYPE).upper().strip() ,\
        "Response type must be error for invalid advice ID"
    assert (str(error_response_message_text).upper().strip() == str(data.constants.ErrorMessage.ADVICE_SLIP_NOT_FOUND).
            strip().upper()), "Response must contain error message text"
    get_logger.info(f"Received expected error for invalid id {invalid_slip_id}: {error_response_message_text}")
