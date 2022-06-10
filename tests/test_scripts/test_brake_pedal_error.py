import allure
import pytest

from tests.constants.pin_ids import PinIDs
from tests.constants.pin_values import PinValues
from tests.constants.signal_states import SignalStates
from tests.steps.common_steps import get_and_check_signals


@pytest.mark.xfail(reason="D2")
@pytest.mark.parametrize(
    "pin_1, pin_2, pin_3, pin_4, pin_5, exp_acc_pos",
    [
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, PinValues.ACC_PEDAL_30,
                    0.99, PinValues.BATTERY_VOLTAGE_READY, SignalStates.ACC_POS_30),
       pytest.param(PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, PinValues.ACC_PEDAL_50,
                    3.01, PinValues.BATTERY_VOLTAGE_READY, SignalStates.ACC_POS_50),
    ],
    ids=["22", "24"]
)
def test_brake_pedal_error(api_client, setup_vehicle_state, pin_1, pin_2, pin_3, pin_4, pin_5, exp_acc_pos):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)

    with allure.step("Step 1. Get all signals, check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=exp_acc_pos,
            brake_state=SignalStates.BRAKE_STATE_ERROR, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.id("23")
def test_change_gear_pos_after_brake_pedal_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_ERROR_2, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    # TODO Workaround. Reason = D2
    with allure.step("WORKAROUND: change voltages on Gear_1, Gear_2 to Reverse GearPosition"):
        api_client.update_pins(pin_1=PinValues.GEAR_1_REVERSE, pin_2=PinValues.GEAR_2_REVERSE)

    with allure.step("Step 1. Change BrakePedalState to Pressed, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_PRESSED)
        # TODO change SignalStates.GEAR_POS_REVERSE to SignalStates.GEAR_POS_DRIVE after D2 is fixed
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_REVERSE, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.xfail(reason="D2")
@pytest.mark.id("25")
def test_change_gear_pos_while_brake_pedal_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_ERROR, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    with allure.step("Step 1. Change GearPosition to Park, check vehicle state"):
        api_client.update_pins(pin_1=PinValues.GEAR_1_PARK, pin_2=PinValues.GEAR_2_PARK)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_ERROR, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.xfail(reason="D1, D2")
@pytest.mark.id("26")
def test_change_acc_pos_while_brake_pedal_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_30,
                        pin_4=PinValues.BRAKE_PEDAL_ERROR, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    with allure.step("Step 1. Change AccPedalPos to 50%, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_50)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_50,
            brake_state=SignalStates.BRAKE_STATE_ERROR, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)

    with allure.step("Step 2. Change AccPedalPos to 100%, check AccPedalPos and ReqTorque"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_100)
        get_and_check_signals(
            api_client=api_client, acc_pos=SignalStates.ACC_POS_100, req_torque=SignalStates.REQ_TORQUE_0)
