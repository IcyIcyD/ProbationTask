import allure
import pytest

from tests.constants.pin_ids import PinIDs
from tests.constants.pin_values import PinValues
from tests.constants.signal_ids import SignalIDs
from tests.constants.signal_states import SignalStates
from tests.steps.common_steps import get_and_check_signals, get_and_check_pins, get_and_check_signal, get_and_check_pin


@pytest.mark.id("27")
def test_battery_state_not_ready(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_50,
                        pin_4=PinValues.BRAKE_PEDAL_RELEASED, pin_5=PinValues.BATTERY_VOLTAGE_NOT_READY)

    with allure.step("Step 1. Get all signals, check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_50,
            brake_state=SignalStates.BRAKE_STATE_RELEASED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_NOT_READY)


@pytest.mark.id("28")
def test_battery_state_not_ready_change_brake_pos_acc_pos(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_50,
                        pin_4=PinValues.BRAKE_PEDAL_RELEASED, pin_5=PinValues.BATTERY_VOLTAGE_NOT_READY_2)

    with allure.step("Step 1. Change AccPedalPos to 30%, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_30)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_30,
            brake_state=SignalStates.BRAKE_STATE_RELEASED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_NOT_READY)

    with allure.step("Step 2. Change BrakePedalState to Pressed, check BrakePedalState"):
        api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_PRESSED)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_BRAKE_PEDAL_STATE,
                             exp_value=SignalStates.BRAKE_STATE_PRESSED)


@pytest.mark.id("29")
def test_change_gear_after_battery_not_ready(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_NOT_READY_3)

    with allure.step("Step 1. Change BatteryState to Ready, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_BATTERY_VOLTAGE, voltage=PinValues.BATTERY_VOLTAGE_READY)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_DRIVE, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.id("30")
def test_change_gear_while_battery_not_ready(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_NOT_READY_4)

    with allure.step("Step 1. Change GearPosition to Park, check vehicle state"):
        api_client.update_pins(pin_1=PinValues.GEAR_1_PARK, pin_2=PinValues.GEAR_2_PARK)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_NOT_READY)


@pytest.mark.id("31")
def test_change_acc_and_brake_to_error_while_battery_not_ready(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_NOT_READY)

    with allure.step("Step 1. Change AccPedalPos to Error, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_ERROR)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_ERROR,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_NOT_READY)

    with allure.step("Step 2. Change BrakePedalState to Error, check BrakePedalState"):
        api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_ERROR)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_BRAKE_PEDAL_STATE,
                             exp_value=SignalStates.BRAKE_STATE_ERROR)


@pytest.mark.id("32")
def test_battery_state_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_ERROR_2)

    with allure.step("Step 1. Get all signals, check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_ERROR,
            brake_state=SignalStates.BRAKE_STATE_ERROR, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_ERROR)


@pytest.mark.parametrize(
    "pin_1, pin_2, pin_3, pin_4, pin_5",
    [
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, PinValues.ACC_PEDAL_50,
                    PinValues.BRAKE_PEDAL_RELEASED, PinValues.BATTERY_VOLTAGE_READY,
                    marks=[pytest.mark.xfail(reason="D3, D4")]),
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, PinValues.ACC_PEDAL_50,
                    PinValues.BRAKE_PEDAL_RELEASED, PinValues.BATTERY_VOLTAGE_NOT_READY,
                    marks=[pytest.mark.xfail(reason="D4")])
    ],
    ids=["33", "37"]
)
def test_battery_state_error_pins_zero(api_client, setup_vehicle_state, pin_1, pin_2, pin_3, pin_4, pin_5):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)

    with allure.step("Step 1. Set BatteryState to Error. Check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_BATTERY_VOLTAGE, voltage=PinValues.BATTERY_VOLTAGE_ERROR)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_ERROR,
            brake_state=SignalStates.BRAKE_STATE_ERROR, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_ERROR)

    with allure.step("Step 2. Get all pins voltage, check that all of them are 0V"):
        get_and_check_pins(
            api_client=api_client, gear_1=PinValues.PIN_VOLTAGE_ZERO, gear_2=PinValues.PIN_VOLTAGE_ZERO,
            acc_ped=PinValues.PIN_VOLTAGE_ZERO, brake_ped=PinValues.PIN_VOLTAGE_ZERO,
            battery_vol=PinValues.PIN_VOLTAGE_ZERO)


@pytest.mark.xfail(reason="D3, D4")
@pytest.mark.id("34")
def test_battery_state_error_update_pins(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_50,
                        pin_4=PinValues.BRAKE_PEDAL_RELEASED, pin_5=PinValues.BATTERY_VOLTAGE_ERROR_3)

    with allure.step("Step 1. Change Gear_1 pin, check GearPosition, check pin voltage"):
        api_client.update_pin(pin_id=PinIDs.ID_GEAR_2, voltage=PinValues.GEAR_1_PARK)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS,
                             exp_value=SignalStates.GEAR_POS_NEUTRAL)
        get_and_check_pin(api_client=api_client, pin_id=PinIDs.ID_GEAR_1, exp_voltage=PinValues.PIN_VOLTAGE_ZERO)

    with allure.step("Step 2. Change Gear_2 pin, check GearPosition, check pin voltage"):
        api_client.update_pin(pin_id=PinIDs.ID_GEAR_2, voltage=PinValues.GEAR_2_PARK)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS,
                             exp_value=SignalStates.GEAR_POS_NEUTRAL)
        get_and_check_pin(api_client=api_client, pin_id=PinIDs.ID_GEAR_2, exp_voltage=PinValues.PIN_VOLTAGE_ZERO)

    with allure.step("Step 3. Change AccPedal pin, check AccPedalPos, check pin voltage"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_30)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_ACC_PEDAL_POS,
                             exp_value=SignalStates.ACC_POS_ERROR)
        get_and_check_pin(api_client=api_client, pin_id=PinIDs.ID_ACC_PEDAL, exp_voltage=PinValues.PIN_VOLTAGE_ZERO)

    with allure.step("Step 4. Change BrakePedal pin, check BrakePedalState, check pin voltage"):
        api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_RELEASED)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_BRAKE_PEDAL_STATE,
                             exp_value=SignalStates.BRAKE_STATE_ERROR)
        get_and_check_pin(api_client=api_client, pin_id=PinIDs.ID_BRAKE_PEDAL, exp_voltage=PinValues.PIN_VOLTAGE_ZERO)


@pytest.mark.parametrize(
    "pin_1, pin_2, pin_3, pin_4, pin_5",
    [
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, PinValues.ACC_PEDAL_0,
                    PinValues.BRAKE_PEDAL_PRESSED, PinValues.BATTERY_VOLTAGE_ERROR),
    ],
    ids=["35"]
)
def test_battery_state_error_to_not_ready_update_pins(api_client, setup_vehicle_state, pin_1, pin_2, pin_3, pin_4,
                                                      pin_5):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)

    with allure.step(f"Step 1. Gear_1 = {pin_1}, Gear_2 = {pin_2}, AccPedalPos = {pin_3}, "
                     f"BrakePedal = {pin_4}, BatteryVoltage = {PinValues.BATTERY_VOLTAGE_NOT_READY}. "
                     f"Check vehicle state"):
        api_client.update_pins(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4,
                               pin_5=PinValues.BATTERY_VOLTAGE_NOT_READY)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_NOT_READY)

    with allure.step("Step 2. Change BrakePedal pin, check BrakePedalState"):
        api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_RELEASED)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_BRAKE_PEDAL_STATE,
                             exp_value=SignalStates.BRAKE_STATE_RELEASED)

    with allure.step("Step 3. Change AccPedal pin, check AccPedalPos and ReqTorque"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_30)
        get_and_check_signals(
            api_client=api_client, acc_pos=SignalStates.ACC_POS_30, req_torque=SignalStates.REQ_TORQUE_0)


@pytest.mark.parametrize(
    "pin_1, pin_2, pin_3, pin_4, pin_5",
    [
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, PinValues.ACC_PEDAL_0,
                    PinValues.BRAKE_PEDAL_PRESSED, PinValues.BATTERY_VOLTAGE_ERROR),
    ],
    ids=["36"]
)
def test_battery_state_error_to_ready_update_pins(api_client, setup_vehicle_state, pin_1, pin_2, pin_3, pin_4, pin_5):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)

    with allure.step(f"Step 1. Gear_1 = {pin_1}, Gear_2 = {pin_2}, AccPedalPos = {pin_3}, "
                     f"BrakePedal = {pin_4}, BatteryVoltage = {PinValues.BATTERY_VOLTAGE_READY}. "
                     f"Check vehicle state"):
        api_client.update_pins(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4,
                               pin_5=PinValues.BATTERY_VOLTAGE_READY)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_DRIVE, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)

    with allure.step("Step 2. Change BrakePedal pin, check BrakePedalState"):
        api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_RELEASED)
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_BRAKE_PEDAL_STATE,
                             exp_value=SignalStates.BRAKE_STATE_RELEASED)

    with allure.step("Step 3. Change AccPedal pin, check AccPedalPos and ReqTorque"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_30)
        get_and_check_signals(
            api_client=api_client, acc_pos=SignalStates.ACC_POS_30, req_torque=SignalStates.REQ_TORQUE_3000)
