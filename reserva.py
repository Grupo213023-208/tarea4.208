from logger import registrar_evento
from excepciones import DatoInvalidoError, DisponibilidadError

class Reserva:
    def init(self, cliente, servicio, duracion):
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
