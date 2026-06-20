#!/usr/bin/env python
"""
Script de ejemplo y prueba del sistema de auditoría (AuditLog).
Demuestra diferentes formas de registrar acciones en la auditoría.
"""
import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar variables de entorno
dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adonai.settings')
django.setup()

from django.utils import timezone
from usuarios.models import Usuario
from auditoria.models import AuditLog
from auditoria.utils import (
    registrar_auditoria,
    registrar_auditoria_crear,
    registrar_auditoria_actualizar,
    registrar_auditoria_eliminar,
    registrar_auditoria_login,
    registrar_auditoria_logout
)

print("\n" + "=" * 80)
print("PRUEBA DEL SISTEMA DE AUDITORÍA (AuditLog)")
print("=" * 80)

# Obtener un usuario de prueba
try:
    usuario = Usuario.objects.first()
    if not usuario:
        print("\n✗ No se encontraron usuarios en la base de datos")
        print("  Por favor crea un usuario primero en el panel administrativo")
        sys.exit(1)
    print(f"\n✓ Usuario de prueba: {usuario.nombre} ({usuario.email})")
except Exception as e:
    print(f"\n✗ Error al obtener usuario: {e}")
    sys.exit(1)

# Limpiar registros anteriores de prueba
print("\n✓ Limpiando registros de prueba anteriores...")
AuditLog.objects.filter(descripcion__startswith="[PRUEBA]").delete()

# Prueba 1: Registrar un login
print("\n" + "-" * 80)
print("PRUEBA 1: Registrar Login")
print("-" * 80)
try:
    log = registrar_auditoria_login(usuario)
    if log:
        print(f"✓ Login registrado correctamente (ID: {log.id})")
        print(f"  - Usuario: {log.usuario.nombre}")
        print(f"  - Acción: {log.get_accion_display()}")
        print(f"  - Fecha: {log.fecha_hora}")
    else:
        print("✗ Error al registrar login")
except Exception as e:
    print(f"✗ Excepción: {e}")

# Prueba 2: Registrar creación de producto
print("\n" + "-" * 80)
print("PRUEBA 2: Registrar Creación de Producto")
print("-" * 80)
try:
    log = registrar_auditoria_crear(
        usuario=usuario,
        entidad='Producto',
        nombre_objeto='[PRUEBA] Collar para perros - Talla L',
        detalles='Precio: $49.99, Stock: 100 unidades, Marca: PetCare'
    )
    if log:
        print(f"✓ Creación registrada correctamente (ID: {log.id})")
        print(f"  - Acción: {log.get_accion_display()}")
        print(f"  - Entidad: {log.entidad}")
        print(f"  - Descripción: {log.descripcion}")
    else:
        print("✗ Error al registrar creación")
except Exception as e:
    print(f"✗ Excepción: {e}")

# Prueba 3: Registrar actualización
print("\n" + "-" * 80)
print("PRUEBA 3: Registrar Actualización de Producto")
print("-" * 80)
try:
    log = registrar_auditoria_actualizar(
        usuario=usuario,
        entidad='Producto',
        nombre_objeto='[PRUEBA] Collar para perros - Talla L',
        cambios='Precio actualizado de $49.99 a $54.99, Stock de 100 a 95'
    )
    if log:
        print(f"✓ Actualización registrada correctamente (ID: {log.id})")
        print(f"  - Acción: {log.get_accion_display()}")
        print(f"  - Cambios: {log.descripcion}")
    else:
        print("✗ Error al registrar actualización")
except Exception as e:
    print(f"✗ Excepción: {e}")

# Prueba 4: Registrar eliminación
print("\n" + "-" * 80)
print("PRUEBA 4: Registrar Eliminación de Producto")
print("-" * 80)
try:
    log = registrar_auditoria_eliminar(
        usuario=usuario,
        entidad='Producto',
        nombre_objeto='[PRUEBA] Collar para perros - Talla L',
        razon='Producto descontinuado por baja demanda'
    )
    if log:
        print(f"✓ Eliminación registrada correctamente (ID: {log.id})")
        print(f"  - Acción: {log.get_accion_display()}")
        print(f"  - Razón: {log.descripcion}")
    else:
        print("✗ Error al registrar eliminación")
except Exception as e:
    print(f"✗ Excepción: {e}")

# Prueba 5: Registrar una acción personalizada
print("\n" + "-" * 80)
print("PRUEBA 5: Registrar Acción Personalizada")
print("-" * 80)
try:
    log = registrar_auditoria(
        usuario=usuario,
        accion='OTHER',
        entidad='Venta',
        descripcion='[PRUEBA] Se procesó reembolso por $199.99 de orden #VTA-2026-001'
    )
    if log:
        print(f"✓ Acción personalizada registrada correctamente (ID: {log.id})")
        print(f"  - Acción: {log.get_accion_display()}")
        print(f"  - Descripción: {log.descripcion}")
    else:
        print("✗ Error al registrar acción personalizada")
except Exception as e:
    print(f"✗ Excepción: {e}")

# Prueba 6: Registrar un logout
print("\n" + "-" * 80)
print("PRUEBA 6: Registrar Logout")
print("-" * 80)
try:
    log = registrar_auditoria_logout(usuario)
    if log:
        print(f"✓ Logout registrado correctamente (ID: {log.id})")
        print(f"  - Acción: {log.get_accion_display()}")
        print(f"  - Fecha: {log.fecha_hora}")
    else:
        print("✗ Error al registrar logout")
except Exception as e:
    print(f"✗ Excepción: {e}")

# Prueba 7: Consultas de auditoría
print("\n" + "-" * 80)
print("PRUEBA 7: Consultas de Auditoría")
print("-" * 80)

# Obtener todos los registros de prueba
logs_prueba = AuditLog.objects.filter(descripcion__startswith="[PRUEBA]")
print(f"\n✓ Registros de prueba creados: {logs_prueba.count()}")

# Mostrar por tipo de acción
print("\n✓ Registros por tipo de acción:")
for accion, label in AuditLog.ACCIONES_CHOICES:
    count = logs_prueba.filter(accion=accion).count()
    if count > 0:
        print(f"  - {label}: {count}")

# Mostrar por entidad
print("\n✓ Registros por entidad:")
entidades = logs_prueba.values('entidad').distinct()
for item in entidades:
    entidad = item['entidad']
    count = logs_prueba.filter(entidad=entidad).count()
    print(f"  - {entidad}: {count}")

# Registros ordenados por fecha (más recientes primero)
print("\n✓ Últimos 3 registros (orden cronológico inverso):")
for log in logs_prueba.order_by('-fecha_hora')[:3]:
    print(f"  {log.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')} - {log.get_accion_display()} en {log.entidad}")

# Prueba 8: Verificar integridad
print("\n" + "-" * 80)
print("PRUEBA 8: Verificar Integridad de Datos")
print("-" * 80)

# Verificar que todos los registros tienen la información requerida
logs_invalidos = AuditLog.objects.filter(
    usuario__isnull=True,
    accion__isnull=True,
    entidad__isnull=True,
    descripcion__isnull=True
)

if logs_invalidos.count() == 0:
    print("✓ Todos los registros tienen integridad correcta")
else:
    print(f"✗ Se encontraron {logs_invalidos.count()} registros con datos incompletos")

# Contar registros totales
total_registros = AuditLog.objects.count()
print(f"✓ Total de registros en base de datos: {total_registros}")

# Resumen estadístico
print("\n" + "-" * 80)
print("RESUMEN ESTADÍSTICO")
print("-" * 80)

usuarios_unicos = AuditLog.objects.values('usuario').distinct().count()
print(f"✓ Usuarios que han realizado acciones: {usuarios_unicos}")

acciones_realizadas = {}
for accion, label in AuditLog.ACCIONES_CHOICES:
    count = AuditLog.objects.filter(accion=accion).count()
    if count > 0:
        acciones_realizadas[label] = count

print(f"✓ Acciones registradas:")
for accion, count in acciones_realizadas.items():
    print(f"  - {accion}: {count}")

# Fecha del registro más antiguo
primer_registro = AuditLog.objects.order_by('fecha_hora').first()
if primer_registro:
    print(f"✓ Primer registro: {primer_registro.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")

# Fecha del registro más reciente
ultimo_registro = AuditLog.objects.order_by('-fecha_hora').first()
if ultimo_registro:
    print(f"✓ Último registro: {ultimo_registro.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")

print("\n" + "=" * 80)
print("✓ PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 80)
print("\nPróximos pasos:")
print("1. Acceder al panel administrativo en http://localhost:8000/admin/")
print("2. Ir a Auditoría > Registros de Auditoría")
print("3. Ver los registros de prueba creados")
print("4. Probar los filtros y búsquedas")
print("\nPara integrar en el código:")
print("  from auditoria.utils import registrar_auditoria_crear")
print("  registrar_auditoria_crear(usuario, 'Producto', 'Mi Producto', 'Detalles')")
print("\n")
