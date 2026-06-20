# 📖 DOCUMENTACIÓN TÉCNICA - API ENDPOINTS

**Proyecto**: Tienda de Mascotas  
**Versión**: 1.0  
**Fecha**: 2026-06-20  
**Framework**: Django 5.2.7  

---

## 📋 ÍNDICE

1. [Autenticación & Usuarios](#autenticación--usuarios)
2. [Productos & Catálogo](#productos--catálogo)
3. [Panel Administrativo](#panel-administrativo)
4. [Carrito & Checkout](#carrito--checkout)
5. [Chat & Soporte](#chat--soporte)
6. [Ventas & Pagos](#ventas--pagos)
7. [Códigos de Estado](#códigos-de-estado)

---

## 🔐 AUTENTICACIÓN & USUARIOS

### 1. LOGIN - Iniciar Sesión

```
GET/POST /usuarios/login/
```

**Descripción**: Autenticación de usuario con validación de intentos fallidos

**Parámetros** (POST):
```json
{
  "email": "usuario@example.com",
  "password": "contraseña"
}
```

**Respuesta exitosa** (GET):
```html
Página de formulario de login
```

**Respuesta exitosa** (POST 302):
```
Redirección a / (página de inicio)
```

**Respuesta error** (POST 200):
```
Vuelve a mostrar el formulario con mensajes de error
```

**Validaciones**:
- Email debe ser válido y existir
- Máximo 5 intentos fallidos (bloquea temporalmente)
- Registra LOGIN en AuditLog

---

### 2. LOGOUT - Cerrar Sesión

```
GET /usuarios/logout/
```

**Descripción**: Cierra la sesión del usuario autenticado

**Parámetros**: Ninguno

**Respuesta** (302):
```
Redirección a /
Registra LOGOUT en AuditLog
```

**Autenticación requerida**: Sí

---

### 3. PERFIL - Ver/Editar Perfil

```
GET/POST /usuarios/perfil/
```

**Descripción**: Visualizar y editar datos del usuario autenticado

**Parámetros** (POST):
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "+591-71234567",
  "direccion": "Calle Principal 123"
}
```

**Respuesta** (GET):
```html
Página del perfil con formulario editable
```

**Respuesta** (POST 302):
```
Redirección a /usuarios/perfil/
Mensaje: "Perfil actualizado"
Registra UPDATE en AuditLog
```

**Autenticación requerida**: Sí

---

### 4. PERFIL JSON - API

```
GET /usuarios/api/profile/
```

**Descripción**: Retorna datos del perfil en formato JSON

**Parámetros**: Ninguno

**Respuesta** (200):
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

**Autenticación requerida**: Sí

---

### 5. CAMBIAR CONTRASEÑA

```
GET/POST /usuarios/cambiar-contrasena/
```

**Descripción**: Cambio de contraseña desde el panel de usuario

**Parámetros** (POST):
```json
{
  "password_actual": "contraseña_actual",
  "password_nueva": "contraseña_nueva",
  "password_confirma": "contraseña_nueva"
}
```

**Respuesta** (GET):
```html
Página con formulario de cambio de contraseña
```

**Respuesta** (POST 302):
```
Redirección a /usuarios/perfil/
Mensaje: "Contraseña actualizada"
Registra UPDATE en AuditLog con cambios: "Contraseña actualizada"
```

**Validaciones**:
- Contraseña actual debe ser correcta
- Nueva contraseña debe tener mín. 8 caracteres
- Contraseñas deben coincidir

**Autenticación requerida**: Sí

---

### 6. REGISTRARSE - Nuevo Usuario

```
GET/POST /usuarios/register/
```

**Descripción**: Registro de nuevo cliente en el sistema

**Parámetros** (POST):
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "password": "contraseña_segura",
  "password_confirm": "contraseña_segura"
}
```

**Respuesta** (GET):
```html
Página del formulario de registro
```

**Respuesta** (POST 302):
```
Redirección a /usuarios/login/
Mensaje: "Registro exitoso"
Registra CREATE en AuditLog
```

**Validaciones**:
- Email único (no puede repetirse)
- Contraseña mín. 8 caracteres
- Email válido

**Autenticación requerida**: No

---

### 7. FORZAR CAMBIO DE CONTRASEÑA

```
GET/POST /usuarios/force-password-change/
```

**Descripción**: Empleados deben cambiar contraseña temporal en primer login

**Parámetros** (POST):
```json
{
  "password": "nueva_contraseña_permanente",
  "password_confirm": "nueva_contraseña_permanente"
}
```

**Respuesta** (POST 302):
```
Redirección a /panel/empleados/area/
Contraseña permanente establecida
```

**Autenticación requerida**: Sí (empleados)

---

### 8. RECUPERAR CONTRASEÑA - Verificar Email

```
POST /usuarios/recovery/verify/
```

**Descripción**: Primer paso de recuperación: verifica que email existe

**Parámetros** (POST - JSON):
```json
{
  "email": "usuario@example.com"
}
```

**Respuesta** (200):
```json
{
  "status": "success",
  "message": "Código enviado al email"
}
```

**Respuesta error** (400):
```json
{
  "status": "error",
  "message": "Email no encontrado"
}
```

---

### 9. VALIDAR CÓDIGO DE RECUPERACIÓN

```
POST /usuarios/recovery/verify-code/
```

**Descripción**: Valida código de recuperación enviado por email

**Parámetros** (POST - JSON):
```json
{
  "email": "usuario@example.com",
  "code": "123456"
}
```

**Respuesta** (200):
```json
{
  "status": "success",
  "token": "token_temporal_para_reset"
}
```

**Respuesta error** (400):
```json
{
  "status": "error",
  "message": "Código inválido o expirado"
}
```

---

### 10. PASSWORD RESET - Solicitar

```
GET/POST /usuarios/password_reset/
```

**Descripción**: Inicia proceso de reset de contraseña

**Parámetros** (POST):
```json
{
  "email": "usuario@example.com"
}
```

**Respuesta** (POST 302):
```
Redirección a /usuarios/password_reset/done/
Email de reset enviado
```

---

### 11. PASSWORD RESET CONFIRM

```
GET/POST /usuarios/reset/<uidb64>/<token>/
```

**Descripción**: Completa el reset de contraseña con link del email

**Parámetros** (POST):
```json
{
  "new_password1": "nueva_contraseña",
  "new_password2": "nueva_contraseña"
}
```

**Respuesta** (POST 302):
```
Redirección a /usuarios/reset/done/
Contraseña actualizada exitosamente
```

---

## 🛍️ PRODUCTOS & CATÁLOGO

### 12. CATÁLOGO - Listar Productos

```
GET /catalogo/
```

**Descripción**: Lista pública de productos con filtros

**Parámetros Query**:
```
?categoria=1          # ID de categoría
?min_price=100        # Precio mínimo
?max_price=5000       # Precio máximo
?search=collar        # Búsqueda por nombre
?ordenar=precio       # Ordenar: precio, nombre, nuevo
?page=2               # Número de página
```

**Respuesta** (200):
```html
Página HTML con grid de productos paginado
```

**Sin autenticación requerida**

---

### 13. ÚLTIMOS PRODUCTOS - API JSON

```
GET /catalogo/ultimos/?cantidad=5
```

**Descripción**: Retorna últimos N productos en formato JSON

**Parámetros Query**:
```
?cantidad=5    # Cantidad de productos a retornar (default: 10)
```

**Respuesta** (200):
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
    "nombre": "Juguete Pelota",
    "precio": 45.00,
    "categoria": "Juguetes",
    "imagen": "/media/pelota.jpg",
    "stock": 50
  }
]
```

---

### 14. STOCK DE PRODUCTO - API

```
GET /catalogo/stock/<int:product_id>/
```

**Descripción**: Obtiene el stock actual disponible de un producto

**Parámetros Path**:
```
<int:product_id>    # ID del producto (ej: 15)
```

**Respuesta** (200):
```json
{
  "id": 15,
  "nombre": "Alimento Premium",
  "stock": 45,
  "disponible": true
}
```

**Respuesta error** (404):
```json
{
  "error": "Producto no encontrado"
}
```

---

### 15. NOTIFICACIONES - Sin Leer

```
GET /catalogo/notificaciones/
```

**Descripción**: Lista de notificaciones no leídas del usuario

**Parámetros**: Ninguno

**Respuesta** (200):
```json
{
  "total": 3,
  "notificaciones": [
    {
      "id": 1,
      "titulo": "Tu compra fue entregada",
      "mensaje": "Compra #1234 recibida",
      "fecha": "2026-06-20 14:30:00",
      "leida": false
    }
  ]
}
```

**Autenticación requerida**: Sí

---

### 16. MARCAR NOTIFICACIÓN LEÍDA

```
POST /catalogo/notificaciones/marcar/
```

**Descripción**: Marca una notificación como leída

**Parámetros** (POST - JSON):
```json
{
  "notification_id": 1
}
```

**Respuesta** (200):
```json
{
  "status": "success",
  "message": "Notificación marcada como leída"
}
```

**Autenticación requerida**: Sí

---

### 17. VALIDAR CUPÓN

```
POST /catalogo/validar-cupon/
```

**Descripción**: Valida si un código de cupón es válido (AJAX)

**Parámetros** (POST - JSON):
```json
{
  "codigo": "VERANO2026"
}
```

**Respuesta** (200):
```json
{
  "valido": true,
  "descuento": 20,
  "descuento_tipo": "%",
  "descripcion": "20% descuento en compras mayores a $500"
}
```

**Respuesta error** (200):
```json
{
  "valido": false,
  "error": "Cupón expirado o inválido"
}
```

---

### 18. CANJEAR CUPÓN

```
POST /catalogo/canjear-cupon/
```

**Descripción**: Aplica cupón al carrito

**Parámetros** (POST - JSON):
```json
{
  "codigo": "VERANO2026"
}
```

**Respuesta** (200):
```json
{
  "status": "success",
  "descuento_aplicado": 150.00,
  "total_nuevo": 1350.00
}
```

**Autenticación requerida**: Sí

---

## 📊 PANEL ADMINISTRATIVO

### 19. DASHBOARD - Principal

```
GET /panel/
```

**Descripción**: Dashboard con estadísticas principales

**Parámetros Query**:
```
?rango=hoy          # hoy, semana, mes, trimestre
?fecha_inicio=2026-01-01
?fecha_fin=2026-12-31
```

**Respuesta** (200):
```html
Página con gráficos y estadísticas:
- Ventas totales
- Inventario
- Clientes activos
- Órdenes pendientes
```

**Autenticación requerida**: Sí (Admin)

---

### 20. INVENTARIO - Listar Productos

```
GET /panel/inventario/
```

**Descripción**: Lista de productos con búsqueda y filtros

**Parámetros Query**:
```
?search=collar      # Búsqueda por nombre
?categoria=2        # Filtrar por categoría
?stock_bajo=true    # Mostrar solo con stock bajo
```

**Respuesta** (200):
```html
Tabla de productos con acciones: editar, eliminar
```

**Autenticación requerida**: Sí (Admin)

---

### 21. CREAR PRODUCTO

```
GET/POST /panel/inventario/nuevo/
```

**Descripción**: Crear nuevo producto en el inventario

**Parámetros** (POST - FormData):
```
nombre: "Collar Premium"
descripcion: "Collar de cuero premium"
precio: 150.00
categoria: 3
stock: 50
imagen: <archivo>
```

**Respuesta** (POST 302):
```
Redirección a /panel/inventario/
Mensaje: "Producto creado"
Registra CREATE en AuditLog
```

**Autenticación requerida**: Sí (Admin)

---

### 22. ACTUALIZAR PRODUCTO

```
GET/POST /panel/inventario/<int:pk>/editar/
```

**Descripción**: Editar producto existente

**Parámetros Path**:
```
<int:pk>    # ID del producto (ej: 15)
```

**Parámetros** (POST - FormData):
```
nombre: "Collar Premium Plus"
precio: 175.00
stock: 45
```

**Respuesta** (POST 302):
```
Redirección a /panel/inventario/
Mensaje: "Producto actualizado"
Registra UPDATE en AuditLog
```

**Autenticación requerida**: Sí (Admin)

---

### 23. ELIMINAR PRODUCTO

```
GET/POST /panel/inventario/<int:pk>/eliminar/
```

**Descripción**: Eliminar producto del inventario

**Parámetros Path**:
```
<int:pk>    # ID del producto
```

**Respuesta** (GET):
```html
Página de confirmación
```

**Respuesta** (POST 302):
```
Redirección a /panel/inventario/
Mensaje: "Producto eliminado"
Registra DELETE en AuditLog
```

**Autenticación requerida**: Sí (Admin)

---

### 24. CATEGORÍAS - Listar

```
GET /panel/categorias/
```

**Descripción**: Lista de categorías de productos

**Respuesta** (200):
```html
Tabla de categorías con acciones
```

**Autenticación requerida**: Sí (Admin)

---

### 25. CREAR CATEGORÍA

```
GET/POST /panel/categorias/nueva/
```

**Parámetros** (POST - FormData):
```
nombre: "Accesorios"
descripcion: "Accesorios para mascotas"
```

**Respuesta** (POST 302):
```
Redirección a /panel/categorias/
Registra CREATE en AuditLog
```

**Autenticación requerida**: Sí (Admin)

---

### 26. ACTUALIZAR CATEGORÍA

```
GET/POST /panel/categorias/<int:pk>/editar/
```

**Parámetros** (POST):
```
nombre: "Accesorios Premium"
descripcion: "Accesorios de calidad premium"
```

**Respuesta** (POST 302):
```
Redirección a /panel/categorias/
Registra UPDATE en AuditLog
```

---

### 27. ELIMINAR CATEGORÍA

```
GET/POST /panel/categorias/<int:pk>/eliminar/
```

**Respuesta** (POST 302):
```
Redirección a /panel/categorias/
Registra DELETE en AuditLog
```

---

### 28. EMPLEADOS - Listar

```
GET /panel/empleados/
```

**Descripción**: Lista de empleados

**Parámetros Query**:
```
?search=juan        # Búsqueda por nombre
?departamento=2     # Filtrar por departamento
```

**Respuesta** (200):
```html
Tabla de empleados
```

---

### 29. CREAR EMPLEADO

```
GET/POST /panel/empleados/nuevo/
```

**Parámetros** (POST):
```json
{
  "nombre": "Carlos García",
  "email": "carlos@tienda.com",
  "rol": "vendedor",
  "departamento": "ventas"
}
```

**Respuesta** (POST 302):
```
Empleado creado con contraseña temporal
Registra CREATE en AuditLog
```

---

### 30. ACTUALIZAR EMPLEADO

```
GET/POST /panel/empleados/<int:pk>/editar/
```

**Parámetros Path**:
```
<int:pk>    # ID del empleado
```

**Respuesta** (POST 302):
```
Empleado actualizado
Registra UPDATE en AuditLog
```

---

### 31. ELIMINAR EMPLEADO

```
GET/POST /panel/empleados/<int:pk>/eliminar/
```

**Respuesta** (POST 302):
```
Empleado eliminado
Registra DELETE en AuditLog
```

---

### 32. CLIENTES - Listar

```
GET /panel/clientes/
```

**Descripción**: Lista de clientes registrados

**Parámetros Query**:
```
?search=nombre      # Búsqueda
?activos=true       # Solo clientes activos
```

**Respuesta** (200):
```html
Tabla con información de clientes y compras
```

---

### 33. PROMOCIONES - Listar

```
GET /panel/promociones/
```

**Descripción**: Productos próximos a vencer (promociones)

**Respuesta** (200):
```html
Tabla de productos con descuentos aplicables
```

---

### 34. EDITAR PROMOCIÓN

```
GET/POST /panel/promociones/<int:pk>/editar/
```

**Parámetros** (POST):
```json
{
  "descuento_porcentaje": 20,
  "fecha_inicio": "2026-06-20",
  "fecha_fin": "2026-07-20"
}
```

**Respuesta** (POST 302):
```
Promoción actualizada
Registra UPDATE en AuditLog
```

---

### 35. TOGGLE PROMOCIÓN

```
POST /panel/promociones/<int:pk>/toggle/
```

**Descripción**: Activa/desactiva una promoción

**Respuesta** (200):
```json
{
  "status": "success",
  "activa": true
}
```

---

### 36. ELIMINAR PROMOCIÓN

```
GET/POST /panel/promociones/<int:pk>/eliminar/
```

**Respuesta** (POST 302):
```
Promoción eliminada
Registra DELETE en AuditLog
```

---

### 37. CUPONES - Listar

```
GET /panel/cupones/
```

**Descripción**: Lista de códigos de cupón activos

**Respuesta** (200):
```html
Tabla de cupones con código, descuento, vigencia
```

---

### 38. ELIMINAR CUPÓN

```
GET/POST /panel/cupones/<int:pk>/eliminar/
```

**Respuesta** (POST 302):
```
Cupón eliminado
Registra DELETE en AuditLog
```

---

### 39. EXPORTAR PDF

```
GET /panel/exportar/pdf/
```

**Descripción**: Exporta dashboard a PDF

**Parámetros Query**:
```
?rango=mes          # Período de datos
```

**Respuesta** (200):
```
Archivo PDF descargable
```

---

### 40. EXPORTAR EXCEL

```
GET /panel/exportar/excel/
```

**Descripción**: Exporta datos a Excel

**Respuesta** (200):
```
Archivo .xlsx descargable
```

---

### 41. DASHBOARD EMPLEADO

```
GET /panel/empleados/area/
```

**Descripción**: Dashboard limitado para empleados

**Respuesta** (200):
```html
Vista de estadísticas básicas
```

**Autenticación requerida**: Sí (Empleados)

---

### 42. INVENTARIO EMPLEADO (LECTURA)

```
GET /panel/empleados/area/inventario/
```

**Descripción**: Inventario en modo solo lectura para empleados

**Respuesta** (200):
```html
Tabla de productos sin opciones de edición
```

---

### 43. PERFIL EMPLEADO

```
GET /panel/empleados/area/perfil/
```

**Descripción**: Ver perfil personal del empleado

**Respuesta** (200):
```html
Página con datos del empleado
```

---

## 🛒 CARRITO & CHECKOUT

### 44. CHECKOUT

```
GET /carrito/checkout/
```

**Descripción**: Página de checkout del carrito

**Autenticación requerida**: Sí (redirige a register si no auth)

**Respuesta**:
```html
Página con resumen de carrito y formulario de envío
```

---

## 💬 CHAT & SOPORTE

### 45. ENVIAR MENSAJE CHAT

```
POST /chat/send/
```

**Descripción**: Enviar mensaje de chat (con integración Gemini AI)

**Parámetros** (POST - JSON):
```json
{
  "mensaje": "Hola, tengo una pregunta sobre envíos"
}
```

**Respuesta** (200):
```json
{
  "status": "success",
  "respuesta_ai": "Claro, puedo ayudarte con eso..."
}
```

**Registra**: CREATE en AuditLog

**Autenticación requerida**: No

---

### 46. WIDGET CHAT

```
GET /chat/widget/
```

**Descripción**: Widget flotante de chat

**Respuesta** (200):
```html
HTML/JS del widget de chat
```

---

### 47. CHAT PERSONALIZADO

```
GET /chat/personalizado/
```

**Descripción**: Chat avanzado con atención personalizada (M/M/1 queue)

**Respuesta** (200):
```html
Página de chat con cola de atención
```

---

## 📈 VENTAS & PAGOS

### 48. LISTA DE VENTAS (API)

```
GET /api/ventas/
```

**Descripción**: API JSON de todas las ventas (solo autenticado)

**Parámetros Query**:
```
?fecha_inicio=2026-01-01
?fecha_fin=2026-12-31
?estado=completado
```

**Respuesta** (200):
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
    }
  ]
}
```

**Autenticación requerida**: Sí

---

### 49. CHECKOUT PAGOS

```
GET /pagos/checkout/
```

**Descripción**: Página de checkout de pagos

**Respuesta** (200):
```html
Página con resumen y botón de pago
```

---

### 50. CREAR SESIÓN STRIPE

```
POST /pagos/create-checkout-session/
```

**Descripción**: Crea sesión de pago en Stripe

**Parámetros** (POST - JSON):
```json
{
  "items": [
    {"producto_id": 1, "cantidad": 2},
    {"producto_id": 5, "cantidad": 1}
  ]
}
```

**Respuesta** (200):
```json
{
  "url": "https://checkout.stripe.com/pay/cs_...",
  "session_id": "cs_..."
}
```

---

### 51. WEBHOOK STRIPE

```
POST /pagos/webhook/
```

**Descripción**: Webhook para confirmación de pagos Stripe

**Headers requeridos**:
```
Stripe-Signature: t=...,v1=...
```

**Body** (Stripe Event):
```json
{
  "id": "evt_...",
  "type": "charge.succeeded",
  "data": {
    "object": {
      "id": "py_...",
      "amount": 150000,
      "metadata": {
        "session_id": "cs_..."
      }
    }
  }
}
```

**Respuesta** (200):
```json
{
  "received": true
}
```

**Sin autenticación**

---

### 52. PAGO EXITOSO

```
GET /pagos/pago/exito/
```

**Descripción**: Página de confirmación de pago exitoso

**Parámetros Query**:
```
?session_id=cs_...    # ID de sesión de Stripe
```

**Respuesta** (200):
```html
Página de confirmación con número de orden
```

---

### 53. PAGO ERROR

```
GET /pagos/pago/error/
```

**Descripción**: Página de error de pago

**Respuesta** (200):
```html
Página con opción de reintentar
```

---

### 54. RECIBO PDF

```
GET /pagos/pago/recibo/<str:session_id>/
```

**Descripción**: Genera recibo PDF de la compra

**Parámetros Path**:
```
<str:session_id>    # ID de sesión de Stripe
```

**Respuesta** (200):
```
Archivo PDF descargable con detalles de compra
```

---

## 🔢 CÓDIGOS DE ESTADO

### HTTP Status Codes

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| **200** | OK - Éxito | GET exitoso, POST procesado |
| **302** | Redirección | Post exitoso redirige |
| **400** | Bad Request | Parámetros inválidos |
| **401** | No autenticado | Falta login |
| **403** | Prohibido | Permisos insuficientes |
| **404** | No encontrado | Producto/Usuario no existe |
| **405** | Método no permitido | GET en endpoint POST |
| **500** | Error servidor | Error interno |

---

## 🔐 AUTENTICACIÓN

### Tipos de Autenticación

- **Session-based**: Cookies de sesión para usuario web
- **Email verification**: Códigos de 6 dígitos para recuperación
- **Tokens**: JWT para APIs (JSON endpoints)
- **API Key**: Para integraciones de terceros

### Niveles de Permisos

```
Sin autenticación    → Páginas públicas, Catálogo, Registro
Cliente autenticado  → Perfil, Historial, Carrito, Chat
Empleado             → Panel limitado, Inventario (lectura)
Administrador        → Panel completo, CRUD, Reportes
Superuser            → Acceso total al sistema
```

---

## 📝 NOTAS IMPORTANTES

1. **Auditoría**: Todas las acciones CREATE/UPDATE/DELETE se registran en AuditLog
2. **CSRF**: Todos los POST incluyen token CSRF
3. **Rate Limiting**: Login tiene máximo 5 intentos
4. **Timeouts**: Sesión expira después de 30 minutos de inactividad
5. **Validaciones**: Email único, contraseña mín 8 caracteres
6. **Timezone**: UTC por defecto, conversión local en frontend
7. **Paginación**: Por defecto 20 items por página

---

## 📞 CONTACTO & SOPORTE

Para preguntas técnicas sobre los endpoints, contactar al equipo de desarrollo.

**Última actualización**: 2026-06-20  
**Estado**: Documentación Completa ✅
