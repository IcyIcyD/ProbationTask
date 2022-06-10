def soft_assert(actual_values, exp_values):
    """Basic soft assert for multiple checks.

    @:param actual_values (dict): Actual values.
    @:param exp_values (dict): Expected values.
    @:raises AssertionError
    """
    err_msg = ""
    for k, v in exp_values.items():
        try:
            assert actual_values[k] == v
        except AssertionError:
            err_msg += f"Field '{k}' - Expected '{v}', Got '{actual_values[k]}'\n"
    if err_msg:
        err_msg = "Wrong values for following fields:\n" + err_msg
        raise AssertionError(err_msg)
