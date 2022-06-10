class APIConstants:
    """Constants class for working with API."""
    BASE_API_URL = "http://localhost:8099/api"

    GET_ALL_PINS = "/pins"
    GET_ONE_PIN = GET_ALL_PINS + "/{pin_id}"
    UPDATE_ONE_PIN = GET_ONE_PIN + "/update_pin"
    UPDATE_MULTIPLE_PINS = GET_ALL_PINS + "/update_pins"
    GET_ALL_SIGNALS = "/signals"
    GET_ONE_SIGNAL = GET_ALL_SIGNALS + "/{signal_id}"

    PARAM_VOLTAGE = "Voltage"

    RESPONSE_PARAM_NAME = "Name"
    RESPONSE_PARAM_PINID = "PinId"
    RESPONSE_PARAM_VOLTAGE = "Voltage"
    RESPONSE_PARAM_VALUE = "Value"
