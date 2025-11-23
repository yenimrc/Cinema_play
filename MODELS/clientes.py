from MODELS.datos_identificacion import DatosIdentificacion
class Cliente(DatosIdentificacion):
    def __init__(self, id_cliente:int, nombre:str, apellido:str, correo:str, contrasena:str, historial_renta:str):
        super().__init__(nombre, apellido, correo, contrasena)
        self.id_cliente=id_cliente
        self.historial_renta=[]
        
   