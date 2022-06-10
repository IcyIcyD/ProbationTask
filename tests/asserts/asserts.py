from framework.asserts.asserts import soft_assert
from tests.constants.api_constants import APIConstants


def check_pin_voltages(get_pins_response, exp_values):
    """Assert for multiple pin voltages.

    @:param get_pins_response (requests.Response): Response of `get_all_pins` API method.
    @:param exp_values (dict): Expected values.
    @:raises AssertionError
    """
    actual_values = {}
    content = get_pins_response.json()
    for pin_info in content:
        if pin_info[APIConstants.RESPONSE_PARAM_PINID] in exp_values.keys():
            actual_values.update({pin_info[APIConstants.RESPONSE_PARAM_PINID]:
                                  pin_info[APIConstants.RESPONSE_PARAM_VOLTAGE]})
    soft_assert(actual_values, exp_values)


def check_signal_statuses(get_signals_response, exp_values):
    """Assert for multiple signal statuses.

    @:param get_signals_response (requests.Response): Response of `get_all_signals` API method.
    @:param exp_values (dict): Expected values.
    @:raises AssertionError
    """
    actual_values = {}
    content = get_signals_response.json()
    for sig_info in content:
        if sig_info[APIConstants.RESPONSE_PARAM_NAME] in exp_values.keys():
            actual_values.update({sig_info[APIConstants.RESPONSE_PARAM_NAME]:
                                  sig_info[APIConstants.RESPONSE_PARAM_VALUE]})
    soft_assert(actual_values, exp_values)


def check_signal_status(get_signal_response, exp_value):
    """Assert for a single signal status.

    @:param get_signal_response (requests.Response): Response of `get_signal` API method.
    @:param exp_value (str): Expected signal status.
    @:raises AssertionError
    """
    content = get_signal_response.json()
    assert content[APIConstants.RESPONSE_PARAM_VALUE] == exp_value, \
        f"Wrong value for signal '{content[APIConstants.RESPONSE_PARAM_NAME]}'. " \
        f"Expected: {exp_value}; Got: {content[APIConstants.RESPONSE_PARAM_VALUE]}"


def check_pin_voltage(get_pin_response, exp_voltage):
    """Assert for a single pin voltage.

    @:param get_signal_response (requests.Response): Response of `get_pin` API method.
    @:param exp_value (float): Expected pin voltage.
    @:raises AssertionError
    """
    content = get_pin_response.json()
    assert content[APIConstants.RESPONSE_PARAM_VOLTAGE] == exp_voltage, \
        f"Wrong voltage for pin '{content[APIConstants.RESPONSE_PARAM_NAME]}'. " \
        f"Expected: {exp_voltage}; Got: {content[APIConstants.RESPONSE_PARAM_VOLTAGE]}"
