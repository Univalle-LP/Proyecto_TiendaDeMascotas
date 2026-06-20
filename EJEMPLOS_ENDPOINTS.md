# 🛠️ EJEMPLOS DE USO - API ENDPOINTS

**Proyecto**: Tienda de Mascotas  
**Base URL**: `http://localhost:8000` (desarrollo)

---

## 📝 AUTENTICACIÓN - EJEMPLOS

### Ejemplo 1: Registrar Nuevo Usuario

**cURL**:
```bash
curl -X POST http://localhost:8000/usuarios/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "nombre=Juan Pérez&email=juan@example.com&password=Segura123&password_confirm=Segura123"
```

**Python - Requests**:
```python
import requests

url = "http://localhost:8000/usuarios/register/"
data = {
    'nombre': 'Juan Pérez',
    'email': 'juan@example.com',
    'password': 'Segura123',
    'password_confirm': 'Segura123'
}
response = requests.post(url, data=data)
print(response.status_code)  # 302 (redirige a login)
```

**JavaScript - Fetch**:
```javascript
fetch('http://localhost:8000/usuarios/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'nombre=Juan&email=juan@test.com&password=Seg123&password_confirm=Seg123',
  credentials: 'include'
})
.then(r => r.text())
.then(console.log)
```

---

### Ejemplo 2: Login

**cURL**:
```bash
curl -X POST http://localhost:8000/usuarios/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c cookies.txt \
  -d "email=juan@example.com&password=Segura123"
```

**Python**:
```python
import requests

session = requests.Session()
url = "http://localhost:8000/usuarios/login/"
data = {'email': 'juan@example.com', 'password': 'Segura123'}
response = session.post(url, data=data)
print(response.status_code)  # 302 (login exitoso)
print(session.cookies)        # Guarda cookies de sesión
```

---

### Ejemplo 3: Obtener Perfil del Usuario (JSON)

**cURL**:
```bash
curl -X GET http://localhost:8000/usuarios/api/profile/ \
  -H "Cookie: sessionid=abc123..." \
  -H "Accept: application/json"
```

**Python**:
```python
response = session.get('http://localhost:8000/usuarios/api/profile/')
if response.status_code == 200:
    perfil = response.json()
    print(f"Usuario: {perfil['nombre']}")
    print(f"Email: {perfil['email']}")
    print(f"Rol: {perfil['rol']}")
```

**Respuesta**:
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "+591-71234567",
  "rol": "Cliente",
  "estado": "activo",
  "fecha_registro": "2026-01-15"
}
```

---

### Ejemplo 4: Cambiar Contraseña

**cURL**:
```bash
curl -X POST http://localhost:8000/usuarios/cambiar-contrasena/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c cookies.txt \
  -d "password_actual=Segura123&password_nueva=MasSegura456&password_confirma=MasSegura456"
```

---

## 🛍️ PRODUCTOS - EJEMPLOS

### Ejemplo 5: Listar Productos (Catálogo)

**URL con parámetros**:
```
GET http://localhost:8000/catalogo/?categoria=2&min_price=100&max_price=1000
```

**cURL**:
```bash
curl -X GET "http://localhost:8000/catalogo/?search=collar&ordenar=precio&page=1"
```

**Python**:
```python
import requests

params = {
    'search': 'collar',
    'ordenar': 'precio',
    'page': 1
}
response = requests.get('http://localhost:8000/catalogo/', params=params)
# Retorna HTML de la página
```

---

### Ejemplo 6: Obtener Últimos Productos (JSON)

**cURL**:
```bash
curl -X GET http://localhost:8000/catalogo/ultimos/?cantidad=5 \
  -H "Accept: application/json"
```

**Python**:
```python
response = requests.get('http://localhost:8000/catalogo/ultimos/?cantidad=5')
if response.status_code == 200:
    productos = response.json()
    for p in productos:
        print(f"{p['nombre']} - ${p['precio']}")
```

**Respuesta**:
```json
[
  {
    "id": 1,
    "nombre": "Collar Premium",
    "precio": 150.00,
    "categoria": "Accesorios",
    "imagen": "/media/collar.jpg",
    "stock": 25
  },
  {
    "id": 2,
    "nombre": "Alimento Premium",
    "precio": 450.00,
    "categoria": "Alimentos",
    "imagen": "/media/alimento.jpg",
    "stock": 50
  }
]
```

---

### Ejemplo 7: Obtener Stock de Producto

**cURL**:
```bash
curl -X GET http://localhost:8000/catalogo/stock/15/ \
  -H "Accept: application/json"
```

**JavaScript**:
```javascript
fetch('http://localhost:8000/catalogo/stock/15/')
  .then(r => r.json())
  .then(data => {
    console.log(`Producto: ${data.nombre}`);
    console.log(`Stock disponible: ${data.stock}`);
    console.log(`¿Disponible?: ${data.disponible}`);
  })
```

**Respuesta**:
```json
{
  "id": 15,
  "nombre": "Juguete Pelota",
  "stock": 45,
  "disponible": true
}
```

---

### Ejemplo 8: Validar Cupón

**cURL**:
```bash
curl -X POST http://localhost:8000/catalogo/validar-cupon/ \
  -H "Content-Type: application/json" \
  -d '{"codigo": "VERANO2026"}'
```

**Python**:
```python
import requests
import json

url = "http://localhost:8000/catalogo/validar-cupon/"
data = {"codigo": "VERANO2026"}
response = requests.post(url, json=data)

if response.status_code == 200:
    resultado = response.json()
    if resultado['valido']:
        print(f"✓ Descuento: {resultado['descuento']}{resultado['descuento_tipo']}")
    else:
        print(f"✗ {resultado['error']}")
```

**Respuesta exitosa**:
```json
{
  "valido": true,
  "descuento": 20,
  "descuento_tipo": "%",
  "descripcion": "20% descuento en compras mayores a $500"
}
```

---

## 📋 PANEL ADMINISTRATIVO - EJEMPLOS

### Ejemplo 9: Crear Nuevo Producto

**cURL con FormData**:
```bash
curl -X POST http://localhost:8000/panel/inventario/nuevo/ \
  -H "Cookie: sessionid=abc123..." \
  -F "nombre=Collar Premium Plus" \
  -F "descripcion=Collar de cuero premium" \
  -F "precio=175.00" \
  -F "categoria=3" \
  -F "stock=50" \
  -F "imagen=@collar.jpg"
```

**Python - Requests**:
```python
session = requests.Session()
session.cookies.set('sessionid', 'tu_session_id')

url = "http://localhost:8000/panel/inventario/nuevo/"
files = {'imagen': open('collar.jpg', 'rb')}
data = {
    'nombre': 'Collar Premium Plus',
    'descripcion': 'Collar de cuero premium',
    'precio': 175.00,
    'categoria': 3,
    'stock': 50
}

response = session.post(url, files=files, data=data)
print(response.status_code)  # 302 (creado exitosamente)
```

---

### Ejemplo 10: Actualizar Producto

**cURL**:
```bash
curl -X POST http://localhost:8000/panel/inventario/15/editar/ \
  -H "Cookie: sessionid=abc123..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "nombre=Collar Premium Plus&precio=180.00&stock=45"
```

**Python**:
```python
url = "http://localhost:8000/panel/inventario/15/editar/"
data = {
    'nombre': 'Collar Premium Plus',
    'precio': 180.00,
    'stock': 45
}
response = session.post(url, data=data)
print("Producto actualizado" if response.status_code == 302 else "Error")
```

---

### Ejemplo 11: Eliminar Producto

**cURL**:
```bash
curl -X POST http://localhost:8000/panel/inventario/15/eliminar/ \
  -H "Cookie: sessionid=abc123..." \
  -d "confirm=on"
```

---

### Ejemplo 12: Listar Inventario con Búsqueda

**cURL**:
```bash
curl -X GET "http://localhost:8000/panel/inventario/?search=collar&stock_bajo=true" \
  -H "Cookie: sessionid=abc123..."
```

---

### Ejemplo 13: Exportar Dashboard a PDF

**cURL**:
```bash
curl -X GET "http://localhost:8000/panel/exportar/pdf/?rango=mes" \
  -H "Cookie: sessionid=admin..." \
  -o dashboard.pdf
```

**Python**:
```python
response = session.get(
    'http://localhost:8000/panel/exportar/pdf/?rango=mes'
)
with open('dashboard.pdf', 'wb') as f:
    f.write(response.content)
print("PDF descargado")
```

---

## 💬 CHAT - EJEMPLOS

### Ejemplo 14: Enviar Mensaje de Chat

**cURL**:
```bash
curl -X POST http://localhost:8000/chat/send/ \
  -H "Content-Type: application/json" \
  -d '{"mensaje": "Hola, tengo una pregunta sobre envíos"}'
```

**Python**:
```python
import requests

url = "http://localhost:8000/chat/send/"
data = {"mensaje": "¿Cuál es el tiempo de entrega a Santa Cruz?"}
response = requests.post(url, json=data)

if response.status_code == 200:
    resultado = response.json()
    print(f"Respuesta IA: {resultado['respuesta_ai']}")
```

**Respuesta**:
```json
{
  "status": "success",
  "respuesta_ai": "El tiempo de entrega a Santa Cruz es de 3-5 días hábiles. Ofrecemos envío gratis para compras mayores a $500."
}
```

---

## 💳 PAGOS - EJEMPLOS

### Ejemplo 15: Crear Sesión de Pago (Stripe)

**cURL**:
```bash
curl -X POST http://localhost:8000/pagos/create-checkout-session/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=abc123..." \
  -d '{
    "items": [
      {"producto_id": 1, "cantidad": 2},
      {"producto_id": 5, "cantidad": 1}
    ]
  }'
```

**Python**:
```python
session = requests.Session()
session.cookies.set('sessionid', 'tu_session_id')

url = "http://localhost:8000/pagos/create-checkout-session/"
data = {
    "items": [
        {"producto_id": 1, "cantidad": 2},
        {"producto_id": 5, "cantidad": 1}
    ]
}

response = session.post(url, json=data)
if response.status_code == 200:
    pago = response.json()
    print(f"URL de pago: {pago['url']}")
    print(f"Session ID: {pago['session_id']}")
```

**Respuesta**:
```json
{
  "url": "https://checkout.stripe.com/pay/cs_test_...",
  "session_id": "cs_test_..."
}
```

---

### Ejemplo 16: Webhook de Stripe (Interno)

Este endpoint no requiere autenticación. Stripe lo llama automáticamente.

**Respuesta esperada** (200):
```json
{
  "received": true
}
```

---

### Ejemplo 17: Descargar Recibo PDF

**cURL**:
```bash
curl -X GET http://localhost:8000/pagos/pago/recibo/cs_test_123/ \
  -o recibo.pdf
```

**Python**:
```python
response = requests.get('http://localhost:8000/pagos/pago/recibo/cs_test_123/')
with open('recibo.pdf', 'wb') as f:
    f.write(response.content)
print("Recibo descargado")
```

---

## 📊 VENTAS (API) - EJEMPLOS

### Ejemplo 18: Obtener Lista de Ventas

**cURL**:
```bash
curl -X GET "http://localhost:8000/api/ventas/?fecha_inicio=2026-01-01&fecha_fin=2026-12-31&estado=completado" \
  -H "Cookie: sessionid=abc123..."
```

**Python**:
```python
params = {
    'fecha_inicio': '2026-01-01',
    'fecha_fin': '2026-12-31',
    'estado': 'completado'
}
response = session.get('http://localhost:8000/api/ventas/', params=params)

if response.status_code == 200:
    ventas = response.json()
    print(f"Total de ventas: {ventas['total']}")
    for v in ventas['ventas']:
        print(f"Cliente: {v['cliente']} - Total: ${v['total']}")
```

**Respuesta**:
```json
{
  "total": 150,
  "ventas": [
    {
      "id": 1,
      "cliente": "Juan Pérez",
      "total": 1500.00,
      "fecha": "2026-06-20",
      "estado": "entregado"
    },
    {
      "id": 2,
      "cliente": "María García",
      "total": 750.00,
      "fecha": "2026-06-19",
      "estado": "en_transito"
    }
  ]
}
```

---

## 🔑 MANEJO DE ERRORES

### Ejemplo 19: Error 401 (No autenticado)

**Solicitud**:
```bash
curl -X GET http://localhost:8000/panel/inventario/
```

**Respuesta** (302):
```
Location: /usuarios/login/?next=/panel/inventario/
```

---

### Ejemplo 20: Error 403 (Prohibido)

**Solicitud** (cliente intentando acceder a panel admin):
```bash
curl -X GET http://localhost:8000/panel/inventario/ \
  -H "Cookie: sessionid=cliente_session..."
```

**Respuesta** (403):
```html
<h1>Acceso Denegado</h1>
<p>No tienes permisos para acceder a esta página.</p>
```

---

### Ejemplo 21: Error 404 (No encontrado)

**Solicitud**:
```bash
curl -X GET http://localhost:8000/panel/inventario/99999/editar/
```

**Respuesta** (404):
```
Producto no encontrado
```

---

## 📱 CLIENTE JAVASCRIPT COMPLETO

```javascript
class TiendaAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  // Autenticación
  async registrar(nombre, email, password) {
    const formData = new FormData();
    formData.append('nombre', nombre);
    formData.append('email', email);
    formData.append('password', password);
    formData.append('password_confirm', password);
    
    const response = await fetch(`${this.baseURL}/usuarios/register/`, {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });
    return response;
  }

  async login(email, password) {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    
    const response = await fetch(`${this.baseURL}/usuarios/login/`, {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });
    return response;
  }

  async getPerfil() {
    const response = await fetch(`${this.baseURL}/usuarios/api/profile/`, {
      credentials: 'include'
    });
    return response.json();
  }

  // Productos
  async getProductos(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(
      `${this.baseURL}/catalogo/?${queryString}`
    );
    return response.text();
  }

  async getUltimosProductos(cantidad = 5) {
    const response = await fetch(
      `${this.baseURL}/catalogo/ultimos/?cantidad=${cantidad}`
    );
    return response.json();
  }

  async getStock(productoId) {
    const response = await fetch(
      `${this.baseURL}/catalogo/stock/${productoId}/`
    );
    return response.json();
  }

  async validarCupon(codigo) {
    const response = await fetch(`${this.baseURL}/catalogo/validar-cupon/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo })
    });
    return response.json();
  }

  // Chat
  async enviarMensaje(mensaje) {
    const response = await fetch(`${this.baseURL}/chat/send/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensaje })
    });
    return response.json();
  }

  // Pagos
  async crearSesionPago(items) {
    const response = await fetch(
      `${this.baseURL}/pagos/create-checkout-session/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items }),
        credentials: 'include'
      }
    );
    return response.json();
  }
}

// Uso
const api = new TiendaAPI();

// Obtener últimos productos
api.getUltimosProductos(3).then(productos => {
  console.log(productos);
});

// Validar cupón
api.validarCupon('VERANO2026').then(resultado => {
  if (resultado.valido) {
    console.log(`Descuento: ${resultado.descuento}${resultado.descuento_tipo}`);
  }
});

// Enviar mensaje de chat
api.enviarMensaje('Hola, necesito ayuda').then(resultado => {
  console.log(resultado.respuesta_ai);
});
```

---

## 🔐 HEADERS IMPORTANTES

### CSRF Token (Django)

Para POST requests, incluir:
```
X-CSRFToken: <valor_del_token_de_la_cookie>
```

En formularios HTML, está incluido automáticamente.

### Authorization

Para APIs que requieren autenticación:
```
Authorization: Bearer <jwt_token>
```

O usar cookies de sesión (automático con `credentials: 'include'`).

---

## 📞 CONTACTO

Para soporte técnico o ejemplos adicionales, contactar al equipo de desarrollo.

**Última actualización**: 2026-06-20
