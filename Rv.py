import random
import math

class Uniform():
    def __init__(self):
        self.max = 0
        self.min = 0

    def generate(self, max, min):
        self.max = max
        self.min = min
        r = self.max - self.min
        if r < 0:
            raise RuntimeError("Min must be less than max")
        rand = self.min + r * random.random()
        return rand

class Triangle():
    def __init__(self):
        self.min = 0
        self.max = 0
        self.mode = 0
        self.range = 0
        self.crossover_p = 0

    def generate(self, min, max, mode):
        self.min = min
        self.max = max
        self.mode = mode
        self.range = self.max - self.min
        if self.range < 0:
            raise RuntimeError("Min must be less than max")
        if self.mode > self.max or self.mode < self.min:
            raise RuntimeError("Mode must be between min and max")
        self.crossover_p = (self.mode - self.min) / self.range
        u = random.random()
        if u < self.crossover_p:
            return self.min + math.sqrt(self.range * (self.mode - self.min) * u)
        else:
            return self.max - math.sqrt(self.range * (self.max - self.mode) * (1.0 - u))

class Exponential():
    def __init__(self):
        self.rate = 0

    def generate(self, rate):
        self.rate = rate
        if self.rate < 0:
            raise RuntimeError("Rate must be positive")
        r = random.random()
        return -1 * math.log(r) / self.rate
