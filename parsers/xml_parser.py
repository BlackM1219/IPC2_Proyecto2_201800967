import xml.etree.ElementTree as ET
from models.dominio import Invernadero, Plant, Drone
from models.tda import ListaSimple

class XMLParser:
    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        data = ListaSimple()  # lista de Invernaderos

        # parse listaDrones (global list) to map id -> name
        drones_global = {}
        listaDrones = root.find('listaDrones')
        if listaDrones is not None:
            for dr in listaDrones.findall('dron'):
                id_ = dr.get('id')
                nombre = dr.get('nombre')
                drones_global[id_] = nombre

        listaInvernaderos = root.find('listaInvernaderos')
        if listaInvernaderos is None:
            return data

        for inv in listaInvernaderos.findall('invernadero'):
            nombre = inv.get('nombre') if inv.get('nombre') is not None else inv.findtext('nombre')
            numeroHileras = inv.findtext('numeroHileras')
            plantasXhilera = inv.findtext('plantasXhilera')
            inv_obj = Invernadero(nombre, numeroHileras, plantasXhilera)

            listaPlantas = inv.find('listaPlantas')
            if listaPlantas is not None:
                for p in listaPlantas.findall('planta'):
                    hilera = p.get('hilera')
                    posicion = p.get('posicion')
                    litros = p.get('litrosAgua')
                    gramos = p.get('gramosFertilizante')
                    especie = (p.text or '').strip()
                    plant = Plant(hilera, posicion, litros, gramos, especie)
                    inv_obj.agregar_planta(plant)

            asignacion = inv.find('asignacionDrones')
            if asignacion is not None:
                for a in asignacion.findall('dron'):
                    id_ = a.get('id')
                    hilera = a.get('hilera')
                    nombre_d = drones_global.get(id_, f'DR{id_}')
                    d = Drone(id_, nombre_d, hilera)
                    inv_obj.asignar_dron(d)

            planes = inv.find('planesRiego')
            if planes is not None:
                for plan in planes.findall('plan'):
                    pname = plan.get('nombre')
                    seq = (plan.text or '').strip()
                    inv_obj.agregar_plan(pname, seq)

            data.append(inv_obj)

        return data