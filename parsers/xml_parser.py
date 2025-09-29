import xml.etree.ElementTree as ET
from models.dominio import Invernadero, Plant, Drone
from models.tda import ListaEnlazada  # asumiendo que creaste esta TDA propia


class XMLParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.drones = ListaEnlazada()
        self.invernaderos = ListaEnlazada()

    def parse(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        # ------------------------------
        # Cargar lista de drones
        # ------------------------------
        lista_drones = root.find("listaDrones")
        if lista_drones is not None:
            for nodo_dron in lista_drones.findall("dron"):
                dron = Drone(
                    id=nodo_dron.get("id"),
                    nombre=nodo_dron.get("nombre")
                )
                self.drones.append(dron)

        # ------------------------------
        # Cargar invernaderos
        # ------------------------------
        lista_invernaderos = root.find("listaInvernaderos")
        if lista_invernaderos is not None:
            for nodo_inv in lista_invernaderos.findall("invernadero"):
                inv = Invernadero(
                    nombre=nodo_inv.get("nombre")
                )

                # Plantas
                plantas_xml = nodo_inv.find("plantas")
                if plantas_xml is not None:
                    for nodo_planta in plantas_xml.findall("planta"):
                        planta = Plant(
                            nombre=nodo_planta.text.strip(),
                            hilera=int(nodo_planta.get("hilera")),
                            posicion=int(nodo_planta.get("posicion")),
                            litros=int(nodo_planta.get("litrosAgua")),
                            gramos=int(nodo_planta.get("gramosFertilizante"))
                        )
                        inv.plantas.append(planta)

                # Drones asignados al invernadero
                drones_xml = nodo_inv.find("drones")
                if drones_xml is not None:
                    for nodo_dron in drones_xml.findall("dron"):
                        dron_id = nodo_dron.get("id")
                        # buscar dron en lista global
                        dron_obj = self._buscar_dron_por_id(dron_id)
                        if dron_obj:
                            inv.drones.append(dron_obj)

                # Planes de riego
                planes_xml = nodo_inv.find("planes")
                if planes_xml is not None:
                    for nodo_plan in planes_xml.findall("planRiego"):
                        nombre_plan = nodo_plan.get("nombre")
                        instrucciones = ListaEnlazada()
                        for nodo_inst in nodo_plan.findall("instruccionRiego"):
                            instrucciones.append({
                                "hilera": int(nodo_inst.get("hilera")),
                                "posicion": int(nodo_inst.get("posicion")),
                                "accion": nodo_inst.text.strip()
                            })
                        inv.planes.append((nombre_plan, instrucciones))

                self.invernaderos.append(inv)

    # ------------------------------
    # Método auxiliar
    # ------------------------------
    def _buscar_dron_por_id(self, dron_id):
        actual = self.drones.cabeza
        while actual:
            if actual.dato.id == dron_id:
                return actual.dato
            actual = actual.siguiente
        return None
