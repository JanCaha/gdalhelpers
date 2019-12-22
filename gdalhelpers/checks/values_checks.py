import numbers
import math
from angles import normalize


def check_number(variable: numbers.Number, variable_name: str) -> None:
    if not isinstance(variable, numbers.Number):
        raise TypeError("`{0}` must be number. The variable is `{1}`".format(variable_name, type(variable).__name__))


def check_value_is_zero_or_positive(variable: numbers.Number, variable_name: str) -> None:

    check_number(variable, variable_name)

    if variable < 0:
        raise ValueError("`{0}` must be higher than 0. It is {1}.".format(variable_name, variable))


def check_return_value_is_angle(theta: numbers.Number, variable_name: str) -> float:

    check_number(theta, variable_name)

    if not (-math.pi <= theta <= math.pi):
        theta = normalize(theta, -math.pi, math.pi)

    if not (-math.pi <= theta <= math.pi):
        raise ValueError("{0} must be from range `[-pi, pi]`. It is {1}.".format(variable_name, theta))

    return theta


def check_return_value_is_angle_degrees(theta: numbers.Number, variable_name: str) -> float:

    check_number(theta, variable_name)

    if not (0 <= theta <= 360):
        theta = normalize(theta, 0, 360)

    return theta
