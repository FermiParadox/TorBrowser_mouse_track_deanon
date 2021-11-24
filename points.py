from abc import ABC, abstractmethod


class _PointHandler(ABC):
    """
    Points right before browser exit P1 -> P2 -> P3 (exit point; or "critical").

    Points right after browser entry P1 (entry point; or "critical") -> P2 -> P3.
    """

    def __init__(self, index, x_list, y_list, t_list):
        self.index = index
        self.x_list = x_list
        self.y_list = y_list
        self.t_list = t_list

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


class EntryPointHandler(_PointHandler):

    @property
    def p3(self):
        return self.p_x(extra_index=2)

    @property
    def p2(self):
        return self.p_x(extra_index=1)

    @property
    def p1(self):
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
