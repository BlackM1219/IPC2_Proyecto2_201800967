## Archivo: models/dominio.py

from .tda import ListaSimple

class Plant:
    def __init__(self, hilera, posicion, litros, gramos, especie=''):
        self.hilera = int(hilera)
        self.posicion = int(posicion)
        self.litros = float(litros)
        self.gramos = float(gramos)
        self.especie = especie

    def __repr__(self):
        return f"Plant(H{self.hilera}-P{self.posicion}, {self.litros}L, {self.gramos}g)"

class Drone:
    def __init__(self, id_, nombre, hilera):
        self.id = id_
        self.nombre = nombre
        self.hilera = int(hilera)
        self.posicion_actual = 1  # inicio de la hilera
        self.litros_total = 0.0
        self.gramos_total = 0.0

    def mover_a(self, posicion_objetivo):
        # devuelve tiempo en segundos requeridos para llegar (1s por metro)
        distancia = abs(self.posicion_actual - posicion_objetivo)
        self.posicion_actual = posicion_objetivo
        return int(distancia)

    def regar(self, plant: Plant):
        # 1 segundo
        self.litros_total += plant.litros
        self.gramos_total += plant.gramos
        return 1

class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_x_hilera):
        self.nombre = nombre
        self.numero_hileras = int(numero_hileras)
        self.plantas_x_hilera = int(plantas_x_hilera)
        self.plantas = ListaSimple()  # lista de Plant
        self.drones = ListaSimple()   # lista de Drone
        self.planes = ListaSimple()   # lista de (nombre, sequence)

    def agregar_planta(self, plant: Plant):
        self.plantas.append(plant)

    def asignar_dron(self, drone: Drone):
        self.drones.append(drone)

    def agregar_plan(self, nombre, sequence_str):
        # sequence_str: 'H1-P2, H2-P1, ...'
        seq = [s.strip() for s in sequence_str.split(',') if s.strip()]
        self.planes.append((nombre, seq))

    def obtener_plan(self, nombre):
        for p in self.planes.iter():
            if p[0] == nombre:
                return p[1]
        return None

    def plantas_por_hilera_pos(self, hilera, posicion):
        # busca la planta que coincide
        for plant in self.plantas.iter():
            if plant.hilera == int(hilera) and plant.posicion == int(posicion):
                return plant
        return None

    def drone_por_hilera(self, hilera):
        for d in self.drones.iter():
            if d.hilera == int(hilera):
                return d
        return None