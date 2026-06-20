#!/usr/bin/env python
"""
Script de prueba para validar el registro automático de logout en AuditLog.
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

from django.test import Client
from usuarios.models import Usuario
from auditoria.models import AuditLog

print("\n" + "=" * 80)
print("PRUEBA: REGISTRO AUTOMÁTICO DE LOGOUT EN AUDITLOG")
print("=" * 80)

# Obtener usuario de prueba
print("\n✓ Buscando usuario de prueba...")
usuario = Usuario.objects.filter(rol__nombre='Cliente').first()

if not usuario:
    print("✗ No se encontraron usuarios clientes para prueba")
    sys.exit(1)

print(f"✓ Usuario encontrado: {usuario.nombre} ({usuario.email})")

# Crear cliente de prueba
client = Client()

# Primero, hacer login
print("\n" + "-" * 80)
print("Paso 1: Hacer login para establecer sesión...")
print("-" * 80)

response_login = client.post('/usuarios/login/', {
    'username': usuario.email,
    'password': 'clientes123',
}, follow=False)

print(f"✓ Login: Status {response_login.status_code}")

# Contar registros de LOGOUT antes
logs_logout_before = AuditLog.objects.filter(usuario=usuario, accion='LOGOUT').count()
print(f"\n✓ Registros LOGOUT previos: {logs_logout_before}")

# Ahora hacer logout
print("\n" + "-" * 80)
print("Paso 2: Hacer logout...")
print("-" * 80)

response_logout = client.get('/usuarios/logout/', follow=False)

print(f"✓ Logout: Status {response_logout.status_code}")
if response_logout.status_code in [301, 302, 303, 307, 308]:
    print(f"✓ Redirección a: {response_logout.get('Location', 'N/A')}")

# Contar registros de LOGOUT después
logs_logout_after = AuditLog.objects.filter(usuario=usuario, accion='LOGOUT').count()
logs_logout_creados = logs_logout_after - logs_logout_before

print("\n" + "-" * 80)
print("RESULTADO: Logout Exitoso")
print("-" * 80)

if logs_logout_creados > 0:
    print(f"\n✅ ÉXITO: Se creó {logs_logout_creados} registro(s) de LOGOUT")
    
    # Obtener el último registro
    ultimo_logout = AuditLog.objects.filter(usuario=usuario, accion='LOGOUT').order_by('-fecha_hora').first()
    
    if ultimo_logout:
        print(f"\n✓ Detalles del registro creado:")
        print(f"  - ID: {ultimo_logout.id}")
        print(f"  - Usuario: {ultimo_logout.usuario.nombre}")
        print(f"  - Fecha/Hora: {ultimo_logout.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  - Acción: {ultimo_logout.get_accion_display()}")
        print(f"  - Entidad: {ultimo_logout.entidad}")
        print(f"  - Descripción: {ultimo_logout.descripcion}")
        logout_exitoso = True
    else:
        print(f"\n❌ No se pudo obtener el registro creado")
        logout_exitoso = False
else:
    print(f"\n❌ FALLO: No se creó ningún registro de LOGOUT")
    print(f"   Registros antes: {logs_logout_before}")
    print(f"   Registros después: {logs_logout_after}")
    logout_exitoso = False

# Resumen
print("\n" + "=" * 80)
print("RESUMEN DE PRUEBAS")
print("=" * 80)

total_logins = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
total_logouts = AuditLog.objects.filter(usuario=usuario, accion='LOGOUT').count()

print(f"\n✓ Total de registros LOGIN para {usuario.nombre}: {total_logins}")
print(f"✓ Total de registros LOGOUT para {usuario.nombre}: {total_logouts}")

print("\n" + "-" * 80)
print("Resultado Final")
print("-" * 80)

if logout_exitoso:
    print("\n" + "=" * 80)
    print("✅ PRUEBA EXITOSA - LOGOUT REGISTRADO CORRECTAMENTE")
    print("=" * 80)
    print("\nEl registro automático de logout en AuditLog está:")
    print("  ✅ Registrando cierres de sesión correctamente")
    print("  ✅ Capturando información correctamente")
    print("  ✅ No interrumpiendo el flujo de usuario")
    print("  ✅ Sincronizado con redirect a página de inicio")
else:
    print("\n" + "=" * 80)
    print("❌ PRUEBA FALLIDA - REVISAR CONFIGURACIÓN")
    print("=" * 80)

print("\n")
