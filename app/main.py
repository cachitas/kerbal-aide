from kivy.app import App
from kivy.logger import Logger
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import ListProperty
# from kivy.properties import ObjectProperty

g = 9.8


class Spaceship(Widget):
    mass = BoundedNumericProperty(1, min=0.001)
    engines = ListProperty()
    twr = NumericProperty()

    def add_engine(self):
        self.engines.append(Engine(name="Flea", thrust_atm=162.91, pct=100))
        Logger.debug(str(self.engines))

    def calc_twr(self):
        f = sum([engine.thrust * engine.pct / 100 for engine in self.engines])
        Logger.info("Force: %f", f)
        return f / (self.mass * g)


class Engine(Widget):
    name = StringProperty("")
    symmetry_mode = OptionProperty(1, options=[1, 2, 3, 4])
    thrust_atm = NumericProperty(100)
    thrust = NumericProperty()
    pct = BoundedNumericProperty(100, min=0, max=100)

    def __repr__(self):
        return self.name

    def calc_thrust(self):
        Logger.debug("Calculating thrust")
        Logger.debug("Symmetry mode %d", self.symmetry_mode)
        Logger.debug("thrust atm %f", self.thrust_atm)
        Logger.debug("pct %f", self.pct)
        self.thrust = self.symmetry_mode * self.thrust_atm * self.pct / 100
        Logger.debug("Thrust %d", self.thrust)




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
