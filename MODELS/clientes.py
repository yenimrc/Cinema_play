class Cliente:
    def __init__(self, id_cliente=None, nombre=None, correo=None, fecha_registro=None):
        
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.correo = correo
        self.fecha_registro = fecha_registro



    # Métodos getters y setters (opcional)
    def get_id_cliente(self):
        return self.id_cliente

    def set_id_cliente(self, id_cliente):
        self.id_cliente = id_cliente

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo

    def get_fecha_registro(self):
        return self.fecha_registro

    def set_fecha_registro(self, fecha_registro):
        self.fecha_registro = fecha_registro

    def __str__(self):
        #representación legible del cliente.
        return f"Cliente({self.id_cliente}, {self.nombre}, {self.correo}, {self.fecha_registro})"


