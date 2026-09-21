# 🍽️ restaurante_app — Semana 14

**Estudiante:** Dayana Valeria Lema Saldaña  
**Asignatura:** Programación Orientada a Objetos — Universidad Estatal Amazónica  
**Entrega:** Semana 14 · Componentes y contenedores

---

## 📌 ¿Qué cambia esta semana?

Esta entrega evoluciona `restaurante_app` (Sabor Verde) a partir de la interfaz gráfica construida en la Semana 13. El objetivo central es aplicar correctamente **componentes y contenedores de Tkinter/ttk** para transformar la sección de platos en una gestión completa: registro, consulta, actualización y eliminación, manteniendo la arquitectura modular y la persistencia en JSON ya existentes.

---

## 🗂️ Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

---

## 🧩 Responsabilidad de cada capa

- `modelos/`: `Producto` (con indicador vegetariano) y `Usuario` (con correo), validados con `property`.
- `servicios/archivo_servicio.py`: lee y escribe los archivos JSON de `datos/`.
- `servicios/restaurante_servicio.py`: convierte los datos en objetos, valida el acceso y expone el CRUD completo de platos (`registrar_producto`, `buscar_producto_por_codigo`, `actualizar_producto`, `eliminar_producto`, `guardar_productos`).
- `ui/`: `LoginView` y `MainView`, construidas con Tkinter, sin leer los archivos JSON directamente.
- `main.py`: crea la única ventana principal y controla el cambio entre vistas.

---

## 🧱 Componentes y contenedores utilizados

- `Frame`: separa encabezado, barra de navegación, contenido y barra de estado.
- `LabelFrame`: agrupa el formulario ("Datos del plato") y el listado ("Platos disponibles" / "Consulta de clientes").
- `Entry`: código, nombre y precio del plato, y credenciales de acceso.
- `ttk.Combobox` (solo lectura): selector de categoría restringido a `PRINCIPAL`, `GUARNICION`, `SOPA`, `JUGO`, `POSTRE`.
- `ttk.Checkbutton`: indicador "Es vegetariano", vinculado a un `tk.BooleanVar`.
- `ttk.Spinbox`: selector numérico del stock del plato.
- `ttk.Treeview` + `ttk.Scrollbar`: tablas de platos y clientes, con desplazamiento vertical.
- `ttk.Button` / `ttk.Style`: botones de acción (`Registrar`, `Cargar / Consultar`, `Actualizar`, `Eliminar`, `Limpiar`) conectados mediante `command=`.
- Gestores de geometría: `pack()` para la estructura general y `grid()` dentro del formulario y del bloque formulario/listado.

---

## 🥗 Operaciones implementadas sobre platos

| Operación | Acción en la interfaz | Método en `RestauranteServicio` |
|---|---|---|
| Registrar | Botón **Registrar** | `registrar_producto(codigo, nombre, precio, categoria, es_vegetariano, stock)` |
| Consultar | Botón **Cargar / Consultar** | `buscar_producto_por_codigo(codigo)` |
| Actualizar | Botón **Actualizar** | `actualizar_producto(codigo, nombre, precio, categoria, es_vegetariano, stock)` |
| Eliminar | Botón **Eliminar** | `eliminar_producto(codigo)` |

Todas las validaciones (campos vacíos, precio no numérico o negativo, categoría inválida, código duplicado, código de al menos 2 caracteres) se resuelven en `Producto` y `RestauranteServicio`; la interfaz solo captura los datos y muestra el resultado con `messagebox`.

---

## 💾 Persistencia

Los cambios sobre los platos se guardan de inmediato en `datos/productos.json` mediante `RestauranteServicio.guardar_productos()`, que delega en `ArchivoServicio`. Al reabrir la aplicación, los platos modificados se conservan.

---

## ▶️ Flujo de la aplicación

```
Inicio -> LoginView -> RestauranteServicio valida el acceso -> MainView
MainView -> Inicio (resumen) | Clientes (consulta) | Platos (formulario + tabla)
MainView -> Registrar | Cargar/Consultar | Actualizar | Eliminar -> productos.json
MainView -> Cerrar sesion -> LoginView
```

---

## 🔑 Credenciales de acceso (demostración)

| Usuario | Contraseña |
|---|---|
| `dlema` | `verde2026` |
| `admin` | `admin654` |

---

## ⚙️ Cómo ejecutar

```bash
cd restaurante_app
python main.py
```

---

## 🧪 Pruebas realizadas

- **Inicio de la aplicación:** `main.py` se ejecuta sin errores y muestra primero `LoginView`.
- **Acceso correcto:** se despliega `MainView` dentro de la misma ventana.
- **Opción Clientes:** muestra la tabla de clientes cargada desde `usuarios.json`, incluyendo su correo.
- **Opción Platos:** presenta un formulario organizado con componentes y contenedores.
- **Registrar plato:** el nuevo plato aparece de inmediato en la tabla, con su indicador vegetariano.
- **Cargar / Consultar:** los datos del plato buscado se cargan en el formulario, incluyendo el `Checkbutton`.
- **Actualizar plato:** los cambios se reflejan en la tabla y se conservan.
- **Eliminar plato:** el plato deja de aparecer en la tabla.
- **Reabrir la aplicación:** los cambios sobre los platos se mantienen.
- **Cierre de sesión:** regresa a `LoginView` sin abrir una ventana nueva.

---

## 📎 Nota educativa sobre autenticación

El acceso de esta etapa es una simulación con fines académicos; las contraseñas se guardan en JSON sin cifrado, lo cual no sería apropiado para un sistema en producción.
