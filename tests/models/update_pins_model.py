from tests.constants.pin_ids import PinIDs


class UpdatePinsModel:
    """Model for `update_pins` API method input."""

    def __init__(self, pin_1=None, pin_2=None, pin_3=None, pin_4=None, pin_5=None):
        """Model for `update_pins` API method input.

        @:param pin_1 (float): Voltage of pin #1.
        @:param pin_2 (float): Voltage of pin #2.
        @:param pin_3 (float): Voltage of pin #3.
        @:param pin_4 (float): Voltage of pin #4.
        @:param pin_5 (float): Voltage of pin #5.
        """
        self.pins = [pin_1, pin_2, pin_3, pin_4, pin_5]

    def __dict__(self):
        """Represents model in dict format specifically for `update_pins` API method input.

        @:returns dict: Representation of model.
        """
        pins_list = [
            {"PinId": pin_id, "Voltage": voltage} for pin_id, voltage
            in zip(PinIDs.ALL_PIN_IDS, self.pins) if voltage is not None
        ]
        return {"Pins": pins_list}

    def to_dict(self):
        """Represents model in dict format specifically for `update_pins` API method input.

        @:returns dict: Representation of model.
        """
        return self.__dict__()
