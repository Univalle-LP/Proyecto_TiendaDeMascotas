# 📋 Historial de Cambios (CHANGELOG)

Todos los cambios importantes en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y este proyecto respeta [Versionado Semántico](https://semver.org/lang/es/).

---

## [Unreleased]

<!-- Cambios que no están en release todavía -->

### Planeado
- Sistema de caché Redis para productos
- Integración con más proveedores de pago
- Dashboard avanzado con gráficos
- Sistema de recomendaciones con IA
- Mobile app nativa

---

## [1.0.0] - 2026-06-20

### ✨ Agregado

#### Sistema de Auditoría Completo
- **Nuevo modelo `AuditLog`** en app `auditoria`
  - Campos: id, usuario, fecha_hora, accion, entidad, descripcion
  - 8 tipos de acciones: LOGIN, LOGOUT, CREATE, UPDATE, DELETE, VIEW, ERROR, OTHER
  - 3 índices compuestos para optimización de búsquedas
  - Tabla en DB: `audit_logs`

#### Auditoría de Autenticación
- Registro automático de **LOGIN** en `usuarios/views.py`
  - Se registra usuario, fecha/hora y éxito/fracaso
  - Función helper: `registrar_auditoria_login(usuario)`
- Registro automático de **LOGOUT**
  - Se registra usuario y fecha/hora
  - Función helper: `registrar_auditoria_logout(usuario)`

#### Auditoría de Operaciones CRUD
- **CREATE auditing**: Registro automático al crear entidades
  - Integrado en: `producto_create()`, `categoria_create()`, `register()`, `empleado_create()`, `chat_send()`
  - Función helper: `registrar_auditoria_crear(usuario, entidad, nombre, detalles)`
  
- **UPDATE auditing**: Registro automático al modificar datos
  - Integrado en: `producto_update()`, `categoria_update()`, `perfil()`, `cambiar_contrasena_cliente()`, `procesar_cola()`
  - Función helper: `registrar_auditoria_actualizar(usuario, entidad, nombre, cambios)`
  
- **DELETE auditing**: Código listo para eliminaciones
  - Función helper: `registrar_auditoria_eliminar(usuario, entidad, nombre, razon)`
  - Integración pendiente en vistas de eliminación

#### Django Admin Interface
- Panel administrativo para auditoría
- Filtros por: acción, entidad, fecha/hora
- Búsqueda por usuario y entidad
- Campos readonly (logs inmutables)
- Permisos: solo superuser puede eliminar, solo lectura para otros

#### Documentación de API
- **DOCUMENTACION_API.md**: 54 endpoints completamente documentados
  - Rutas, métodos HTTP, parámetros con ejemplos JSON
  - Respuestas esperadas, validaciones, autenticación requerida
  - Códigos de estado HTTP
  - Notas sobre auditoría

- **GUIA_RAPIDA_ENDPOINTS.md**: Tablas de referencia rápida
  - Endpoints por categoría (Autenticación, Productos, etc)
  - Distribución por nivel de autenticación
  - Formatos de datos comunes

- **EJEMPLOS_ENDPOINTS.md**: 21+ ejemplos prácticos
  - Ejemplos en cURL, Python (requests), JavaScript (fetch)
  - Cliente API vanilla JavaScript
  - Casos de uso comunes paso a paso

- **INDICE_DOCUMENTACION.md**: Guía de navegación
  - Mapa por rol (Cliente, Empleado, Admin)
  - Estadísticas (54 endpoints, 100+ funciones)
  - Checklist de uso

#### GitHub Workflow Infrastructure
- **PULL_REQUEST_TEMPLATE.md**
  - 8 tipos de cambio (bug, feature, docs, refactor, performance, security, database, testing)
  - Descripción, issue relacionado, cambios principales
  - Evidencias y testing
  - Checklist de 8 categorías (Código, Seguridad, BD, Performance, Docs, Frontend, Backend, Auditoría)
  - Deploy notes, reviewers sugeridos

- **PR_GUIDELINES.md** (350+ líneas)
  - Antes de crear PR: actualizar rama, tests, linter
  - Escribiendo PRs efectivos: títulos, descripciones, issue linking
  - Evidencias por tipo de cambio
  - Testing (unitarios, cobertura ≥80%)
  - Tipos de cambios con ejemplos
  - Qué evitar (PRs grandes, sin tests, sin docs)
  - Durante la revisión (autor y revisor)
  - Flujo completo paso a paso

#### GitHub Issue Templates
- **bug_report.md**: Reportar bugs
  - Descripción, pasos para reproducir
  - Resultado esperado vs actual
  - Prioridad y responsable
  - Evidencias (capturas, logs)

- **feature_request.md**: Solicitar features
  - Descripción, problema que resuelve
  - Solución propuesta
  - Impacto (campos, BD, UI)
  - Criterios de aceptación
  - Prioridad y responsable

- **documentation.md**: Mejoras de documentación
  - Qué documentación necesita mejora
  - Problema actual y solución
  - Propuesta de texto
  - Prioridad y responsable

- **general.md**: Preguntas, discusiones
  - Descripción general
  - Pasos para reproducir (si aplica)
  - Prioridad y responsable
  - Contexto adicional

- **config.yml**: Configuración de templates
  - Auto-relleno automático
  - Links a Discussions, Documentación, Seguridad

#### Guía de Contribución
- **CONTRIBUTING.md** (400+ líneas)
  - Setup inicial (venv, .env, dependencias)
  - Seleccionar tareas (issues, roadmap)
  - Estructura del código y estilo (PEP 8, Black, Flake8)
  - Commits descriptivos con tipo/scope
  - Nombres de ramas
  - Testing (escribir tests, cobertura ≥80%)
  - Documentación (docstrings, comentarios)
  - Seguridad (validaciones, reportar vulnerabilidades)
  - Abriendo PRs (checklist completo)
  - Código de conducta

#### Configuración de Entorno
- **.env**: Variables de entorno para credenciales
  - DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
  - Cargado en `manage.py` y `adonai/settings.py` con dotenv

- **adonai/settings.py**: Actualizado con dotenv
  - Carga .env al iniciar
  - 'auditoria' agregada a INSTALLED_APPS

---

### 🔄 Modificado

#### Apps Existentes
- **usuarios/views.py**
  - Integración de `registrar_auditoria_login()` en `custom_login()`
  - Integración de `registrar_auditoria_logout()` en `custom_logout()`
  - Integración de `registrar_auditoria_crear()` en `register()`
  - Integración de `registrar_auditoria_actualizar()` en `perfil()` y `cambiar_contrasena_cliente()`
  - Try-except wrappers para audit functions (fallback None)

- **productos/views_admin.py**
  - Integración de `registrar_auditoria_crear()` en 3 puntos
  - Integración de `registrar_auditoria_actualizar()` en 2 puntos
  - Try-except wrappers para audit functions

- **chat/views.py**
  - Integración de `registrar_auditoria_crear()` en `chat_send()` y `chat_personalizado()`
  - Integración de `registrar_auditoria_actualizar()` en `procesar_cola()`
  - Try-except wrappers para audit functions

#### Configuración Django
- **adonai/settings.py**
  - Import de `dotenv` y `load_dotenv`
  - Carga de variables de entorno desde .env
  - App 'auditoria' agregada a INSTALLED_APPS
  - Credenciales de BD desde os.environ

---

### 🐛 Corregido

#### Base de Datos
- Migraciones iniciales para `auditoria` app creadas
- Tabla `audit_logs` con estructura correcta
- Índices compuestos para optimización de búsquedas

#### Carga de Credenciales
- Problema: "Access denied for user 'root'@'localhost' (using password: NO)"
- Solución: Dotenv loading en import time (ambos manage.py y settings.py)
- Resultado: Credenciales ahora se cargan correctamente antes de Django init

#### Importación de Funciones de Auditoría
- Problema: ModuleNotFoundError al importar `auditoria.utils`
- Solución: Try-except wrappers con fallback None
- Resultado: Si auditoria falla, user flow continúa sin interrupciones

#### Duplicación de Emails en Tests
- Problema: test_auditlog_update.py causaba error de unique constraint
- Solución: Usar timestamps/counters para emails únicos en tests
- Resultado: Tests pueden correrse múltiples veces sin conflictos

#### Missing Django App Registration
- Problema: 'auditoria' no registrada en INSTALLED_APPS
- Solución: Agregada a INSTALLED_APPS entre 'pagos' y 'django.contrib.sites'
- Resultado: App reconocida por Django, migrations funcionan

---

## [0.9.0] - 2026-05-15

### ✨ Agregado

#### Dashboard y Reportes Iniciales
- Vista de dashboard con resumen de ventas
- Gráficos básicos de productos más vendidos
- Resumen de usuarios registrados
- Panel de control de inventario

#### Sistema de Pagos Stripe
- Integración completa con Stripe
- Webhooks para eventos de pago
- Validación de cupones
- Historial de transacciones

#### Sistema de Chat con IA
- Integración con Gemini AI
- Chat en tiempo real entre usuarios y empleados
- Sistema de colas M/M/1 para atención
- Historial de conversaciones

#### Sistema de Carrito
- Agregar/quitar productos del carrito
- Cálculo de totales
- Aplicar cupones de descuento
- Persistencia en BD

#### Roles y Permisos
- Roles: Cliente, Empleado, Administrador
- Permisos granulares por rol
- Admin panel para gestión de permisos

### 🔄 Modificado

#### Modelo de Usuarios
- Agregados campos de perfil
- Integración con roles
- Campos de dirección para envíos

#### Estructura de Productos
- Categorías para productos
- Atributos adicionales (color, tamaño, etc)
- Imágenes de productos
- Stock management

### 🐛 Corregido

#### Autenticación
- Problema con reset de contraseña
- Validación de emails duplicados
- Logout no funciona correctamente

#### Pagos
- Webhooks de Stripe no se procesaban
- Validación de cupones incompleta
- Transacciones huérfanas

#### Chat
- Notificaciones perdidas en chat
- Colas no procesaban correctamente
- Timeouts en conexiones

---

## Convenciones de Versionado

Este proyecto utiliza **Versionado Semántico 2.0.0**:

- **MAJOR** (1.0.0): Cambios incompatibles en la API
- **MINOR** (1.1.0): Nueva funcionalidad compatible
- **PATCH** (1.0.1): Correcciones de bugs

### Formato de Lanzamiento

```
[Versión] - YYYY-MM-DD

### ✨ Agregado
- Nueva funcionalidad

### 🔄 Modificado
- Cambios a funcionalidad existente

### 🐛 Corregido
- Fixes de bugs

### ⚠️ Deprecado
- Funcionalidad a remover pronto

### 🗑️ Removido
- Funcionalidad removida

### 🔐 Seguridad
- Fixes de seguridad
```

---

## Cómo Contribuir

### Documentar Cambios

Cuando hagas cambios, actualiza este archivo:

1. Agrega la sección `[Unreleased]` si no existe
2. Categoriza tu cambio: Agregado, Modificado, Corregido, etc
3. Describe el cambio de forma clara
4. Incluye detalles técnicos si es relevante
5. Haz un commit separado para el changelog

### Ejemplo de Commit

```bash
git add CHANGELOG.md
git commit -m "docs: agregar cambios a CHANGELOG para feature X"
```

---

## Timeline de Lanzamientos

| Versión | Fecha | Estado |
|---------|-------|--------|
| 1.0.0 | 2026-06-20 | ✅ Lanzada |
| 0.9.0 | 2026-05-15 | ✅ Archivada |
| 1.1.0 | Planificado | 🔄 En desarrollo |
| 2.0.0 | Planificado | 📋 Análisis |

---

## Estadísticas

### Versión 1.0.0

| Métrica | Cantidad |
|---------|----------|
| Nuevas features | 8 |
| Bugfixes | 5 |
| Archivos documentados | 4 |
| Líneas de documentación | 2000+ |
| Endpoints documentados | 54 |
| Tests incluidos | 10+ |
| Templates GitHub | 6 |

---

## Notas Importantes

### Para Desarrolladores

- 🔄 Actualiza CHANGELOG.md con cada cambio importante
- 🎯 Sé descriptivo pero conciso
- 🏷️ Categoriza correctamente
- 📝 Incluye ejemplos de código si es necesario

### Para Users

- 📖 Lee las notas de ruptura (Breaking Changes)
- 🔐 Revisa fixes de seguridad
- 📦 Actualiza siguiendo las instrucciones
- 💬 Reporta problemas en Issues

---

## Referencias

- [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
- [Versionado Semántico](https://semver.org/lang/es/)
- [Conventional Commits](https://www.conventionalcommits.org/es)

---

## Contacto

Para preguntas sobre el changelog:

- 📧 Email: development@example.com
- 💬 Discussions: https://github.com/Univalle-LP/Proyecto_TiendaDeMascotas/discussions
- 🐛 Issues: https://github.com/Univalle-LP/Proyecto_TiendaDeMascotas/issues

---

**Última actualización**: 2026-06-20  
**Mantenedor**: Equipo de Desarrollo  
**Licencia**: MIT
