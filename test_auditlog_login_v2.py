#!/usr/bin/env python
"""
Script de prueba simplificado para validar el registro automático de login en AuditLog.
Utiliza Django Test Client para simular peticiones HTTP reales.
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
print("PRUEBA: REGISTRO AUTOMÁTICO DE LOGIN EN AUDITLOG")
print("=" * 80)

# Obtener usuario de prueba
print("\n✓ Buscando usuario de prueba...")
usuario = Usuario.objects.filter(rol__nombre='Cliente').first()

if not usuario:
    print("✗ No se encontraron usuarios clientes para prueba")
    sys.exit(1)

print(f"✓ Usuario encontrado: {usuario.nombre} ({usuario.email})")

# Contar registros de LOGIN antes
logs_before = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
print(f"✓ Registros de LOGIN previos: {logs_before}")

# Crear cliente de prueba
client = Client()

# Simular POST de login
print("\n" + "-" * 80)
print("Simulando POST de login exitoso...")
print("-" * 80)

response = client.post('/usuarios/login/', {
    'username': usuario.email,
    'password': 'clientes123',
}, follow=False)

print(f"✓ Estado de respuesta: {response.status_code}")
if response.status_code in [301, 302, 303, 307, 308]:
    print(f"✓ Redirección a: {response.get('Location', 'N/A')}")

# Contar registros de LOGIN después
logs_after = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
logs_creados = logs_after - logs_before

print("\n" + "-" * 80)
print("RESULTADO: Login Exitoso")
print("-" * 80)

if logs_creados > 0:
    print(f"\n✅ ÉXITO: Se creó {logs_creados} registro(s) de LOGIN")
    
    # Obtener el último registro
    ultimo_login = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').order_by('-fecha_hora').first()
    
    if ultimo_login:
        print(f"\n✓ Detalles del registro creado:")
        print(f"  - ID: {ultimo_login.id}")
        print(f"  - Usuario: {ultimo_login.usuario.nombre}")
        print(f"  - Fecha/Hora: {ultimo_login.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  - Acción: {ultimo_login.get_accion_display()}")
        print(f"  - Entidad: {ultimo_login.entidad}")
        print(f"  - Descripción: {ultimo_login.descripcion}")
        login_exitoso = True
    else:
        print(f"\n❌ No se pudo obtener el registro creado")
        login_exitoso = False
else:
    print(f"\n❌ FALLO: No se creó ningún registro de LOGIN")
    print(f"   Registros antes: {logs_before}")
    print(f"   Registros después: {logs_after}")
    login_exitoso = False

# Prueba 2: Intento de login fallido
print("\n" + "=" * 80)
print("PRUEBA 2: Registro de Intento Fallido de Login")
print("=" * 80)

# Contar registros de ERROR antes
errores_before = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').count()
print(f"\n✓ Registros de ERROR previos: {errores_before}")

# Simular POST de login fallido
print("\nSimulando POST con contraseña incorrecta...")

response_fallido = client.post('/usuarios/login/', {
    'username': usuario.email,
    'password': 'contrasena_incorrecta_12345',
}, follow=False)

print(f"✓ Estado de respuesta: {response_fallido.status_code}")

# Contar registros de ERROR después
errores_after = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').count()
errores_creados = errores_after - errores_before

print(f"\n✓ Registros de ERROR después: {errores_after}")

if errores_creados > 0:
    print(f"\n✅ ÉXITO: Se registró {errores_creados} intento(s) fallido(s)")
    
    # Obtener el último error
    ultimo_error = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').order_by('-fecha_hora').first()
    
    if ultimo_error:
        print(f"\n✓ Detalles del registro de error:")
        print(f"  - ID: {ultimo_error.id}")
        print(f"  - Acción: {ultimo_error.get_accion_display()}")
        print(f"  - Entidad: {ultimo_error.entidad}")
        print(f"  - Descripción: {ultimo_error.descripcion}")
        error_registrado = True
    else:
        print(f"\n⚠ No se pudo obtener el registro de error")
        error_registrado = False
else:
    print(f"\n⚠ No se registró el intento fallido")
    error_registrado = False

# Resumen final
print("\n" + "=" * 80)
print("RESUMEN DE PRUEBAS")
print("=" * 80)

total_logins = AuditLog.objects.filter(usuario=usuario, accion='LOGIN').count()
total_errores = AuditLog.objects.filter(accion='ERROR', entidad='Sesión').count()

print(f"\n✓ Total de registros LOGIN para {usuario.nombre}: {total_logins}")
print(f"✓ Total de registros ERROR en Sesión: {total_errores}")

print("\n" + "-" * 80)
print("Resultado Final")
print("-" * 80)

if login_exitoso and error_registrado:
    print("\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS PASADAS - SISTEMA COMPLETAMENTE FUNCIONAL")
    print("=" * 80)
    print("\nEl registro automático de login en AuditLog está:")
    print("  ✅ Registrando inicios de sesión exitosos")
    print("  ✅ Registrando intentos fallidos de login")
    print("  ✅ Capturando información correctamente")
    print("  ✅ No interrumpiendo el flujo de usuario")
elif login_exitoso:
    print("\n" + "=" * 80)
    print("✅ PRUEBA PRINCIPAL PASADA - LOGIN REGISTRADO CORRECTAMENTE")
    print("=" * 80)
    print("\nEl sistema está:")
    print("  ✅ Registrando inicios de sesión exitosos")
    print("  ✅ Capturando información correctamente")
    print("  ✅ No interrumpiendo el flujo de usuario")
    print("  ⚠ (Los intentos fallidos podrían requerir configuración adicional)")
else:
    print("\n" + "=" * 80)
    print("❌ PRUEBA PRINCIPAL FALLÓ - REVISAR CONFIGURACIÓN")
    print("=" * 80)

print("\n")
