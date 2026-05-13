from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, DisponibilidadError

class Servicio(ABC):
    def init(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, kwargs):
        pass

    @abstractmethod
    def validar_parametros(self, kwargs):
        pass

class ReservaSalas(Servicio):
    def calcular_costo(self, horas=1):
        return self.costo_base * horas

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatoInvalidoError("Las horas deben ser un número mayor a cero.")

class AlquilerEquipos(Servicio):
    def calcular_costo(self, dias=1, seguro=False):
        total = self.costo_base * dias
        if seguro:
            total += (total * 0.10)
        return total

    def validar_parametros(self, dias):
        if not isinstance(dias, (int, float)) or dias > 30:
            raise DisponibilidadError("No se permite alquiler por más de 30 días.")

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, nivel="basico"):
        tarifas = {"basico": 1.0, "premium": 1.5}
        return self.costo_base * tarifas.get(nivel, 1.0)

    def validar_parametros(self, nivel):
        if nivel not in ["basico", "premium"]:
            raise DatoInvalidoError(f"Nivel '{nivel}' no reconocido.")
