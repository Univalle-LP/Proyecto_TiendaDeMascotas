#!/usr/bin/env python
"""
Script de prueba para validar el registro automático de login en AuditLog.
Simula un login y verifica que se registró correctamente.
"""
import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adonai.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from usuarios.models import Usuario
from auditoria.models import AuditLog
from usuarios.views import custom_login

print("\n" + "=" * 80)
print("PRUEBA: REGISTRO AUTOMÁTICO DE LOGIN EN AUDITLOG")
print("=" * 80)

# Obtener un usuario existente
print("\n✓ Buscando usuario de prueba...")
usuario = Usuario.objects.filter(rol__nombre='Cliente').first()

if not usuario:
    print("✗ No se encontraron usuarios clientes para prueba")
    sys.exit(1)

print(f"✓ Usuario encontrado: {usuario.nombre} ({usuario.email})")

# Verificar que exista el usuario en auth
auth_user = User.objects.filter(username=usuario.email.lower()).first()
if not auth_user:
    print("✗ Usuario no encontrado en django.contrib.auth")
    sys.exit(1)

print(f"✓ Usuario de auth encontrado: {auth_user.username}")

# Contar registros de AuditLog antes
logs_before = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
print(f"\n✓ Registros de LOGIN previos para este usuario: {logs_before}")

# Simular un POST de login
print("\n" + "-" * 80)
print("Simulando POST de login...")
print("-" * 80)

factory = RequestFactory()
request = factory.post('/usuarios/login/', {
    'username': usuario.email,
    'password': 'clientes123',  # Contraseña default
})
request.session = {}

try:
    # Ejecutar la vista de login
    response = custom_login(request)
    print(f"✓ Vista de login ejecutada")
    print(f"✓ Redirección: {response.url if hasattr(response, 'url') else 'Sin redirección'}")
except Exception as e:
    print(f"⚠ Vista retornó excepción (esperado en algunas casos): {type(e).__name__}")

# Contar registros de AuditLog después
logs_after = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
logs_creados = logs_after - logs_before

print("\n" + "-" * 80)
print("Resultado de la Prueba")
print("-" * 80)

if logs_creados > 0:
    print(f"\n✅ ÉXITO: Se crearon {logs_creados} nuevo(s) registro(s) de LOGIN")
    
    # Obtener los últimos registros
    ultimo_login = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').order_by('-fecha_hora').first()
    
    if ultimo_login:
        print(f"\n✓ Detalles del registro creado:")
        print(f"  - ID: {ultimo_login.id}")
        print(f"  - Usuario: {ultimo_login.usuario.nombre}")
        print(f"  - Fecha/Hora: {ultimo_login.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  - Acción: {ultimo_login.get_accion_display()}")
        print(f"  - Entidad: {ultimo_login.entidad}")
        print(f"  - Descripción: {ultimo_login.descripcion}")
else:
    print(f"\n❌ FALLO: No se creó ningún registro de LOGIN")
    print(f"   Registros antes: {logs_before}")
    print(f"   Registros después: {logs_after}")

# Verificar el formato de la descripción
if logs_creados > 0 and ultimo_login:
    print(f"\n✓ Validación de descripción:")
    if 'inició sesión' in ultimo_login.descripcion.lower():
        print(f"  ✓ Descripción contiene 'inició sesión': {ultimo_login.descripcion}")
    else:
        print(f"  ⚠ Descripción no tiene formato esperado: {ultimo_login.descripcion}")

# Prueba 2: Intentar login con contraseña incorrecta
print("\n" + "-" * 80)
print("PRUEBA 2: Registro de Intento Fallido de Login")
print("-" * 80)

# Contar registros de ERROR antes
errores_before = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').count()
print(f"\n✓ Registros de ERROR previos: {errores_before}")

# Simular un POST de login fallido
request_fallido = factory.post('/usuarios/login/', {
    'username': usuario.email,
    'password': 'contrasena_incorrecta_12345',
})
request_fallido.session = {}

try:
    response = custom_login(request_fallido)
    print(f"✓ Vista de login con fallo ejecutada")
except Exception as e:
    print(f"⚠ Vista retornó excepción: {type(e).__name__}")

# Contar registros de ERROR después
errores_after = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').count()
errores_creados = errores_after - errores_before

print(f"\n✓ Registros de ERROR después: {errores_after}")

if errores_creados > 0:
    print(f"\n✅ ÉXITO: Se registró intento fallido de login")
    
    # Obtener el último error
    ultimo_error = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').order_by('-fecha_hora').first()
    
    if ultimo_error:
        print(f"\n✓ Detalles del registro de error:")
        print(f"  - ID: {ultimo_error.id}")
        print(f"  - Usuario: {ultimo_error.usuario}")
        print(f"  - Fecha/Hora: {ultimo_error.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  - Acción: {ultimo_error.get_accion_display()}")
        print(f"  - Entidad: {ultimo_error.entidad}")
        print(f"  - Descripción: {ultimo_error.descripcion}")
else:
    print(f"\n⚠ No se registró el intento fallido")

# Resumen final
print("\n" + "=" * 80)
print("RESUMEN DE PRUEBAS")
print("=" * 80)

total_logins = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
total_errores = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').count()

print(f"\n✓ Total de registros LOGIN para {usuario.nombre}: {total_logins}")
print(f"✓ Total de registros ERROR en Sesión: {total_errores}")

if logs_creados > 0 and errores_creados > 0:
    print("\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS PASADAS - SISTEMA FUNCIONANDO CORRECTAMENTE")
    print("=" * 80)
    print("\nEl registro automático de login en AuditLog está:")
    print("  ✓ Registrando inicios de sesión exitosos")
    print("  ✓ Registrando intentos fallidos de login")
    print("  ✓ Capturando información correctamente")
    print("  ✓ No interrumpiendo el flujo de usuario")
elif logs_creados > 0:
    print("\n" + "=" * 80)
    print("⚠ PRUEBAS PARCIALES - LOGINS REGISTRADOS, ERRORES NO")
    print("=" * 80)
else:
    print("\n" + "=" * 80)
    print("❌ PRUEBAS FALLIDAS - SISTEMA NO ESTÁ REGISTRANDO LOGINS")
    print("=" * 80)

print("\n")
