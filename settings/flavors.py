# flavors.py
import os
from abc import ABC, abstractmethod

class Flavor(ABC):
    flavors = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically registers all subclasses in the flavors dictionary."""
        super().__init_subclass__(**kwargs)
        Flavor.flavors[cls.__name__.lower()] = cls

    def __init__(self):
        self.work_duration: int
        self.break_duration: int
        self.emoji: str
        self.break_sound: str


# Define each flavor class, inheriting from Flavor
class Aurane(Flavor):
    def __init__(self):
        super().__init__()
        self.work_duration = 25
        self.break_duration = 5
        self.emoji = "🍅"
        self.break_sound: str = "happy-bell.wav"

class Maria(Flavor):
    def __init__(self):
        super().__init__()
        self.work_duration = 20
        self.break_duration = 10
        self.emoji = "🍕"
        self.break_sound = "relaxed_break.wav"

class Alkiku(Flavor):
    def __init__(self):
        super().__init__()
        self.work_duration = 50
        self.break_duration = 10
        self.emoji = "🧑🏿‍🦲"
        self.break_sound = "intense_break.wav"

class Julie(Flavor):
    def __init__(self):
        super().__init__()
        self.work_duration = 20
        self.break_duration = 10
        self.emoji = "🍫"
        self.break_sound = "relaxed_break.wav"
