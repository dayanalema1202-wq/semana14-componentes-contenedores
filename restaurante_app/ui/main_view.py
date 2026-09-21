import tkinter as tk
from tkinter import messagebox, ttk

from modelos.producto import Producto


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f1f8f2")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}

        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_precio_entry = None
        self.producto_categoria_combo = None
        self.producto_vegetariano_var = None
        self.producto_stock_spin = None
        self.tabla_productos = None
        self.tabla_usuarios = None

        self.definir_estilos()
        self.construir_interfaz()

    # -------------------------------------------------------------------
    # Colores y estilos reutilizables de la vista principal.
    # -------------------------------------------------------------------
    def definir_estilos(self):
        self.color_fondo = "#f1f8f2"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#1b4d20"
        self.color_texto = "#264d29"
        self.color_secundario = "#c8e6c9"
        self.color_resaltado = "#2e7d32"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuApp.TButton", background=[("active", "#a9d5ab")])
        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuActivo.TButton", background=[("active", "#256428")])
        estilo.configure(
            "CerrarSesion.TButton",
            background="#8b3a1f",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("CerrarSesion.TButton", background=[("active", "#6f2e18")])
        estilo.configure(
            "Accion.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", "#256428")])
        estilo.configure(
            "Secundario.TButton",
            background="#5c7a5e",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Secundario.TButton", background=[("active", "#48604a")])
        estilo.configure(
            "Eliminar.TButton",
            background="#8b3a1f",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Eliminar.TButton", background=[("active", "#6f2e18")])
        estilo.configure(
            "Treeview.Heading",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
        )
        estilo.configure("Treeview", rowheight=24, font=("Arial", 10))
        estilo.configure(
            "Vegetariano.TCheckbutton",
            background=self.color_panel,
            foreground=self.color_texto,
            font=("Arial", 10),
        )

    # -------------------------------------------------------------------
    # Estructura principal: encabezado, navegacion, contenido y estado.
    # -------------------------------------------------------------------
    def construir_interfaz(self):
        encabezado = tk.Frame(self, bg=self.color_encabezado, padx=28, pady=18)
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text="🍽️ SABOR VERDE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 19, "bold"),
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text=f"Bienvenido, {self.usuario_actual.nombre}",
            bg=self.color_encabezado,
            fg="#c8e6c9",
            font=("Arial", 11),
        ).pack(anchor="w", pady=(6, 0))

        barra = tk.Frame(self, bg=self.color_secundario, padx=18, pady=10)
        barra.pack(fill="x")

        self.crear_boton_menu(barra, "Inicio", self.mostrar_inicio)
        self.crear_boton_menu(barra, "Platos", self.mostrar_productos)
        self.crear_boton_menu(barra, "Clientes", self.mostrar_usuarios)
        self.crear_boton_menu(barra, "Pedidos", self.mostrar_funcionalidad_pendiente)
        self.crear_boton_menu(barra, "Promociones", self.mostrar_funcionalidad_pendiente)

        ttk.Button(
            barra,
            text="Cerrar sesion",
            command=self.cerrar_sesion,
            style="CerrarSesion.TButton",
        ).pack(side="right")

        self.contenido = tk.Frame(self, bg=self.color_fondo, padx=28, pady=22)
        self.contenido.pack(fill="both", expand=True)

        self.crear_barra_estado()
        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando):
        boton = ttk.Button(contenedor, text=texto, command=comando, style="MenuApp.TButton")
        boton.pack(side="left", padx=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            estilo = "MenuActivo.TButton" if texto == seccion else "MenuApp.TButton"
            boton.configure(style=estilo)

    def limpiar_contenido(self):
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def crear_barra_estado(self):
        barra_estado = tk.Frame(self, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")
        self.actualizar_barra_estado()

    def actualizar_barra_estado(self):
        assert self.etiqueta_estado is not None

        self.etiqueta_estado.config(
            text=(
                f"Platos: {self.restaurante_servicio.cantidad_productos()} | "
                f"Clientes: {self.restaurante_servicio.cantidad_usuarios()} | "
                "Informacion cargada desde JSON"
            )
        )

    # -------------------------------------------------------------------
    # Seccion Inicio: resumen general del panel principal.
    # -------------------------------------------------------------------
    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 18, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.contenido,
            text="Consulte los clientes registrados y gestione el menu saludable "
            "desde las opciones superiores.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12),
        ).pack(anchor="w", pady=(0, 22))

        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")

        self.crear_tarjeta_resumen(
            resumen, "Platos disponibles", self.restaurante_servicio.cantidad_productos()
        )
        self.crear_tarjeta_resumen(
            resumen, "Clientes registrados", self.restaurante_servicio.cantidad_usuarios()
        )

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 24, "bold"),
        ).pack(anchor="w", pady=(8, 0))

    # -------------------------------------------------------------------
    # Seccion Clientes: consulta mediante tabla (solo lectura).
    # -------------------------------------------------------------------
    def mostrar_usuarios(self):
        self.marcar_seccion("Clientes")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Clientes registrados")
        listado = self.crear_panel_listado(self.contenido, "Consulta de clientes")
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificacion", "nombre", "correo", "usuario"),
            ("Identificacion", "Nombre", "Correo", "Usuario"),
        )
        self.refrescar_usuarios()

    def refrescar_usuarios(self):
        assert self.tabla_usuarios is not None

        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.usuario),
            )

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------
    # Seccion Platos: formulario + tabla + operaciones CRUD.
    # -------------------------------------------------------------------
    def mostrar_productos(self):
        self.marcar_seccion("Platos")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de platos")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del plato",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.producto_codigo_entry = self.crear_campo(formulario, "Codigo", 0)
        self.producto_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.producto_precio_entry = self.crear_campo(formulario, "Precio", 2)
        self.producto_categoria_combo = self.crear_campo_categoria(formulario, "Categoria", 3)
        self.producto_vegetariano_var = self.crear_campo_vegetariano(formulario, 4)
        self.producto_stock_spin = self.crear_campo_stock(formulario, "Stock", 5)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_producto, "Accion.TButton"),
            ("Cargar / Consultar", self.cargar_producto_en_formulario, "Secundario.TButton"),
            ("Actualizar", self.actualizar_producto, "Accion.TButton"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton"),
            ("Limpiar", self.limpiar_formulario_producto, "Secundario.TButton"),
        )

        for texto, comando, estilo in botones:
            ttk.Button(acciones, text=texto, command=comando, style=estilo).pack(
                fill="x", pady=(0, 7)
            )

        listado = self.crear_panel_listado(cuerpo, "Platos disponibles", usar_grid=True)
        self.tabla_productos = self.crear_tabla(
            listado,
            ("codigo", "nombre", "precio", "categoria", "tipo", "stock"),
            ("Codigo", "Nombre", "Precio", "Categoria", "Tipo", "Stock"),
        )
        self.refrescar_productos()

    def obtener_datos_producto(self):
        assert self.producto_codigo_entry is not None
        assert self.producto_nombre_entry is not None
        assert self.producto_precio_entry is not None
        assert self.producto_categoria_combo is not None
        assert self.producto_vegetariano_var is not None
        assert self.producto_stock_spin is not None

        return (
            self.producto_codigo_entry.get(),
            self.producto_nombre_entry.get(),
            self.producto_precio_entry.get(),
            self.producto_categoria_combo.get(),
            self.producto_vegetariano_var.get(),
            self.producto_stock_spin.get(),
        )

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(*self.obtener_datos_producto())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Platos", "Plato registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Platos", str(error))

    def cargar_producto_en_formulario(self):
        assert self.producto_codigo_entry is not None

        producto = self.restaurante_servicio.buscar_producto_por_codigo(
            self.producto_codigo_entry.get()
        )
        if producto is None:
            messagebox.showerror("Platos", "No existe un plato con ese codigo.")
            return

        self.limpiar_formulario_producto()
        self.producto_codigo_entry.insert(0, producto.codigo)
        self.producto_nombre_entry.insert(0, producto.nombre)
        self.producto_precio_entry.insert(0, f"{producto.precio:.2f}")
        self.producto_categoria_combo.set(producto.categoria)
        self.producto_vegetariano_var.set(producto.es_vegetariano)
        self.producto_stock_spin.insert(0, str(producto.stock))

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(*self.obtener_datos_producto())
            self.refrescar_productos()
            messagebox.showinfo("Platos", "Plato actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Platos", str(error))

    def eliminar_producto(self):
        assert self.producto_codigo_entry is not None

        try:
            self.restaurante_servicio.eliminar_producto(self.producto_codigo_entry.get())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Platos", "Plato eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Platos", str(error))

    def limpiar_formulario_producto(self):
        for entrada in (
            self.producto_codigo_entry,
            self.producto_nombre_entry,
            self.producto_precio_entry,
            self.producto_stock_spin,
        ):
            assert entrada is not None
            entrada.delete(0, tk.END)

        assert self.producto_categoria_combo is not None
        assert self.producto_vegetariano_var is not None
        self.producto_categoria_combo.set("")
        self.producto_vegetariano_var.set(False)
        self.producto_stock_spin.insert(0, "0")

    def refrescar_productos(self):
        assert self.tabla_productos is not None

        self.limpiar_tabla(self.tabla_productos)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.categoria,
                    producto.etiqueta_tipo(),
                    producto.stock,
                ),
            )

        self.actualizar_barra_estado()

    def mostrar_funcionalidad_pendiente(self):
        messagebox.showinfo(
            "Proximamente",
            "Esta seccion se incorporara en una entrega posterior.",
        )

    # -------------------------------------------------------------------
    # Utilidades de interfaz compartidas por las secciones.
    # -------------------------------------------------------------------
    def crear_titulo_seccion(self, texto):
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 14))

    def crear_campo(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        entrada = tk.Entry(contenedor, width=24, font=("Arial", 10))
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_campo_categoria(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        combo = ttk.Combobox(
            contenedor,
            width=21,
            font=("Arial", 10),
            state="readonly",
            values=Producto.CATEGORIAS_VALIDAS,
        )
        combo.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return combo

    def crear_campo_vegetariano(self, contenedor, fila):
        variable = tk.BooleanVar(value=False)
        check = ttk.Checkbutton(
            contenedor,
            text="Es vegetariano",
            variable=variable,
            style="Vegetariano.TCheckbutton",
        )
        check.grid(row=fila, column=0, columnspan=2, sticky="w", pady=(0, 8))
        return variable

    def crear_campo_stock(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        spin = ttk.Spinbox(contenedor, from_=0, to=999, width=22, font=("Arial", 10))
        spin.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        spin.delete(0, tk.END)
        spin.insert(0, "0")
        return spin

    def crear_panel_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12,
        )

        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)

        return listado

    def crear_tabla(self, contenedor, columnas, encabezados):
        frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
        frame_tabla.pack(fill="both", expand=True)

        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)

        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=120, anchor="w")

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()
