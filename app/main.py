import itertools

from kivy.app import App
from kivy.logger import Logger
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import ListProperty
# from kivy.properties import ObjectProperty

SYMMETRY_MODES = [1, 2, 3, 4]
# SYMMETRY_MODE_CYCLE = itertools.cycle(SYMMETRY_MODES)
g = 9.8


class Spaceship(Widget):
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


class Engine(Widget):
    name = StringProperty("")
    symmetry_mode = OptionProperty(1, options=SYMMETRY_MODES)
    thrust_atm = NumericProperty(100)
    thrust = NumericProperty()
    pct = BoundedNumericProperty(100, min=0, max=100)

    def __repr__(self):
        # TODO remove
        return "%s %d %f %f" % (self.name, self.symmetry_mode, self.thrust, self.pct)

    def on_symmetry_mode(self, instance, event):
        self.compute_thrust()

    def compute_thrust(self):
        Logger.debug("Engine: Computing thrust")
        self.thrust = self.thrust_atm * self.pct / 100
        self.thrust *= int(self.symmetry_mode)


class SymmetryModeButton(ButtonBehavior, Image):

    value = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symmetry_modes = itertools.cycle(SYMMETRY_MODES)
        self.change_symmetry_mode()

    def change_symmetry_mode(self):
        self.value = next(self.symmetry_modes)
        self.source = "symmetry_%d.png" % self.value
        Logger.debug("Symmetry mode changed to %d", self.value)



# class SymmetryModeButton(ToggleButton):
#     value = NumericProperty(1)

#     # TODO add symmetry game images
#     value_image = {
#         1: (0, .5, 0, 1),
#         2: (.4, .5, 0, 1),
#         3: (.6, .5, 0, 1),
#         4: (.8, .5, 0, 1),
#     }

#     def on_state(self, widget, value):
#         if value == 'down':
#             print("Symmetry mode selected:", self.value)
#             # TODO
#             self.color = self.value_image[self.value]
#         else:
#             # TODO
#             self.color = (.2, .2, .2, 1)

    # def get_selected(self):
    #     selected_btn = None
    #     btns = self.get_widgets('symmetry')
    #     for btn in btns:
    #         if btn.state == 'down':
    #             selected_btn = btn
    #     del btns  # Docs say to release the result of calling get_widgets()
    #     return selected_btn


class TWRCalculator(FloatLayout):
    pass


class KerbalAideApp(App):
    title = "Kerbal Aide"

    def build(self):
        # return Spaceship()
        return Engine(name="F", thrust_atm=162.91, pct=100)


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'debug')
    app = KerbalAideApp()
    app.run()
