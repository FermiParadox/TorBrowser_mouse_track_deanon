from abc import ABC, abstractmethod

import physics

"""
When calculating angle, speed, etc. using only the last 2 points 
causes huge errors at low mouse speeds, 
due to pixels being chessboard-like boxes.
A better solution would be (linear) fitting of more than 2 points.
"""


class _PointHandler(ABC):
    """
    Points right before browser exit:
        P1 -> P2 -> P3 (exit point; or "critical").

    Points right after browser entry:
        P1 (entry point; or "critical") -> P2 -> P3.
    """

    def __init__(self, index, mouse_txy):
        self.index = index
        self.x_list = mouse_txy.x
        self.y_list = mouse_txy.y
        self.t_list = mouse_txy.time

    def p_x(self, extra_index):
        index = self.index + extra_index
        return self.x_list[index], self.y_list[index]

    def t_x(self, extra_index):
        index = self.index + extra_index
        return self.t_list[index]

    @property
    @abstractmethod
    def p3(self):
        pass

    @property
    @abstractmethod
    def p2(self):
        pass

    @property
    @abstractmethod
    def p1(self):
        pass

    @property
    @abstractmethod
    def t1(self):
        pass

    @property
    @abstractmethod
    def t2(self):
        pass

    @property
    @abstractmethod
    def t3(self):
        pass


class ExitPointHandler(_PointHandler):
    @property
    def p3(self):
        return self.p_x(extra_index=0)

    @property
    def p2(self):
        return self.p_x(extra_index=-1)

    @property
    def p1(self):
        return self.p_x(extra_index=-2)

    @property
    def t3(self):
        return self.t_x(extra_index=0)

    @property
    def t2(self):
        return self.t_x(extra_index=-1)

    @property
    def t1(self):
        return self.t_x(extra_index=-2)

    @property
    def exit_critical_angle(self):
        """Return approximate angle when exiting browser."""
        if self.index <= 1:  # not enough points
            return None
        return physics.Slope2Points(p1=self.p2, p2=self.p3).angle


class EntryPointHandler(_PointHandler):
    @property
    def p3(self):
        return self.p_x(extra_index=2)

    @property
    def p2(self):
        return self.p_x(extra_index=1)

    @property
    def p1(self):
        """First entry point"""
        return self.p_x(extra_index=0)

    @property
    def t3(self):
        return self.t_x(extra_index=2)

    @property
    def t2(self):
        return self.t_x(extra_index=1)

    @property
    def t1(self):
        return self.t_x(extra_index=0)

    @property
    def entry_critical_angle(self):
        """Return approximate angle when exiting browser."""
        if self.index <= 1:  # not enough points
            return None
        return physics.Slope2Points(p1=self.p1, p2=self.p2).angle
