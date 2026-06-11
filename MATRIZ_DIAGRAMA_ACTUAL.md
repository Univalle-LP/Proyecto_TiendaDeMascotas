# 🏗️ MATRIZ Y DIAGRAMA - ARQUITECTURA ACTUAL
## Adonai D'Empanadas - Estado Actual Completo

**Fecha**: 11 de junio, 2026  
**Status**: Análisis de Arquitectura Actual  
**Versión**: 1.0  
**⚠️ SIN MODIFICACIONES - SOLO ANÁLISIS**

---

## 📊 1. DIAGRAMA GENERAL DEL MONOLITO

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENTE / NAVEGADOR                          │
│                       (Frontend HTML/JS)                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    HTTPS/HTTP Requests
                             │
                             ▼
        ┌────────────────────────────────────────────────────┐
        │        DJANGO ADONAI (Monolito - Un proyecto)     │
        │                  Puerto: 8000                      │
        ├────────────────────────────────────────────────────┤
        │                                                    │
        │  APP: USUARIOS         (Autenticación)            │
        │  ├─ models.py: Usuario, Rol                      │
        │  ├─ views.py: login, register, perfil            │
        │  ├─ backends.py: Auth personalizado              │
        │  └─ urls.py: /usuarios/login, /usuarios/register │
        │                                                    │
        │  APP: PRODUCTOS        (Catálogo e Inventario)   │
        │  ├─ models.py: Producto, Categoria, Inventario   │
        │  ├─ views.py: catalogo, agregar_producto         │
        │  ├─ views_admin.py: CRUD completo                │
        │  ├─ signals.py: Auto-notificaciones              │
        │  └─ urls.py: /catalogo, /panel/inventario        │
        │                                                    │
        │  APP: CARRITO          (Carrito de Compras)       │
        │  ├─ models.py: Carrito, CarritoItem              │
        │  ├─ views.py: checkout                           │
        │  └─ urls.py: /carrito/checkout                   │
        │                                                    │
        │  APP: PAGOS            (Stripe Integration)       │
        │  ├─ models.py: Payment (legacy)                  │
        │  ├─ views.py: create_checkout_session            │
        │  ├─ stripe_webhook()                             │
        │  ├─ create_venta_from_stripe_session()           │
        │  └─ urls.py: /pago/*, /webhook/stripe            │
        │                                                    │
        │  APP: VENTAS           (Órdenes y Detalles)       │
        │  ├─ models.py: Venta, VentaDetalle               │
        │  ├─ views.py: historial_ventas                   │
        │  └─ urls.py: /historial                          │
        │                                                    │
        │  APP: DELIVERY         (Entregas)                 │
        │  ├─ models.py: Delivery (OneToOne con Venta)    │
        │  └─ views.py: delivery tracking                  │
        │                                                    │
        │  APP: CHAT             (Chat Inteligente)         │
        │  ├─ models.py: Chat, MensajeChat                 │
        │  ├─ views.py: chat_send (Gemini 2.5)            │
        │  ├─ Sistema M/M/1 (colas)                        │
        │  └─ urls.py: /chat/send, /chat/widget            │
        │                                                    │
        │  APP: CORE             (Vistas Públicas)          │
        │  ├─ views.py: inicio, historial                  │
        │  └─ urls.py: /inicio                             │
        │                                                    │
        │  MIDDLEWARE PERSONALIZADO:                        │
        │  └─ LoginAttemptsMiddleware (bloqueo intentos)   │
        │                                                    │
        └────────────────────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
            ┌────────┐  ┌─────────┐  ┌─────────────┐
            │ MySQL  │  │Stripe   │  │Gemini 2.5   │
            │ DB     │  │API      │  │Flash API    │
            │        │  │         │  │             │
            │adonai_ │  │Webhooks │  │Chat responses
            │store   │  │         │  │             │
            └────────┘  └─────────┘  └─────────────┘
```

---

## 🔄 2. FLUJO ACTUAL DE DATOS (Diagrama Detallado)

### **FLUJO A: Registro y Autenticación**

```
┌──────────────────────────────────────────────────────────────────────┐
│ 1. CLIENTE ACCEDE /usuarios/register                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   GET /usuarios/register                                            │
│   ↓                                                                 │
│   usuarios/views.py (custom_login L97-156)                         │
│   ├─ Renderiza template: usuarios/login.html                       │
│   ├─ Formulario con: email, password, confirmación                 │
│   └─ Si es POST: RegistroForm validation                           │
│                                                                      │
│ 2. CLIENTE COMPLETA REGISTRO Y ENVÍA FORM                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   POST /usuarios/register                                           │
│   └─ Data: {email, password, nombre, telefono, direccion}          │
│       ↓                                                             │
│       usuarios/views.py (register L57-90)                          │
│       ├─ 1. Valida form (usuarios/forms.py:RegistroFormulario)    │
│       ├─ 2. Hash password con check_password()                    │
│       ├─ 3. Crea Usuario:                                         │
│       │   INSERT INTO usuarios_usuario (email, password, rol_id)  │
│       │   VALUES ('user@email', 'hashed_pass', 3)                 │
│       ├─ 4. Crea/actualiza auth.User (Django default):           │
│       │   INSERT INTO auth_user (username, password, email)       │
│       │   VALUES ('user@email', 'hashed_pass', 'user@email')     │
│       ├─ 5. Asigna a grupo según rol:                            │
│       │   INSERT INTO auth_user_groups (user_id, group_id)       │
│       └─ 6. Redirige a /inicio (login automático)                │
│                                                                      │
│ 3. CLIENTE INTENTA LOGIN                                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   POST /usuarios/login                                              │
│   └─ Data: {email, password}                                       │
│       ↓                                                             │
│       Middleware: LoginAttemptsMiddleware                          │
│       ├─ Lee sesión['failed_attempts'] (default 0)               │
│       ├─ Si >= 3: redirige a /usuarios/login (bloqueado)         │
│       └─ Sino: continúa                                           │
│       ↓                                                             │
│       usuarios/views.py (custom_login L97-156)                    │
│       ├─ 1. Backend = UsuarioBackend (usuarios/backends.py L6)   │
│       ├─ 2. authenticate(email=email, password=password)         │
│       │   ↓                                                       │
│       │   UsuarioBackend.authenticate():                         │
│       │   ├─ Query: Usuario.objects.get(email__iexact=email)    │
│       │   ├─ Valida: check_password(password, usuario.password) │
│       │   ├─ Si válido:                                         │
│       │   │   - Busca/crea auth.User (username=email.lower())   │
│       │   │   - Sincroniza: password, email, is_active         │
│       │   │   - Obtiene grupo del rol                           │
│       │   └─ Devuelve: auth.User                               │
│       │                                                         │
│       ├─ 3. Si auth exitosa:                                   │
│       │   ├─ django.auth.login(request, user)                 │
│       │   ├─ Resetea sesión['failed_attempts'] = 0           │
│       │   └─ Redirige según rol:                             │
│       │       - Superuser → /panel/                          │
│       │       - Empleado → /panel/empleados/area/            │
│       │       - Cliente → /inicio/                           │
│       │                                                       │
│       └─ 4. Si auth falla:                                   │
│           ├─ sesión['failed_attempts'] += 1                 │
│           ├─ Muestra error: "Email o contraseña incorrectos"│
│           └─ Si >= 3: bloquea por 30 segundos               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### **FLUJO B: Navegación de Catálogo**

```
┌──────────────────────────────────────────────────────────────────────┐
│ 1. CLIENTE ACCEDE A CATÁLOGO                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   GET /catalogo/                                                    │
│   ↓                                                                 │
│   productos/views.py (catalogo L13-53)                             │
│   ├─ Query base: Producto.objects.filter(estado='activo')         │
│   │                                                                │
│   │  FILTROS APLICADOS (Query Parameters):                       │
│   │  ?categoria=2              → filter(categoria_id=2)          │
│   │  ?q=empanada               → filter(Q(nombre__icontains))   │
│   │  ?precio_min=10&precio_max=50 → filter(precio__range=[10,50])
│   │                                                                │
│   ├─ Ejecuta Query:                                              │
│   │  SELECT * FROM productos_producto                           │
│   │  WHERE estado='activo'                                      │
│   │  AND categoria_id=? (si aplica)                             │
│   │  AND (nombre LIKE % o descripcion LIKE %)                  │
│   │  AND precio BETWEEN ? AND ?                                │
│   │                                                                │
│   ├─ Renderiza: productos/catalogo.html                         │
│   │  ├─ Para cada producto:                                    │
│   │  │  ├─ Nombre, Descripción, Precio                        │
│   │  │  ├─ Imagen (media/productos/...)                       │
│   │  │  ├─ Stock disponible                                   │
│   │  │  ├─ Botón: "Agregar al carrito"                        │
│   │  │  └─ Si stock <= stock_minimo: Mostrar alerta           │
│   │  │                                                         │
│   │  ├─ Sidebar con filtros:                                  │
│   │  │  ├─ Checkbox de categorías                             │
│   │  │  ├─ Range de precio (slider)                           │
│   │  │  └─ Campo de búsqueda                                  │
│   │  │                                                         │
│   │  └─ Notificaciones no leídas (badge):                     │
│   │     contador = NotificationRead.objects.filter(            │
│   │                user=request.user, read_at=None).count()   │
│   │                                                                │
│   └─ Responde HTML + CSS                                        │
│                                                                      │
│ 2. CLIENTE FILTRA (ej: categoría "Empanadas")                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   GET /catalogo/?categoria=1                                       │
│   ↓ (mismo flujo pero con filtro categoria_id=1)                  │
│                                                                      │
│ 3. CLIENTE VE NOTIFICACIÓN DE NUEVO PRODUCTO                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   A. Admin crea nuevo producto:                                   │
│   └─ POST /panel/inventario/nuevo/                              │
│      ├─ Signal post_save en Producto (productos/models L169-177)│
│      ├─ Crea registro en Notification:                         │
│      │  INSERT INTO productos_notification (producto_id, creado_en)
│      │  VALUES (123, NOW())                                   │
│      └─ Django signals automáticos                           │
│                                                                      │
│   B. Cliente recibe notificación:                                │
│   └─ AJAX: GET /notificaciones/ (productos/views L98-126)     │
│      ├─ Query:                                                │
│      │  SELECT notif FROM Notification                       │
│      │  WHERE NOT EXISTS (                                  │
│      │    SELECT 1 FROM NotificationRead                   │
│      │    WHERE notification=notif AND user=request.user  │
│      │  )                                                   │
│      ├─ Responde JSON:                                     │
│      │  {                                                  │
│      │    "count": 3,                                      │
│      │    "notifications": [                              │
│      │      {                                              │
│      │        "id": 1,                                     │
│      │        "producto": "Empanada Mixta",               │
│      │        "tipo": "nuevo_producto",                   │
│      │        "creado_en": "2026-06-11T10:30:00"          │
│      │      }                                              │
│      │    ]                                                │
│      │  }                                                  │
│      └─ Frontend muestra badge con contador               │
│                                                                      │
│ 4. CLIENTE MARCA NOTIFICACIÓN COMO LEÍDA                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   POST /notificaciones/marcar/ (productos/views L129-155)         │
│   └─ Data: {notification_id: 1}                                  │
│      ├─ INSERT INTO productos_notificationread                  │
│      │  (notification_id, user_id, read_at)                    │
│      │  VALUES (1, request.user.id, NOW())                    │
│      │                                                          │
│      │  Note: unique_together=(notification, user)            │
│      │  Evita duplicados                                       │
│      │                                                          │
│      └─ Responde: {"success": true}                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### **FLUJO C: Compra Completa (Crítico)**

```
┌──────────────────────────────────────────────────────────────────────┐
│ PASO 1: CLIENTE AGREGA PRODUCTO AL CARRITO                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   AJAX/JavaScript:                                                 │
│   └─ POST /carrito/item/agregar/                                  │
│      ├─ Data: {product_id: 1, quantity: 2}                       │
│      ├─ Headers: Authorization (si está logueado)               │
│      │                                                            │
│      └─ Si no logueado:                                          │
│         └─ Guardar en localStorage (frontend)                   │
│            {carrito: [{id: 1, qty: 2}, {id: 3, qty: 1}]}      │
│                                                                      │
│   Si logueado → Backend:                                          │
│   └─ carrito/views.py (agregar_item)                            │
│      ├─ Busca/crea Carrito:                                    │
│      │  carrito, created = Carrito.objects.get_or_create(     │
│      │    usuario=request.user                                │
│      │  )                                                       │
│      │                                                          │
│      ├─ Verifica stock en PRODUCTO:                           │
│      │  product = Producto.objects.get(id=1)                 │
│      │  if product.stock_actual >= 2:                       │
│      │     OK                                               │
│      │  else:                                               │
│      │     raise OutOfStockError()                         │
│      │                                                          │
│      ├─ Crea/actualiza CarritoItem:                          │
│      │  carrito_item, created = CarritoItem.objects.update_or_create(
│      │    carrito=carrito,                                  │
│      │    producto=product,                                │
│      │    defaults={'quantity': 2}                         │
│      │  )                                                   │
│      │                                                          │
│      └─ Responde JSON:                                       │
│         {                                                    │
│           "success": true,                                  │
│           "carrito_count": 3,                              │
│           "total": 150.00                                 │
│         }                                                    │
│                                                                      │
│ PASO 2: CLIENTE REVISA CARRITO Y HACE CHECKOUT                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   GET /carrito/checkout/                                          │
│   ↓                                                               │
│   carrito/views.py (checkout L12-30)                             │
│   ├─ Si no autenticado:                                         │
│   │  └─ @login_required → Redirige a /usuarios/login/         │
│   │                                                             │
│   ├─ Si autenticado:                                           │
│   │  ├─ Busca carrito del usuario:                           │
│   │  │  carrito = Carrito.objects.get(usuario=request.user) │
│   │  │                                                       │
│   │  ├─ Obtiene items:                                      │
│   │  │  items = carrito.carritoitem_set.all()              │
│   │  │                                                       │
│   │  ├─ Calcula total:                                     │
│   │  │  total = sum(item.producto.precio * item.quantity) │
│   │  │                                                       │
│   │  ├─ Renderiza: carrito/checkout.html                  │
│   │  │  ├─ Tabla con items del carrito                   │
│   │  │  │  ├─ Nombre producto                           │
│   │  │  │  ├─ Precio unitario                           │
│   │  │  │  ├─ Cantidad                                   │
│   │  │  │  └─ Subtotal (precio × cantidad)              │
│   │  │  │                                                 │
│   │  │  ├─ Total de compra                              │
│   │  │  ├─ Botón: "Proceder al pago"                    │
│   │  │  └─ Stripe key público en template               │
│   │  │                                                    │
│   │  └─ Responde HTML                                   │
│                                                                      │
│ PASO 3: CLIENTE INICIA PAGO CON STRIPE                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   POST /create-checkout-session (pagos/views L247-310)           │
│   └─ Data: {cart_items: [{id, qty}, ...]}                       │
│      │                                                            │
│      pagos/views.py (create_checkout_session):                  │
│      ├─ 1. Convierte cart_items a JSON:                        │
│      │    cart_json = json.dumps([                            │
│      │      {"id": 1, "qty": 2, "precio": 25.00},            │
│      │      {"id": 3, "qty": 1, "precio": 15.00}             │
│      │    ])                                                  │
│      │                                                        │
│      ├─ 2. Calcula total en centavos:                        │
│      │    total_cents = 55.00 * 100 = 5500 (BOB)           │
│      │                                                        │
│      ├─ 3. Crea sesión Stripe:                              │
│      │    session = stripe.checkout.Session.create(         │
│      │      payment_method_types=["card"],                  │
│      │      line_items=[                                    │
│      │        {                                             │
│      │          "price_data": {                            │
│      │            "currency": "bob",                       │
│      │            "unit_amount": 5500,                    │
│      │            "product_data": {                       │
│      │              "name": "Compra Adonai"               │
│      │            }                                        │
│      │          },                                         │
│      │          "quantity": 1                             │
│      │        }                                            │
│      │      ],                                              │
│      │      metadata={"cart_items": cart_json},            │
│      │      success_url="https://app.com/pago/exito/",    │
│      │      cancel_url="https://app.com/pago/error/"      │
│      │    )                                                 │
│      │                                                        │
│      ├─ 4. Guarda sesión_id en BD:                         │
│      │    # Opcional - para tracking                      │
│      │    Payment.objects.create(                         │
│      │      stripe_session_id=session.id,                │
│      │      amount_cents=5500,                           │
│      │      status='created',                            │
│      │      user=request.user                            │
│      │    )                                               │
│      │                                                        │
│      └─ 5. Responde JSON:                                 │
│         {                                                  │
│           "sessionId": "cs_test_...",                     │
│           "url": "https://checkout.stripe.com/..."      │
│         }                                                  │
│                                                                      │
│ PASO 4: STRIPE CHECKOUT PAGE (CLIENTE PAGA)                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Frontend:                                                        │
│   ├─ Redirige a Stripe: window.location = response.url         │
│   └─ Cliente ingresa tarjeta en checkout.stripe.com            │
│                                                                      │
│   Stripe procesa:                                                 │
│   ├─ Valida tarjeta                                            │
│   ├─ Cobra dinero                                              │
│   ├─ Envía webhook a nuestra app                              │
│   └─ Redirige cliente a success_url                           │
│                                                                      │
│ PASO 5: WEBHOOK DE STRIPE (ASINCRÓNICO - CRÍTICO)                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   POST /pago/webhook/ (pagos/views L1-60)                        │
│   └─ Headers: {"Stripe-Signature": "..."}                       │
│      │                                                            │
│      pagos/views.py (stripe_webhook):                          │
│      ├─ 1. Valida webhook signature:                          │
│      │    event = stripe.Webhook.construct_event(            │
│      │      payload,                                         │
│      │      sig_header,                                      │
│      │      STRIPE_WEBHOOK_SECRET                           │
│      │    )                                                  │
│      │                                                        │
│      │    Si inválida: return HttpResponse(400)             │
│      │                                                        │
│      ├─ 2. Verifica tipo de evento:                         │
│      │    if event['type'] == 'payment_intent.succeeded':  │
│      │                                                        │
│      ├─ 3. CREA VENTA (crear_venta_from_stripe_session):   │
│      │    L61-140:                                          │
│      │    ├─ Obtiene session_id del evento                │
│      │    ├─ Lee metadata['cart_items'] (JSON)            │
│      │    ├─ Parsea items: [{id, qty, precio}, ...]      │
│      │    │                                               │
│      │    ├─ Busca/crea Usuario:                         │
│      │    │  └─ Si no existe: crea Usuario con datos   │
│      │    │     de Stripe (email, etc)                 │
│      │    │                                               │
│      │    ├─ Crea Venta:                                │
│      │    │  INSERT INTO ventas_venta (                │
│      │    │    usuario_id, total, metodo_pago,        │
│      │    │    estado, stripe_session_id              │
│      │    │  ) VALUES (                                │
│      │    │    user_id, 55.00, 'stripe',             │
│      │    │    'pagado', 'cs_test_...'               │
│      │    │  )                                         │
│      │    │                                               │
│      │    ├─ Crea VentaDetalle para cada item:        │
│      │    │  For cada item en cart_items:             │
│      │    │  INSERT INTO ventas_ventadetalle (        │
│      │    │    venta_id, producto_id, cantidad,       │
│      │    │    precio_unitario                        │
│      │    │  ) VALUES (venta_id, item.id, qty, precio)
│      │    │                                               │
│      │    └─ Devuelve venta creada                     │
│      │                                                        │
│      ├─ 4. REDUCE STOCK (process_payment_stock):            │
│      │    L141-225:                                         │
│      │    For cada VentaDetalle:                           │
│      │    ├─ Obtiene Producto:                           │
│      │    │  product = Producto.objects.get(id)        │
│      │    │                                              │
│      │    ├─ Reduce stock:                             │
│      │    │  product.stock_actual -= cantidad         │
│      │    │  product.save()                           │
│      │    │                                              │
│      │    ├─ Registra movimiento en Inventario:        │
│      │    │  INSERT INTO productos_inventario (       │
│      │    │    producto_id, cantidad, tipo_movimiento,│
│      │    │    usuario_id, fecha_hora               │
│      │    │  ) VALUES (                             │
│      │    │    product.id, -qty, 'Salida',         │
│      │    │    None, NOW()                         │
│      │    │  )                                        │
│      │    │                                              │
│      │    └─ Signal post_save en Inventario crea    │
│      │       Notification automáticamente             │
│      │                                                        │
│      ├─ 5. ACTUALIZA PAYMENT STATUS:                       │
│      │    Payment.objects.filter(                       │
│      │      stripe_session_id=session_id             │
│      │    ).update(                                    │
│      │      status='paid'                            │
│      │    )                                           │
│      │                                                        │
│      ├─ 6. LIMPIA CARRITO:                                │
│      │    Carrito.objects.filter(                      │
│      │      usuario=venta.usuario                    │
│      │    ).delete()                                  │
│      │                                                        │
│      │    CarritoItem.objects.filter(                 │
│      │      carrito__usuario=venta.usuario          │
│      │    ).delete()                                 │
│      │                                                        │
│      └─ 7. Responde:                                      │
│         return JsonResponse({'status': 'success'})     │
│                                                                      │
│ PASO 6: CLIENTE VE CONFIRMACIÓN                                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   GET /pago/exito/?session_id=cs_test_...                        │
│   ↓                                                               │
│   pagos/views.py (pago_exito):                                  │
│   ├─ Verifica que session_id exista en Payment.status='paid'   │
│   ├─ Obtiene Venta asociada                                    │
│   ├─ Renderiza: pagos/pago_exito.html                         │
│   │  ├─ "Pago realizado exitosamente"                        │
│   │  ├─ Total: 55.00 BOB                                      │
│   │  ├─ Número de transacción                                │
│   │  ├─ Items comprados                                      │
│   │  ├─ Botón: "Descargar recibo PDF"                        │
│   │  └─ Botón: "Volver al catálogo"                          │
│   │                                                            │
│   └─ Responde HTML                                           │
│                                                                      │
│ PASO 7: CLIENTE DESCARGA RECIBO                                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   GET /pago/recibo/cs_test_.../                                  │
│   ↓                                                               │
│   pagos/views.py (recibo_pdf):                                  │
│   ├─ Obtiene Venta desde sesión Stripe                        │
│   ├─ Genera PDF con ReportLab:                               │
│   │  ├─ Encabezado: Logo Adonai                             │
│   │  ├─ Detalles: Número de orden, fecha, total            │
│   │  ├─ Items: Lista de productos comprados                │
│   │  ├─ Pie: Gracias por su compra                          │
│   │  └─ QR con número de transacción                        │
│   │                                                           │
│   └─ Responde PDF (Content-Type: application/pdf)           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 📊 3. MATRIZ DE COMPONENTES Y DEPENDENCIAS

### **Tabla: Apps y sus Relaciones**

```
┌──────────────┬─────────────────────────┬──────────────────────────────────┐
│ APP          │ MODELOS PRINCIPALES     │ DEPENDE DE                      │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ usuarios     │ Usuario, Rol            │ -                               │
│              │                         │ (Base de todo)                  │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ productos    │ Producto, Categoria     │ → usuarios (creado_por,         │
│              │ Inventario              │  actualizado_por)               │
│              │ Notification            │                                 │
│              │ Empleado                │                                 │
│              │ Promotion               │                                 │
│              │ Cupon                   │                                 │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ carrito      │ Carrito, CarritoItem    │ → usuarios (usuario)            │
│              │                         │ → productos (producto)          │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ pagos        │ Payment (legacy)        │ → carrito (items)               │
│              │                         │ → productos (stock)             │
│              │ (Metadata Stripe)       │ → ventas (crea venta)           │
│              │                         │ → usuarios (usuario)            │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ ventas       │ Venta, VentaDetalle     │ → pagos (creada por webhook)   │
│              │                         │ → usuarios (usuario)            │
│              │                         │ → productos (producto)          │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ delivery     │ Delivery                │ → ventas (venta)                │
│              │                         │ → usuarios (repartidor)         │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ chat         │ Chat, MensajeChat       │ → usuarios (usuario)            │
│              │                         │ → Gemini 2.5 API (externa)      │
│              │                         │ → productos (recomendaciones)   │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ core         │ (Solo vistas)           │ → ventas (historial)            │
│              │                         │ → usuarios (autenticación)      │
├──────────────┼─────────────────────────┼──────────────────────────────────┤
│ roles        │ Rol (choices)           │ ← usuarios (FK)                 │
│              │                         │ ← django.contrib.auth.Group    │
└──────────────┴─────────────────────────┴──────────────────────────────────┘
```

---

## 🔀 4. MATRIZ DE FLUJOS DE DATOS

```
┌────────────────────────────────────────────────────────────────────────┐
│                      MATRIZ DE FLUJOS (¿Quién Usa Qué?)               │
├────────────────────────────────────────────────────────────────────────┤

USUARIOS:
  ├─ Lee/Escribe: Usuario, Rol, auth.User
  ├─ Consulta de: produtos (para crear), pagos (para pagar)
  ├─ Autentica con: Backend personalizado (check_password)
  └─ Almacena en: BD usuarios_usuario, roles_rol

PRODUCTOS:
  ├─ Lee: Categoria, Producto, Inventario
  ├─ Escribe: Notification (via signals)
  ├─ Consulta de: carrito (items), pagos (reduce stock via webhook)
  ├─ Valida: Stock disponible
  └─ Emite: Signals cuando stock cambia

CARRITO:
  ├─ Lee: Usuario (propietario), Producto (precios)
  ├─ Escribe: Carrito, CarritoItem
  ├─ Usa: Email del usuario autenticado
  └─ Envía a: pagos (items en metadata)

PAGOS:
  ├─ Lee: Carrito (items), Producto (precios), Usuario
  ├─ Escribe: Payment (estado)
  ├─ Recibe: Webhook de Stripe
  ├─ Crea: Venta (via create_venta_from_stripe_session)
  ├─ Reduce: Stock de Producto
  ├─ Registra: Inventario (movimiento)
  └─ Limpia: Carrito después de pago exitoso

VENTAS:
  ├─ Lee: Usuario, Producto, VentaDetalle
  ├─ Escribe: Venta, VentaDetalle (desde pagos)
  ├─ Consume: Metadata de sesión Stripe
  ├─ Consulta en: Delivery (para rastreo)
  └─ Usado por: core (historial), reportes (admin)

DELIVERY:
  ├─ Lee: Venta, Usuario (repartidor)
  ├─ Escribe: Delivery (estado)
  └─ Publica: Estado de entrega

CHAT:
  ├─ Lee: Usuario, Producto, Venta
  ├─ Escribe: Chat, MensajeChat
  ├─ Consulta API: Gemini 2.5 Flash
  ├─ Usa: Datos del usuario para contexto
  └─ Sistema: M/M/1 (colas, prioridades)

CORE:
  ├─ Lee: Usuario (autenticado), Venta (historial), Producto (catálogo)
  ├─ No escribe nada
  └─ Renderiza: Página de inicio
```

---

## 🗄️ 5. ESTRUCTURA DE BASE DE DATOS (Monolito)

```
MySQL Database: adonai_store

TABLA: usuarios_usuario
├─ id (PK)
├─ nombre (VARCHAR 100)
├─ email (VARCHAR 255, UNIQUE)
├─ password (VARCHAR 255) ← Hash + fallback texto plano
├─ rol_id (FK → roles_rol)
├─ telefono (VARCHAR 20)
├─ direccion (TEXT)
├─ estado (ENUM: activo, inactivo)
├─ must_change_password (BOOLEAN)
├─ creado_en (DATETIME)
└─ (Sincroniza con auth_user)

TABLA: roles_rol
├─ id (PK)
├─ nombre (VARCHAR 100, UNIQUE) ← 'Administrador', 'Empleado', 'Cliente'
└─ descripcion (TEXT)

TABLA: productos_categoria
├─ id (PK)
├─ nombre (VARCHAR 100, UNIQUE)
└─ descripcion (TEXT)

TABLA: productos_producto
├─ id (PK)
├─ categoria_id (FK → productos_categoria)
├─ nombre (VARCHAR 100)
├─ precio (DECIMAL 10,2)
├─ stock_actual (INT)
├─ stock_minimo (INT)
├─ imagen (VARCHAR 100)
├─ fecha_vencimiento (DATE)
├─ creado_por_id (FK → usuarios_usuario, nullable)
├─ actualizado_por_id (FK → usuarios_usuario, nullable)
├─ estado (ENUM: activo, inactivo)
└─ [SIGNAL]: Si stock cambia → Crea Notification

TABLA: productos_inventario
├─ id (PK)
├─ producto_id (FK → productos_producto)
├─ cantidad (INT)
├─ tipo_movimiento (ENUM: Entrada, Salida)
├─ usuario_id (FK → usuarios_usuario, nullable)
├─ fecha_hora (DATETIME)
└─ [SIGNAL]: post_save → Crea Notification

TABLA: productos_notification
├─ id (PK)
├─ producto_id (FK → productos_producto)
├─ creado_en (DATETIME)
└─ [Usado por]: Cliente para ver cambios

TABLA: productos_notificationread
├─ id (PK)
├─ notification_id (FK → productos_notification)
├─ user_id (FK → auth_user)
├─ read_at (DATETIME)
└─ unique_together: (notification, user)

TABLA: carrito_carrito
├─ id (PK)
├─ usuario_id (FK → usuarios_usuario, unique)
└─ creado_en (DATETIME)

TABLA: carrito_carritoitem
├─ id (PK)
├─ carrito_id (FK → carrito_carrito)
├─ producto_id (FK → productos_producto)
├─ quantity (INT)
└─ unique_together: (carrito, producto)

TABLA: pagos_payment (legacy)
├─ id (PK)
├─ stripe_session_id (VARCHAR, UNIQUE)
├─ amount_cents (INT)
├─ status (ENUM: created, paid, failed, canceled)
└─ creado_en (DATETIME)

TABLA: ventas_venta
├─ id (PK)
├─ usuario_id (FK → usuarios_usuario, nullable)
├─ total (DECIMAL 10,2)
├─ metodo_pago (VARCHAR 50)
├─ estado (ENUM: pendiente, pagado, en_preparacion, etc)
├─ direccion_entrega (TEXT)
├─ ciudad_entrega (VARCHAR 100)
├─ codigo_postal (VARCHAR 20)
├─ creado_en (DATETIME)
└─ [Creada por]: pagos/webhook

TABLA: ventas_ventadetalle
├─ id (PK)
├─ venta_id (FK → ventas_venta)
├─ producto_id (FK → productos_producto)
├─ cantidad (INT)
├─ precio_unitario (DECIMAL 10,2)
└─ [Creada por]: pagos/webhook

TABLA: delivery_delivery
├─ id (PK)
├─ venta_id (FK → ventas_venta, unique)
├─ repartidor_id (FK → usuarios_usuario)
├─ estado (ENUM: pendiente, en_ruta, entregado)
└─ creado_en (DATETIME)

TABLA: chat_chat
├─ id (PK)
├─ usuario_id (FK → usuarios_usuario)
├─ estado (ENUM: esperando, en_atencion, finalizado, cancelado)
├─ prioridad (INT 1-3)
├─ llegada (DATETIME)
├─ inicio_servicio (DATETIME, nullable)
├─ fin_servicio (DATETIME, nullable)
└─ duracion_segundos (INT, nullable)

TABLA: chat_mensajechat
├─ id (PK)
├─ chat_id (FK → chat_chat)
├─ remitente (ENUM: Cliente, Bot, Empleado)
├─ contenido (TEXT)
└─ fecha_envio (DATETIME)

TABLA: django.contrib.auth.User (Sincronizado con usuarios_usuario)
├─ id (PK)
├─ username (VARCHAR, UNIQUE) ← email.lower()
├─ password (VARCHAR) ← Sincronizado
├─ email (VARCHAR)
├─ is_active (BOOLEAN) ← De usuarios.estado
├─ is_staff (BOOLEAN)
├─ is_superuser (BOOLEAN)
└─ groups (M2M) ← Del rol
```

---

## 🔌 6. INTEGRACIONES EXTERNAS

```
┌────────────────────────────────────────────────────────────────┐
│                    INTEGRACIONES EXTERNAS                      │
├────────────────────────────────────────────────────────────────┤

1. STRIPE (Pagos)
   ├─ Ubicación: pagos/views.py
   ├─ Uso:
   │  ├─ stripe.checkout.Session.create() → Crear sesión pago
   │  ├─ stripe.Webhook.construct_event() → Validar webhook
   │  └─ stripe.Event.retrieve() → Obtener detalles evento
   ├─ Flujo:
   │  ├─ 1. Frontend: user → Stripe Checkout
   │  ├─ 2. Stripe: Procesa pago
   │  ├─ 3. Stripe: POST /pago/webhook/ → nuestra app
   │  ├─ 4. Nuestra app: Crea Venta + reduce stock
   │  └─ 5. Stripe: Redirige a success_url
   ├─ Configuración:
   │  ├─ STRIPE_SECRET_KEY = "sk_test_..."
   │  ├─ STRIPE_WEBHOOK_SECRET = "whsec_..."
   │  └─ Currency: 'bob' (Bolivianos)
   └─ Seguridad:
      └─ Validación de firma webhook (CRÍTICO)

2. GOOGLE GEMINI 2.5 FLASH (Chat AI)
   ├─ Ubicación: chat/views.py (get_gemini_response L65-127)
   ├─ Uso:
   │  ├─ genai.GenerativeModel('gemini-2.5-flash')
   │  ├─ model.generate_content(contents, system_instruction)
   │  └─ Response: Texto de respuesta IA
   ├─ Flujo:
   │  ├─ 1. Usuario: POST /chat/send {mensaje}
   │  ├─ 2. Backend: Detecta intención (palabras clave)
   │  ├─ 3. Si no detecta: Envía a Gemini
   │  ├─ 4. Gemini: Genera respuesta
   │  └─ 5. Backend: Devuelve respuesta + opciones
   ├─ Configuración:
   │  └─ GEMINI_API_KEY = "AIzaSyA7MsTs9K6..." (hardcoded L45)
   ├─ System Instruction:
   │  ├─ Eres asistente "Adonai"
   │  ├─ Tienda de mascotas
   │  ├─ Teoría de colas M/M/1
   │  └─ Contexto de prioridades
   └─ Limitaciones:
      ├─ Free tier: 60 requests/min
      └─ Timeout: si Gemini no responde

3. EMAIL (Recuperación de Contraseña)
   ├─ Ubicación: usuarios/views.py (recovery_verify)
   ├─ Servicio: SMTP (Gmail)
   ├─ Configuración:
   │  ├─ EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
   │  ├─ EMAIL_HOST = "smtp.gmail.com"
   │  ├─ EMAIL_PORT = 587
   │  └─ EMAIL_HOST_USER = settings.py
   ├─ Uso:
   │  └─ send_mail(subject, message, from, [to])
   └─ Flujo:
      ├─ 1. Usuario: POST /recovery/verify {email}
      ├─ 2. Backend: Genera token
      ├─ 3. Envía email con link reset
      ├─ 4. Usuario: Click en link
      └─ 5. Backend: Resetea contraseña
```

---

## 📈 7. FLUJO DE AUTENTICACIÓN (DETALLADO)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUTENTICACIÓN                            │
├──────────────────────────────────────────────────────────────────────┤

STEP 1: CLIENTE INTENTA LOGIN
└─ GET /usuarios/login/ → Renderiza form

STEP 2: USUARIO ENVÍA CREDENCIALES
└─ POST /usuarios/login/
   └─ Data: {email: "user@example.com", password: "123456"}

STEP 3: MIDDLEWARE VALIDA INTENTOS
└─ LoginAttemptsMiddleware (usuarios/middleware.py)
   ├─ Lee sesión['failed_attempts'] (default: 0)
   ├─ Lee sesión['block_time'] (timestamp)
   │
   ├─ Si block_time presente y < 30 segundos:
   │  └─ Bloquea: Redirige a /usuarios/login/ sin procesarSTATUS: BLOQUEADO
   │
   └─ Si block_time expiró: Resetea failed_attempts = 0

STEP 4: AUTHENTICATE (Backend Personalizado)
└─ usuarios/backends.py: UsuarioBackend.authenticate()
   │
   ├─ Query: Usuario.objects.get(email__iexact=email)
   │         ↓ Case-insensitive, busca en tabla usuarios
   │         usuarios_usuario.email = "user@example.com"
   │
   ├─ Si no existe: raise ObjectDoesNotExist
   │
   ├─ Si existe:
   │  └─ Valida password:
   │     ├─ check_password(password, usuario.password)
   │     ├─ Método 1: Usa algoritmo Django (bcrypt)
   │     ├─ Método 2: Si método 1 falla, compara texto plano
   │     │           (para compatibilidad legacy)
   │     │
   │     └─ Si válido:
   │        ├─ SINCRONIZA CON DJANGO AUTH:
   │        │  ├─ Busca/crea auth.User(username=email.lower())
   │        │  ├─ Actualiza:
   │        │  │  ├─ password ← sincronizado
   │        │  │  ├─ email ← sincronizado
   │        │  │  ├─ is_active ← De usuario.estado
   │        │  │  └─ groups ← De usuario.rol
   │        │  │
   │        │  └─ Guarda en BD
   │        │
   │        └─ Devuelve auth.User()

STEP 5: LOGIN (Django Session)
└─ django.auth.login(request, user)
   ├─ Crea session:
   │  ├─ django_session.session_key
   │  ├─ django_session.session_data (pickled)
   │  ├─ django_session.expire_date = now + 24h
   │  └─ Cookie: sessionid = session_key
   │
   └─ Middleware resetea:
      ├─ request.session['failed_attempts'] = 0
      └─ request.session.delete('block_time')

STEP 6: REDIRIGE SEGÚN ROL
└─ usuarios/views.py (custom_login L152-155)
   │
   ├─ Si es_superuser() o es_staff():
   │  └─ Redirige a: /panel/ (dashboard admin)
   │
   ├─ Elif rol == "Empleado":
   │  └─ Redirige a: /panel/empleados/area/ (vista limitada)
   │
   └─ Else (rol == "Cliente"):
      └─ Redirige a: /inicio/ (página de inicio cliente)

STEP 7: CLIENTE AUTENTICADO NAVEGA
└─ GET /inicio/
   ├─ @login_required ← Valida sesión
   ├─ request.user disponible en vistas
   ├─ {% if user.is_authenticated %} en templates
   └─ Usuario ve:
      ├─ Catálogo de productos
      ├─ Historial de compras
      ├─ Carrito
      └─ Chat

ERROR: INTENTOS FALLIDOS
└─ Si authenticate() falla 3 veces:
   ├─ request.session['failed_attempts'] += 1
   ├─ request.session['block_time'] = now + 30 segundos
   ├─ Renderiza error: "Email o contraseña incorrectos"
   │
   ├─ Si session['failed_attempts'] >= 3:
   │  └─ Middleware en siguiente request:
   │     ├─ Detecta: block_time < 30 segundos
   │     └─ Bloquea: Redirige sin procesar login
   │
   └─ Después de 30 segundos:
      └─ block_time expira, puede reintentar

LOGOUT
└─ GET /usuarios/logout/
   ├─ django.auth.logout(request)
   ├─ Elimina sesión de BD
   ├─ Borra cookie sessionid
   └─ Redirige a: /usuarios/login/
```

---

## 🎯 8. TABLA RESUMIDA DE ENDPOINTS PRINCIPALES

```
┌─────────────────────────────────────┬──────────┬───────────────────────┐
│ ENDPOINT                            │ MÉTODO   │ VISTA / FUNCIÓN       │
├─────────────────────────────────────┼──────────┼───────────────────────┤
│ /usuarios/login/                    │ GET/POST │ custom_login()        │
│ /usuarios/register/                 │ GET/POST │ register()            │
│ /usuarios/logout/                   │ GET      │ custom_logout()       │
│ /usuarios/perfil/                   │ GET/POST │ perfil()              │
│ /usuarios/cambiar-contraseña/       │ GET/POST │ cambiar_contrasena()  │
│                                     │          │                       │
│ /catalogo/                          │ GET      │ catalogo()            │
│ /panel/inventario/                  │ GET      │ inventario_list()     │
│ /panel/inventario/nuevo/            │ GET/POST │ producto_create()     │
│ /panel/inventario/1/editar/         │ GET/POST │ producto_update()     │
│ /panel/categorias/                  │ GET      │ categoria_list()      │
│ /panel/empleados/                   │ GET      │ empleado_list()       │
│ /panel/promociones/                 │ GET      │ promociones_list()    │
│ /panel/cupones/                     │ GET      │ cupones_list()        │
│ /panel/exportar/pdf/                │ GET      │ export_dashboard_pdf()│
│                                     │          │                       │
│ /carrito/checkout/                  │ GET      │ checkout()            │
│                                     │          │                       │
│ /create-checkout-session/           │ POST     │ create_checkout()     │
│ /pago/exito/                        │ GET      │ pago_exito()          │
│ /pago/error/                        │ GET      │ pago_error()          │
│ /pago/recibo/[session_id]/          │ GET      │ recibo_pdf()          │
│ /pago/webhook/                      │ POST     │ stripe_webhook()      │
│                                     │          │                       │
│ /chat/widget/                       │ GET      │ chat_widget()         │
│ /chat/send/                         │ POST     │ chat_send()           │
│                                     │          │                       │
│ /notificaciones/                    │ GET      │ notifications_unread()│
│ /notificaciones/marcar/             │ POST     │ mark_notification()   │
│                                     │          │                       │
│ /inicio/                            │ GET      │ inicio()              │
│ /historial/                         │ GET      │ (en core)             │
└─────────────────────────────────────┴──────────┴───────────────────────┘
```

---

## ⚙️ 9. CONFIGURACIÓN ACTUAL (settings.py)

```
INSTALLED_APPS:
  ├─ django.contrib.admin
  ├─ django.contrib.auth
  ├─ django.contrib.contenttypes
  ├─ django.contrib.sessions
  ├─ django.contrib.messages
  ├─ django.contrib.staticfiles
  ├─ usuarios
  ├─ productos
  ├─ carrito
  ├─ pagos
  ├─ ventas
  ├─ delivery
  ├─ chat
  ├─ core
  └─ roles

MIDDLEWARE:
  ├─ SecurityMiddleware
  ├─ SessionMiddleware
  ├─ CommonMiddleware
  ├─ CsrfViewMiddleware
  ├─ AuthenticationMiddleware
  ├─ MessagesMiddleware
  ├─ XFrameOptionsMiddleware
  └─ LoginAttemptsMiddleware (personalizado)

AUTHENTICATION_BACKENDS:
  ├─ usuarios.backends.UsuarioBackend (personalizado)
  └─ django.contrib.auth.backends.ModelBackend

DATABASE:
  ├─ ENGINE: mysql
  ├─ NAME: adonai_store
  ├─ USER: root
  ├─ PASSWORD: [del sistema]
  └─ HOST: localhost

LANGUAGE/TIMEZONE:
  ├─ LANGUAGE_CODE: es
  └─ TIME_ZONE: America/La_Paz

LOGIN SECURITY:
  ├─ LOGIN_FAILURE_LIMIT: 3
  ├─ LOGIN_BLOCK_TIME: 30 segundos
  ├─ SESSION_COOKIE_AGE: 86400 (24h)
  └─ SESSION_EXPIRE_AT_BROWSER_CLOSE: True

EMAIL:
  ├─ EMAIL_BACKEND: smtp
  ├─ EMAIL_HOST: smtp.gmail.com
  └─ EMAIL_PORT: 587
```

---

## 🔐 10. SEGURIDAD ACTUAL

```
IMPLEMENTADO:
  ✅ @login_required en vistas protegidas
  ✅ CSRF tokens en formularios
  ✅ Password hashing (check_password)
  ✅ Session management (Django)
  ✅ Email validation
  ✅ Bloqueo de intentos fallidos (3 intentos = 30s bloqueo)
  ✅ Stripe webhook signature validation
  ✅ Sinc auth.User automática

```

---

**Documento Generado**: 11 de junio, 2026  
**Status**: ✅ ANÁLISIS ACTUAL COMPLETO  
**Próximo**: Listo para diagrama de migración a microservicios
