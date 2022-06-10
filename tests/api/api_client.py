from framework.api.base_api_client import BaseAPIClient
from framework.constants.common_constants import DATA_TYPE_JSON
from tests.constants.api_constants import APIConstants
from tests.models.update_pins_model import UpdatePinsModel


class APIClient(BaseAPIClient):

    def get_all_pins(self):
        """API method that returns all pins info.

        @:returns (requests.Response): API response.
        """
        return self._request_get(APIConstants.GET_ALL_PINS)

    def get_pin(self, pin_id):
        """API method that returns specific pin info.

        @:param pin_id (int): PinId of specific pin.
        @:returns (requests.Response): API response.
        """
        return self._request_get(APIConstants.GET_ONE_PIN.format(pin_id=pin_id))

    def update_pin(self, pin_id, voltage):
        """API method that updates voltage of specified pin.

        @:param pin_id (int): PinId of specific pin.
        @:param voltage (float): Voltage.
        @:returns (requests.Response): API response.
        """
        return self._request_post(APIConstants.UPDATE_ONE_PIN.format(pin_id=pin_id),
                                  data={APIConstants.PARAM_VOLTAGE: voltage})

    def update_pins(self, pin_1=None, pin_2=None, pin_3=None, pin_4=None, pin_5=None):
        """API method that updates voltage of chosen pins.

        @:param pin_1 (float): Voltage of pin #1.
        @:param pin_2 (float): Voltage of pin #2.
        @:param pin_3 (float): Voltage of pin #3.
        @:param pin_4 (float): Voltage of pin #4.
        @:param pin_5 (float): Voltage of pin #5.
        @:returns (requests.Response): API response.
        """
        model = UpdatePinsModel(pin_1=pin_1, pin_2=pin_2, pin_3=pin_3, pin_4=pin_4, pin_5=pin_5)
        headers = {'content-type': DATA_TYPE_JSON}
        return self._request_post(APIConstants.UPDATE_MULTIPLE_PINS, headers=headers, json=model.to_dict())

    def get_all_signals(self):
        """API method that returns all signals info.

        @:returns (requests.Response): API response.
        """
        return self._request_get(APIConstants.GET_ALL_SIGNALS)

    def get_signal(self, signal_id):
        """API method that returns info of specified signal.

        @:param signal_id (int): SigId.
        @:returns (requests.Response): API response.
        """
        return self._request_get(APIConstants.GET_ONE_SIGNAL.format(signal_id=signal_id))
