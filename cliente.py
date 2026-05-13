from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError

class EntidadSistema(ABC):
    def init(self, id_sistema):
        self._id_sistema = id_sistema  # Atributo protegido

    @abstractmethod
    def mostrar_informacion(self):
        pass

class Cliente(EntidadSistema):
    def init(self, id_cliente, nombre, email):
        super().init(id_cliente)
        self.nombre = nombre  # Privado
        self.email = self._validar_email(email)  # Privado

    def _validar_email(self, email):
        if "@" not in email:
            raise DatoInvalidoError(f"Email inválido: {email}")
        return email

    @property
    def nombre(self):
        return self.nombre

    def mostrar_informacion(self):
        return f"Cliente: {self.nombre} (ID: {self._id_sistema})"