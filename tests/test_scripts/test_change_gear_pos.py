import allure
import pytest

from tests.constants.pin_ids import PinIDs
from tests.constants.pin_values import PinValues
from tests.constants.signal_ids import SignalIDs
from tests.constants.signal_states import SignalStates
from tests.steps.common_steps import get_and_check_signals, get_and_check_signal


@pytest.mark.parametrize(
    "pin_1, pin_2, pin_3, pin_4, pin_5, exp_gear_pos",
    [
       pytest.param(PinValues.GEAR_1_PARK, PinValues.GEAR_2_PARK, 1, 1, 400.01,
                    SignalStates.GEAR_POS_PARK),
       pytest.param(PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_NEUTRAL, 1.01, 1.01, 600,
                    SignalStates.GEAR_POS_NEUTRAL),
       pytest.param(PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, 1.5, 1.5, 799.99,
                    SignalStates.GEAR_POS_REVERSE),
       pytest.param(PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, 1.99, 1.99, 800,
                    SignalStates.GEAR_POS_DRIVE),
    ],
    ids=["1", "2", "3", "4"]
)
def test_apply_gear_pos(api_client, setup_vehicle_state, pin_1, pin_2, pin_3, pin_4, pin_5, exp_gear_pos):
    setup_vehicle_state(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)

    with allure.step("Step 1. Get all signals, check vehicle state"):
        get_and_check_signals(
            api_client=api_client, gear_pos=exp_gear_pos, acc_pos=SignalStates.ACC_POS_0,
            brake_state=SignalStates.BRAKE_STATE_PRESSED, req_torque=SignalStates.REQ_TORQUE_0,
            battery_state=SignalStates.BATTERY_STATE_READY)


@pytest.mark.id("13")
def test_change_gear_pos(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_PARK, pin_2=PinValues.GEAR_2_PARK, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    with allure.step("Step 1. Check that GearPosition == Park"):
        get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS,
                             exp_value=SignalStates.GEAR_POS_PARK)

    for gear_1, gear_2, exp_gear_pos, step in [
        [PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_NEUTRAL, SignalStates.GEAR_POS_NEUTRAL, 2],
        [PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, SignalStates.GEAR_POS_REVERSE, 3],
        [PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, SignalStates.GEAR_POS_DRIVE, 4],
    ]:
        with allure.step(f"Step {step}. Change Gear_1 to {gear_1}, Gear_2 to {gear_2}, "
                         f"check that GearPosition == {exp_gear_pos}"):
            api_client.update_pins(pin_1=gear_1, pin_2=gear_2)
            get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS, exp_value=exp_gear_pos)


@pytest.mark.id("14")
def test_change_gear_pos_incorrect_values(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_PARK, pin_2=PinValues.GEAR_2_PARK, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    for gear_1, gear_2, step in [
        [PinValues.GEAR_1_PARK, PinValues.GEAR_2_DRIVE, 1],
        [PinValues.GEAR_1_PARK, PinValues.GEAR_2_REVERSE, 2],
        [PinValues.GEAR_1_PARK, PinValues.GEAR_2_NEUTRAL, 3],
        [PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_DRIVE, 4],
        [PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_REVERSE, 5],
        [PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_PARK, 6],
        [PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_DRIVE, 7],
        [PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_NEUTRAL, 8],
        [PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_PARK, 9],
        [PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_REVERSE, 10],
        [PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_NEUTRAL, 11],
        [PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_PARK, 12],
    ]:
        with allure.step(f"Step {step}. Change Gear_1 to {gear_1}, Gear_2 to {gear_2}, "
                         f"check that GearPosition == {SignalStates.GEAR_POS_NEUTRAL}"):
            api_client.update_pins(pin_1=gear_1, pin_2=gear_2)
            get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS,
                                 exp_value=SignalStates.GEAR_POS_NEUTRAL)


@pytest.mark.id("15")
def test_change_gear_pos_with_brake_released(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_PARK, pin_2=PinValues.GEAR_2_PARK, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_RELEASED, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    for gear_1, gear_2, step in [
        [PinValues.GEAR_1_NEUTRAL, PinValues.GEAR_2_NEUTRAL, 1],
        [PinValues.GEAR_1_REVERSE, PinValues.GEAR_2_REVERSE, 2],
        [PinValues.GEAR_1_DRIVE, PinValues.GEAR_2_DRIVE, 3],
    ]:
        with allure.step(f"Step {step}. Change Gear_1 to {gear_1}, Gear_2 to {gear_2}, "
                         f"check that GearPosition == {SignalStates.GEAR_POS_PARK}"):
            api_client.update_pins(pin_1=gear_1, pin_2=gear_2)
            get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS,
                                 exp_value=SignalStates.GEAR_POS_PARK)


@pytest.mark.xfail(reason="D1")
@pytest.mark.ids("16")
def test_change_gear_pos_with_acc_pos_not_zero(api_client, setup_vehicle_state):
    setup_vehicle_state(pin_1=PinValues.GEAR_1_PARK, pin_2=PinValues.GEAR_2_PARK, pin_3=PinValues.ACC_PEDAL_0,
                        pin_4=PinValues.BRAKE_PEDAL_PRESSED, pin_5=PinValues.BATTERY_VOLTAGE_READY)

    for acc_pedal, exp_acc_pos, step in [
        [PinValues.ACC_PEDAL_30, SignalStates.ACC_POS_30, 1],
        [PinValues.ACC_PEDAL_50, SignalStates.ACC_POS_50, 3],
        [PinValues.ACC_PEDAL_100, SignalStates.ACC_POS_100, 5]
    ]:
        with allure.step(f"Step {step}. Change AccPedal to {acc_pedal}, check AccPedalPos and ReqTorque"):
            api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=acc_pedal)
            get_and_check_signals(
                api_client=api_client, acc_pos=exp_acc_pos, req_torque=SignalStates.REQ_TORQUE_0)

        with allure.step(f"Step {step+1}. Change Gear_1 to {PinValues.GEAR_1_NEUTRAL}, "
                         f"Gear_2 to {PinValues.GEAR_2_NEUTRAL}, "
                         f"check that GearPosition == {SignalStates.GEAR_POS_PARK}"):
            api_client.update_pins(pin_1=PinValues.GEAR_1_NEUTRAL, pin_2=PinValues.GEAR_2_NEUTRAL)
            get_and_check_signal(api_client=api_client, signal_id=SignalIDs.ID_GEAR_POS,
                                 exp_value=SignalStates.GEAR_POS_PARK)
