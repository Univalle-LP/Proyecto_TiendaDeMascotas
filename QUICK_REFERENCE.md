# ⚡ QUICK REFERENCE - MICROSERVICIOS ADONAI
## Guía Rápida para Developers

**Generado**: 11 de junio, 2026  
**Audiencia**: Developers, DevOps, QA  
**Propósito**: Referencia rápida durante implementación  
**Mantener abierto durante**: Semanas 1-16 de migración

---

## 🚀 COMANDOS ESENCIALES

### **Setup Inicial (Semana 1)**

```bash
# Clonar repos base
git clone https://github.com/Dxtr0203/adonai-base-project.git
cd adonai-base-project

# Setup de Docker
docker-compose up -d mysql redis rabbitmq

# Verificar servicios
docker-compose ps

# Ver logs
docker-compose logs -f mysql

# Acceder a MySQL
docker exec -it adonai-mysql mysql -u root -p adonai_store
```

### **Por Cada Nuevo Servicio**

```bash
# Crear estructura
mkdir adonai-[servicio]-service
cd adonai-[servicio]-service
git init

# Si es FastAPI
pip install fastapi uvicorn sqlalchemy pydantic

# Si es Django
django-admin startproject config .
python manage.py startapp [app_name]

# Setup testing
pip install pytest pytest-asyncio pytest-cov

# Instalar pre-commit hooks
pre-commit install

# Correr tests
pytest tests/ -v --cov

# Correr en dev
uvicorn main:app --reload --port 8001  # FastAPI
python manage.py runserver 8001         # Django
```

---

## 🏗️ ARQUITECTURA DE CARPETAS

### **FastAPI Service (ejemplo CHAT SERVICE)**

```
adonai-chat-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── message.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── messages.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   ├── gemini_service.py
│   │   └── websocket_manager.py
│   ├── database.py
│   ├── security.py
│   └── events.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_chat.py
│   ├── test_messages.py
│   └── test_websocket.py
├── docker/
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

### **Django Service (ejemplo ORDER SERVICE)**

```
adonai-order-service/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── signals.py
│   └── admin.py
├── migrations/
│   ├── 0001_initial.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
├── docker/
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## 🔐 VARIABLES DE ENTORNO

### **Todas los servicios (.env.example)**

```bash
# Database
DB_ENGINE=mysql
DB_NAME=adonai_[service]_db
DB_USER=root
DB_PASSWORD=secretpassword
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672//

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# API Gateway
API_GATEWAY_URL=http://localhost:8000
AUTH_SERVICE_URL=http://auth-service:8001

# Stripe (solo PAYMENT SERVICE)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Google Gemini (solo CHAT SERVICE)
GEMINI_API_KEY=your-api-key

# Environment
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1
LOG_LEVEL=DEBUG
```

---

## 🔀 FLUJOS DE INTEGRACIÓN

### **1. Flujo de Login → JWT**

```
┌─────────────────────────────────────────────────┐
│ Cliente hace POST /auth/login                   │
├─────────────────────────────────────────────────┤
│                                                 │
│ API Gateway:                                    │
│  1. Recibe request                             │
│  2. Valida Content-Type (JSON)                 │
│  3. Redirige a AUTH SERVICE:8001               │
│                                                 │
│ AUTH SERVICE:                                   │
│  1. Busca Usuario por email (case-insensitive) │
│  2. Valida password con bcrypt.verify()        │
│  3. Genera JWT:                                │
│     {                                          │
│       "sub": "user_id",                       │
│       "email": "user@example.com",            │
│       "role": "Cliente",                      │
│       "exp": timestamp,                       │
│       "iat": timestamp                        │
│     }                                          │
│  4. Devuelve:                                  │
│     {                                          │
│       "access_token": "eyJ...",               │
│       "refresh_token": "eyJ...",              │
│       "token_type": "bearer",                 │
│       "expires_in": 3600                      │
│     }                                          │
│                                                 │
│ Cliente:                                        │
│  1. Guarda token en localStorage              │
│  2. En próximos requests: Authorization: Bearer <token>
│                                                 │
└─────────────────────────────────────────────────┘
```

### **2. Flujo de Compra (Crítico)**

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Cliente ve catálogo (PRODUCT SERVICE)                         │
├──────────────────────────────────────────────────────────────────┤
│  GET /api/v1/products?categoria=empanadas&precio_max=50         │
│  ← PRODUCT SERVICE devuelve lista                               │
│                                                                  │
│ 2. Agrega a carrito (CART SERVICE)                              │
├──────────────────────────────────────────────────────────────────┤
│  POST /api/v1/cart/items                                        │
│  {"product_id": 1, "quantity": 2}                               │
│  ← Carrito guardado en BD                                       │
│                                                                  │
│ 3. Inicia checkout (PAYMENT SERVICE)                            │
├──────────────────────────────────────────────────────────────────┤
│  POST /api/v1/payments/checkout-session                         │
│  {                                                              │
│    "items": [{"product_id": 1, "quantity": 2}],               │
│    "user_id": 123,                                             │
│    "return_url": "https://app.com/exito"                      │
│  }                                                              │
│                                                                  │
│  PAYMENT SERVICE:                                               │
│    1. Valida cantidad en PRODUCT SERVICE                       │
│    2. Crea sesión Stripe                                       │
│    3. Guarda session_id en BD                                  │
│    4. Devuelve Stripe checkout URL                             │
│                                                                  │
│ 4. Cliente paga en Stripe                                      │
├──────────────────────────────────────────────────────────────────┤
│  Cliente redirigido a checkout.stripe.com                       │
│  Ingresa tarjeta, paga                                          │
│  Stripe redirige a return_url con session_id                   │
│                                                                  │
│ 5. Webhook de Stripe (ASYNC)                                   │
├──────────────────────────────────────────────────────────────────┤
│  Stripe → POST /api/v1/payments/webhook                         │
│  Signature validation: ✓                                        │
│                                                                  │
│  PAYMENT SERVICE procesa:                                       │
│                                                                  │
│  SAGA PATTERN COMIENZA:                                         │
│                                                                  │
│  Step 1: CREAR VENTA (ORDER SERVICE)                           │
│  POST http://order-service:8005/api/v1/orders/internal/create  │
│  {                                                              │
│    "user_id": 123,                                             │
│    "items": [...],                                             │
│    "total": 150.00,                                            │
│    "stripe_session_id": "cs_test_..."                          │
│  }                                                              │
│  ← ORDER SERVICE crea Venta                                    │
│                                                                  │
│  Step 2: REDUCIR STOCK (PRODUCT SERVICE)                       │
│  POST http://product-service:8002/api/v1/internal/reduce-stock │
│  {"product_id": 1, "quantity": 2}                              │
│  ← PRODUCT SERVICE reduce stock                                │
│                                                                  │
│  Si algo falla → COMPENSATING TRANSACTION                      │
│  - DELETE venta                                                │
│  - Aumentar stock otra vez                                     │
│                                                                  │
│  Step 3: NOTIFICAR (NOTIFICATION SERVICE)                      │
│  Emit event: "payment.succeeded"                               │
│  ← NOTIFICATION SERVICE escucha y notifica                    │
│                                                                  │
│ 6. Cliente ve confirmación                                     │
├──────────────────────────────────────────────────────────────────┤
│  GET /api/v1/payments/{session_id}/receipt                     │
│  ← PDF con detalles de la venta                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📡 PATRONES DE COMUNICACIÓN

### **Pattern 1: Request-Response Síncrono (Bloqueante)**

```python
# Service A (Payment) → Service B (Order)

import requests
from requests.exceptions import Timeout, ConnectionError

def create_order_sync(order_data):
    """Llamada síncrona - BLOQUEA hasta respuesta"""
    
    try:
        response = requests.post(
            "http://order-service:8005/api/v1/orders/internal/create",
            json=order_data,
            timeout=10  # 10 segundos max
        )
        response.raise_for_status()
        return response.json()
        
    except Timeout:
        logger.error("Order service timeout")
        raise OrderServiceTimeoutError()
    
    except ConnectionError:
        logger.error("Order service unreachable")
        raise OrderServiceUnavailableError()
```

### **Pattern 2: Pub/Sub Asincrónico (No Bloquea)**

```python
# Service A (Payment) publica evento
# Service B (Notification) se suscribe

import pika
import json

def publish_event(event_type: str, data: dict):
    """Publicar evento a bus - NO BLOQUEA"""
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq')
    )
    channel = connection.channel()
    
    # Declarar exchange si no existe
    channel.exchange_declare(
        exchange='adonai',
        exchange_type='topic'
    )
    
    # Publicar
    channel.basic_publish(
        exchange='adonai',
        routing_key=event_type,  # e.g., 'payment.succeeded'
        body=json.dumps(data)
    )
    
    connection.close()
    return True

# Suscriptor (Notification Service)
def subscribe_to_payment_events():
    """Escucha eventos de pago"""
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq')
    )
    channel = connection.channel()
    
    channel.exchange_declare(exchange='adonai', exchange_type='topic')
    
    # Crear cola
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    # Vincular a patrón
    channel.queue_bind(
        exchange='adonai',
        queue=queue_name,
        routing_key='payment.*'  # Escuchar todos los payment.*
    )
    
    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Evento recibido: {data}")
        handle_payment_event(data)
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    channel.start_consuming()
```

### **Pattern 3: Saga Pattern (Transacciones Distribuidas)**

```python
# PAYMENT SERVICE - Orquestar transacciones

class PaymentSaga:
    """Manejar compra atómica entre múltiples servicios"""
    
    def __init__(self, order_service, product_service):
        self.order_service = order_service
        self.product_service = product_service
        self.saga_id = uuid.uuid4()
    
    def execute(self, order_data):
        """Ejecutar saga con compensación si falla"""
        
        logger.info(f"Iniciando saga: {self.saga_id}")
        
        try:
            # PASO 1: Crear venta
            logger.info("Paso 1: Creando venta")
            venta = self.order_service.create_order(order_data)
            venta_id = venta['id']
            
            # PASO 2: Reducir stock
            logger.info("Paso 2: Reduciendo stock")
            for item in order_data['items']:
                self.product_service.reduce_stock(
                    item['product_id'],
                    item['quantity']
                )
            
            # PASO 3: Confirmar pago
            logger.info("Paso 3: Confirmando pago")
            payment = self.payment_repo.update_status(
                stripe_session_id,
                'confirmed'
            )
            
            logger.info(f"Saga exitosa: {self.saga_id}")
            return venta
            
        except Exception as e:
            logger.error(f"Error en saga: {e}")
            
            # COMPENSATING TRANSACTIONS (revertir)
            logger.info("Ejecutando compensaciones...")
            
            # Compensación 1: Eliminar venta
            try:
                self.order_service.cancel_order(venta_id)
            except:
                logger.error(f"No se pudo cancelar venta {venta_id}")
            
            # Compensación 2: Restaurar stock
            try:
                for item in order_data['items']:
                    self.product_service.add_stock(
                        item['product_id'],
                        item['quantity']
                    )
            except:
                logger.error("No se pudo restaurar stock")
            
            # Marcar pago como fallido
            self.payment_repo.update_status(
                stripe_session_id,
                'failed'
            )
            
            raise PaymentSagaFailedError(f"Saga falló: {self.saga_id}")
```

---

## 🧪 TESTING CHECKLIST

### **Por cada servicio - Correr antes de Pull Request**

```bash
# 1. Unit Tests
pytest tests/unit/ -v --cov=app --cov-report=html

# 2. Integration Tests (con BD real)
pytest tests/integration/ -v

# 3. E2E Tests (con otros servicios)
pytest tests/e2e/ -v

# 4. Load Tests (100 req/s durante 1 min)
locust -f tests/load/locustfile.py --users=50 --spawn-rate=5

# 5. Security Tests
bandit -r app/  # Buscar vulnerabilidades Python
safety check     # Buscar dependencias vulnerables

# 6. Linting
black app/ --check
flake8 app/
mypy app/        # Type checking

# 7. Pre-commit
pre-commit run --all-files

# Coverage mínimo: 80%
# TODOS deben pasar antes de merge
```

---

## 🚨 CASOS DE ERROR COMUNES

### **Error 1: Webhook duplicado de Stripe**

```python
# ❌ MAL: Procesar sin verificar
def stripe_webhook(request):
    event = stripe.Webhook.construct_event(...)
    create_venta(...)  # ← Crearía venta 2x
    return JsonResponse({'ok': True})

# ✅ BIEN: Idempotency key
def stripe_webhook(request):
    event = stripe.Webhook.construct_event(...)
    
    # Verificar si ya fue procesado
    stripe_session_id = event['data']['object']['id']
    if Payment.objects.filter(
        stripe_session_id=stripe_session_id,
        status='confirmed'
    ).exists():
        return JsonResponse({'status': 'already_processed'})
    
    # Procesar
    create_venta(...)
    return JsonResponse({'ok': True})
```

### **Error 2: Order Service caído**

```python
# ❌ MAL: Esperar hasta timeout (30+ segundos)
response = requests.post(
    "http://order-service:8005/api/...",
    json=data
)

# ✅ BIEN: Circuit breaker
from pybreaker import CircuitBreaker

order_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=60
)

try:
    order_breaker.call(order_service.create_order, data)
except CircuitBreakerListener:
    logger.error("Order service down - retry later")
    # Guardar en tabla "pending_orders" para reintentar
    Pending.objects.create(
        order_data=data,
        status='pending',
        retry_count=0
    )
```

### **Error 3: Race condition en stock**

```python
# ❌ MAL: Leer stock, luego reducir
stock = Product.objects.get(id=1).stock_actual
if stock >= 2:
    product.stock_actual -= 2  # ← Otro request puede haber cambiado stock
    product.save()

# ✅ BIEN: Usar transacción atómica
from django.db import transaction

with transaction.atomic():
    product = Product.objects.select_for_update().get(id=1)
    if product.stock_actual >= 2:
        product.stock_actual -= 2
        product.save()
    else:
        raise OutOfStockError()
```

---

## 🔍 DEBUGGING DISTRIBUIDO

### **Ver logs de todos los servicios**

```bash
# Docker Compose
docker-compose logs -f

# Filtrar por servicio
docker-compose logs -f order-service

# Seguir logs de múltiples
docker-compose logs -f payment-service order-service

# Ver últimas 100 líneas
docker-compose logs --tail=100
```

### **Jaeger Distributed Tracing**

```bash
# Instalar Jaeger (puerto 16686)
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  jaegertracing/all-in-one:latest

# Acceder: http://localhost:16686
```

### **Request Tracing**

```python
# FastAPI - Jaeger integration
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

jaeger_exporter = JaegerExporter(agent_host_name="jaeger", agent_port=6831)
trace.get_tracer_provider().add_span_processor(
    trace.BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

@app.post("/api/v1/payments/checkout")
async def create_checkout(data: CheckoutRequest):
    with tracer.start_as_current_span("create_checkout") as span:
        span.set_attribute("order_id", data.order_id)
        span.set_attribute("amount", data.amount)
        
        # ... lógica
        
        return response
```

---

## 📚 REFERENCIAS RÁPIDAS

### **Por Tecnología**

| Tecnología | Docs | Port | Comando Start |
|---|---|---|---|
| **FastAPI** | fastapi.tiangolo.com | 8001-8008 | `uvicorn main:app --reload --port 8001` |
| **Django** | djangoproject.com | 8005 | `python manage.py runserver 8005` |
| **MySQL** | dev.mysql.com | 3306 | `docker run -d -e MYSQL_ROOT_PASSWORD=pass mysql:8` |
| **Redis** | redis.io | 6379 | `docker run -d redis:7` |
| **RabbitMQ** | rabbitmq.com | 5672 | `docker run -d rabbitmq:3-management` |
| **Stripe** | stripe.com/docs | - | Usar sandbox test keys |
| **Kong** | konghq.com | 8000 | `docker-compose -f docker-compose.kong.yml up` |

### **Usuarios de Test**

```bash
# Usuario Admin
email: admin@adonai.local
password: Admin123!

# Usuario Cliente
email: client@adonai.local
password: Cliente123!

# Usuario Empleado
email: employee@adonai.local
password: Employee123!
```

### **Stripe Test Cards**

```bash
# Pago exitoso
4242 4242 4242 4242

# Pago rechazado
4000 0000 0000 0002

# Autenticación 3D Secure
4000 0025 0000 3010
```

---

## 🎯 DAILY STANDUP TEMPLATE

```markdown
## Daily Standup - [Servicio]

**Fecha**: [Hoy]

### ✅ Completado hoy
- [ ] Item 1
- [ ] Item 2

### 🔄 En progreso
- [ ] Item 1 (70% done)
- [ ] Item 2

### 🚧 Bloqueadores
- [ ] Bloqueador 1 - Necesita revisión de arquitecto

### 📊 Status del Servicio
- Tests: ![100%](Líneas verdes)
- Coverage: 85%
- Build: ✅ Passing

### 📝 Notas
- Cualquier cambio importante en el plan
- Riesgos identificados
```

---

## 🔐 SECURITY CHECKLIST

- [ ] JWT secret key rotado
- [ ] CORS correctly configured
- [ ] SQL injection prevention (ORM usage)
- [ ] Rate limiting enabled
- [ ] HTTPS enforced (TLS 1.2+)
- [ ] Secrets no commiteados
- [ ] CSRF tokens en forms
- [ ] Input validation en todos endpoints
- [ ] Output encoding
- [ ] Dependencies sin vulnerabilidades (`safety check`)
- [ ] No logs de passwords/tokens

---

## 🚀 DEPLOYMENT CHECKLIST

```bash
# Pre-deployment
- [ ] Todos tests pasando
- [ ] Code review aprobado
- [ ] Migrations tested
- [ ] Rollback plan documentado
- [ ] Database backup tomado

# Deployment
- [ ] Build Docker image
- [ ] Push a registry
- [ ] Update docker-compose.yml
- [ ] Correr migrations (si necesario)
- [ ] Redeploy servicio

# Post-deployment
- [ ] Health check passing
- [ ] Logs sin errores
- [ ] Smoke tests running
- [ ] Alerts activos
- [ ] Notificar a equipo
```

---

**Last Updated**: 11 de junio, 2026  
**Versión**: 1.0  
**Mantener actualizado durante**: Semanas 1-16 de migración
