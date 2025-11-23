from MODELS.datos_identificacion import DatosIdentificacion 
class Empleado(DatosIdentificacion):
    def __init__(self, id_empleado:int, nombre:str, apellido:str, correo:str, contrasena:str):
        super.__init__(self, nombre, apellido, correo, contrasena)
        self.id_empleado=id_empleado
        
