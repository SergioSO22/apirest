"""
Script de pruebas automatizado para la API REST de Productos
Ejecutar: python test_api.py
"""

import requests
import json
import time

# Configuración
BASE_URL = 'http://localhost:4000'
API_ENDPOINT = f'{BASE_URL}/productos'

# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(test_name, status, details=''):
    """Imprime el resultado de un test con formato"""
    symbol = '✓' if status else '✗'
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}{symbol} {test_name}{Colors.RESET}")
    if details:
        print(f"  {details}")

def print_section(title):
    """Imprime un separador de sección"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def test_connection():
    """Verifica que el servidor esté disponible"""
    try:
        response = requests.get(API_ENDPOINT, timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

def test_get_all_productos():
    """Test: GET /productos - Obtener todos los productos"""
    try:
        response = requests.get(API_ENDPOINT)
        success = response.status_code == 200 and 'productos' in response.json()
        data = response.json()
        details = f"Status: {response.status_code} | Productos encontrados: {len(data.get('productos', []))}"
        print_test("GET /productos", success, details)
        return success, data
    except Exception as e:
        print_test("GET /productos", False, f"Error: {str(e)}")
        return False, None

def test_create_producto():
    """Test: POST /productos - Crear un nuevo producto"""
    producto_data = {
        "nombre": "Laptop Test",
        "precio": 999.99,
        "descripcion": "Laptop de prueba automatizada",
        "stock": 5
    }

    try:
        response = requests.post(
            API_ENDPOINT,
            json=producto_data,
            headers={'Content-Type': 'application/json'}
        )
        success = response.status_code == 201 and response.json().get('success', False)
        data = response.json()

        if success:
            producto_id = data.get('producto', {}).get('id')
            details = f"Status: {response.status_code} | ID creado: {producto_id}"
        else:
            details = f"Status: {response.status_code}"

        print_test("POST /productos", success, details)
        return success, data.get('producto', {}).get('id') if success else None
    except Exception as e:
        print_test("POST /productos", False, f"Error: {str(e)}")
        return False, None

def test_create_producto_sin_campos_requeridos():
    """Test: POST /productos - Intentar crear sin campos requeridos"""
    producto_data = {
        "nombre": "Test incompleto"
        # Falta precio y stock
    }

    try:
        response = requests.post(
            API_ENDPOINT,
            json=producto_data,
            headers={'Content-Type': 'application/json'}
        )
        # Debería fallar (500 o 400)
        success = response.status_code in [400, 500]
        details = f"Status: {response.status_code} (esperado error)"
        print_test("POST /productos (datos inválidos)", success, details)
        return success
    except Exception as e:
        print_test("POST /productos (datos inválidos)", False, f"Error: {str(e)}")
        return False

def test_update_producto(producto_id):
    """Test: PUT /productos/<id> - Actualizar un producto"""
    if not producto_id:
        print_test("PUT /productos/<id>", False, "No hay ID de producto para actualizar")
        return False

    update_data = {
        "precio": 899.99,
        "stock": 3
    }

    try:
        response = requests.put(
            f"{API_ENDPOINT}/{producto_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        success = response.status_code == 200 and response.json().get('success', False)
        details = f"Status: {response.status_code} | ID actualizado: {producto_id}"
        print_test(f"PUT /productos/{producto_id}", success, details)
        return success
    except Exception as e:
        print_test(f"PUT /productos/{producto_id}", False, f"Error: {str(e)}")
        return False

def test_update_producto_inexistente():
    """Test: PUT /productos/<id> - Actualizar producto que no existe"""
    fake_id = 99999
    update_data = {"precio": 100.0}

    try:
        response = requests.put(
            f"{API_ENDPOINT}/{fake_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        # Debería retornar 404
        success = response.status_code == 404
        details = f"Status: {response.status_code} (esperado 404)"
        print_test(f"PUT /productos/{fake_id} (inexistente)", success, details)
        return success
    except Exception as e:
        print_test(f"PUT /productos/{fake_id} (inexistente)", False, f"Error: {str(e)}")
        return False

def test_delete_producto(producto_id):
    """Test: DELETE /productos/<id> - Eliminar un producto"""
    if not producto_id:
        print_test("DELETE /productos/<id>", False, "No hay ID de producto para eliminar")
        return False

    try:
        response = requests.delete(f"{API_ENDPOINT}/{producto_id}")
        success = response.status_code == 200 and response.json().get('success', False)
        details = f"Status: {response.status_code} | ID eliminado: {producto_id}"
        print_test(f"DELETE /productos/{producto_id}", success, details)
        return success
    except Exception as e:
        print_test(f"DELETE /productos/{producto_id}", False, f"Error: {str(e)}")
        return False

def test_delete_producto_inexistente():
    """Test: DELETE /productos/<id> - Eliminar producto que no existe"""
    fake_id = 99999

    try:
        response = requests.delete(f"{API_ENDPOINT}/{fake_id}")
        # Debería retornar 404
        success = response.status_code == 404
        details = f"Status: {response.status_code} (esperado 404)"
        print_test(f"DELETE /productos/{fake_id} (inexistente)", success, details)
        return success
    except Exception as e:
        print_test(f"DELETE /productos/{fake_id} (inexistente)", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests"""
    print(f"{Colors.BOLD}Iniciando pruebas de la API REST de Productos{Colors.RESET}")

    # Verificar conexión
    print_section("1. VERIFICACIÓN DE CONEXIÓN")
    if not test_connection():
        print(f"{Colors.RED}Error: No se puede conectar al servidor en {BASE_URL}{Colors.RESET}")
        print(f"{Colors.YELLOW}Asegúrate de que el servidor esté corriendo: python app.py{Colors.RESET}")
        return
    print_test("Conexión al servidor", True, f"Servidor disponible en {BASE_URL}")

    time.sleep(0.5)

    # Tests de lectura
    print_section("2. TESTS DE LECTURA (GET)")
    test_get_all_productos()

    time.sleep(0.5)

    # Tests de creación
    print_section("3. TESTS DE CREACIÓN (POST)")
    success_create, producto_id = test_create_producto()
    test_create_producto_sin_campos_requeridos()

    time.sleep(0.5)

    # Tests de actualización
    print_section("4. TESTS DE ACTUALIZACIÓN (PUT)")
    if success_create and producto_id:
        test_update_producto(producto_id)
    test_update_producto_inexistente()

    time.sleep(0.5)

    # Tests de eliminación
    print_section("5. TESTS DE ELIMINACIÓN (DELETE)")
    test_delete_producto_inexistente()
    if success_create and producto_id:
        test_delete_producto(producto_id)

    # Resumen final
    print_section("RESUMEN")
    print(f"{Colors.GREEN}✓ Pruebas completadas{Colors.RESET}")
    print(f"\n{Colors.YELLOW}Nota: Revisa los resultados arriba para ver qué tests pasaron o fallaron{Colors.RESET}\n")

if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Pruebas interrumpidas por el usuario{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error inesperado: {str(e)}{Colors.RESET}")
