from modelos.producto import Producto
from modelos.usuario import Usuario


class RestauranteServicio:
    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.usuarios: list[Usuario] = []
        self.productos: list[Producto] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        # Convierte los registros de usuarios.json y productos.json en objetos del dominio.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")

        self.usuarios = []
        for datos in usuarios_json:
            try:
                usuario = Usuario(
                    datos.get("identificacion", ""),
                    datos.get("nombre", ""),
                    datos.get("correo", ""),
                    datos.get("usuario", ""),
                    datos.get("contrasena", ""),
                )
                self.usuarios.append(usuario)
            except ValueError as error:
                print(f"Cliente con datos invalidos, no se agrego: {error}")

        self.productos = []
        for datos in productos_json:
            try:
                producto = Producto(
                    datos.get("codigo", ""),
                    datos.get("nombre", ""),
                    datos.get("precio", 0),
                    datos.get("categoria", ""),
                    datos.get("es_vegetariano", False),
                    datos.get("stock", 0),
                )
                self.productos.append(producto)
            except ValueError as error:
                print(f"Plato con datos invalidos, no se agrego: {error}")

    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        # Recorre los clientes cargados y delega la comparacion de credenciales.
        for usuario_registrado in self.usuarios:
            if usuario_registrado.validar_credenciales(usuario, contrasena):
                return usuario_registrado
        return None

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        # Localiza un plato ya cargado a partir de su codigo.
        codigo_normalizado = Producto.validar_y_formatear_codigo(codigo)
        for producto in self.productos:
            if producto.codigo == codigo_normalizado:
                return producto
        return None

    def guardar_productos(self) -> None:
        # Persiste el estado actual de los platos en productos.json.
        datos = [producto.convertir_a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        es_vegetariano: bool,
        stock: int,
    ) -> Producto:
        # Valida los datos mediante el modelo antes de agregar el plato.
        nuevo_producto = Producto(codigo, nombre, precio, categoria, es_vegetariano, stock)

        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un plato registrado con ese codigo.")

        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        es_vegetariano: bool,
        stock: int,
    ) -> Producto:
        # El codigo identifica al plato existente; el resto se actualiza.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un plato registrado con ese codigo.")

        datos_validados = Producto(codigo, nombre, precio, categoria, es_vegetariano, stock)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.precio = datos_validados.precio
        producto_actual.categoria = datos_validados.categoria
        producto_actual.es_vegetariano = datos_validados.es_vegetariano
        producto_actual.stock = datos_validados.stock

        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo: str) -> Producto:
        # Quita el plato de la lista en memoria y actualiza el archivo.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un plato registrado con ese codigo.")

        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual
