import flet as ft
from MODELS.clientes import Cliente
from CONTROLLERS.clientes_controller import ClienteController

class ClienteView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = ClienteController()
        self.clientes = []
        self.cargar_clientes()
        
        # Controles principales
        self.titulo = ft.Text(
            "Gestión de Clientes - CiNENA_PLAY",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_900
        )
        
        self.txt_buscar = ft.TextField(
            label="Buscar cliente por nombre o email",
            expand=True,
            on_change=self.buscar_cliente
        )
        
        self.btn_nuevo = ft.ElevatedButton(
            "Nuevo Cliente",
            icon=ft.icons.PERSON_ADD,
            on_click=self.abrir_dialogo_nuevo_cliente
        )
        
        # DataTable para mostrar clientes
        self.tabla_clientes = ft.DataTable(
            columns=[
                #ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        
        # Diálogo para nuevo/editar cliente
        self.dialogo_cliente = ft.AlertDialog(
            modal=True,
            title=ft.Text("Registrar Nuevo Cliente"),
            content=ft.Column([
                ft.TextField(label="Nombre completo", prefix_icon=ft.icons.PERSON),
                ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL),
                ft.TextField(label="Teléfono", prefix_icon=ft.icons.PHONE),
                #ft.TextField(label="Dirección", prefix_icon=ft.icons.HOME),
            ],
            tight=True,
            height=300),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                ft.TextButton("Guardar", on_click=self.guardar_cliente),
            ],
        )

    def cargar_clientes(self):
        """Carga la lista de clientes desde el controlador"""
        self.clientes = self.controller.obtener_todos_clientes()
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Actualiza la tabla con los clientes actuales"""
        rows = []
        for cliente in self.clientes:
            row = ft.DataRow(
                cells=[
                    #ft.DataCell(ft.Text(str(cliente.id_cliente))),
                    ft.DataCell(ft.Text(cliente.nombre)),
                    ft.DataCell(ft.Text(cliente.email)),
                    ft.DataCell(ft.Text(cliente.telefono or "-")),
                    ft.DataCell(
                        ft.Container(
                            ft.Text(
                                cliente.estado,
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor=ft.colors.GREEN if cliente.estado == "Activo" else ft.colors.RED,
                            padding=5,
                            border_radius=5,
                        )
                    ),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE,
                                tooltip="Editar",
                                on_click=lambda e, c=cliente: self.editar_cliente(c)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                tooltip="Eliminar",
                                on_click=lambda e, c=cliente: self.eliminar_cliente(c)
                            ),
                            ft.IconButton(
                                icon=ft.icons.MOVIE,
                                icon_color=ft.colors.GREEN,
                                tooltip="Ver Rentas",
                                on_click=lambda e, c=cliente: self.ver_rentas_cliente(c)
                            ),
                        ],
                        spacing=5)
                    ),
                ]
            )
            rows.append(row)
        
        self.tabla_clientes.rows = rows
        self.page.update()

    def buscar_cliente(self, e):
        """Busca clientes por nombre o email"""
        texto_busqueda = self.txt_buscar.value.lower()
        if texto_busqueda:
            clientes_filtrados = [
                cliente for cliente in self.clientes 
                if texto_busqueda in cliente.nombre.lower() or texto_busqueda in cliente.email.lower()
            ]
            self.clientes = clientes_filtrados
        else:
            self.cargar_clientes()
        self.actualizar_tabla()

    def abrir_dialogo_nuevo_cliente(self, e):
        """Abre el diálogo para registrar nuevo cliente"""
        self.dialogo_cliente.title = ft.Text("Registrar Nuevo Cliente")
        self.modo_edicion = False
        self.limpiar_formulario()
        self.page.dialog = self.dialogo_cliente
        self.dialogo_cliente.open = True
        self.page.update()

    def editar_cliente(self, cliente):
        """Abre el diálogo para editar un cliente existente"""
        self.cliente_actual = cliente
        self.dialogo_cliente.title = ft.Text(f"Editar Cliente: {cliente.nombre}")
        self.modo_edicion = True
        
        # Llenar el formulario con los datos actuales
        contenido = self.dialogo_cliente.content.controls
        contenido[0].value = cliente.nombre
        contenido[1].value = cliente.email
        contenido[2].value = cliente.telefono
        #contenido[3].value = cliente.direccion
        
        self.page.dialog = self.dialogo_cliente
        self.dialogo_cliente.open = True
        self.page.update()

    def guardar_cliente(self, e):
        """Guarda un cliente nuevo o editado"""
        try:
            contenido = self.dialogo_cliente.content.controls
            nombre = contenido[0].value
            email = contenido[1].value
            telefono = contenido[2].value
            direccion = contenido[3].value
            
            if not nombre or not email:
                raise ValueError("Nombre y email son obligatorios")
            
            if self.modo_edicion:
                # Actualizar cliente existente
                self.cliente_actual.nombre = nombre
                self.cliente_actual.email = email
                self.cliente_actual.telefono = telefono
                self.cliente_actual.direccion = direccion
                self.controller.actualizar_cliente(self.cliente_actual)
            else:
                # Crear nuevo cliente
                nuevo_cliente = Cliente(
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                   #direccion=direccion
                )
                self.controller.registrar_cliente(nuevo_cliente)
            
            self.cerrar_dialogo(e)
            self.cargar_clientes()
            self.mostrar_mensaje("Cliente guardado exitosamente", ft.colors.GREEN)
            
        except Exception as ex:
            self.mostrar_mensaje(f"Error: {str(ex)}", ft.colors.RED)

    def eliminar_cliente(self, cliente):
        """Elimina un cliente (cambia estado a Inactivo)"""
        def confirmar_eliminacion(e):
            cliente.estado = "Inactivo"
            self.controller.actualizar_cliente(cliente)
            self.cargar_clientes()
            self.page.dialog.open = False
            self.page.update()
            self.mostrar_mensaje("Cliente desactivado", ft.colors.ORANGE)
        
        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Desactivación"),
            content=ft.Text(f"¿Estás seguro de desactivar al cliente {cliente.nombre}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(self.page.dialog, 'open', False)),
                ft.TextButton("Desactivar", on_click=confirmar_eliminacion),
            ],
        )
        
        self.page.dialog = dialogo_confirmacion
        dialogo_confirmacion.open = True
        self.page.update()

    def ver_rentas_cliente(self, cliente):
        """Muestra las rentas activas del cliente"""
        self.mostrar_mensaje(f"Mostrando rentas de {cliente.nombre}", ft.colors.BLUE)
        # Aquí se integraría con el módulo de rentas

    def limpiar_formulario(self):
        """Limpia el formulario del diálogo"""
        for control in self.dialogo_cliente.content.controls:
            control.value = ""

    def cerrar_dialogo(self, e):
        """Cierra el diálogo"""
        self.dialogo_cliente.open = False
        self.page.update()

    def mostrar_mensaje(self, mensaje, color):
        """Muestra un mensaje temporal al usuario"""
        snackbar = ft.SnackBar(ft.Text(mensaje), bgcolor=color)
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()

    def get_view(self):
        """Retorna la vista completa de gestión de clientes"""
        return ft.Column([
            self.titulo,
            ft.Divider(),
            ft.Row([self.txt_buscar, self.btn_nuevo]),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    ft.Text("Lista de Clientes", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.tabla_clientes,
                        height=400,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        padding=10,
                    )
                ])
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE)