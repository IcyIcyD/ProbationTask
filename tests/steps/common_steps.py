from tests.asserts.asserts import check_signal_statuses, check_pin_voltages, check_signal_status, check_pin_voltage
from tests.constants.pin_ids import PinIDs
from tests.constants.signal_ids import SignalIDs


def get_and_check_signals(api_client, gear_pos=None, acc_pos=None, brake_state=None, req_torque=None,
                          battery_state=None):
    """Gets all signal values and checks chosen signals.

    exp_signals dict example:
    {"GearPosition": "Drive",
     "AccPedalPos": "0 %",
     "BrakePedalState": "Released",
     "ReqTorque": "0 Nm",
     "BatteryState": "Ready"}

     @:param api_client (APIClient): Instance of API client.
     @:param gear_pos (str): Expected GearPosition signal value.
     @:param acc_pos (str): Expected AccPedalPos signal value.
     @:param brake_state (str): Expected BrakePedalState signal value.
     @:param req_torque (str): Expected ReqTorque signal value.
     @:param battery_state (str): Expected BatteryState signal value.
     @:returns exp_signals (dict): Dict with expected signal values.
     @:raises AssertionError.
    """
    actual_signals = api_client.get_all_signals()

    exp_signals = {}
    for name, value in [
        [SignalIDs.NAME_GEAR_POS, gear_pos],
        [SignalIDs.NAME_ACC_PEDAL_POS, acc_pos],
        [SignalIDs.NAME_BRAKE_PEDAL_STATE, brake_state],
        [SignalIDs.NAME_REQ_TORQUE, req_torque],
        [SignalIDs.NAME_BATTERY_STATE, battery_state]
    ]:
        if value is not None:
            exp_signals[name] = value

    check_signal_statuses(get_signals_response=actual_signals, exp_values=exp_signals)
    return exp_signals


def get_and_check_signal(api_client, signal_id, exp_value):
    """Gets specified signal value and check it.

     @:param api_client (APIClient): Instance of API client.
     @:param signal_id (int): ID of signal.
     @:param exp_value (str): Expected signal value.
     @:raises AssertionError.
    """
    actual_signal = api_client.get_signal(signal_id=signal_id)
    check_signal_status(get_signal_response=actual_signal, exp_value=exp_value)


def get_and_check_pins(api_client, gear_1=None, gear_2=None, acc_ped=None, brake_ped=None, battery_vol=None):
    """Gets all pin voltages and checks chosen pins.

    exp_pins dict example:
    {1: 0.67,
     2: 3.12,
     3: 1,
     4: 1,
     5: 600}

     @:param gear_1 (float): Expected Gear_1 pin voltage.
     @:param gear_2 (float): Expected Gear_2 pin voltage.
     @:param acc_ped (float): Expected AccPedal pin voltage.
     @:param brake_ped (float): Expected BrakePedal pin voltage.
     @:param battery_vol (float): Expected BatteryVoltage pin voltage.
     @:returns exp_pins (dict): Dict with expected pin voltages.
     @:raises AssertionError.
    """
    actual_pins = api_client.get_all_pins()
    exp_pins = {}
    for name, value in [
        [PinIDs.ID_GEAR_1, gear_1],
        [PinIDs.ID_GEAR_2, gear_2],
        [PinIDs.ID_ACC_PEDAL, acc_ped],
        [PinIDs.ID_BRAKE_PEDAL, brake_ped],
        [PinIDs.ID_BATTERY_VOLTAGE, battery_vol]
    ]:
        if value is not None:
            exp_pins[name] = value

    check_pin_voltages(get_pins_response=actual_pins, exp_values=exp_pins)
    return exp_pins


def get_and_check_pin(api_client, pin_id, exp_voltage):
    """Gets specified pin voltage and check it.

     @:param api_client (APIClient): Instance of API client.
     @:param pin_id (int): ID of pin.
     @:param exp_voltage (float): Expected pin voltage.
     @:raises AssertionError.
    """
    actual_pin = api_client.get_pin(pin_id=pin_id)
    check_pin_voltage(get_pin_response=actual_pin, exp_voltage=exp_voltage)
