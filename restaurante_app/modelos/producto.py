class Producto:
    CATEGORIAS_VALIDAS: tuple[str, ...] = (
        "PRINCIPAL",
        "GUARNICION",
        "SOPA",
        "JUGO",
        "POSTRE",
    )

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        es_vegetariano: bool = False,
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.es_vegetariano = es_vegetariano
        self.stock = stock

    @staticmethod
    def validar_y_formatear_codigo(valor: str) -> str:
        codigo = valor.strip().upper()
        if len(codigo) < 2:
            raise ValueError("El codigo debe tener al menos 2 caracteres.")
        return codigo

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo no puede estar vacio.")
        self._codigo = Producto.validar_y_formatear_codigo(valor)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del plato no puede estar vacio.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            precio = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un valor numerico.")
        if precio < 0:
            raise ValueError("El precio no puede ser menor a cero.")
        self._precio = round(precio, 2)

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("Debe indicar una categoria.")
        cat = valor.strip().upper()
        if cat not in self.CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria desconocida. Disponibles: {', '.join(self.CATEGORIAS_VALIDAS)}")
        self._categoria = cat

    @property
    def es_vegetariano(self) -> bool:
        return self._es_vegetariano

    @es_vegetariano.setter
    def es_vegetariano(self, valor: bool) -> None:
        self._es_vegetariano = bool(valor)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            stock = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un numero entero.")
        if stock < 0:
            raise ValueError("El stock no puede quedar en negativo.")
        self._stock = stock

    def vender(self, cantidad: int) -> bool:
        if cantidad <= 0 or self._stock < cantidad:
            return False
        self._stock -= cantidad
        return True

    def etiqueta_tipo(self) -> str:
        return "Vegetariano" if self._es_vegetariano else "No vegetariano"

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "es_vegetariano": self.es_vegetariano,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | Categoria: {self.categoria} | "
            f"Tipo: {self.etiqueta_tipo()} | Stock: {self.stock}"
        )
