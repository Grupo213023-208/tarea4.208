import datetime
import logging
from abc import ABC, abstractmethod

# ============================================================
# 1. SISTEMA DE REGISTRO (LOGGING)
# ============================================================
logging.basicConfig(
    filename='software_fj_events.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_evento(mensaje, nivel="info"):
    if nivel == "error":
        logging.error(mensaje)
    else:
        logging.info(mensaje)

# ============================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ============================================================
class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class DatoInvalidoError(SoftwareFJError):
    """Excepción para validaciones de datos fallidas."""
    pass

class DisponibilidadError(SoftwareFJError):
    """Excepción cuando un servicio no puede reservarse."""
    pass

# ============================================================
# 3. CLASES ABSTRACTAS Y ENTIDADES
# ============================================================
class EntidadSistema(ABC):
    """Clase abstracta para entidades generales."""
    def __init__(self, id_sistema):
        self._id_sistema = id_sistema  # Atributo protegido

    @abstractmethod
    def mostrar_informacion(self):
        pass

class Cliente(EntidadSistema):
    """Clase con encapsulación robusta."""
    def __init__(self, id_cliente, nombre, email):
        super().__init__(id_cliente)
        self.__nombre = nombre  # Privado
        self.__email = self._validar_email(email)  # Privado

    def _validar_email(self, email):
        if "@" not in email:
            raise DatoInvalidoError(f"Email inválido: {email}")
        return email

    @property
    def nombre(self):
        return self.__nombre

    def mostrar_informacion(self):
        return f"Cliente: {self.__nombre} (ID: {self._id_sistema})"

# ============================================================
# 4. JERARQUÍA DE SERVICIOS (POLIMORFISMO)
# ============================================================
class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
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
            raise DisponibilidadError("No se permite alquiler por más de 30 días o formato inválido.")

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, nivel="basico"):
        tarifas = {"basico": 1.0, "premium": 1.5}
        # Si el nivel no es válido, se asume básico por defecto en el cálculo
        return self.costo_base * tarifas.get(nivel, 1.0)

    def validar_parametros(self, nivel):
        if nivel not in ["basico", "premium"]:
            raise DatoInvalidoError(f"Nivel de asesoría '{nivel}' no reconocido.")

# ============================================================
# 5. GESTIÓN DE RESERVAS
# ============================================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar(self):
        try:
            print(f"Procesando reserva de {self.servicio.nombre} para {self.cliente.nombre}...")
            self.servicio.validar_parametros(self.duracion)
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "Confirmada"
            registrar_evento(f"Reserva Exitosa: {self.cliente.nombre} - Costo: {costo}")
            print(f"Éxito. Costo total: ${costo}")
        
        except (DatoInvalidoError, DisponibilidadError) as e:
            self.estado = "Cancelada"
            registrar_evento(f"Fallo en reserva: {e}", "error")
            print(f"Error controlado: {e}")
            raise 
        except Exception as e:
            self.estado = "Error Crítico"
            registrar_evento(f"Error inesperado: {e}", "error")
            print(f"Error inesperado: {e}")
        finally:
            print(f"Estado final: {self.estado}\n")

# ============================================================
# 6. SIMULACIÓN DE OPERACIONES
# ============================================================
def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN SOFTWARE FJ ===\n")
    
    servicios = {
        "sala": ReservaSalas("Sala Alpha", 50000),
        "pc": AlquilerEquipos("Laptops Dell", 25000),
        "asesor": AsesoriaEspecializada("Consultoría IT", 100000)
    }

    # Esta es la lista de casos corregida
    casos = [
        ("C-001", "Yesid Preciado", "yesid@unad.edu.co", "sala", 3),
        ("C-002", "Angela Gomez", "angela@unad.com", "sala", 2),
        ("C-003", "Boris Lopez", "boris@unad.edu.co", "pc", 5),
        ("C-004", "Kelly Ruiz", "kelly@unad.edu.co", "pc", 40),
        ("C-005", "Patricia Sol", "patricia@unad.edu.co", "asesor", "pro"),
        ("C-006", "Brayan Diaz", "brayan@unad.edu.co", "sala", -1),
        ("C-007", "Cesar Paz", "cesar@unad.edu.co", "asesor", "premium"),
        ("C-008", "Esteban Mar", "esteban@unad.edu.co", "sala", 5),
        ("C-009", "Jose Becerra", "jose@unad.edu.co", "pc", 10),
        ("C-010", "Mariana Rosas", "mariana@unad.edu.co", "asesor", "basico")
    ]

    for id_c, nom, mail, srv_key, val in casos:
        try:
            # 1. Crear Cliente
            cliente = Cliente(id_c, nom, mail)
            # 2. Obtener Servicio
            servicio = servicios[srv_key]
            # 3. Crear y procesar Reserva
            reserva = Reserva(cliente, servicio, val)
            reserva.procesar()
        except SoftwareFJError as e:
            # Captura errores de negocio y sigue con el siguiente caso
            print(f"Operación saltada por error de datos: {e}\n")
            continue
        except Exception as e:
            print(f"Error técnico omitido: {e}\n")
            continue

if __name__ == "__main__":
    ejecutar_simulacion()