class Empleado:
    def __init__(self, id_empleado=None, nombre=None, puesto=None, correo=None, contrasena=None):
        self.id_empleado = id_empleado      # Identificador único del empleado
        self.nombre = nombre                # Nombre completo del empleado
        self.puesto = puesto                # Cargo o rol (por ejemplo: "Administrador", "Cajero")
        self.correo = correo                # Correo del empleado para contacto o login
        self.contrasena = contrasena        # Contraseña para acceso al sistema

    # ---------- Métodos getters y setters ----------
    def get_id_empleado(self):
        return self.id_empleado

    def set_id_empleado(self, id_empleado):
        self.id_empleado = id_empleado

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_puesto(self):
        return self.puesto

    def set_puesto(self, puesto):
        self.puesto = puesto

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo

    def get_contrasena(self):
        return self.contrasena

    def set_contrasena(self, contrasena):
        self.contrasena = contrasena

    # ---------- Método de utilidad ----------
    def __str__(self):
        """Devuelve una representación legible del empleado"""
        return f"Empleado({self.id_empleado}, {self.nombre}, {self.puesto}, {self.correo})"
