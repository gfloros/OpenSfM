# generated by fbsource/fbcode/mapillary/vision/buck_tools/stubgen.py

# Stubs for opensfm.pygeo (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

from typing import overload
import numpy

@overload
def ecef_from_lla(arg0: numpy.ndarray) -> numpy.ndarray: ...
@overload
def ecef_from_lla(arg0: float, arg1: float, arg2: float) -> numpy.ndarray: ...
@overload
def ecef_from_lla(*args, **kwargs) -> Any: ...
@overload
def ecef_from_topocentric_transform(arg0: numpy.ndarray) -> numpy.ndarray: ...
@overload
def ecef_from_topocentric_transform(arg0: float, arg1: float, arg2: float) -> numpy.ndarray: ...
@overload
def ecef_from_topocentric_transform(*args, **kwargs) -> Any: ...
@overload
def ecef_from_topocentric_transform_finite_diff(arg0: numpy.ndarray) -> numpy.ndarray: ...
@overload
def ecef_from_topocentric_transform_finite_diff(arg0: float, arg1: float, arg2: float) -> numpy.ndarray: ...
@overload
def ecef_from_topocentric_transform_finite_diff(*args, **kwargs) -> Any: ...
def gps_distance(arg0: numpy.ndarray, arg1: numpy.ndarray) -> float: ...
@overload
def lla_from_ecef(arg0: numpy.ndarray) -> numpy.ndarray: ...
@overload
def lla_from_ecef(arg0: float, arg1: float, arg2: float) -> numpy.ndarray: ...
@overload
def lla_from_ecef(*args, **kwargs) -> Any: ...
@overload
def lla_from_topocentric(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray: ...
@overload
def lla_from_topocentric(arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float) -> numpy.ndarray: ...
@overload
def lla_from_topocentric(*args, **kwargs) -> Any: ...
@overload
def topocentric_from_lla(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray: ...
@overload
def topocentric_from_lla(arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float) -> numpy.ndarray: ...
@overload
def topocentric_from_lla(*args, **kwargs) -> Any: ...

class TopocentricConverter:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None: ...
    @overload
    def __init__(*args, **kwargs) -> None: ...
    @property
    def alt(self) -> Any: ...
    @property
    def lat(self) -> Any: ...
    @property
    def lon(self) -> Any: ...