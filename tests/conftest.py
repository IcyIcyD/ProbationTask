import allure
import pytest

from tests.api.api_client import APIClient
from tests.constants.api_constants import APIConstants
from tests.constants.pin_ids import PinIDs
from tests.constants.pin_values import PinValues


@pytest.fixture(scope="session")
def api_client():
    """Basic fixture for opening API session."""
    api_client = APIClient(url=APIConstants.BASE_API_URL)
    yield api_client


@pytest.fixture()
def setup_vehicle_state(api_client):
    """Fixture for preparing vehicle state. Changes all pins to given values."""

    def setup(pin_1, pin_2, pin_3, pin_4, pin_5):
        """Preparing vehicle state, considering all the restrictions:

        1. BatteryState should be "Ready".
        2. To change GearPosition, AccPedalPos should be "0%" and BrakePedalState should be "Pressed".
        3. To change AccPedalPos, BrakePedalState should be "Released".

        @:param pin_1 (float): Voltage of pin #1.
        @:param pin_2 (float): Voltage of pin #2.
        @:param pin_3 (float): Voltage of pin #3.
        @:param pin_4 (float): Voltage of pin #4.
        @:param pin_5 (float): Voltage of pin #5.
        """
        with allure.step(f"Preconditions: Gear_1 = {pin_1}, Gear_2 = {pin_2}, AccPos = {pin_3}, "
                         f"BrakePedal = {pin_4}, BatteryVoltage = {pin_5}"):
            # BatteryState should be "Ready"
            api_client.update_pin(pin_id=PinIDs.ID_BATTERY_VOLTAGE, voltage=PinValues.BATTERY_VOLTAGE_READY)

            # To change GearPosition, AccPedalPos should be "0%" and BrakePedalState should be "Pressed"
            api_client.update_pins(pin_3=PinValues.ACC_PEDAL_0, pin_4=PinValues.BRAKE_PEDAL_PRESSED)
            api_client.update_pins(pin_1=pin_1, pin_2=pin_2)

            # To change AccPedalPos, BrakePedalState should be "Released"
            api_client.update_pin(pin_id=PinIDs.ID_BRAKE_PEDAL, voltage=PinValues.BRAKE_PEDAL_RELEASED)
            api_client.update_pin(pin_id=PinIDs.ID_ACC_PEDAL, voltage=pin_3)

            # Now we can change BrakePedalState and BatteryState
            api_client.update_pins(pin_4=pin_4, pin_5=pin_5)

    yield setup
