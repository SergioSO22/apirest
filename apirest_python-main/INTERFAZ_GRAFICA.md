# Guía de Uso - Interfaz Gráfica

Interfaz web moderna y funcional para gestionar productos a través de la API REST.

## Capturas de Pantalla

La interfaz incluye:
- 📊 Panel de estadísticas en tiempo real
- ➕ Formulario para crear/editar productos
- 📦 Tabla interactiva de productos
- 🎨 Diseño moderno con gradientes y animaciones
- 📱 Diseño responsivo (móvil y escritorio)

## Instalación y Configuración

### 1. Instalar dependencias (si no lo has hecho)

```bash
# Activar ambiente virtual
source venv/bin/activate

# Instalar Flask-CORS (nueva dependencia requerida)
pip install -r requirements.txt
```

### 2. Iniciar el servidor

```bash
python app.py
```

El servidor iniciará en `http://localhost:4000`

### 3. Abrir la interfaz gráfica

Abre tu navegador web y visita:

```
http://localhost:4000
```

La interfaz se cargará automáticamente.

## Características de la Interfaz

### 📊 Panel de Estadísticas

En la parte superior verás tres tarjetas con estadísticas en tiempo real:

- **Total Productos**: Número total de productos en la base de datos
- **Valor Total**: Valor total del inventario (precio × stock de todos los productos)
- **Stock Total**: Suma de todas las unidades en stock

Las estadísticas se actualizan automáticamente al crear, editar o eliminar productos.

### ➕ Crear Nuevo Producto

1. Completa el formulario con los datos del producto:
   - **Nombre** (requerido): Nombre del producto
   - **Precio** (requerido): Precio unitario en formato decimal
   - **Stock** (requerido): Cantidad disponible
   - **Descripción** (opcional): Descripción detallada

2. Haz clic en **"Crear Producto"**

3. Verás una notificación verde confirmando la creación

4. El producto aparecerá automáticamente en la tabla

### ✏️ Editar Producto

1. En la tabla de productos, haz clic en el botón **"✏️ Editar"** del producto que deseas modificar

2. El formulario se llenará automáticamente con los datos actuales

3. Modifica los campos que desees cambiar

4. Haz clic en **"Actualizar Producto"**

5. Para cancelar la edición, haz clic en **"Cancelar"**

### 🗑️ Eliminar Producto

1. En la tabla de productos, haz clic en el botón **"🗑️ Eliminar"**

2. Confirma la eliminación en el cuadro de diálogo

3. El producto se eliminará de la base de datos

### 🔄 Actualizar Lista

Haz clic en el botón **"🔄 Actualizar"** en la esquina superior derecha de la tabla para recargar la lista de productos desde el servidor.

## Indicadores Visuales

### Badges de Stock

Los productos muestran badges de colores según su nivel de stock:

- 🟢 **Verde** (Stock Alto): 30 o más unidades
- 🟡 **Amarillo** (Stock Medio): Entre 10 y 29 unidades
- 🔴 **Rojo** (Stock Bajo): Menos de 10 unidades

### Estado de la API

En la parte inferior de la página verás el estado de conexión:

- 🟢 **Conectado**: La API está funcionando correctamente
- 🔴 **Desconectado**: No se puede conectar al servidor
- 🔴 **Error**: Hay un problema con la API

### Notificaciones

Las notificaciones aparecen en la esquina superior derecha:

- 🟢 **Verde** (Éxito): Operación completada correctamente
- 🔴 **Rojo** (Error): Ocurrió un error
- 🔵 **Azul** (Info): Información general

Las notificaciones desaparecen automáticamente después de 3 segundos.

## Estructura de Archivos

```
apirest_python/
├── static/
│   ├── index.html      # Estructura HTML de la interfaz
│   ├── styles.css      # Estilos y diseño visual
│   └── app.js          # Lógica y comunicación con la API
├── app.py              # Servidor Flask (actualizado)
└── productos.db        # Base de datos SQLite
```

## Funcionalidades Técnicas

### CORS Habilitado

La aplicación ahora incluye Flask-CORS, lo que permite:
- Realizar peticiones desde cualquier origen
- Probar la API desde diferentes dominios
- Desarrollar el frontend y backend por separado

### Validación de Datos

El formulario incluye validación HTML5:
- Campos requeridos marcados con asterisco (*)
- Validación de tipo numérico para precio y stock
- Formato decimal para precios (con decimales)

### Manejo de Errores

La interfaz maneja errores de manera amigable:
- Mensajes de error claros y descriptivos
- Verificación de conexión al servidor
- Validación de respuestas de la API
- Confirmación antes de eliminar productos

### Diseño Responsivo

La interfaz se adapta automáticamente a diferentes tamaños de pantalla:
- **Escritorio**: Diseño completo con múltiples columnas
- **Tablet**: Diseño adaptado con columnas flexibles
- **Móvil**: Diseño vertical optimizado para pantallas pequeñas

## Atajos de Teclado

- **Enter** en el formulario: Crear/Actualizar producto
- **Escape** (planificado): Cancelar edición

## Solución de Problemas

### La interfaz no carga

```bash
# Verifica que el servidor esté corriendo
python app.py

# Debería mostrar:
# * Running on http://127.0.0.1:4000
```

### Error: "ModuleNotFoundError: No module named 'flask_cors'"

```bash
# Instala Flask-CORS
pip install flask-cors

# O reinstala todas las dependencias
pip install -r requirements.txt
```

### Los productos no se cargan

1. Verifica el estado de la API en la parte inferior de la página
2. Abre la consola del navegador (F12) para ver errores
3. Verifica que el servidor Flask esté corriendo
4. Haz clic en el botón "🔄 Actualizar"

### Error de CORS

Si ves errores de CORS en la consola del navegador:

```bash
# Asegúrate de que Flask-CORS esté instalado
pip install flask-cors

# Reinicia el servidor
python app.py
```

### La tabla está vacía pero hay productos

1. Haz clic en "🔄 Actualizar"
2. Verifica la consola del navegador (F12)
3. Revisa que `productos.db` exista y tenga datos

## Personalización

### Cambiar colores

Edita [static/styles.css](static/styles.css:1) y modifica las variables de color en el gradiente:

```css
/* Línea 10 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Cambiar puerto

Edita [app.py](app.py:153):

```python
app.run(debug=True, port=4000)  # Cambia 4000 por el puerto deseado
```

Y actualiza [static/app.js](static/app.js:2):

```javascript
const API_URL = 'http://localhost:4000/productos';  // Cambia el puerto
```

### Agregar campos adicionales

1. Actualiza la base de datos en [app.py](app.py:11-20)
2. Agrega campos al formulario en [static/index.html](static/index.html)
3. Actualiza la lógica en [static/app.js](static/app.js)

## Mejoras Futuras (Sugerencias)

- 🔍 Búsqueda y filtrado de productos
- 📄 Paginación para listas largas
- 📊 Gráficos de estadísticas
- 🖼️ Soporte para imágenes de productos
- 🌙 Modo oscuro/claro
- 💾 Exportar datos a CSV/Excel
- 🔐 Autenticación de usuarios
- 📱 Aplicación móvil nativa

## Recursos Adicionales

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de Flask-CORS](https://flask-cors.readthedocs.io/)
- [Guía de Fetch API](https://developer.mozilla.org/es/docs/Web/API/Fetch_API)

## Soporte

Si encuentras problemas o tienes sugerencias:

1. Revisa la consola del navegador (F12) para errores de JavaScript
2. Revisa la terminal donde corre Flask para errores del servidor
3. Verifica que todas las dependencias estén instaladas
4. Asegúrate de tener la versión correcta de Python (3.7+)

---

**¡Disfruta usando tu interfaz gráfica!** 🎉
