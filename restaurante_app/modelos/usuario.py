class Usuario:
    LONGITUD_MINIMA_USUARIO: int = 3
    LONGITUD_MINIMA_CONTRASENA: int = 6

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        usuario: str,
        contrasena: str,
    ) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion es requerida.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente es requerido.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El correo electronico es requerido.")
        if "@" not in valor:
            raise ValueError("El correo debe contener el caracter @.")
        self._correo = valor.strip()

    @property
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre de usuario es requerido.")
        usuario_limpio = valor.strip()
        if len(usuario_limpio) < self.LONGITUD_MINIMA_USUARIO:
            raise ValueError(
                f"El usuario debe tener al menos {self.LONGITUD_MINIMA_USUARIO} caracteres."
            )
        self._usuario = usuario_limpio

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La contrasena es requerida.")
        valor_limpio = valor.strip()
        if len(valor_limpio) < self.LONGITUD_MINIMA_CONTRASENA:
            raise ValueError(
                f"La contrasena debe tener al menos {self.LONGITUD_MINIMA_CONTRASENA} caracteres."
            )
        self._contrasena = valor_limpio

    def validar_credenciales(self, usuario: str, contrasena: str) -> bool:
        # Compara las credenciales ingresadas con las registradas para este cliente.
        return self._usuario == usuario.strip() and self._contrasena == contrasena.strip()

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
        }

    def __str__(self) -> str:
        return (
            f"Identificacion: {self.identificacion} | "
            f"Nombre: {self.nombre} | Correo: {self.correo}"
        )
