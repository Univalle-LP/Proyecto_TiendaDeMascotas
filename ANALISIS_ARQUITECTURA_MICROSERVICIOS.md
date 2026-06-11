# 🏗️ ANÁLISIS ARQUITECTÓNICO - CONVERSIÓN A MICROSERVICIOS
## Adonai D'Empanadas - Proyecto Django

**Fecha**: 11 de junio, 2026  
**Analista**: Software Architect (Microservices Specialist)  
**Estado**: Análisis Completo - Sin Cambios Implementados

---

# 📋 TABLA DE CONTENIDOS

1. [Funcionalidades Actuales](#funcionalidades-actuales)
2. [Análisis de Acoplamiento](#análisis-de-acoplamiento)
3. [Componentes Candidatos a Microservicios](#componentes-candidatos-a-microservicios)
4. [Componentes que NO Deberían Separarse](#componentes-que-no-deberían-separarse)
5. [Arquitectura de Microservicios Propuesta](#arquitectura-de-microservicios-propuesta)
6. [Tabla de Migración](#tabla-de-migración)
7. [Matriz de Dependencias](#matriz-de-dependencias)
8. [Arquitectura Recomendada Final](#arquitectura-recomendada-final)
9. [Plan de Migración Paso a Paso](#plan-de-migración-paso-a-paso)
10. [Consideraciones Técnicas](#consideraciones-técnicas)

---

## 🎯 FUNCIONALIDADES ACTUALES

### **1. Gestión de Usuarios y Autenticación**
- ✅ Registro de clientes (auto-rol 'Cliente')
- ✅ Login personalizado con backend custom (email + password)
- ✅ Bloqueo por intentos fallidos (3 intentos, 30 segundos)
- ✅ Recuperación de contraseña por email
- ✅ Cambio obligatorio de contraseña (empleados)
- ✅ Sincronización automática con Django auth.User
- ✅ Sistema de roles: Administrador, Empleado, Cliente
- ✅ Perfiles de usuario (datos personales)

### **2. Catálogo de Productos**
- ✅ Listado de productos con filtros (categoría, búsqueda, precio)
- ✅ Gestión de categorías
- ✅ Control de inventario (stock actual, stock mínimo)
- ✅ Notificaciones automáticas de cambios de stock
- ✅ Validación de fecha de vencimiento
- ✅ Imagen de productos (almacenamiento en media/)

### **3. Sistema de Carrito y Checkout**
- ✅ Carrito persistente (BD, OneToOne con Usuario)
- ✅ Items en carrito (Carrito → CarritoItem → Producto)
- ✅ Checkout requerido autenticación
- ✅ Integración con Stripe para pagos

### **4. Pagos y Transacciones**
- ✅ Integración Stripe (sesiones de checkout)
- ✅ Webhook de Stripe para confirmación de pago
- ✅ Creación automática de Venta desde webhook
- ✅ Reducción automática de stock al pagar
- ✅ Generación de recibos PDF
- ✅ Registro de pagos (tabla legacy)
- ✅ Manejo de errores de pago

### **5. Gestión de Ventas**
- ✅ Registro de ventas (usuario, total, método de pago)
- ✅ Detalles de venta (productos comprados, cantidades, precios)
- ✅ Estados de venta (pendiente, pagado, preparación, envío, entregado, cancelado)
- ✅ Historial de compras para cliente
- ✅ Vistas admin de reportes de ventas
- ✅ Exportación a PDF y Excel

### **6. Entregas (Delivery)**
- ✅ Asignación de repartidor a venta
- ✅ Registro de entregas (OneToOne con Venta)
- ✅ Vinculación repartidor (Usuario con rol Empleado)

### **7. Chat Inteligente**
- ✅ Widget de chat en tiempo real
- ✅ Integración con Google Gemini 2.5 Flash
- ✅ Detección de intenciones (productos, delivery, info, promociones)
- ✅ Sistema de colas M/M/1 (prioridades, timestamps)
- ✅ Estados de chat (esperando, en_atencion, finalizado, cancelado)
- ✅ Historial de conversaciones
- ✅ Respuestas internas rápidas + fallback a Gemini

### **8. Promociones y Descuentos**
- ✅ Sistema de promociones (2x1, descuentos, ofertas)
- ✅ Status de aprobación (pending, approved, rejected)
- ✅ Cupones de descuento (código único, de un uso)
- ✅ Validación y canje de cupones

### **9. Notificaciones**
- ✅ Notificaciones de cambios de producto
- ✅ Notificaciones de entrada de stock
- ✅ Marca como leída (tabla NotificationRead)
- ✅ Endpoint JSON para cliente

### **10. Panel Administrativo**
- ✅ Dashboard con estadísticas (ventas, inventario, top productos)
- ✅ CRUD de productos (crear, editar, eliminar)
- ✅ CRUD de categorías
- ✅ CRUD de empleados
- ✅ CRUD de promociones (con aprobación)
- ✅ CRUD de cupones
- ✅ Listado de clientes
- ✅ Reportes exportables (PDF, Excel)
- ✅ Vista limitada para empleados

---

## 🔗 ANÁLISIS DE ACOPLAMIENTO

### **NIVEL DE ACOPLAMIENTO: MODERADO-ALTO**

#### **Acoplamiento FUERTE (No Separable Actualmente)**

| Apps | Razón | Dependencia |
|------|-------|------------|
| **productos ↔ pagos** | Webhook de Stripe crea Venta usando cart_items metadata | `strip_webhook()` → `create_venta_from_stripe_session()` |
| **pagos ↔ ventas** | Pagos crea/modifica Venta y VentaDetalle | FK directo en webhook |
| **pagos ↔ productos** | Webhook reduce stock_actual de Producto | `process_payment_stock()` accede Producto/Inventario |
| **carrito ↔ productos** | CarritoItem → Producto (FK) | Cada item referencia un producto |
| **carrito ↔ pagos** | Checkout usa items del carrito | `create_checkout_session()` lee CarritoItem |
| **usuarios ↔ todos** | Foreign Key en Producto, Venta, Chat, etc | Usuario es creador/propietario de objetos |
| **chat ↔ usuarios** | Chat → Usuario (FK), mensajes con remitente | Contexto de usuario necesario |
| **chat ↔ productos** | Gemini puede recomendar productos | `get_top_products()` SQL directo |

#### **Acoplamiento MODERADO (Parcialmente Separable)**

| Apps | Razón | Mitigación |
|------|-------|-----------|
| **productos ↔ delivery** | Venta vincula con Delivery | Solo lectura; podrían ser servicios distintos |
| **core ↔ todos** | Core muestra historial de Venta | Solo lectura de datos |
| **chat ↔ gemini** | Chat depende de API externa | Abstractible en service layer |

#### **Acoplamiento DÉBIL (Fácilmente Separable)**

| Apps | Razón | Estado |
|------|-------|--------|
| **roles** | Standalone, solo define choices | Podría ser constantes |
| **delivery** | OneToOne con Venta pero lógica simple | Independiente |
| **notificaciones** | Sistema de signals, independiente | Podría migrar a event bus |

---

## 🎯 COMPONENTES CANDIDATOS A MICROSERVICIOS

### **1️⃣ AUTH SERVICE (ALTA PRIORIDAD)**

**Responsabilidad**: Autenticación, autorización, gestión de usuarios

**Modelos asociados**:
- `Usuario` (custom)
- `Rol`
- Sincronización con `auth.User` (Django)

**Vistas**:
- `login`, `logout`, `register`, `perfil`, `cambiar_contrasena`, `recovery_verify`

**APIs que expondría**:
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Autenticar (email + password)
- `POST /auth/logout` - Cerrar sesión
- `GET /auth/me` - Info usuario autenticado
- `PUT /auth/perfil` - Actualizar perfil
- `POST /auth/cambiar-contraseña` - Cambiar contraseña
- `POST /auth/recuperar-contraseña` - Iniciar recuperación
- `POST /auth/verificar-token` - JWT token validation
- `POST /auth/refresh-token` - Renovar token

**Dependencias con otros servicios**:
- Envía email (servicio externo de email)
- Valida tokens JWT en otras apps
- Ningún otro servicio depende de lógica de auth (todo por token)

**Base de datos propia**: ✅ **SÍ**
- Tabla `usuarios` (custom)
- Tabla `roles`
- Tabla `auth_user` (de Django, requeriría sincronización)

**Complejidad de extracción**: ⭐⭐⭐ (MEDIA)
- Backend custom necesita refactorización
- Middleware de bloqueo necesita reemplazo (por decorador/servicio)
- Sincronización legacy con `auth.User` debe simplificarse
- Token JWT debe implementarse

---

### **2️⃣ PRODUCT SERVICE (ALTA PRIORIDAD)**

**Responsabilidad**: Gestión de productos, categorías, inventario, stock

**Modelos asociados**:
- `Producto`
- `Categoria`
- `Inventario`
- `Notification` + `NotificationRead`
- `Empleado`

**Vistas**:
- Catálogo, agregar producto, actualizaciones de stock, notificaciones

**APIs que expondría**:
- `GET /products` - Listar productos (con filtros: categoría, búsqueda, precio)
- `GET /products/<id>` - Detalle de producto
- `GET /products/<id>/stock` - Stock disponible (JSON)
- `POST /products` - Crear producto (admin)
- `PUT /products/<id>` - Actualizar producto
- `DELETE /products/<id>` - Eliminar producto
- `GET /categories` - Listar categorías
- `POST /categories` - Crear categoría
- `GET /inventory` - Historial de movimientos
- `POST /inventory/entrada` - Registrar entrada
- `POST /inventory/salida` - Registrar salida (para pagos)
- `GET /notifications` - Notificaciones de usuario
- `POST /notifications/<id>/read` - Marcar leída
- `GET /stock-alert` - Productos con stock bajo

**Dependencias con otros servicios**:
- **Payment Service**: Recibe petición de salida de stock → `POST /inventory/salida`
- **Auth Service**: Usuario que crea/modifica productos
- **Notification Service**: Emite eventos de cambios

**Base de datos propia**: ✅ **SÍ**
- Tabla `productos_producto`
- Tabla `productos_categoria`
- Tabla `productos_inventario`
- Tabla `productos_notification`
- Tabla `productos_notificationread`

**Complejidad de extracción**: ⭐⭐⭐⭐ (MEDIA-ALTA)
- Signals automáticos requieren pub/sub o event bus
- Validación de stock en tiempo real es crítica
- Integración tight con Payment Service (webhook)

---

### **3️⃣ PAYMENT SERVICE (ALTA PRIORIDAD)**

**Responsabilidad**: Pagos, integraciones Stripe, procesamiento de transacciones

**Modelos asociados**:
- `Payment` (legacy)
- Metadata de sesión Stripe

**Vistas**:
- Checkout, webhook Stripe, confirmación, recibos

**APIs que expondría**:
- `POST /payments/checkout-session` - Crear sesión Stripe
- `POST /payments/webhook` - Webhook Stripe (internal)
- `GET /payments/<session_id>` - Estado de pago
- `GET /payments/<session_id>/receipt` - Recibo PDF
- `POST /payments/retry` - Reintentar pago fallido
- `GET /payments/history` - Historial de pagos (para usuario)

**Dependencias con otros servicios**:
- **Order Service**: Crea Venta al pago exitoso
- **Product Service**: Reduce stock
- **Auth Service**: Usuario que realiza pago
- **Notification Service**: Notifica estado de pago

**Integraciones externas**:
- **Stripe API** (pagos)
- **ReportLab** (generación PDF)
- **Email Service** (confirmación de pago)

**Base de datos propia**: ✅ **SÍ** (parcial)
- Tabla `pagos_payment`
- PERO la Venta se crea en Order Service
- Requiere transacciones distribuidas (2PC o Saga pattern)

**Complejidad de extracción**: ⭐⭐⭐⭐⭐ (ALTA)
- Transacción crítica (pago + stock + venta debe ser atómico)
- Webhook de Stripe requiere sincronización perfecta
- Requiere manejo de saga en caso de fallo
- Idempotencia es crítica para reintentos

---

### **4️⃣ ORDER SERVICE (MEDIA PRIORIDAD)**

**Responsabilidad**: Gestión de ventas, órdenes, estados, historial

**Modelos asociados**:
- `Venta`
- `VentaDetalle`

**Vistas**:
- Historial de compras, detalles, estados

**APIs que expondría**:
- `POST /orders` - Crear orden (solo desde Payment Service)
- `GET /orders/<id>` - Detalle de orden
- `GET /orders` - Historial de órdenes del usuario
- `PUT /orders/<id>/status` - Cambiar estado (en_preparacion, en_envio, etc)
- `GET /orders/<id>/details` - Detalles de productos en orden
- `DELETE /orders/<id>` - Cancelar orden
- `GET /orders/stats` - Estadísticas (admin)

**Dependencias con otros servicios**:
- **Payment Service**: Crea orden al pago exitoso
- **Product Service**: Lee detalles de productos
- **Auth Service**: Usuario propietario de orden
- **Delivery Service**: Entrega asociada a orden

**Base de datos propia**: ✅ **SÍ**
- Tabla `ventas_venta`
- Tabla `ventas_ventadetalle`

**Complejidad de extracción**: ⭐⭐⭐ (MEDIA)
- Modelo simple (dos tablas)
- Relación clara con Payment Service
- Estados bien definidos

---

### **5️⃣ CART SERVICE (MEDIA PRIORIDAD)**

**Responsabilidad**: Gestión de carrito, items, persistencia

**Modelos asociados**:
- `Carrito`
- `CarritoItem`

**Vistas**:
- Actualización de carrito, checkout

**APIs que expondría**:
- `GET /cart` - Obtener carrito del usuario
- `POST /cart/items` - Agregar item al carrito
- `PUT /cart/items/<id>` - Actualizar cantidad
- `DELETE /cart/items/<id>` - Eliminar item
- `DELETE /cart` - Vaciar carrito
- `POST /cart/checkout` - Iniciar checkout (redirige a Payment Service)

**Dependencias con otros servicios**:
- **Auth Service**: Usuario propietario de carrito
- **Product Service**: Lee precios/stock de productos
- **Payment Service**: Envía items al checkout

**Base de datos propia**: ✅ **SÍ**
- Tabla `carrito_carrito`
- Tabla `carrito_carritoitem`

**Complejidad de extracción**: ⭐⭐ (BAJA)
- Modelo simple
- Pocas dependencias
- Lógica sencilla

---

### **6️⃣ DELIVERY SERVICE (BAJA PRIORIDAD)**

**Responsabilidad**: Gestión de entregas, repartidores, tracking

**Modelos asociados**:
- `Delivery`
- Repartidor (Usuario con rol Empleado)

**Vistas**:
- Asignación de entregas, tracking

**APIs que expondría**:
- `POST /deliveries` - Crear entrega (desde orden)
- `GET /deliveries/<id>` - Estado de entrega
- `PUT /deliveries/<id>` - Actualizar estado (en_ruta, entregado)
- `GET /deliveries?repartidor=<id>` - Entregas asignadas
- `POST /deliveries/<id>/confirm` - Confirmar entrega (repartidor)
- `GET /deliveries/<id>/tracking` - Historial de cambios

**Dependencias con otros servicios**:
- **Order Service**: Lee orden asociada
- **Auth Service**: Repartidor asignado

**Base de datos propia**: ✅ **SÍ**
- Tabla `delivery_delivery`

**Complejidad de extracción**: ⭐⭐ (BAJA)
- OneToOne con Venta (relación simple)
- Poca lógica de negocio
- Independiente del flujo crítico

---

### **7️⃣ CHAT SERVICE (MEDIA PRIORIDAD)**

**Responsabilidad**: Chat con clientes, integración Gemini, sistema de colas M/M/1

**Modelos asociados**:
- `Chat`
- `MensajeChat`

**Vistas**:
- Widget de chat, envío de mensajes, historial

**APIs que expondría**:
- `POST /chat/messages` - Enviar mensaje
- `GET /chat` - Historial de chat del usuario
- `GET /chat/widget` - Renderizar widget
- `GET /chat/<id>/messages` - Mensajes del chat
- `POST /chat/<id>/close` - Cerrar chat
- `GET /chat/stats` - Estadísticas (tiempo promedio, resolución, etc)

**Dependencias con otros servicios**:
- **Auth Service**: Usuario que inicia chat
- **Product Service**: Recomendación de productos
- **Order Service**: Información de órdenes del usuario

**Integraciones externas**:
- **Google Gemini 2.5 Flash API**
- **Email Service** (notificaciones)

**Base de datos propia**: ✅ **SÍ**
- Tabla `chat_chat`
- Tabla `chat_mensajechat`

**Complejidad de extracción**: ⭐⭐⭐ (MEDIA)
- Integración con Gemini es sencilla
- Sistema M/M/1 puede extraerse
- Independiente del flujo crítico

---

### **8️⃣ NOTIFICATION SERVICE (BAJA PRIORIDAD)**

**Responsabilidad**: Notificaciones en tiempo real, eventos

**Modelos asociados**:
- `Notification` (en productos)
- `NotificationRead`

**Vistas**:
- Mostrar notificaciones, marcar como leída

**APIs que expondría**:
- `POST /notifications` - Crear notificación (evento interno)
- `GET /notifications` - Notificaciones del usuario
- `POST /notifications/<id>/read` - Marcar como leída
- `DELETE /notifications/<id>` - Eliminar notificación
- `GET /notifications/unread` - Contar no leídas (badge)
- `WS /notifications/subscribe` - WebSocket para push en tiempo real

**Dependencias con otros servicios**:
- **Product Service**: Emite eventos de cambios de stock
- **Order Service**: Emite eventos de cambios de estado
- **Auth Service**: Usuario propietario de notificaciones

**Base de datos propia**: ✅ **SÍ** (o servicios otros)
- Tabla `productos_notification`
- Tabla `productos_notificationread`

**Complejidad de extracción**: ⭐ (BAJA)
- Modelo simple
- Podría usar event bus (RabbitMQ/Kafka)
- Totalmente independiente

---

### **9️⃣ PROMOTION SERVICE (BAJA PRIORIDAD)**

**Responsabilidad**: Promociones, cupones, descuentos

**Modelos asociados**:
- `Promotion`
- `Cupon`

**Vistas**:
- Listar promociones, validar/canjear cupones

**APIs que expondría**:
- `GET /promotions` - Listar promociones activas
- `POST /promotions` - Crear promoción (admin)
- `PUT /promotions/<id>` - Editar promoción
- `POST /promotions/<id>/approve` - Aprobar promoción
- `GET /coupons` - Listar cupones disponibles
- `POST /coupons/validate` - Validar código de cupón
- `POST /coupons/redeem` - Canjear cupón

**Dependencias con otros servicios**:
- **Product Service**: Lectura de productos asociados
- **Auth Service**: Usuario que crea/usa promoción
- **Payment Service**: Aplica descuento en checkout

**Base de datos propia**: ✅ **SÍ**
- Tabla `productos_promotion`
- Tabla `productos_cupon`

**Complejidad de extracción**: ⭐⭐ (BAJA-MEDIA)
- Lógica de negocio simple
- Relaciones claras
- Podría abstraerse fácilmente

---

## ❌ COMPONENTES QUE NO DEBERÍAN SEPARARSE

### **1. `roles` ← Mantener en Auth Service**
**Razón**: 
- Modelo simple (solo nombre, choices de strings)
- Todos los servicios necesitan consultar roles
- Bajo valor de extraer en servicio independiente
- **Mejor solución**: Constantes/enum en Auth Service

### **2. `core` ← Integrar con Frontend o Auth**
**Razón**:
- Solo renderiza páginas públicas
- Lee datos de múltiples servicios (Vista de lectura)
- No tiene lógica de negocio compleja
- **Mejor solución**: Frontend que consume APIs de servicios

### **3. `admin` (panel administrativo) ← Backend flexible**
**Razón**:
- Accede a todos los servicios
- No es un servicio independiente, es interfaz
- **Mejor solución**: Admin único (BFF - Backend for Frontend) que orquesta llamadas a microservicios

### **4. Sincronización `usuarios.User ↔ auth.User` ← Simplificar, NO separar**
**Razón**:
- Complejidad innecesaria
- En arquitectura de microservicios, usar SOLO JWT tokens
- **Mejor solución**: Migrar a tablaa única en Auth Service

### **5. `Inventario` ← Mantener en Product Service**
**Razón**:
- Es parte de la lógica de stock
- Tight coupling con Producto
- Mejor que sea transacción atómica
- **Mejor solución**: Tabla de auditoría/changelog en Product Service

---

## 🏛️ ARQUITECTURA DE MICROSERVICIOS PROPUESTA

### **Visión General de Servicios**

```
                            ┌─────────────────────────────────────────┐
                            │         API GATEWAY                     │
                            │  (Kong, AWS API Gateway, o Nginx)       │
                            └────────────────┬────────────────────────┘
                                             │
                 ┌───────────────────────────┼────────────────────────────────┐
                 │                           │                                │
         ┌───────▼────────┐        ┌────────▼────────┐        ┌─────────▼────────┐
         │ AUTH SERVICE   │        │ PRODUCT SERVICE │        │ PAYMENT SERVICE  │
         │ (Node.js/Py)   │        │ (Django REST)   │        │ (Django/FastAPI) │
         └────────────────┘        └─────────────────┘        └──────────────────┘
                 │                           │                          │
        ┌────────┴────────┐        ┌────────┴────────┐       ┌─────────┴──────────┐
        │   usuarios_db   │        │  productos_db   │       │    pagos_db        │
        │    (MySQL)      │        │    (MySQL)      │       │    (MySQL)         │
        └─────────────────┘        └─────────────────┘       └────────────────────┘
                                             │
                 ┌───────────────────────────┼────────────────────────────────┐
                 │                           │                                │
         ┌───────▼────────┐        ┌────────▼────────┐        ┌─────────▼────────┐
         │ CART SERVICE   │        │ ORDER SERVICE   │        │ DELIVERY SERVICE │
         │ (FastAPI)      │        │ (Django REST)   │        │ (FastAPI)        │
         └────────────────┘        └─────────────────┘        └──────────────────┘
                 │                           │                          │
        ┌────────┴────────┐        ┌────────┴────────┐       ┌─────────┴──────────┐
        │  carrito_db     │        │  ventas_db      │       │   delivery_db      │
        │   (MySQL)       │        │   (MySQL)       │       │    (MySQL)         │
        └─────────────────┘        └─────────────────┘       └────────────────────┘
                 │                           │
         ┌───────┴────────┐        ┌────────┴────────┐
         │ CHAT SERVICE   │        │EVENT BUS/QUEUE │
         │ (FastAPI)      │        │ (RabbitMQ/Kafka)
         └────────────────┘        └──────┬──────────┘
                 │                         │
        ┌────────┴────────┐        ┌───────▼───────────┐
        │   chat_db       │        │ NOTIFICATION SVC  │
        │   (MySQL)       │        │ (FastAPI)         │
        └─────────────────┘        └────────────────────┘
                                           │
                                  ┌────────▼────────┐
                                  │   notif_db      │
                                  │   (Redis/MySQL) │
                                  └─────────────────┘
                 
         ┌──────────────────────────────────────────────────────┐
         │            PROMOTION SERVICE (OPCIONAL)              │
         │            (FastAPI)                                 │
         ├──────────────────────────────────────────────────────┤
         │  promo_db (MySQL)                                    │
         └──────────────────────────────────────────────────────┘

         ┌──────────────────────────────────────────────────────┐
         │     SHARED SERVICES / INFRASTRUCTURE                 │
         ├──────────────────────────────────────────────────────┤
         │ - Email Service (SMTP / SendGrid)                    │
         │ - Logging Service (ELK Stack / Datadog)              │
         │ - Configuration Service (Consul / Etcd)              │
         │ - Service Discovery (Consul / Kubernetes)            │
         │ - Tracing (Jaeger / Zipkin)                          │
         └──────────────────────────────────────────────────────┘

         ┌──────────────────────────────────────────────────────┐
         │         EXTERNAL INTEGRATIONS                        │
         ├──────────────────────────────────────────────────────┤
         │ - Stripe API (Payments)                              │
         │ - Google Gemini 2.5 Flash (Chat)                     │
         │ - Email Provider (SendGrid / Gmail)                  │
         └──────────────────────────────────────────────────────┘
```

### **Responsabilidades por Servicio**

#### **🔐 AUTH SERVICE**
```yaml
Responsabilidad: Autenticación, autorización, gestión de usuarios

Endpoints:
  POST   /api/v1/auth/register          # Registrar usuario
  POST   /api/v1/auth/login             # Login (devuelve JWT)
  POST   /api/v1/auth/logout            # Logout
  POST   /api/v1/auth/refresh           # Renovar JWT
  GET    /api/v1/auth/me                # Info del usuario actual
  PUT    /api/v1/auth/profile           # Actualizar perfil
  POST   /api/v1/auth/change-password   # Cambiar contraseña
  POST   /api/v1/auth/recover-password  # Iniciar recuperación
  POST   /api/v1/auth/verify-token      # Validar JWT (usado por Gateway)

Database:
  - usuarios (usuarios, roles)
  - Eliminar tabla auth_user (simplificar)

Integraciones:
  - Email Service (recuperación de contraseña)
  - Event Bus (emite: user.registered, user.updated, user.deleted)

Comunicación:
  - Recibe JWT en headers (Authorization: Bearer <token>)
  - Genera y valida JWT (RS256)
```

#### **📦 PRODUCT SERVICE**
```yaml
Responsabilidad: Productos, categorías, inventario, notificaciones

Endpoints:
  GET    /api/v1/products               # Listar (filtro: categoria, búsqueda, precio)
  GET    /api/v1/products/<id>          # Detalle
  GET    /api/v1/products/<id>/stock    # Stock actual (JSON)
  POST   /api/v1/products               # Crear (admin)
  PUT    /api/v1/products/<id>          # Actualizar (admin)
  DELETE /api/v1/products/<id>          # Eliminar (admin)
  
  GET    /api/v1/categories             # Listar categorías
  POST   /api/v1/categories             # Crear (admin)
  
  GET    /api/v1/inventory              # Historial
  POST   /api/v1/inventory/entrada      # Registrar entrada
  POST   /api/v1/inventory/salida       # Registrar salida
  
  GET    /api/v1/notifications          # Notificaciones del usuario
  POST   /api/v1/notifications/<id>/read # Marcar leída

Database:
  - productos_producto
  - productos_categoria
  - productos_inventario
  - productos_notification
  - productos_notificationread

Integraciones:
  - Event Bus (emite: product.created, product.updated, stock.changed)
  - Escucha eventos: payment.succeeded (para reducir stock)

Comunicación:
  - JWT validation via API Gateway
  - Llamadas internas: /api/v1/internal/products/<id>/reduce-stock
```

#### **💳 PAYMENT SERVICE**
```yaml
Responsabilidad: Pagos, Stripe, transacciones

Endpoints:
  POST   /api/v1/payments/checkout-session    # Crear sesión Stripe
  GET    /api/v1/payments/<session_id>        # Estado
  GET    /api/v1/payments/<session_id>/receipt # Recibo PDF
  POST   /api/v1/payments/webhook             # Webhook Stripe
  POST   /api/v1/payments/<id>/retry          # Reintentar
  GET    /api/v1/payments/history             # Historial usuario

Database:
  - pagos_payment
  - transacciones_log (auditoría)

Integraciones:
  - Stripe API (webhooks, checkout sessions)
  - Order Service (crea orden)
  - Product Service (reduce stock)
  - Notification Service (notifica estado)
  - Email Service (confirmación de pago)
  - Event Bus (emite: payment.created, payment.succeeded, payment.failed)

Critical:
  - Idempotency keys para webhooks
  - Transacciones distribuidas (Saga pattern)
  - Retry logic con exponential backoff
```

#### **🛒 CART SERVICE**
```yaml
Responsabilidad: Carrito de compras

Endpoints:
  GET    /api/v1/cart                   # Obtener carrito
  POST   /api/v1/cart/items             # Agregar item
  PUT    /api/v1/cart/items/<id>        # Actualizar cantidad
  DELETE /api/v1/cart/items/<id>        # Eliminar item
  DELETE /api/v1/cart                   # Vaciar

Database:
  - carrito_carrito
  - carrito_carritoitem

Integraciones:
  - Product Service (lee precios/stock)
  - Auth Service (usuario)
  - Payment Service (checkout)

Comunicación:
  - JWT validation via API Gateway
```

#### **📋 ORDER SERVICE**
```yaml
Responsabilidad: Órdenes/ventas, estados

Endpoints:
  POST   /api/v1/orders                 # Crear (solo Payment Service)
  GET    /api/v1/orders/<id>            # Detalle
  GET    /api/v1/orders                 # Historial usuario
  PUT    /api/v1/orders/<id>/status     # Cambiar estado
  DELETE /api/v1/orders/<id>            # Cancelar
  GET    /api/v1/orders/stats           # Estadísticas (admin)

Database:
  - ventas_venta
  - ventas_ventadetalle

Integraciones:
  - Payment Service (crea orden)
  - Product Service (detalles de productos)
  - Delivery Service (entrega)
  - Notification Service (cambios de estado)
  - Event Bus (emite: order.created, order.updated, order.cancelled)

Critical:
  - Estados bien definidos
  - Validación de transición de estados
```

#### **🚚 DELIVERY SERVICE**
```yaml
Responsabilidad: Entregas

Endpoints:
  POST   /api/v1/deliveries             # Crear
  GET    /api/v1/deliveries/<id>        # Estado
  PUT    /api/v1/deliveries/<id>        # Actualizar (en_ruta, entregado)
  GET    /api/v1/deliveries?driver=<id> # Entregas asignadas
  GET    /api/v1/deliveries/<id>/tracking # Historial

Database:
  - delivery_delivery

Integraciones:
  - Order Service (lee orden)
  - Auth Service (repartidor)
  - Notification Service (notificaciones de estado)
  - Event Bus (emite: delivery.created, delivery.updated, delivery.completed)
```

#### **💬 CHAT SERVICE**
```yaml
Responsabilidad: Chat en tiempo real

Endpoints:
  POST   /api/v1/chat/messages          # Enviar mensaje
  GET    /api/v1/chat                   # Historial
  GET    /api/v1/chat/widget            # Widget (HTML)
  POST   /api/v1/chat/<id>/close        # Cerrar chat
  GET    /api/v1/chat/stats             # Estadísticas

WebSocket:
  WS     /ws/chat/<chat_id>             # Conexión en tiempo real

Database:
  - chat_chat
  - chat_mensajechat

Integraciones:
  - Product Service (recomendaciones)
  - Order Service (info de órdenes)
  - Gemini API (respuestas inteligentes)
  - Event Bus (emite: chat.started, chat.closed)

Critical:
  - Sistema M/M/1 (colas, prioridades)
  - WebSocket para tiempo real
```

#### **🔔 NOTIFICATION SERVICE**
```yaml
Responsabilidad: Notificaciones

Endpoints:
  POST   /api/v1/notifications          # Crear (interno)
  GET    /api/v1/notifications          # Listar
  POST   /api/v1/notifications/<id>/read # Marcar leída
  DELETE /api/v1/notifications/<id>     # Eliminar
  GET    /api/v1/notifications/unread   # Contar no leídas

WebSocket:
  WS     /ws/notifications              # Push en tiempo real

Database:
  - notificaciones (puede ser Redis o MySQL)

Integraciones:
  - Product Service (escucha: stock.changed)
  - Order Service (escucha: order.updated)
  - Payment Service (escucha: payment.succeeded)
  - Event Bus (suscriptor)

Critical:
  - Push en tiempo real vía WebSocket
  - Event-driven
```

---

## 📊 TABLA DE MIGRACIÓN

| # | Componente Actual | Microservicio Propuesto | Complejidad | Riesgo | Recomendación | Notas |
|---|---|---|---|---|---|---|
| 1 | `usuarios/` | **AUTH SERVICE** | Media | Bajo | ✅ **EXTRAER PRIMERO** | Backend custom → JWT. Remover sincronización auth.User |
| 2 | `productos/` | **PRODUCT SERVICE** | Alta | Medio | ✅ **EXTRAER SEGUNDO** | Signals → Event Bus. Stock crítico. Tight coupling con pagos |
| 3 | `pagos/` | **PAYMENT SERVICE** | Muy Alta | Alto | ⚠️ **EXTRAER CON CUIDADO** | Requiere Saga pattern. Webhook sincronización perfecta. Idempotency keys |
| 4 | `carrito/` | **CART SERVICE** | Baja | Bajo | ✅ **EXTRAER TERCERO** | Modelo simple. Independiente. Bajo riesgo |
| 5 | `ventas/` | **ORDER SERVICE** | Media | Bajo | ✅ **EXTRAER CUARTO** | Después de Payment. Validar transacciones distribuidas |
| 6 | `delivery/` | **DELIVERY SERVICE** | Baja | Bajo | ✅ **EXTRAER QUINTO** | OneToOne simple. No crítico. Bajo riesgo |
| 7 | `chat/` | **CHAT SERVICE** | Media | Bajo | ✅ **EXTRAER SEXTO** | Gemini abstracción limpia. M/M/1 encapsulado |
| 8 | `productos/Notification` | **NOTIFICATION SERVICE** | Baja | Bajo | ⚠️ **OPCIONAL** | Puede quedar en Product Service inicialmente |
| 9 | `productos/Promotion` | **PROMOTION SERVICE** | Baja | Bajo | ⚠️ **OPCIONAL** | Puede quedar en Product Service inicialmente |
| 10 | `core/` | **FRONTEND / BFF** | Baja | Bajo | ✅ **MIGRAR A FRONTEND** | Convertir en SPA que consume APIs |
| 11 | `roles/` | **Constants en AUTH** | Muy Baja | Nada | ✅ **NO SEPARAR** | Enum/choices, no servicio |
| 12 | Panel Admin | **Admin BFF** | Media | Bajo | ✅ **CREAR NUEVO** | Backend for Frontend que orquesta llamadas |

### **Orden Recomendado de Extracción**

```
FASE 1 - FUNDAMENTOS (Semana 1-2)
├── 1. AUTH SERVICE ← Infraestructura base
└── Setup: Event Bus (RabbitMQ/Kafka), API Gateway

FASE 2 - CORE (Semana 3-4)
├── 2. PRODUCT SERVICE ← Con Event Bus
├── 3. PAYMENT SERVICE ← Con Saga pattern
└── 4. CART SERVICE ← Sencillo

FASE 3 - TRANSACCIONES (Semana 5-6)
├── 5. ORDER SERVICE ← Integración Payment + Product
└── Validar transacciones distribuidas

FASE 4 - COMPLEMENTARIOS (Semana 7-8)
├── 6. DELIVERY SERVICE
├── 7. CHAT SERVICE
└── 8. NOTIFICATION SERVICE (opcional)

FASE 5 - FRONT-END (Semana 9+)
├── Migrar core/ a SPA (React/Vue)
├── Crear Admin BFF
└── API Gateway configuration
```

---

## 🔗 MATRIZ DE DEPENDENCIAS

### **Grafo de Dependencias Críticas**

```
┌─────────────────────────────────────┐
│      PAYMENT SERVICE (CRÍTICO)      │
├─────────────────────────────────────┤
│ ↓ Crea orden en ORDER SERVICE       │
│ ↓ Reduce stock en PRODUCT SERVICE   │
│ ↓ Notifica NOTIFICATION SERVICE     │
│ ↓ Valida JWT con AUTH SERVICE       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      ORDER SERVICE (CRÍTICO)        │
├─────────────────────────────────────┤
│ ↓ Lee productos de PRODUCT SERVICE  │
│ ↓ Crea delivery en DELIVERY SERVICE │
│ ↓ Notifica NOTIFICATION SERVICE     │
│ ↓ Valida JWT con AUTH SERVICE       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│     PRODUCT SERVICE (CRÍTICO)       │
├─────────────────────────────────────┤
│ ↓ Valida JWT con AUTH SERVICE       │
│ ↓ Recibe peticiones de PAYMENT      │
│ ↓ Recibe peticiones de CART         │
│ ↓ Emite eventos a EVENT BUS         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      AUTH SERVICE (INFRAESTRUCTURA) │
├─────────────────────────────────────┤
│ ← Todos los servicios validan aquí  │
│ ← API Gateway valida aquí           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      CART SERVICE (INDEPENDIENTE)   │
├─────────────────────────────────────┤
│ ↓ Lee precios de PRODUCT SERVICE    │
│ ↓ Redirige a PAYMENT SERVICE        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   CHAT/NOTIFICATION (INDEPENDIENTES)│
├─────────────────────────────────────┤
│ Suscriptores de EVENT BUS           │
│ No bloquean flujo crítico            │
└─────────────────────────────────────┘
```

### **Tabla de Dependencias Detallada**

| Servicio | Depende De | Tipo | Sincrónico | Crítico |
|----------|-----------|------|-----------|---------|
| PAYMENT | ORDER | Llamada | ✅ Sí | 🔴 CRÍTICO |
| PAYMENT | PRODUCT | Llamada | ✅ Sí | 🔴 CRÍTICO |
| PAYMENT | AUTH | JWT | ✅ Sí | 🔴 CRÍTICO |
| PAYMENT | NOTIFICATION | Evento | ❌ Async | 🟡 Importante |
| ORDER | PRODUCT | Llamada | ✅ Sí | 🔴 CRÍTICO |
| ORDER | DELIVERY | Llamada | ✅ Sí | 🟡 Importante |
| ORDER | NOTIFICATION | Evento | ❌ Async | 🟡 Importante |
| ORDER | AUTH | JWT | ✅ Sí | 🔴 CRÍTICO |
| PRODUCT | AUTH | JWT | ✅ Sí | 🔴 CRÍTICO |
| PRODUCT | EVENT BUS | Evento | ❌ Async | 🟡 Importante |
| CART | PRODUCT | Llamada | ✅ Sí | 🟡 Importante |
| CART | PAYMENT | Redirección | ✅ Sí | 🔴 CRÍTICO |
| CART | AUTH | JWT | ✅ Sí | 🔴 CRÍTICO |
| CHAT | PRODUCT | Llamada | ✅ Sí | 🟢 Bajo |
| CHAT | ORDER | Llamada | ✅ Sí | 🟢 Bajo |
| CHAT | GEMINI API | Llamada | ✅ Sí | 🟡 Importante |
| DELIVERY | ORDER | Llamada | ✅ Sí | 🟡 Importante |
| NOTIFICATION | EVENT BUS | Evento | ❌ Async | 🟡 Importante |

**Leyenda**:
- 🔴 **CRÍTICO**: Si falla, impacta flujo principal de compra
- 🟡 **IMPORTANTE**: Si falla, degrada experiencia pero no bloquea compra
- 🟢 **BAJO**: Si falla, no afecta funcionalidades principales

---

## 🏛️ ARQUITECTURA RECOMENDADA FINAL

### **Componentes Principales**

```
┌────────────────────────────────────────────────────────────────────────┐
│                         CLIENTE / FRONTEND                             │
│              (React SPA, Angular, Vue en puerto 3000)                  │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ HTTPS
                            ↓
        ┌───────────────────────────────────────────────────┐
        │           API GATEWAY & LOAD BALANCER             │
        │  (Kong, AWS API Gateway, Nginx, o Traefik)       │
        │                                                   │
        │  - JWT validation & caching                       │
        │  - Rate limiting (100 req/min per user)           │
        │  - Request routing & load balancing               │
        │  - CORS, security headers                         │
        │  - Request/Response logging                       │
        │  - Service discovery                              │
        └──────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────────────────────────────────────────┐
        │                                                         │
        ↓                                                         ↓
    ┌─────────────────────────────────┐      ┌──────────────────────────────┐
    │       AUTH SERVICE              │      │    PRODUCT SERVICE           │
    │  Port: 8001 (FastAPI/Django)    │      │  Port: 8002 (Django REST)    │
    │                                 │      │                              │
    │  - register, login, refresh     │      │  - List, detail, filter      │
    │  - JWT generation (RS256)       │      │  - Create, update, delete    │
    │  - Password recovery            │      │  - Stock management          │
    │  - Token validation (internal)  │      │  - Categories                │
    │  - User profile                 │      │  - Notifications             │
    │                                 │      │  - Event emission            │
    └──────────┬──────────────────────┘      └──────────┬───────────────────┘
               │                                          │
               └──────────────────┬───────────────────────┘
                                  │
    ┌─────────────────────────────────┐      ┌──────────────────────────────┐
    │       PAYMENT SERVICE           │      │      CART SERVICE            │
    │  Port: 8003 (FastAPI/Django)    │      │  Port: 8004 (FastAPI)        │
    │                                 │      │                              │
    │  - Stripe integration           │      │  - Add/remove items          │
    │  - Checkout sessions            │      │  - Quantity updates          │
    │  - Payment confirmation         │      │  - Cart persistence          │
    │  - Webhook processing           │      │  - Checkout redirect         │
    │  - Receipt generation           │      │                              │
    │  - Idempotency handling         │      │                              │
    │  - Saga orchestration           │      │                              │
    └──────────┬──────────────────────┘      └──────────┬───────────────────┘
               │                                          │
               └──────────────────┬───────────────────────┘
                                  │
    ┌─────────────────────────────────┐      ┌──────────────────────────────┐
    │       ORDER SERVICE             │      │    DELIVERY SERVICE          │
    │  Port: 8005 (Django REST)       │      │  Port: 8006 (FastAPI)        │
    │                                 │      │                              │
    │  - Create orders (from payment) │      │  - Create deliveries         │
    │  - Order history                │      │  - Assign drivers            │
    │  - Status management            │      │  - Track status              │
    │  - Order details                │      │  - Delivery confirmation     │
    │  - Reporting                    │      │                              │
    │  - Event emission               │      │                              │
    └──────────┬──────────────────────┘      └──────────┬───────────────────┘
               │                                          │
               └──────────────────┬───────────────────────┘
                                  │
    ┌─────────────────────────────────┐      ┌──────────────────────────────┐
    │       CHAT SERVICE              │      │ NOTIFICATION SERVICE         │
    │  Port: 8007 (FastAPI)           │      │  Port: 8008 (FastAPI)        │
    │                                 │      │                              │
    │  - WebSocket connection         │      │  - Subscribe to events       │
    │  - Message persistence          │      │  - Push notifications        │
    │  - Gemini integration           │      │  - WebSocket push            │
    │  - Queue M/M/1 system           │      │  - Email notifications       │
    │  - Intent detection             │      │  - SMS integration (future)  │
    │                                 │      │                              │
    └──────────┬──────────────────────┘      └──────────┬───────────────────┘
               │                                          │
               └──────────────────┬───────────────────────┘
                                  │
                                  ↓
                ┌────────────────────────────────────────┐
                │      EVENT BUS / MESSAGE QUEUE         │
                │    (RabbitMQ o Apache Kafka)           │
                │                                        │
                │  Topics/Exchanges:                     │
                │  - user.* (registered, updated, ...)  │
                │  - product.* (created, stock, ...)    │
                │  - order.* (created, updated, ...)    │
                │  - payment.* (created, succeeded, ...) │
                │  - delivery.* (created, updated, ...)  │
                │  - notification.* events               │
                └────────────────────────────────────────┘
                                  │
                ┌─────────────────┴─────────────────┐
                │     SUBSCRIBER SERVICES           │
                │                                   │
                │  - Notification Service           │
                │  - Analytics Service              │
                │  - Search Indexing (ES)           │
                │  - Caching invalidation (Redis)   │
                └───────────────────────────────────┘

        ┌──────────────────────────────────────────────────────┐
        │          SHARED INFRASTRUCTURE                       │
        ├──────────────────────────────────────────────────────┤
        │                                                      │
        │  📦 DATABASES                                        │
        │  ├─ MySQL 8.0 (Primary - Replication)              │
        │  │  ├─ usuarios (auth)                             │
        │  │  ├─ productos (product)                         │
        │  │  ├─ pagos (payment)                             │
        │  │  ├─ ventas (order)                              │
        │  │  ├─ carrito (cart)                              │
        │  │  ├─ delivery (delivery)                         │
        │  │  ├─ chat (chat)                                 │
        │  │  └─ notifications                               │
        │  │                                                  │
        │  └─ Redis (Cache + Session)                        │
        │     ├─ JWT token blacklist                         │
        │     ├─ Rate limiting                               │
        │     ├─ Cart (session)                              │
        │     └─ Notification cache                          │
        │                                                      │
        │  🔐 AUTHENTICATION                                  │
        │  ├─ JWT (RS256) - generated by AUTH SERVICE        │
        │  ├─ Token validation in API GATEWAY                │
        │  └─ Refresh token rotation                         │
        │                                                      │
        │  📊 MONITORING & LOGGING                           │
        │  ├─ ELK Stack (Elasticsearch, Logstash, Kibana)   │
        │  ├─ Prometheus (metrics)                           │
        │  ├─ Grafana (dashboards)                           │
        │  ├─ Jaeger (distributed tracing)                   │
        │  └─ CloudWatch (AWS logs)                          │
        │                                                      │
        │  🔧 INFRASTRUCTURE                                  │
        │  ├─ Docker & Docker Compose (dev)                  │
        │  ├─ Kubernetes (prod) - optional                   │
        │  ├─ GitLab CI/CD (pipeline)                        │
        │  └─ Consul/Etcd (service discovery)                │
        │                                                      │
        │  📧 EXTERNAL SERVICES                              │
        │  ├─ Stripe API (payments)                          │
        │  ├─ Google Gemini 2.5 Flash (AI chat)             │
        │  ├─ SendGrid (email)                               │
        │  └─ Twilio (SMS) - optional                        │
        │                                                      │
        └──────────────────────────────────────────────────────┘
```

### **Comunicación Entre Servicios**

#### **Síncrona (HTTP REST)**
```
CLIENT → API GATEWAY → [AUTH, PRODUCT, PAYMENT, ORDER, CART, DELIVERY, CHAT]
                         ↓ (interno)
                      Validación JWT en cada servicio
                      
PAYMENT → ORDER (crea venta)
PAYMENT → PRODUCT (reduce stock)
ORDER → PRODUCT (lee detalles)
ORDER → DELIVERY (crea entrega)
CART → PRODUCT (lee precios)
CHAT → PRODUCT (recomendaciones)
CHAT → ORDER (info de órdenes)
```

#### **Asíncrona (Event Bus)**
```
PRODUCT emite stock.changed
  ↓ Escucha: NOTIFICATION SERVICE
    
PAYMENT emite payment.succeeded
  ↓ Escucha: ORDER SERVICE, NOTIFICATION SERVICE, ANALYTICS

ORDER emite order.created, order.updated
  ↓ Escucha: NOTIFICATION SERVICE, ANALYTICS, REPORTING

DELIVERY emite delivery.updated
  ↓ Escucha: NOTIFICATION SERVICE, ANALYTICS
```

---

## 📈 PLAN DE MIGRACIÓN PASO A PASO

### **FASE 0: PREPARACIÓN (1 SEMANA)**

#### **0.1 Setup Infrastructure**
```bash
# Iniciar servicios base
docker-compose up -d mysql redis rabbitmq

# Crear bases de datos
mysql -u root -p
  CREATE DATABASE auth_db;
  CREATE DATABASE product_db;
  CREATE DATABASE payment_db;
  CREATE DATABASE order_db;
  CREATE DATABASE cart_db;
  CREATE DATABASE delivery_db;
  CREATE DATABASE chat_db;
```

#### **0.2 Crear Repositorios**
```
GitHub Repos:
├─ adonai-auth-service (FastAPI)
├─ adonai-product-service (Django REST)
├─ adonai-payment-service (Django)
├─ adonai-order-service (Django REST)
├─ adonai-cart-service (FastAPI)
├─ adonai-delivery-service (FastAPI)
├─ adonai-chat-service (FastAPI)
├─ adonai-api-gateway (Kong/Nginx)
└─ adonai-frontend (React)
```

#### **0.3 Setup API Gateway (Kong)**
```yaml
# kong.yml configuración
services:
  auth-service:
    host: auth-service
    port: 8001
  product-service:
    host: product-service
    port: 8002
  # ... demás servicios
```

---

### **FASE 1: EXTRAER AUTH SERVICE (SEMANA 1-2)**

#### **1.1 Crear Nuevo Proyecto FastAPI**
```bash
mkdir adonai-auth-service
cd adonai-auth-service

# Estructura
auth_service/
├── main.py
├── config.py
├── models.py
├── schemas.py
├── routers/
│   ├── auth.py
│   ├── users.py
│   └── tokens.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   └── token_service.py
├── middleware/
│   └── jwt_validation.py
├── dependencies.py
├── requirements.txt
└── docker/
    └── Dockerfile
```

#### **1.2 Implementar JWT Token System**
```python
# Cambio importante: De email/password → JWT
# Token contiene:
# {
#   "sub": "usuario_id",
#   "email": "user@example.com",
#   "role": "Cliente",
#   "exp": timestamp,
#   "iat": timestamp
# }
```

#### **1.3 Crear Endpoint POST /auth/login**
```python
# Respuesta
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### **1.4 API Gateway Configuration**
```
Ruta: /api/v1/auth/login
  → Kong valida formato JSON
  → Kong redirige a auth-service:8001/login
  → Auth Service responde JWT
  → Kong cachea token en Redis (opcional)
```

#### **1.5 Migrar Datos**
```bash
# Script de migración
python migrate_usuarios_to_auth_db.py
  - Copia tabla usuarios
  - Hash passwords con bcrypt
  - Elimina sincronización auth.User
```

#### **1.6 Tests en Auth Service**
```bash
pytest tests/test_auth_service.py
  - Test register
  - Test login
  - Test JWT validation
  - Test token refresh
  - Test password recovery
```

---

### **FASE 2: EXTRAER PRODUCT SERVICE (SEMANA 3-4)**

#### **2.1 Crear Product Service con Django REST Framework**
```
product_service/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── signals.py
├── categories/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── inventory/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── notifications/
│   ├── models.py
│   └── views.py
└── docker/
    └── Dockerfile
```

#### **2.2 Implementar Event Bus Integration**
```python
# signals.py - En lugar de crear directamente, emitir evento
from product_service.events import emit_event

@receiver(post_save, sender=Producto)
def product_created(sender, instance, created, **kwargs):
    if created:
        emit_event('product.created', {
            'product_id': instance.id,
            'name': instance.nombre,
            'stock': instance.stock_actual
        })
```

#### **2.3 Crear Event Publisher**
```python
# events.py
import pika

def emit_event(event_type: str, data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange='adonai', exchange_type='topic')
    channel.basic_publish(
        exchange='adonai',
        routing_key=event_type,
        body=json.dumps(data)
    )
```

#### **2.4 Implementar Internal API**
```python
# views.py - Endpoint para Payment Service
@api_view(['POST'])
@permission_classes([IsInternal])  # Validar token interno
def reduce_stock(request, product_id):
    """
    Llamada desde Payment Service al procesar pago
    """
    quantity = request.data['quantity']
    product = Product.objects.get(id=product_id)
    product.stock_actual -= quantity
    product.save()
    return Response({'success': True})
```

#### **2.5 Migrar Datos de Productos**
```bash
# Script SQL
mysqldump -u root old_adonai productos > productos_export.sql
mysql -u root product_db < productos_export.sql

# Actualizar IDs de foreign keys si es necesario
```

#### **2.6 Tests**
```bash
pytest tests/test_products.py
  - Test list/filter products
  - Test create product
  - Test stock reduction
  - Test notifications
  - Test event emission
```

---

### **FASE 3: EXTRAER PAYMENT SERVICE (SEMANA 5-6) ⚠️ CRÍTICA**

#### **3.1 Crear Payment Service**
```
payment_service/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── payments/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── stripe_handler.py
│   └── saga.py
├── webhooks/
│   ├── stripe_webhooks.py
│   └── handlers.py
└── docker/
    └── Dockerfile
```

#### **3.2 Implementar Saga Pattern**
```python
# saga.py - Manejar transacción distribuida
class PaymentSaga:
    def execute(self, cart_items, user_id, amount):
        try:
            # Paso 1: Crear sesión Stripe
            stripe_session = self.create_stripe_session(...)
            
            # Paso 2: Esperar webhook de Stripe
            # (async callback)
            
            # En webhook:
            # Paso 3: Crear Venta en Order Service
            order = self.order_service.create_order(...)
            
            # Paso 4: Reducir Stock en Product Service
            self.product_service.reduce_stock(...)
            
            # Paso 5: Crear notificaciones
            self.notify(...)
            
        except Exception as e:
            # Compensating transaction
            self.rollback(stripe_session.id)
```

#### **3.3 Webhook Seguro**
```python
# stripe_webhooks.py
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        handle_payment_success(event['data']['object'])
    
    return JsonResponse({'success': True})
```

#### **3.4 Idempotency Keys**
```python
# Stripe maneja idempotency natively, pero asegurarse:
@idempotent_key('stripe_session_{cart_hash}')
def create_checkout_session(cart_items):
    return stripe.checkout.Session.create(
        idempotency_key=idempotency_key,
        ...
    )
```

#### **3.5 Circuit Breaker para Llamadas a Otros Servicios**
```python
from pybreaker import CircuitBreaker

order_service_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=60
)

def create_order_safe(order_data):
    try:
        return order_service_breaker.call(
            order_service.create_order,
            order_data
        )
    except CircuitBreakerListener:
        # Reintentar más tarde o fallar
        log_payment_pending(order_data)
```

#### **3.6 Tests Críticos**
```bash
pytest tests/test_payments.py -v
  - Test checkout session creation
  - Test webhook processing (success)
  - Test webhook processing (failure)
  - Test idempotency (webhook duplicate)
  - Test payment confirmation
  - Test rollback scenario
  - Test circuit breaker
```

---

### **FASE 4: EXTRAER CART, ORDER, DELIVERY (SEMANA 7-8)**

#### **4.1 Cart Service (FastAPI)**
```bash
# Estructura similar a payment
cart_service/
├── main.py
├── models/
├── schemas/
├── routers/
│   └── cart.py
├── services/
│   └── cart_service.py
└── dependencies.py
```

#### **4.2 Order Service**
```bash
# Django REST
order_service/
├── orders/
│   ├── models.py (Venta, VentaDetalle)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── events.py (emit order.created, etc)
└── consumers.py (escucha payment.succeeded)
```

#### **4.3 Delivery Service**
```bash
# FastAPI
delivery_service/
├── deliveries/
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       └── deliveries.py
└── services/
    └── delivery_service.py
```

---

### **FASE 5: EXTRAER CHAT Y NOTIFICATIONS (SEMANA 9)**

#### **5.1 Chat Service con WebSocket**
```python
# FastAPI + WebSocket
from fastapi import WebSocket

@app.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            response = await gemini_service.get_response(data)
            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass
```

#### **5.2 Notification Service con Push**
```python
# WebSocket para notificaciones en tiempo real
@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket, user_id: int):
    await websocket.accept()
    # Suscribir a eventos de usuario
    event_bus.subscribe(f'user.{user_id}.*', websocket)
```

---

### **FASE 6: FRONTEND & ADMIN (SEMANA 10+)**

#### **6.1 Migrar a React SPA**
```bash
npx create-react-app adonai-frontend

src/
├── pages/
│   ├── login/
│   ├── products/
│   ├── cart/
│   ├── checkout/
│   └── dashboard/
├── services/
│   ├── authService.ts
│   ├── productService.ts
│   ├── paymentService.ts
│   └── apiClient.ts
├── components/
├── hooks/
│   ├── useAuth.ts
│   ├── useCart.ts
│   └── useFetch.ts
└── App.tsx
```

#### **6.2 API Client con JWT**
```typescript
// services/apiClient.ts
export const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_GATEWAY,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Refrescar token
      const refreshToken = localStorage.getItem('refresh_token');
      const newToken = await authService.refreshToken(refreshToken);
      localStorage.setItem('access_token', newToken);
      // Reintentar
      return apiClient(error.config);
    }
    return Promise.reject(error);
  }
);
```

#### **6.3 Admin BFF (Backend for Frontend)**
```python
# Admin BFF - Orquesta llamadas a múltiples servicios
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/admin/dashboard")
async def dashboard():
    """Obtiene datos de múltiples servicios para el dashboard"""
    sales_stats = await order_service.get_sales_stats()
    inventory = await product_service.get_inventory_summary()
    chat_stats = await chat_service.get_queue_stats()
    
    return {
        "sales": sales_stats,
        "inventory": inventory,
        "chat": chat_stats
    }
```

---

## ⚠️ CONSIDERACIONES TÉCNICAS

### **1. Manejo de Transacciones Distribuidas**

**Problema**: Un pago requiere crear Venta + reducir Stock. Si uno falla, el otro queda inconsistente.

**Soluciones**:

#### **A) Saga Pattern (RECOMENDADO)**
```python
class PaymentSaga:
    async def execute(self):
        # Transacción 1: Crear venta
        venta_id = await order_service.create_venta(...)
        
        # Transacción 2: Reducir stock
        try:
            await product_service.reduce_stock(...)
        except Exception:
            # Compensating transaction
            await order_service.cancel_venta(venta_id)
            raise
```

#### **B) Outbox Pattern**
```python
# En Payment Service
@transaction.atomic
def process_payment(payment):
    payment.status = 'succeeded'
    payment.save()
    
    # Guardar evento en tabla outbox (misma BD)
    Outbox.objects.create(
        event_type='payment.succeeded',
        payload=payment.to_dict()
    )

# Polling Service (asincrono)
def poll_outbox():
    for event in Outbox.objects.filter(published=False):
        publish_to_rabbitmq(event)
        event.published = True
        event.save()
```

#### **C) 2-Phase Commit (NO RECOMENDADO)**
- Complejidad muy alta
- Rendimiento pobre
- No escalable

### **2. Idempotencia**

**Problema**: Webhook de Stripe se reintenta. Si lo procesamos 2 veces, creamos 2 ventas.

**Solución**: Idempotency Key
```python
# Stripe webhook - debe ser idempotente
stripe_session_id = event['data']['object']['id']

# Verificar si ya fue procesado
if Payment.objects.filter(stripe_session_id=stripe_session_id).exists():
    return JsonResponse({'success': True})  # Ya procesado

# Procesar por primera vez
...
```

### **3. Circuit Breaker**

**Problema**: Si Order Service está caído, Payment Service falla.

**Solución**: Circuit Breaker Pattern
```python
from pybreaker import CircuitBreaker

order_breaker = CircuitBreaker(
    fail_max=5,        # Fallar después de 5 errores
    reset_timeout=60   # Reintentar después de 60 segundos
)

try:
    order_breaker.call(order_service.create_order, data)
except CircuitBreakerListener:
    # Log + alerta
    # Reintentar más tarde (store en BD con status pending)
```

### **4. Caching Strategy**

```
NIVEL 1: Redis Cache (24h)
  - Productos frecuentemente consultados
  - Categorías
  - Promociones activas

NIVEL 2: CDN (Cloudflare)
  - Imágenes de productos
  - Assets estáticos

NIVEL 3: Database Cache (Query Results)
  - Top 10 productos
  - Estadísticas diarias
  
Cache Invalidation:
  - Evento product.updated → invalidar redis
  - Evento stock.changed → invalidar cache de ese producto
```

### **5. Rate Limiting**

```
API Gateway (Kong):
  - 100 requests/minute per user
  - 1000 requests/minute per IP
  - 10 requests/second para payment endpoints

Stripe Webhook:
  - Validar signature siempre
  - Timeout: 30 segundos
  - Reintento automático por Stripe
```

### **6. Logging & Monitoring**

```
ELK Stack:
  - Logs centralizados
  - Agregación por servicio
  - Alertas en errores críticos
  
Prometheus:
  - Métricas de request duration
  - Error rates
  - Database query times
  
Jaeger:
  - Distributed tracing
  - Ver request a través de múltiples servicios
  - Detectar cuellos de botella
```

### **7. Database Migration Strategy**

```
Fase 1: Dual-write
  - Código escribe en AMBAS BDs (old + new)
  - Verificar consistencia
  - Duración: 1-2 semanas

Fase 2: Dual-read
  - Leer de nueva BD
  - Comparar con vieja
  - Duración: 1 semana

Fase 3: Cutover
  - Migración de datos históricos
  - Punto de no retorno
  - Rollback plan

Fase 4: Cleanup
  - Eliminar columnas viejas
  - Decommission vieja infraestructura
```

### **8. API Versioning**

```
URLs:
  /api/v1/products    ← v1 (monolito actual)
  /api/v2/products    ← v2 (microservicios)

Timeout Strategy:
  - Mantener v1 en paralelo 6 meses
  - Deprecation warnings en v1
  - Eliminar v1 después de migración completa
```

### **9. Secret Management**

```
NO hacer:
  ❌ Hardcodear STRIPE_SECRET_KEY
  ❌ Guardar en .env commiteado
  ❌ Pasar por variables de entorno simples

SÍ hacer:
  ✅ HashiCorp Vault
  ✅ AWS Secrets Manager
  ✅ Kubernetes Secrets (if using K8s)
  ✅ Environment variables + CI/CD secure

Rotación:
  - Stripe API keys: cada 3 meses
  - JWT signing keys: cada 6 meses
  - Database passwords: cada mes
```

### **10. Disaster Recovery**

```
RTO (Recovery Time Objective): 1 hora
RPO (Recovery Point Objective): 15 minutos

Backup Strategy:
  - Base de datos: Daily + replication
  - S3 backups: 30 días (cold storage)
  - Stripe metadata: Synced every 6 hours
  
Failover:
  - Load balancer automático
  - Database replica (standby)
  - Service mesh (Istio) para rerouting
```

---

## 📝 RESUMEN EJECUTIVO

### **Estado Actual**
- **Arquitectura**: Monolito Django (un solo proyecto)
- **Complejidad**: Media-Alta (9 apps integradas)
- **Acoplamiento**: Moderado-Alto (especialmente Payment ↔ Product)
- **Escalabilidad**: Limitada (single database, vertical scaling)

### **Recomendación**
✅ **SÍ proceder con migración a microservicios**, pero de forma incremental:

1. **Fase 1**: Auth Service (bajo riesgo, infraestructura base)
2. **Fase 2**: Product + Payment Services (core business logic)
3. **Fase 3**: Cart + Order (completar transacción)
4. **Fase 4**: Delivery + Chat (complementarios)
5. **Fase 5**: Frontend + Admin (presentación)

### **Beneficios Esperados**
- ✅ Escalabilidad independiente (Product Service puede tener 10 instancias, Auth solo 2)
- ✅ Despliegues independientes (cambios en Chat no afectan Payment)
- ✅ Equipos independientes (un equipo por servicio)
- ✅ Tecnologías diversas (Django REST para Order, FastAPI para Chat)
- ✅ Resilencia (si Chat falla, compras siguen funcionando)

### **Riesgos a Mitigar**
- ⚠️ **Complejidad operacional**: Requiere Docker, K8s, monitoring distribuido
- ⚠️ **Transacciones distribuidas**: Necesita Saga pattern bien implementado
- ⚠️ **Eventual consistency**: Los datos no son 100% consistentes en tiempo real
- ⚠️ **Debugging difícil**: Logs dispersos, hay que usar distributed tracing
- ⚠️ **Costo inicial alto**: Más infraestructura, más DevOps

### **Costo Estimado**
- **Desarrollo**: 12-16 semanas (3-4 meses)
- **Testing**: 4 semanas
- **Deployment**: 2 semanas
- **Stabilization**: 2 semanas
- **Total**: 5-6 meses

### **Equipo Necesario**
- 1 Backend Lead (arquitectura)
- 2-3 Backend Engineers (servicios)
- 1 DevOps Engineer (infraestructura, CI/CD)
- 1 QA Engineer (testing distribuido)
- 1 Frontend Engineer (SPA)

---

## 🎯 PRÓXIMOS PASOS

1. **Crear documento de decisión arquitectónica (ADR)**
   - Justificar migración a microservicios
   - Documentar trade-offs

2. **Setup de CI/CD pipeline**
   - GitHub Actions para cada servicio
   - Docker image building
   - Automated testing

3. **Implementar API Gateway**
   - Kong o Nginx
   - JWT validation
   - Rate limiting

4. **Comenzar Fase 1: Auth Service**
   - Crear repositorio
   - Implementar endpoints
   - Tests exhaustivos
   - Deployment a staging

5. **Monitoreo y observabilidad**
   - Setup ELK Stack
   - Setup Prometheus
   - Setup Jaeger

---

**Documento Generado**: 2026-06-11  
**Versión**: 1.0  
**Estado**: ✅ Análisis Completo - Listo para Revisión  
**Siguiente**: Esperar aprobación → Comenzar Implementación Fase 1
