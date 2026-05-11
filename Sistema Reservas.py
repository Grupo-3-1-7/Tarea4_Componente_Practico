


from abc import ABC, abstractmethod
import logging

# Configuración de logs
logging.basicConfig(filename="logs.txt", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------------------
# Clase abstracta base
# -------------------------------
class Entidad(ABC):
    @abstractmethod
    def validar(self):
        pass

# -------------------------------
# Clase Cliente con encapsulación
# -------------------------------
class Cliente(Entidad):
    def __init__(self, nombre, correo, telefono):
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.validar()

    def validar(self):
        if not self.__nombre or not isinstance(self.__nombre, str):
            raise ValueError("Nombre inválido")
        if "@" not in self.__correo:
            raise ValueError("Correo inválido")
        if not self.__telefono.isdigit():
            raise ValueError("Teléfono inválido")

    def get_nombre(self):
        return self.__nombre

    def __str__(self):
        return f"Cliente: {self.__nombre}, Correo: {self.__correo}, Teléfono: {self.__telefono}"

# -------------------------------
# Clase abstracta Servicio
# -------------------------------
class Servicio(Entidad, ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0):
        pass

    def validar(self):
        if not self.nombre or self.costo_base <= 0:
            raise ValueError("Servicio inválido")

# -------------------------------
# Servicios especializados
# -------------------------------
class ReservaSala(Servicio):
    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0):
        costo = self.costo_base * duracion
        costo += costo * impuesto
        costo -= costo * descuento
        return costo

class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0):
        return (self.costo_base * duracion) * (1 + impuesto) - descuento

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion=1, impuesto=0.0, descuento=0.0):
        return (self.costo_base * duracion) + (self.costo_base * 0.2)

# -------------------------------
# Excepción personalizada
# -------------------------------
class ServicioNoDisponible(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

# -------------------------------
# Clase Reserva
# -------------------------------
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion, impuesto=0.19)
            self.estado = "Confirmada"
            print(f"Reserva confirmada para {self.cliente.get_nombre()}. Costo: {costo}")
        except Exception as e:
            logging.error(f"Error al confirmar reserva: {e}")
            self.estado = "Error"

    def cancelar(self):
        try:
            if self.estado == "Confirmada":
                self.estado = "Cancelada"
                print(f"Reserva cancelada para {self.cliente.get_nombre()}")
            else:
                raise Exception("No se puede cancelar una reserva no confirmada")
        except Exception as e:
            logging.error(f"Error al cancelar reserva: {e}")

# -------------------------------
# Simulación de operaciones
# -------------------------------
def main():
    try:
        # Cliente válido
        cliente1 = Cliente("Juan Pérez", "juan@mail.com", "3214567890")

        # Cliente inválido
        try:
            cliente2 = Cliente("", "correo_invalido", "abc")
        except Exception as e:
            logging.error(f"Error creando cliente: {e}")

        # Servicios
        sala = ReservaSala("Sala de reuniones", 100)
        equipo = AlquilerEquipo("Proyector", 50)
        asesoria = AsesoriaEspecializada("Consultoría TI", 200)

        # Reservas exitosas
        reserva1 = Reserva(cliente1, sala, 2)
        reserva1.confirmar()

        reserva2 = Reserva(cliente1, equipo, 3)
        reserva2.confirmar()

        reserva3 = Reserva(cliente1, asesoria, 1)
        reserva3.confirmar()

        # Cancelación correcta
        reserva1.cancelar()

        # Cancelación incorrecta
        reserva2.cancelar()
        reserva2.cancelar()  # Intento inválido

        # Error con servicio no disponible
        try:
            raise ServicioNoDisponible("Este servicio no está disponible")
        except ServicioNoDisponible as e:
            logging.error(f"Error: {e}")

    except Exception as e:
        logging.error(f"Error general: {e}")

if __name__ == "__main__":
    main()
