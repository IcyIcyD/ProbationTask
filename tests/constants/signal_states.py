class SignalStates:
    """Constants class for working with signal outputs."""
    GEAR_POS_PARK = "Park"
    GEAR_POS_NEUTRAL = "Neutral"
    GEAR_POS_REVERSE = "Reverse"
    GEAR_POS_DRIVE = "Drive"

    BRAKE_STATE_PRESSED = "Pressed"
    BRAKE_STATE_RELEASED = "Released"
    BRAKE_STATE_ERROR = "Error"

    ACC_POS_ERROR = "Error"
    ACC_POS_0 = "0 %"
    ACC_POS_30 = "30 %"
    ACC_POS_50 = "50 %"
    ACC_POS_100 = "100 %"

    REQ_TORQUE_0 = "0 Nm"
    REQ_TORQUE_3000 = "3000 Nm"
    REQ_TORQUE_5000 = "5000 Nm"
    REQ_TORQUE_10000 = "10000 Nm"

    BATTERY_STATE_READY = "Ready"
    BATTERY_STATE_NOT_READY = "NotReady"
    BATTERY_STATE_ERROR = "Error"
