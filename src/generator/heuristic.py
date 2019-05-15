from abc import ABCMeta, abstractmethod
from module import Module
from grid import Grid

class Heuristic(metaclass=ABCMeta):

    def __init__(self, initial_grid: Grid, heuristic_function):
        self.initial_grid = initial_grid
        self.heuristic_function = heuristic_function

    def h(self, module: Module) -> 'int':
        return self.heuristic_function(self, module, self.dist_function, self.norm)

    @abstractmethod
    def f(self, state: 'State') -> 'int': pass

    @abstractmethodr
    def __repr__(self): raise NotImplementedError

    def manhattan_distance(self, first, second):
        raise NotImplementedError