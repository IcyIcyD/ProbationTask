import allure
import pytest

from tests.constants.pin_ids import PinIDs
from tests.constants.pin_values import PinValues
from tests.constants.signal_states import SignalStates
from tests.steps.common_steps import get_and_check_signals


@pytest.mark.xfail(reason="D1")
@pytest.mark.parametrize(
    "pin_1, pin_2, pin_4, pin_5, exp_gear_pos, can_change_req_torque, acc_pedal_30, acc_pedal_50, acc_pedal_100",
    [
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, 2,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_DRIVE, True, 2, 2.5, 3),
       pytest.param(PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, 2.01,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_REVERSE, True, 2.01, 2.51, 3.01),
       pytest.param(PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_NEUTRAL, 2.5,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_NEUTRAL, False, 2.25, 2.75, 3.25),
       pytest.param(PinValues.GEAR_1_PARK, PinValues.GEAR_2_PARK, 2.99,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_PARK, False, 2.49, 2.99, 3.49),
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, 1,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_DRIVE, False, 2, 2.5, 3),
       pytest.param(PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, 1,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_REVERSE, False, 2, 2.5, 3),
       pytest.param(PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_NEUTRAL, 1,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_NEUTRAL, False, 2, 2.5, 3),
       pytest.param(PinValues.GEAR_1_PARK, PinValues.GEAR_2_PARK, 1,
                    PinValues.BATTERY_VOLTAGE_READY, SignalStates.GEAR_POS_PARK, False, 2, 2.5, 3),
    ],
    ids=["5", "6", "7", "8", "9", "10", "11", "12"]
)
def test_change_acc_pedal_pos(api_client, setup_vehicle_state, pin_1, pin_2, pin_4, pin_5, exp_gear_pos,
                              can_change_req_torque, acc_pedal_30, acc_pedal_50, acc_pedal_100):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=PinValues.ACC_PEDAL_0, pin_4=pin_4, pin_5=pin_5)

    with allure.step("Step 1. AccPedalPos = 0%. Check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=exp_gear_pos, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED if pin_4 == PinValues.BRAKE_PEDAL_PRESSED
            else SignalStates.BRAKE_STATE_RELEASED,
            req_torque=SignalStates.REQ_TORQUE_0, battery_state=SignalStates.BATTERY_STATE_READY)

    for acc_pedal, acc_pos, req_torque, step in [
        [acc_pedal_30, SignalStates.ACC_POS_30, SignalStates.REQ_TORQUE_3000, 2],
        [acc_pedal_50, SignalStates.ACC_POS_50, SignalStates.REQ_TORQUE_5000, 3],
        [acc_pedal_100, SignalStates.ACC_POS_100, SignalStates.REQ_TORQUE_10000, 4]
    ]:
        with allure.step(f"Step {step}. Change AccPedalPos to {acc_pos}, check vehicle state"):
            api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=acc_pedal)
            get_and_check_signals(
                api_client=api_client, gear_pos=exp_gear_pos, acc_pos=acc_pos,
                brake_state=SignalStates.BRAKE_STATE_PRESSED if pin_4 == PinValues.BRAKE_PEDAL_PRESSED
                else SignalStates.BRAKE_STATE_RELEASED,
                req_torque=req_torque if can_change_req_torque else SignalStates.REQ_TORQUE_0,
                battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.parametrize(
    "pin_1, pin_2, pin_3, pin_4, pin_5",
    [
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, 0, PinValues.BRAKE_PEDAL_RELEASED,
                    PinValues.BATTERY_VOLTAGE_READY),
       pytest.param(PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, 3.5, PinValues.BRAKE_PEDAL_RELEASED,
                    PinValues.BATTERY_VOLTAGE_READY),
    ],
    ids=["17", "19"]
)
def test_change_acc_pedal_pos_to_error(api_client, setup_vehicle_state, pin_1, pin_2, pin_3, pin_4, pin_5):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)

    with allure.step("Step 1. Get all signals, check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_ERROR,
            brake_state=SignalStates.BRAKE_STATE_RELEASED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.id("18")
def test_change_gear_pos_after_acc_pedal_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_DRIVE, pin_2=PinValues.GEAR_2_DRIVE, pin_3=PinValues.ACC_PEDAL_ERROR_2,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    with allure.step("Step 1. Change AccPedalPos to 0%, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_0)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_DRIVE, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.id("20")
def test_change_gear_acc_pos_req_torque_after_acc_pedal_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_REVERSE, pin_2=PinValues.GEAR_2_REVERSE, pin_3=PinValues.ACC_PEDAL_30,
                        pin_4=PinValues.BRAKE_PEDAL_RELEASED, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    with allure.step("Step 1. Change AccPedalPos to Error, check vehicle state"):
        api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=PinValues.ACC_PEDAL_ERROR_3)
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_ERROR,
            brake_state=SignalStates.BRAKE_STATE_RELEASED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.id("21")
def test_acc_pedal_error_brake_pedal_error(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_REVERSE, pin_2=PinValues.GEAR_2_REVERSE, pin_3=PinValues.ACC_PEDAL_ERROR,
                        pin_4=PinValues.BRAKE_PEDAL_ERROR, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    with allure.step("Step 1. Get all signals, check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=SignalStates.GEAR_POS_NEUTRAL, acc_pos=SignalStates.ACC_POS_ERROR,
            brake_state=SignalStates.BRAKE_STATE_ERROR, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)
