// Configuración de la API
const API_URL = 'http://localhost:4000/productos';
let editandoId = null;

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
    verificarEstadoAPI();

    // Event listener para el formulario
    document.getElementById('productoForm').addEventListener('submit', handleSubmit);
});

// Verificar estado de la API
async function verificarEstadoAPI() {
    try {
        const response = await fetch(API_URL);
        if (response.ok) {
            document.getElementById('apiStatus').innerHTML = '🟢 Conectado';
        } else {
            document.getElementById('apiStatus').innerHTML = '🔴 Error';
        }
    } catch (error) {
        document.getElementById('apiStatus').innerHTML = '🔴 Desconectado';
    }
}

// Cargar productos desde la API
async function cargarProductos() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');
    const emptyState = document.getElementById('emptyState');
    const productosTable = document.getElementById('productosTable');

    // Mostrar spinner de carga
    loadingSpinner.style.display = 'block';
    errorMessage.style.display = 'none';
    emptyState.style.display = 'none';
    productosTable.style.display = 'none';

    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        loadingSpinner.style.display = 'none';

        if (!data.success) {
            throw new Error(data.error || 'Error al cargar productos');
        }

        const productos = data.productos;

        if (productos.length === 0) {
            emptyState.style.display = 'block';
            actualizarEstadisticas([]);
        } else {
            productosTable.style.display = 'table';
            renderizarProductos(productos);
            actualizarEstadisticas(productos);
        }

        verificarEstadoAPI();
    } catch (error) {
        loadingSpinner.style.display = 'none';
        errorMessage.textContent = `Error: ${error.message}. Asegúrate de que el servidor esté corriendo.`;
        errorMessage.style.display = 'block';
        console.error('Error al cargar productos:', error);
    }
}

// Renderizar productos en la tabla
function renderizarProductos(productos) {
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';

    productos.forEach(producto => {
        const tr = document.createElement('tr');
        tr.className = 'fade-in';

        // Determinar clase de stock
        let stockClass = 'stock-alto';
        if (producto.stock < 10) {
            stockClass = 'stock-bajo';
        } else if (producto.stock < 30) {
            stockClass = 'stock-medio';
        }

        tr.innerHTML = `
            <td>${producto.id}</td>
            <td><strong>${producto.nombre}</strong></td>
            <td><span class="precio-badge">$${parseFloat(producto.precio).toFixed(2)}</span></td>
            <td><span class="stock-badge ${stockClass}">${producto.stock}</span></td>
            <td>${producto.descripcion || '<em>Sin descripción</em>'}</td>
            <td>${formatearFecha(producto.fecha_creacion)}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-edit" onclick="editarProducto(${producto.id})">
                        ✏️ Editar
                    </button>
                    <button class="btn btn-delete" onclick="eliminarProducto(${producto.id}, '${producto.nombre}')">
                        🗑️ Eliminar
                    </button>
                </div>
            </td>
        `;

        tbody.appendChild(tr);
    });
}

// Actualizar estadísticas
function actualizarEstadisticas(productos) {
    const totalProductos = productos.length;
    const valorTotal = productos.reduce((sum, p) => sum + (p.precio * p.stock), 0);
    const stockTotal = productos.reduce((sum, p) => sum + p.stock, 0);

    document.getElementById('totalProductos').textContent = totalProductos;
    document.getElementById('valorTotal').textContent = `$${valorTotal.toFixed(2)}`;
    document.getElementById('stockTotal').textContent = stockTotal;
}

// Formatear fecha
function formatearFecha(fechaStr) {
    if (!fechaStr) return 'N/A';
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Manejar envío del formulario
async function handleSubmit(e) {
    e.preventDefault();

    const producto = {
        nombre: document.getElementById('nombre').value,
        precio: parseFloat(document.getElementById('precio').value),
        descripcion: document.getElementById('descripcion').value,
        stock: parseInt(document.getElementById('stock').value)
    };

    if (editandoId) {
        await actualizarProducto(editandoId, producto);
    } else {
        await crearProducto(producto);
    }
}

// Crear nuevo producto
async function crearProducto(producto) {
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');

    submitBtn.disabled = true;
    submitText.textContent = 'Creando...';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(producto)
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Error al crear producto');
        }

        mostrarNotificacion('Producto creado exitosamente', 'success');
        limpiarFormulario();
        cargarProductos();
    } catch (error) {
        mostrarNotificacion(`Error: ${error.message}`, 'error');
        console.error('Error al crear producto:', error);
    } finally {
        submitBtn.disabled = false;
        submitText.textContent = 'Crear Producto';
    }
}

// Editar producto
async function editarProducto(id) {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        if (!data.success) {
            throw new Error('Error al obtener productos');
        }

        const producto = data.productos.find(p => p.id === id);

        if (!producto) {
            throw new Error('Producto no encontrado');
        }

        // Llenar el formulario con los datos del producto
        document.getElementById('productoId').value = producto.id;
        document.getElementById('nombre').value = producto.nombre;
        document.getElementById('precio').value = producto.precio;
        document.getElementById('stock').value = producto.stock;
        document.getElementById('descripcion').value = producto.descripcion || '';

        // Cambiar el título y botón del formulario
        document.getElementById('formTitle').textContent = '✏️ Editar Producto';
        document.getElementById('submitText').textContent = 'Actualizar Producto';
        document.getElementById('cancelBtn').style.display = 'block';

        editandoId = id;

        // Scroll al formulario
        document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        mostrarNotificacion(`Error: ${error.message}`, 'error');
        console.error('Error al editar producto:', error);
    }
}

// Actualizar producto
async function actualizarProducto(id, producto) {
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');

    submitBtn.disabled = true;
    submitText.textContent = 'Actualizando...';

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(producto)
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Error al actualizar producto');
        }

        mostrarNotificacion('Producto actualizado exitosamente', 'success');
        limpiarFormulario();
        cargarProductos();
    } catch (error) {
        mostrarNotificacion(`Error: ${error.message}`, 'error');
        console.error('Error al actualizar producto:', error);
    } finally {
        submitBtn.disabled = false;
        submitText.textContent = 'Actualizar Producto';
    }
}

// Eliminar producto
async function eliminarProducto(id, nombre) {
    if (!confirm(`¿Estás seguro de que deseas eliminar "${nombre}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Error al eliminar producto');
        }

        mostrarNotificacion('Producto eliminado exitosamente', 'success');
        cargarProductos();
    } catch (error) {
        mostrarNotificacion(`Error: ${error.message}`, 'error');
        console.error('Error al eliminar producto:', error);
    }
}

// Cancelar edición
function cancelarEdicion() {
    limpiarFormulario();
}

// Limpiar formulario
function limpiarFormulario() {
    document.getElementById('productoForm').reset();
    document.getElementById('productoId').value = '';
    document.getElementById('formTitle').textContent = '➕ Crear Nuevo Producto';
    document.getElementById('submitText').textContent = 'Crear Producto';
    document.getElementById('cancelBtn').style.display = 'none';
    editandoId = null;
}

// Mostrar notificación
function mostrarNotificacion(mensaje, tipo = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = mensaje;
    notification.className = `notification ${tipo}`;

    // Mostrar notificación
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    // Ocultar después de 3 segundos
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
