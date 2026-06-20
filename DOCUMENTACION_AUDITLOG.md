# Documentación del Sistema de Auditoría (AuditLog)

## Descripción General

El modelo **AuditLog** es un sistema centralizado para registrar todas las acciones realizadas por los usuarios en la plataforma. Esto permite:

- **Trazabilidad**: Rastrear quién hizo qué y cuándo
- **Cumplimiento**: Satisfacer requisitos de auditoría y cumplimiento normativo
- **Seguridad**: Detectar actividades sospechosas o no autorizadas
- **Análisis**: Entender patrones de uso y comportamiento de usuarios

## Estructura del Modelo

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| **id** | BigAutoField | Identificador único (PK, Auto-increment) |
| **usuario** | ForeignKey(Usuario) | Referencia al usuario que realizó la acción (nullable) |
| **fecha_hora** | DateTimeField | Timestamp automático de cuándo ocurrió la acción |
| **accion** | CharField | Tipo de acción realizada (valores predefinidos) |
| **entidad** | CharField | Nombre del modelo/tabla afectada (ej: Producto, Venta) |
| **descripcion** | TextField | Descripción detallada de la acción |

### Acciones Disponibles

```python
ACCIONES_CHOICES = (
    ('CREATE', 'Creación'),      # Creación de registros
    ('UPDATE', 'Actualización'),  # Modificación de registros
    ('DELETE', 'Eliminación'),    # Borrado de registros
    ('VIEW', 'Visualización'),    # Ver información (opcional)
    ('LOGIN', 'Inicio de sesión'),# Acceso al sistema
    ('LOGOUT', 'Cierre de sesión'),# Salida del sistema
    ('ERROR', 'Error'),           # Errores en el sistema
    ('OTHER', 'Otro'),            # Otras acciones
)
```

## Base de Datos

### Información de la Tabla

```
Tabla: audit_logs
Motor: MySQL (InnoDB)
Charset: utf8mb4
```

### Índices Creados

```
1. PRIMARY KEY (id)
   - Identificación única de registros

2. Índice Compuesto: usuario_id + fecha_hora
   - Búsqueda rápida por usuario y rango de fechas

3. Índice Compuesto: accion + fecha_hora
   - Búsqueda rápida por tipo de acción

4. Índice Compuesto: entidad + fecha_hora
   - Búsqueda rápida por entidad/tabla afectada
```

## Panel Administrativo

El modelo está completamente integrado en el panel administrativo de Django (`/admin/`).

### Funcionalidades del Admin

- **Ver registros**: Lista con filtros avanzados
- **Búsqueda**: Por usuario, entidad, acción o descripción
- **Filtros**: Por acción, entidad, fecha, usuario
- **Jerarquía de fechas**: Navegación por año, mes, día
- **Solo lectura**: Los registros no pueden ser modificados desde el admin
- **Eliminación**: Solo superusers pueden eliminar registros

### Columnas Visibles en Lista

```python
list_display = ('usuario', 'accion', 'entidad', 'fecha_hora', 'descripcion_corta')
```

## Uso en el Código

### Método 1: Función Helper Simple

```python
from auditoria.utils import registrar_auditoria

# Registrar una acción genérica
registrar_auditoria(
    usuario=request.user.usuario,
    accion='CREATE',
    entidad='Producto',
    descripcion='Se creó el producto: Collar para perros raza grande'
)
```

### Método 2: Funciones Especializadas

```python
from auditoria.utils import (
    registrar_auditoria_crear,
    registrar_auditoria_actualizar,
    registrar_auditoria_eliminar,
    registrar_auditoria_error
)

# Registrar creación
registrar_auditoria_crear(
    usuario=request.user.usuario,
    entidad='Producto',
    nombre_objeto='Collar para perros',
    detalles='Precio: $45.99, Stock: 100'
)

# Registrar actualización
registrar_auditoria_actualizar(
    usuario=request.user.usuario,
    entidad='Producto',
    nombre_objeto='Collar para perros',
    cambios='Precio actualizado de $45.99 a $49.99'
)

# Registrar eliminación
registrar_auditoria_eliminar(
    usuario=request.user.usuario,
    entidad='Producto',
    nombre_objeto='Collar para perros',
    razon='Producto descontinuado'
)

# Registrar error
registrar_auditoria_error(
    usuario=request.user.usuario,
    entidad='Pago',
    error_msg='Fallo en conexión con Stripe',
    detalles='Timeout después de 30 segundos'
)
```

### Método 3: Login/Logout

```python
from auditoria.utils import registrar_auditoria_login, registrar_auditoria_logout

# En la vista de login después de autenticar
registrar_auditoria_login(usuario=usuario_autenticado)

# En la vista de logout
registrar_auditoria_logout(usuario=request.user.usuario)
```

### Método 4: Creación Directa en Vistas

```python
from auditoria.models import AuditLog

# Crear un registro directamente
AuditLog.objects.create(
    usuario=request.user.usuario,
    accion='CREATE',
    entidad='Venta',
    descripcion=f'Se creó venta #12345 por ${total}'
)
```

## Ejemplo Completo en una Vista

```python
from django.shortcuts import render, redirect
from django.views import View
from auditoria.utils import registrar_auditoria_crear, registrar_auditoria_error
from productos.models import Producto

class CrearProductoView(View):
    def post(self, request):
        try:
            # Procesar formulario
            nombre = request.POST.get('nombre')
            precio = request.POST.get('precio')
            
            # Crear producto
            producto = Producto.objects.create(
                nombre=nombre,
                precio=precio
            )
            
            # Registrar en auditoría
            registrar_auditoria_crear(
                usuario=request.user.usuario,
                entidad='Producto',
                nombre_objeto=nombre,
                detalles=f'Precio: ${precio}'
            )
            
            return redirect('producto_detail', pk=producto.id)
            
        except Exception as e:
            # Registrar error
            registrar_auditoria_error(
                usuario=request.user.usuario,
                entidad='Producto',
                error_msg='Error al crear producto',
                detalles=str(e)
            )
            raise
```

## Consultas Útiles

### Obtener acciones de un usuario

```python
from auditoria.models import AuditLog

# Últimas 10 acciones de un usuario
logs = AuditLog.objects.filter(usuario_id=usuario_id).order_by('-fecha_hora')[:10]

# Acciones en un rango de fechas
from datetime import datetime, timedelta
from django.utils import timezone

hace_7_dias = timezone.now() - timedelta(days=7)
logs = AuditLog.objects.filter(
    usuario_id=usuario_id,
    fecha_hora__gte=hace_7_dias
)
```

### Obtener acciones por tipo

```python
# Todas las creaciones
creaciones = AuditLog.objects.filter(accion='CREATE')

# Todas las eliminaciones
eliminaciones = AuditLog.objects.filter(accion='DELETE')

# Todos los errores
errores = AuditLog.objects.filter(accion='ERROR')
```

### Obtener acciones de una entidad

```python
# Todas las acciones en la tabla Producto
logs = AuditLog.objects.filter(entidad='Producto')

# Últimas 5 modificaciones en Ventas
logs = AuditLog.objects.filter(
    entidad='Venta',
    accion__in=['CREATE', 'UPDATE']
).order_by('-fecha_hora')[:5]
```

## Consideraciones de Rendimiento

### Índices
Los índices están optimizados para las consultas más comunes:
- Búsquedas por usuario
- Búsquedas por acción
- Búsquedas por entidad
- Búsquedas por rango de fechas

### Recomendaciones
1. **Archivar registros antiguos**: Considerar hacer backup y eliminar registros más antiguos de 1 año
2. **Límites de consulta**: Usar `.paginate()` en queries grandes
3. **Caché**: Para reportes frecuentes, considerar usar memcache

## Migración

### Archivos Generados

```
auditoria/
├── migrations/
│   ├── 0001_initial.py      # Migración inicial
│   └── __init__.py
├── __init__.py
├── admin.py                 # Registro en panel admin
├── apps.py
├── models.py               # Definición del modelo
├── tests.py
├── utils.py                # Funciones helper (NUEVO)
├── views.py
└── urls.py
```

### Registros de Migración

```
Database: adonai_store
Migration: auditoria.0001_initial
Status: Applied (OK)
Table: audit_logs
```

## Seguridad

### Protecciones Implementadas

1. **Integridad de datos**: No se pueden modificar registros existentes
2. **Solo lectura**: Los registros son grabados una sola vez (write-once)
3. **Permisos**: Solo superusers pueden eliminar registros
4. **Relación con Usuario**: Permite rastrear el usuario aunque su cuenta sea eliminada (nullable)

## Próximas Mejoras (Opcionales)

- [ ] Señales Django para registrar automáticamente cambios en modelos
- [ ] API REST para consultas de auditoría
- [ ] Dashboard de reportes de auditoría
- [ ] Exportación a CSV/Excel
- [ ] Encriptación de datos sensibles en descripción
- [ ] Sistema de alertas para actividades sospechosas

## Testing

Para probar el modelo:

```bash
# Ejecutar verificación de tabla
python verify_auditlog.py

# Ejecutar verificación de admin
python verify_admin_auditlog.py

# Acceder al admin
python manage.py runserver
# Ir a http://localhost:8000/admin/
```

---

**Última actualización**: 2026-06-20
**Versión**: 1.0
**App**: auditoria
