# 📊 ANÁLISIS VISUAL Y MATRICES DE DECISIÓN
## Adonai D'Empanadas - Arquitectura de Microservicios

---

## 1. MATRIZ DE ACOPLAMIENTO DETALLADA

### **Tabla de Acoplamiento (Escala 1-10, siendo 10 máximo acoplamiento)**

```
┌─────────────────┬──────────────┬──────────┬───────────────────────────┐
│ De → A          │ Tipo de FK   │ Score    │ Razón / Impacto           │
├─────────────────┼──────────────┼──────────┼───────────────────────────┤
│ PAGOS → VENTAS  │ Direct FK    │ 10/10    │ Crea venta directamente   │
│ PAGOS → PRODUCT │ Direct FK    │ 9/10     │ Reduce stock en webhook   │
│ CARRITO → PROD  │ Direct FK    │ 8/10     │ Cada item = FK a producto │
│ VENTAS → PROD   │ Direct FK    │ 8/10     │ Detalles = FK a producto  │
│ TODOS → USUARIOS│ Direct FK    │ 7/10     │ Usuario propietario       │
│ DELIVERY → VENTA│ OneToOne FK  │ 7/10     │ Entrega ligada a venta    │
│ CHAT → USUARIOS │ Direct FK    │ 5/10     │ Chat del usuario          │
│ CHAT → PRODUCT  │ No FK        │ 4/10     │ Solo lectura (query)      │
│ PROD → NOTIF    │ Signal       │ 3/10     │ Event-driven (separable)  │
│ DELIVERY → EMPL │ Direct FK    │ 3/10     │ Repartidor asignado       │
└─────────────────┴──────────────┴──────────┴───────────────────────────┘

Acoplamiento CRÍTICO (8-10): Difícil separar, requiere Saga pattern
Acoplamiento ALTO (5-7):      Separable con transacciones distribuidas
Acoplamiento BAJO (1-4):      Fácil de separar, solo eventos
```

---

## 2. ANÁLISIS DE COMPLEJIDAD POR COMPONENTE

```
┌───────────────────────────────────────────────────────────────┐
│              COMPLEJIDAD DE EXTRACCIÓN                         │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  PAYMENT SERVICE        ████████████████░░  (Muy Alta - 9/10) │
│  PRODUCT SERVICE        ███████████░░░░░░░  (Alta - 7/10)     │
│  ORDER SERVICE          ██████░░░░░░░░░░░░  (Media - 5/10)    │
│  CHAT SERVICE           █████░░░░░░░░░░░░░  (Media - 4/10)    │
│  DELIVERY SERVICE       ███░░░░░░░░░░░░░░░  (Baja - 3/10)     │
│  CART SERVICE           ███░░░░░░░░░░░░░░░  (Baja - 2/10)     │
│  AUTH SERVICE           ████░░░░░░░░░░░░░░  (Media - 4/10)    │
│  NOTIFICATION SERVICE   ██░░░░░░░░░░░░░░░░  (Muy Baja - 1/10) │
│                                                                │
└───────────────────────────────────────────────────────────────┘

Factores de Complejidad:
  - Acoplamiento con otros servicios
  - Número de dependencias externas
  - Transacciones críticas
  - Datos históricos a migrar
  - Tests necesarios
```

---

## 3. MATRIZ DE DECISIÓN MULTI-CRITERIO

### **Evaluación de Cada Componente**

```
Criterios de Evaluación (1-5, siendo 5 lo mejor):
  • Independencia: ¿Qué tan independiente puede ser?
  • Escalabilidad: ¿Necesita escalar diferente al resto?
  • Equipo Dedicado: ¿Justifica un equipo separado?
  • ROI: ¿Cuál es el beneficio/esfuerzo?
  • Riesgo: ¿Cuán riesgosa es la extracción? (5=bajo riesgo)

┌────────────────────┬─────────────┬──────────┬────────┬────┬───────┬────┐
│ SERVICIO           │ INDEPNDENCIA│ESCALABIL│ EQUIPO │ROI │ RIESGO│ AVG│
├────────────────────┼─────────────┼──────────┼────────┼────┼───────┼────┤
│ AUTH SERVICE       │     5       │    4     │   5    │  5 │  4    │ 4.6│
│ PRODUCT SERVICE    │     4       │    5     │   4    │  5 │  3    │ 4.2│
│ PAYMENT SERVICE    │     3       │    4     │   5    │  5 │  2    │ 3.8│
│ ORDER SERVICE      │     4       │    3     │   3    │  4 │  3    │ 3.4│
│ CART SERVICE       │     5       │    3     │   2    │  3 │  5    │ 3.6│
│ DELIVERY SERVICE   │     4       │    2     │   2    │  2 │  5    │ 3.0│
│ CHAT SERVICE       │     5       │    3     │   3    │  3 │  4    │ 3.6│
│ NOTIFICATION       │     5       │    2     │   1    │  2 │  5    │ 3.0│
└────────────────────┴─────────────┴──────────┴────────┴────┴───────┴────┘

RECOMENDACIÓN POR SCORE:
  AVG > 4.0: EXTRAER PRIMERO (Alto beneficio, bajo riesgo)
  AVG 3-4:   EXTRAER EN ORDEN (Beneficio moderado)
  AVG < 3:   CONSIDERAR DEJAR EN MONOLITO (Bajo beneficio)
```

### **Matriz de Impacto vs Esfuerzo**

```
                    ESFUERZO →
          BAJO              MEDIO              ALTO
    ↑ ┌──────────────────┬──────────────────┬──────────────────┐
    │ │   QUICK WINS     │   STRATEGIC      │    DIFICULTOSOS  │
    │ │                  │                  │                  │
   A │ │ • CART           │ • CHAT           │ • PAYMENT        │
   L │ │ • DELIVERY       │ • ORDER          │ • PRODUCT        │
   T │ │ • NOTIFICATION   │ • AUTH           │                  │
   O │ │                  │                  │                  │
    │ ├──────────────────┼──────────────────┼──────────────────┤
    │ │   FILL-INS       │  LONG-TERM       │    EVITAR        │
    │ │                  │                  │                  │
    │ │ • (Ninguno)      │ • (Ninguno)      │ • (Ninguno)      │
    │ │                  │                  │                  │
    ↓ └──────────────────┴──────────────────┴──────────────────┘
   IMPACTO POSITIVO

ESTRATEGIA:
  1. Empezar con QUICK WINS (Auth, Cart, Delivery)
  2. Luego STRATEGIC (Chat, Order, Product)
  3. Último DIFICULTOSOS (Payment, pero crítico hacerlo bien)
```

---

## 4. TIMELINE DE MIGRACIÓN GANTT

```
SEMANA    1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16
├─────────┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
PREP      ███ Infrastructure setup, repos, CI/CD
AUTH SVC  ███ ███ Implementation y testing
PRODUCT   ════════ ███ Implementation
PAYMENT   ════════════ ███ ███ Implementation (Crítico)
CART      ════════════════ ███ Implementation (Rápido)
ORDER     ════════════════════ ███ Implementation
DELIVERY  ════════════════════════ ███ Quick
CHAT      ════════════════════════════ ███ Quick
FRONTEND  ════════════════════════════════ ███ ███ React migration
TESTING   ══════════════════════════════════════════════ Intégration
DEPLOY    ════════════════════════════════════════════════════════ ███

HITO CLAVE:
  ✓ Semana 2: Auth Service en Staging
  ✓ Semana 4: Product Service en Staging
  ✓ Semana 6: Payment Service en Staging
  ✓ Semana 10: Todos los servicios en Staging
  ✓ Semana 14: Todos los servicios en Production
  ✓ Semana 16: Deprecación de monolito

PARALLELIZACIÓN:
  - Product y Cart pueden paralelizarse
  - Auth debe estar primero
  - Payment depende de Order/Product
```

---

## 5. FLUJO ACTUAL VS FUTURO

### **Flujo Actual (Monolito)**

```
                        Django Adonai
                     ┌────────────────┐
                     │                │
        ┌────────────┤ Usuarios App   │◄────────┐
        │            │ Productos App  │         │
        │            │ Pagos App      │         │
        │            │ Ventas App     │         │
        │            │ Chat App       │         │
        │            │                │         │
        │            └────────┬───────┘         │
        │                     │                 │
   Cliente Browser     MySQL (adonai_store)    Stripe
        │                     │                 │
        │  HTML/CSS/JS        │      Webhook   │
        └─────────────────────┴─────────────────┘
        
  Ventajas:
    ✓ Simple de deployar
    ✓ Transacciones ACID fáciles
    ✓ Testing integrado
    
  Desventajas:
    ✗ Difícil escalar (todo o nada)
    ✗ Depliegues acoplados (cambio en chat afecta pagos)
    ✗ Imposible tener equipos independientes
    ✗ Difícil usar diferentes lenguajes/frameworks
```

### **Flujo Futuro (Microservicios)**

```
                           Navegador
                              │
                              ▼
                    ┌──────────────────────┐
                    │  React SPA Frontend  │
                    │    (puerto 3000)     │
                    └──────────┬───────────┘
                               │ HTTPS
                               ▼
           ┌───────────────────────────────────────┐
           │       API GATEWAY (Kong/Nginx)        │
           │  - JWT validation                     │
           │  - Rate limiting                      │
           │  - Request routing                    │
           │  - CORS                               │
           │  - Service discovery                  │
           └────┬──┬────┬──┬──┬──┬──┬──┬──┬──────┘
                │  │    │  │  │  │  │  │  │
        ┌───────┘  │    │  │  │  │  │  │  └──────────────┐
        │          │    │  │  │  │  │  │                 │
        ▼          ▼    ▼  ▼  ▼  ▼  ▼  ▼                 ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      ┌─────────┐
    │ AUTH   │ │PRODUCT │ │PAYMENT │ │ ORDER  │      │ CHAT    │
    │ SVC    │ │ SVC    │ │ SVC    │ │ SVC    │      │ SVC     │
    │:8001   │ │:8002   │ │:8003   │ │:8005   │      │:8007    │
    └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘      └────┬────┘
        │          │          │          │                │
        └─────┬────┴─────┬────┴─────┬────┴─────────────────┘
              │          │          │
              ▼          ▼          ▼
         ┌────────────┬────────────┬─────────────┐
         │MySQL       │MySQL       │MySQL        │
         │auth_db     │product_db  │payment_db   │
         └────────────┴────────────┴─────────────┘
              
              ┌─────────────────────────────────┐
              │   EVENT BUS (RabbitMQ/Kafka)    │
              │  - product.created              │
              │  - payment.succeeded            │
              │  - order.created                │
              │  - delivery.updated             │
              └──────────┬──────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
         ┌──────────┐         ┌────────────┐
         │NOTIF SVC │         │ANALYTICS   │
         │:8008     │         │ (async)    │
         └──────────┘         └────────────┘
              
         ┌──────────────────────────────────────────┐
         │  SHARED INFRASTRUCTURE                   │
         │  - Redis Cache                           │
         │  - ELK Stack (logging)                   │
         │  - Prometheus (metrics)                  │
         │  - Jaeger (tracing)                      │
         │  - Email Service (SendGrid)              │
         └──────────────────────────────────────────┘
              
         ┌──────────────────────────────────────────┐
         │  EXTERNAL APIS                           │
         │  - Stripe (pagos)                        │
         │  - Google Gemini (chat)                  │
         └──────────────────────────────────────────┘

  Ventajas:
    ✓ Escalabilidad granular (Payment 10x, Auth 2x)
    ✓ Depliegues independientes
    ✓ Equipos autónomos
    ✓ Diferentes tecnologías (FastAPI para Chat, Django para Order)
    
  Desventajas:
    ✗ Complejidad operacional
    ✗ Transacciones distribuidas (Saga pattern)
    ✗ Debugging distribuido
    ✗ Latencia de red
```

---

## 6. GRAFO DE DEPENDENCIAS

### **Dependencias Síncronas (Bloqueantes)**

```
                    ┌─────────────────┐
                    │  API GATEWAY    │
                    │  JWT Validation │
                    └────────┬────────┘
                             │
                   ┌─────────┴──────────┐
                   │                    │
              CLIENTE           TODOS LOS SERVICIOS
                                USAN JWT DEL GATEWAY
                             
FLUJO CRÍTICO (Compra):

CLIENT ─────POST /checkout────────> CART SERVICE
                                            │
                                           ▼
                            POST /checkout-session
                                   PAYMENT SERVICE
                                     (Stripe)
                                            │
                              Webhook de Stripe
                                    (async)
                                            │
                         ┌──────────────────┴──────────────────┐
                         │                                     │
                        ▼                                      ▼
                  ORDER SERVICE              PRODUCT SERVICE
                  (Crea Venta)               (Reduce Stock)
                         │                                      │
                         │            ┌───────────────────────┘
                         │            │
                         └────────────┴──────────────────┐
                                                        │
                                                       ▼
                                         NOTIFICATION SERVICE
                                         (notifica cambios)
```

### **Dependencias Asincrónicas (No Bloqueantes)**

```
                        EVENT BUS
                      (RabbitMQ/Kafka)
                           ▲
                           │
                    emite eventos
                    (mediante Topic)
                           │
          ┌────────────────┼────────────────┐
          │                │                │
      PRODUCT         PAYMENT          ORDER
      SERVICE         SERVICE          SERVICE
          │                │                │
          └────────────────┼────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          NOTIFICATION          ANALYTICS
          SERVICE               SERVICE
          
  - No bloquean al publicador
  - Procesamiento asincrónico
  - Retries automáticos
  - Order no garantizado
```

---

## 7. MATRIZ DE COMUNICACIÓN ENTRE SERVICIOS

```
┌──────────┬───────┬─────────┬─────────┬───────┬──────────┬──────┬──────┐
│DE \ A    │AUTH   │PRODUCT  │PAYMENT  │ORDER  │CART      │DELIV │CHAT  │
├──────────┼───────┼─────────┼─────────┼───────┼──────────┼──────┼──────┤
│AUTH      │   -   │  (V)    │  (V)    │ (V)   │   (V)    │ (V)  │ (V)  │
│PRODUCT   │   -   │   -     │  (L)    │ (L)   │   (L)    │  -   │ (L)  │
│PAYMENT   │   -   │  (L)    │   -     │ (C)   │   (L)    │  -   │  -   │
│ORDER     │   -   │  (L)    │   -     │   -   │   -      │ (C)  │  -   │
│CART      │   -   │  (L)    │  (C)    │  -    │   -      │  -   │  -   │
│DELIVERY  │   -   │   -     │   -     │ (L)   │   -      │  -   │  -   │
│CHAT      │   -   │  (L)    │   -     │ (L)   │   -      │  -   │  -   │
└──────────┴───────┴─────────┴─────────┴───────┴──────────┴──────┴──────┘

Leyenda:
  (V)  = Validación de JWT (todos hacen esto via API Gateway)
  (C)  = Llamada Síncrona Crítica (bloquea)
  (L)  = Llamada Síncrona Lectura (no bloquea mucho)
  (E)  = Evento Asincrónico
  -    = Sin comunicación
  
PATRONES:
  - AUTH es consultor (validación)
  - PRODUCT es consultor (lectura de datos)
  - PAYMENT → ORDER es crítica (crear venta)
  - EVENT BUS para cambios (stock, estado de pedido)
```

---

## 8. RIESGOS Y MITIGACIONES

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAPA DE RIESGOS                              │
└─────────────────────────────────────────────────────────────────┘

RIESGO                    │ PROBABILIDAD │ IMPACTO │ MITIGACIÓN
──────────────────────────┼──────────────┼─────────┼────────────
Transacción fallida       │ ALTA (8/10)  │ CRÍTICO │ Saga Pattern
(pago + stock inconsist.) │              │         │ Outbox Pattern
                          │              │         │ Tests
──────────────────────────┼──────────────┼─────────┼────────────
Webhook Stripe duplicado  │ MEDIA (5/10) │ ALTO    │ Idempotency Key
                          │              │         │ Verificación
──────────────────────────┼──────────────┼─────────┼────────────
Servicio Order caído      │ BAJA (3/10)  │ CRÍTICO │ Circuit Breaker
                          │              │         │ Retry logic
                          │              │         │ Health checks
──────────────────────────┼──────────────┼─────────┼────────────
Data inconsistency        │ MEDIA (6/10) │ ALTO    │ Event sourcing
                          │              │         │ Audit log
──────────────────────────┼──────────────┼─────────┼────────────
Network latency           │ MEDIA (5/10) │ MEDIO   │ Caching
                          │              │         │ Rate limiting
──────────────────────────┼──────────────┼─────────┼────────────
Secret leak               │ BAJA (2/10)  │ CRÍTICO │ Vault/Secrets Mgr
                          │              │         │ Rotation policy
──────────────────────────┼──────────────┼─────────┼────────────
Database corruption       │ MUY BAJA (1%)│ CRÍTICO │ Backups
                          │              │         │ Replication
                          │              │         │ WAL archiving
──────────────────────────┼──────────────┼─────────┼────────────
Service discovery failure │ BAJA (2/10)  │ ALTO    │ Consul/K8s
                          │              │         │ Fallback DNS
──────────────────────────┼──────────────┼─────────┼────────────
Capacity overload         │ MEDIA (4/10) │ MEDIO   │ Auto-scaling
                          │              │         │ Load balancer
                          │              │         │ Rate limiting

MATRIZ DE RIESGOS:
   ▲
   │
 C │    [Transacción Fallida]
 R │    [Data Inconsistency]
 Í │         [Webhook Dup]
 T │         [Service Down]      [Latency]
 I │                              
 C │    [Secret Leak]
 O │        [DB Corruption]
   │    [Service Discovery]     [Capacity]
   │
   └──────────────────────────────────────▶
       PROBABILIDAD
       
Prioridad de Mitigación:
  1️⃣ Transacción Fallida (arriba-derecha)
  2️⃣ Data Inconsistency
  3️⃣ Webhook Duplicado
  4️⃣ Service Down
```

---

## 9. COSTO-BENEFICIO ANÁLISIS

### **Inversión Inicial**

```
CONCEPTO                    │ COSTO     │ DURACIÓN     │ NOTAS
────────────────────────────┼───────────┼──────────────┼─────────────
Personal (5 FTE)            │ $150k     │ 5-6 meses    │ 5 people
Infrastructure Setup        │ $20k      │ 1-2 semanas  │ Servidores
Herramientas (Kong, ELK)    │ $10k      │ Mensual      │ SaaS o self
Testing/QA                  │ $30k      │ 4 semanas    │ Automación
Contingency (10%)           │ $21k      │ -            │ Buffer
────────────────────────────┼───────────┼──────────────┼─────────────
TOTAL INICIAL               │ $231k     │ 5-6 meses    │
────────────────────────────┴───────────┴──────────────┴─────────────

COSTO MENSUAL OPERACIÓN:
  - Infraestructura (AWS/GCP)  : $3k
  - Personal DevOps            : $15k
  - Herramientas/SaaS          : $2k
  - Monitoring/Alerting        : $1k
  ────────────────────────────────────
  TOTAL MENSUAL               : $21k
```

### **Beneficios Esperados**

```
BENEFICIO                   │ ESTIMADO  │ TIMING       │ NOTAS
────────────────────────────┼───────────┼──────────────┼──────────────
Reducción de Outages        │ -60%      │ Año 1+       │ Menos downtime
Escalabilidad (Revenue)     │ +5-10x    │ Año 1-2      │ Más clientes
Time-to-Market Mejora       │ +40%      │ Después M3   │ Deploy rápido
Retención de Talento        │ +30%      │ Inmediato    │ Mejor arquitectura
Costos Infra Optimizados    │ -20%      │ Año 1+       │ Escala exacta
────────────────────────────┼───────────┼──────────────┼──────────────

BREAK-EVEN: ~8-10 meses (suponiendo revenue crecimiento 5-10%)

ROI PROYECTADO:
  Año 1: 0% (inversión inicial)
  Año 2: 150% (mejoras operacionales)
  Año 3+: 300%+ (escala y eficiencia)
```

---

## 10. CHECKLIST DE IMPLEMENTACIÓN

### **FASE 1: Preparación (Semana 1)**

- [ ] Aprobación arquitectura y presupuesto
- [ ] Crear repositories en GitHub
- [ ] Setup CI/CD pipeline básico
- [ ] Crear Docker images base (Python/Node)
- [ ] Setup MySQL/Redis/RabbitMQ en docker-compose
- [ ] Documentar API contracts
- [ ] Crear ambientes: Dev, Staging, Prod
- [ ] Setup monitoring (Prometheus, Grafana)
- [ ] Crear secret management (Vault o AWS Secrets)

### **FASE 2: AUTH SERVICE (Semana 2-3)**

- [ ] Implementar endpoints REST
- [ ] JWT token generation (RS256)
- [ ] Password hashing (bcrypt)
- [ ] Email service (SendGrid)
- [ ] Tests unitarios (95%+ coverage)
- [ ] Tests de integración
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Deployment a Staging
- [ ] Load testing
- [ ] Security review

### **FASE 3: PRODUCT SERVICE (Semana 4-6)**

- [ ] Django REST Framework setup
- [ ] Modelos duplicados desde monolito
- [ ] Serializers y ViewSets
- [ ] Event publisher (RabbitMQ)
- [ ] Cache layer (Redis)
- [ ] Search/Filter implementation
- [ ] Tests (90%+ coverage)
- [ ] Data migration script
- [ ] Dual-write (write to both DBs)
- [ ] Staging deployment

### **FASE 4: PAYMENT SERVICE (Semana 7-9)**

- [ ] Stripe integration review
- [ ] Saga pattern implementation
- [ ] Idempotency key handling
- [ ] Event consumer (escuchar payment.succeeded)
- [ ] Circuit breaker implementation
- [ ] Webhook processing
- [ ] Transaction logging/audit
- [ ] Tests de saga (success, failure, retry)
- [ ] Chaos engineering tests
- [ ] Load testing (1000+ req/min)
- [ ] Staging deployment

### **FASE 5: Servicios Complementarios (Semana 10-12)**

- [ ] CART SERVICE
  - [ ] Endpoints CRUD
  - [ ] Persistence layer
  - [ ] Tests
  - [ ] Deployment

- [ ] ORDER SERVICE
  - [ ] Crear desde Payment Service
  - [ ] State machine implementation
  - [ ] Tests transaccionales
  - [ ] Reporting views

- [ ] DELIVERY SERVICE
  - [ ] Endpoints de delivery
  - [ ] Driver assignment
  - [ ] Tracking

- [ ] CHAT SERVICE
  - [ ] WebSocket implementation
  - [ ] Gemini integration
  - [ ] Queue M/M/1
  - [ ] Tests end-to-end

### **FASE 6: Frontend & Gateway (Semana 13-15)**

- [ ] API Gateway (Kong) configuration
- [ ] React SPA scaffolding
- [ ] Authentication flow (JWT)
- [ ] Pages implementation
- [ ] Error handling
- [ ] Loading states
- [ ] Responsive design
- [ ] E2E tests (Cypress/Playwright)

### **FASE 7: Testing & Launch (Semana 16+)**

- [ ] Integration tests (todos los servicios)
- [ ] Smoke tests
- [ ] Performance tests
- [ ] Security audit
- [ ] Data validation
- [ ] Cutover plan
- [ ] Rollback plan
- [ ] Launch
- [ ] Monitoring intenso (primeros días)
- [ ] Deprecación del monolito

---

## 11. DECISIONES ARQUITECTÓNICAS CLAVE

### **ADR-001: Usar Saga Pattern para Transacciones**

**Estado**: Propuesto  
**Contexto**: Pagos requieren atomicidad entre servicios  
**Decisión**: Implementar Saga Orchestration (vs Choreography)  
**Consecuencias**:
- ✅ Lógica centralizada en Payment Service
- ❌ Más complejo que monolito
- ❌ Eventual consistency

### **ADR-002: JWT Tokens en lugar de Sessions**

**Estado**: Propuesto  
**Decisión**: Usar RS256 con API Gateway validation  
**Consecuencias**:
- ✅ Stateless auth
- ✅ Escalable
- ❌ Token revocation es lento (cache)

### **ADR-003: Event Bus Asincrónico**

**Estado**: Propuesto  
**Decisión**: RabbitMQ (inicial) → Kafka (futuro)  
**Consecuencias**:
- ✅ Desacoplamiento
- ✅ Escalabilidad
- ❌ Eventual consistency
- ❌ Complexidad operacional

### **ADR-004: Database per Service**

**Estado**: Propuesto  
**Decisión**: Cada servicio tiene su propia BD  
**Excepciones**: Shared data (usuarios, productos) en replicas  
**Consecuencias**:
- ✅ Independencia
- ✅ Escalabilidad
- ❌ Denormalización
- ❌ Data duplication

---

**Documento Generado**: 2026-06-11  
**Versión**: 1.0  
**Estado**: ✅ Visualizaciones Completas
