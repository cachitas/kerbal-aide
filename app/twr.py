from collections import namedtuple

g = 9.8

flea = {
    'fuel_type': 'solid',
    'thrust': 162.91,
    'pct': 100,
    'symmetry': 1,
}


class Engine:
    name = ""
    symmetry = 1


e = Engine()
print(e.name)


e = Engine()
e.name = "lll"
print(e.name)


e = Engine()
print(e.name)


# Engine = namedtuple("Engine", ['fuel_type', 'thrust', 'pct'])

# flea = Engine(fuel_type='solid', thrust=162.91, pct=100)

Stage = namedtuple("Stage", ['mass', 'engines'])

stage = Stage(mass=10, engines=[flea])


def twr(stage):
    F = sum([engine.thrust * engine.pct / 100 for engine in stage.engines])
    return F / (stage.mass * g)


print(twr(stage))

flea.pct = 50
print(twr(stage))
