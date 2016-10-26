import itertools

from kivy.app import App
from kivy.logger import Logger
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import ListProperty
# from kivy.properties import ObjectProperty

SYMMETRY_MODES = [1, 2, 3, 4]
# SYMMETRY_MODE_CYCLE = itertools.cycle(SYMMETRY_MODES)
g = 9.8


class Spaceship(BoxLayout):
    mass = BoundedNumericProperty(1, min=0.001)
    engines = ListProperty()
    twr = NumericProperty()

    def on_engines(self, instance, value):
        print("Engines list modified")

    def add_engine(self):
        self.engines.append(Engine(name="Flea", thrust_atm=162.91, pct=100))
        Logger.debug(str(self.engines))

    def compute_twr(self):
        f = sum([engine.thrust * engine.pct / 100 for engine in self.engines])
        Logger.info("Force: %f", f)
        self.twr = f / (self.mass * g)


class Engine(BoxLayout):
    symmetry_mode = OptionProperty(1, options=SYMMETRY_MODES)
    pct = BoundedNumericProperty(100, min=0, max=100)
    thrust = NumericProperty(-1)

    def __init__(self, name, thrust_atm, *args, **kwargs):
        self.name = name
        self.thrust_atm = thrust_atm
        self.compute_thrust()
        super().__init__(*args, **kwargs)

    def on_symmetry_mode(self, instance, event):
        self.compute_thrust()

    def compute_thrust(self):
        Logger.debug("Engine: Computing thrust %.1f * %.1f / 100",
                     self.thrust_atm, self.pct)
        self.thrust = self.thrust_atm * self.pct / 100
        self.thrust *= int(self.symmetry_mode)


class SymmetryModeButton(ButtonBehavior, Label):

    # TODO set symemtry images as in KSP

    value = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symmetry_modes = itertools.cycle(SYMMETRY_MODES)
        self.change_symmetry_mode()

    def change_symmetry_mode(self):
        self.value = next(self.symmetry_modes)
        self.text = str(self.value)
        Logger.debug("Symmetry mode changed to %d", self.value)


class TWRCalculator(FloatLayout):
    pass


class KerbalAideApp(App):
    title = "Kerbal Aide"

    def build(self):
        return Spaceship()
        # return Engine(name="F", thrust_atm=162.91, pct=100)


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'debug')
    app = KerbalAideApp()
    app.run()
