from typing import Union, Type


class MetricValueUndefined:
    """
    Some metrics can't be determined always.

    E.g. the angle of an exit point when there is only 1 point.
    """


METRIC_TYPE = Union[float, Type[MetricValueUndefined]]
