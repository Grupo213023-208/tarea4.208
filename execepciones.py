class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class DatoInvalidoError(SoftwareFJError):
    """Excepción para validaciones de datos fallidas."""
    pass

class DisponibilidadError(SoftwareFJError):
    """Excepción cuando un servicio no puede reservarse."""
    pass
