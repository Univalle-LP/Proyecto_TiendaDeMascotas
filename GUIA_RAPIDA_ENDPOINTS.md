# 📊 GUÍA RÁPIDA - ENDPOINTS POR CATEGORÍA

## 🔐 AUTENTICACIÓN

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/usuarios/login/` | GET/POST | Iniciar sesión |
| `/usuarios/logout/` | GET | Cerrar sesión |
| `/usuarios/register/` | GET/POST | Registro de usuario |
| `/usuarios/password_reset/` | GET/POST | Solicitar reset de contraseña |
| `/usuarios/reset/<uidb64>/<token>/` | GET/POST | Confirmar reset de contraseña |

---

## 👤 PERFIL DE USUARIO

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/usuarios/perfil/` | GET/POST | Ver/editar perfil | Sí |
| `/usuarios/api/profile/` | GET | Perfil en JSON | Sí |
| `/usuarios/cambiar-contrasena/` | GET/POST | Cambiar contraseña | Sí |
| `/usuarios/force-password-change/` | GET/POST | Forzar cambio (empleados) | Sí |

---

## 🛍️ PRODUCTOS

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/catalogo/` | GET | Listar productos con filtros | No |
| `/catalogo/ultimos/` | GET | Últimos N productos (JSON) | No |
| `/catalogo/stock/<id>/` | GET | Stock disponible | No |
| `/catalogo/validar-cupon/` | POST | Validar código de cupón | No |
| `/catalogo/canjear-cupon/` | POST | Aplicar cupón | Sí |

---

## 📢 NOTIFICACIONES

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/catalogo/notificaciones/` | GET | Notificaciones no leídas | Sí |
| `/catalogo/notificaciones/marcar/` | POST | Marcar como leída | Sí |

---

## 📋 PANEL ADMINISTRATIVO

### Inventario

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/panel/inventario/` | GET | Listar productos | Sí |
| `/panel/inventario/nuevo/` | GET/POST | Crear producto | Sí |
| `/panel/inventario/<id>/editar/` | GET/POST | Editar producto | Sí |
| `/panel/inventario/<id>/eliminar/` | GET/POST | Eliminar producto | Sí |

### Categorías

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/panel/categorias/` | GET | Listar categorías | Sí |
| `/panel/categorias/nueva/` | GET/POST | Crear categoría | Sí |
| `/panel/categorias/<id>/editar/` | GET/POST | Editar categoría | Sí |
| `/panel/categorias/<id>/eliminar/` | GET/POST | Eliminar categoría | Sí |

### Empleados

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/panel/empleados/` | GET | Listar empleados | Sí |
| `/panel/empleados/nuevo/` | GET/POST | Crear empleado | Sí |
| `/panel/empleados/<id>/editar/` | GET/POST | Editar empleado | Sí |
| `/panel/empleados/<id>/eliminar/` | GET/POST | Eliminar empleado | Sí |

### Gestión

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/panel/` | GET | Dashboard principal | Sí |
| `/panel/clientes/` | GET | Lista de clientes | Sí |
| `/panel/promociones/` | GET | Promociones activas | Sí |
| `/panel/cupones/` | GET | Cupones activos | Sí |
| `/panel/exportar/pdf/` | GET | Exportar a PDF | Sí |
| `/panel/exportar/excel/` | GET | Exportar a Excel | Sí |

### Área de Empleados

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/panel/empleados/area/` | GET | Dashboard empleado | Sí |
| `/panel/empleados/area/inventario/` | GET | Inventario (lectura) | Sí |
| `/panel/empleados/area/perfil/` | GET | Perfil personal | Sí |

---

## 🛒 COMPRAS

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/carrito/checkout/` | GET | Página de checkout | Sí |

---

## 💬 CHAT & SOPORTE

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/chat/send/` | POST | Enviar mensaje (Gemini AI) | No |
| `/chat/widget/` | GET | Widget flotante | No |
| `/chat/personalizado/` | GET | Chat avanzado (M/M/1) | No |

---

## 💳 PAGOS

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/pagos/checkout/` | GET | Página de pago | Sí |
| `/pagos/create-checkout-session/` | POST | Crear sesión Stripe | Sí |
| `/pagos/webhook/` | POST | Webhook Stripe | No |
| `/pagos/pago/exito/` | GET | Confirmación de pago | No |
| `/pagos/pago/error/` | GET | Error de pago | No |
| `/pagos/pago/recibo/<session_id>/` | GET | Descargar recibo PDF | No |

---

## 📊 VENTAS (API)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/api/ventas/` | GET | Lista de ventas (JSON) | Sí |

---

## 📈 ESTADÍSTICAS POR MÉTODO

### GET (Lecturas)
- 36 endpoints GET
- Mostrar datos, descargar archivos, listar

### POST (Escrituras)
- 21 endpoints POST
- Crear, actualizar, procesar acciones

### GET/POST (Formularios)
- 21 endpoints combinados
- Mostrar formulario (GET), procesar (POST)

---

## 🔐 DISTRIBUCIÓN POR AUTENTICACIÓN

### Públicos (0 autenticación)
```
GET  /catalogo/
GET  /catalogo/ultimos/
GET  /catalogo/stock/<id>/
POST /catalogo/validar-cupon/
GET  /usuarios/login/
POST /usuarios/login/
GET  /usuarios/register/
POST /usuarios/register/
POST /usuarios/recovery/verify/
POST /usuarios/recovery/verify-code/
POST /chat/send/
GET  /chat/widget/
POST /pagos/webhook/
GET  /pagos/pago/exito/
GET  /pagos/pago/error/
```

### Autenticados (Cliente)
```
GET  /usuarios/perfil/
POST /usuarios/perfil/
GET  /usuarios/api/profile/
POST /usuarios/cambiar-contrasena/
POST /catalogo/canjear-cupon/
GET  /catalogo/notificaciones/
POST /catalogo/notificaciones/marcar/
GET  /carrito/checkout/
GET  /pagos/checkout/
POST /pagos/create-checkout-session/
```

### Autenticados (Empleado)
```
GET  /panel/empleados/area/
GET  /panel/empleados/area/inventario/
GET  /panel/empleados/area/perfil/
POST /usuarios/force-password-change/
```

### Autenticados (Admin)
```
GET  /panel/
GET  /panel/inventario/
GET/POST /panel/inventario/nuevo/
GET/POST /panel/inventario/<id>/editar/
GET/POST /panel/inventario/<id>/eliminar/
GET  /panel/categorias/
GET/POST /panel/categorias/nueva/
GET/POST /panel/categorias/<id>/editar/
GET/POST /panel/categorias/<id>/eliminar/
GET  /panel/empleados/
GET/POST /panel/empleados/nuevo/
GET/POST /panel/empleados/<id>/editar/
GET/POST /panel/empleados/<id>/eliminar/
GET  /panel/clientes/
GET  /panel/promociones/
GET/POST /panel/promociones/<id>/editar/
POST /panel/promociones/<id>/toggle/
GET/POST /panel/promociones/<id>/eliminar/
GET  /panel/cupones/
GET/POST /panel/cupones/<id>/eliminar/
GET  /panel/exportar/pdf/
GET  /panel/exportar/excel/
GET  /api/ventas/
```

---

## 💾 FORMATO DE DATOS

### Request Headers Comunes
```
Content-Type: application/json
Authorization: Bearer <token>    # Para APIs con autenticación
X-CSRFToken: <csrf_token>       # Para POST en Django
```

### Response Headers Comunes
```
Content-Type: application/json
Set-Cookie: sessionid=...        # Para mantener sesión
X-Frame-Options: SAMEORIGIN      # Seguridad
```

---

## ⏱️ LÍMITES & TIMEOUTS

| Recurso | Límite | Duración |
|---------|--------|----------|
| Intentos de login | 5 fallos | 15 minutos |
| Sesión activa | 30 minutos | Inactividad |
| Código de recuperación | 6 dígitos | 15 minutos |
| Token de reset | URL con token | 24 horas |
| Cupón válido | Fecha vigencia | Variable |

---

## 🚀 CASOS DE USO COMUNES

### Nuevo Cliente
```
1. POST /usuarios/register/              → Crear cuenta
2. GET  /usuarios/login/                 → Mostrar form
3. POST /usuarios/login/                 → Autenticar
4. GET  /catalogo/                       → Ver catálogo
5. POST /catalogo/validar-cupon/         → Validar cupón
6. GET  /carrito/checkout/               → Preparar compra
7. POST /pagos/create-checkout-session/  → Crear pago
8. POST /pagos/webhook/                  → Confirmar (automático)
9. GET  /pagos/pago/recibo/              → Descargar recibo
```

### Admin: Crear Producto
```
1. GET  /panel/inventario/               → Ver inventario
2. GET  /panel/inventario/nuevo/         → Mostrar formulario
3. POST /panel/inventario/nuevo/         → Crear producto
```

### Admin: Descuento
```
1. GET  /panel/promociones/              → Ver promociones
2. GET  /panel/promociones/<id>/editar/  → Mostrar form
3. POST /panel/promociones/<id>/editar/  → Actualizar descuento
```

---

## 📞 INFORMACIÓN ADICIONAL

- **Documentación completa**: Ver `DOCUMENTACION_API.md`
- **Código fuente**: Revisar archivos en `usuarios/`, `productos/`, `pagos/`, `chat/`
- **Base de datos**: MySQL con ORM Django
- **Auditoría**: Todos los cambios registrados en tabla `audit_logs`

**Última actualización**: 2026-06-20
