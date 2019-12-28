import numbers
import math
from angles import normalize


def check_number(variable: numbers.Number, variable_name: str) -> None:
    """
    Checks if `variable` is valid number using class `numbers.Number`. Raises `TypeError` if it is not.

    :param variable:
    :param variable_name: string. Variable name for error message.
    :return: nothing
    """
    if not isinstance(variable, numbers.Number):
        raise TypeError("`{0}` must be number. The variable is `{1}`.".format(variable_name, type(variable).__name__))


def check_value_is_zero_or_positive(variable: numbers.Number, variable_name: str) -> None:
    """
    Checks if `variable` is equal or higher than zero. Raises `TypeError` if it is not.

    :param variable:
    :param variable_name: string. Variable name for error message.
    :return: nothing
    """
    check_number(variable, variable_name)

    if variable < 0:
        raise ValueError("`{0}` must be higher than 0. It is `{1}`.".format(variable_name, variable))


def check_return_value_is_angle(theta: numbers.Number, variable_name: str) -> float:
    """
    Checks if `theta` is number and normalizes it into range `[-pi, pi]`.
    Values outside of the range are transformed into the range.

    :param theta: numbers.Number (float or integer). Represents angle.
    :param variable_name: string. Variable name for error message.
    :return: float. Value of theta normalized into range [-pi, pi].
    """
    check_number(theta, variable_name)

    if not (-math.pi <= theta <= math.pi):
        theta = normalize(theta, -math.pi, math.pi)

    if not (-math.pi <= theta <= math.pi):
        raise ValueError("{0} must be from range `[-pi, pi]`. It is {1}.".format(variable_name, theta))

    return float(theta)


def check_return_value_is_angle_degrees(theta: numbers.Number, variable_name: str) -> float:
    """
    Checks if `theta` is number and normalizes it into range `[0, 360]`.
    Values outside of the range are transformed into the range.

    :param theta: numbers.Number (float or integer). Represents angle.
    :param variable_name: string. Variable name for error message.
    :return: float. Value of theta normalized into range [0, 360].
    """

    check_number(theta, variable_name)

    if not (0 <= theta <= 360):
        theta = normalize(theta, 0, 360)

    return float(theta)
