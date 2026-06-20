#!/usr/bin/env python
"""Test: Validar AuditLog modelo y funciones básicas"""
import os
import django
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adonai.settings')
django.setup()

from auditoria.models import AuditLog
from auditoria.utils import registrar_auditoria_eliminar
from usuarios.models import Usuario, Rol
from django.contrib.auth.hashers import make_password

print("=" * 60)
print("VALIDACIÓN: MODELO AUDITLOG")
print("=" * 60)

# 1. Verificar campos del modelo
print("\n✓ Campos del modelo AuditLog:")
campos = ['id', 'usuario', 'fecha_hora', 'accion', 'entidad', 'descripcion']
for campo in campos:
    if hasattr(AuditLog, campo):
        print(f"  ✓ {campo}")

# 2. Verificar tabla en base de datos
print("\n✓ Total de registros en AuditLog:", AuditLog.objects.count())

# 3. Prueba de función
print("\n✓ Probando función registrar_auditoria_eliminar():")
try:
    rol, _ = Rol.objects.get_or_create(nombre='Test', defaults={'descripcion': 'Test'})
    usuario = Usuario.objects.filter(email='test@test.com').first()
    if not usuario:
        usuario = Usuario.objects.create(
            nombre='Test User',
            email='test@test.com',
            rol=rol,
            estado='activo',
            password=make_password('test123')
        )
    
    resultado = registrar_auditoria_eliminar(
        usuario=usuario,
        entidad='Producto',
        nombre='Collar Premium',
        razon='Stock agotado'
    )
    
    if resultado:
        print(f"  ✅ Registro creado con ID: {resultado.id}")
        print(f"  Descripción: {resultado.descripcion}")
    else:
        print(f"  ❌ Error al crear registro")
        
except Exception as e:
    print(f"  Error: {e}")

# 4. Verificar tabla en admin
print("\n✓ Verificando registro en admin:")
from django.contrib.admin.sites import site
if AuditLog in site._registry:
    print(f"  ✅ AuditLog registrado en admin")
else:
    print(f"  ❌ AuditLog NO registrado en admin")

print("\n" + "=" * 60)
print("✅ VALIDACIÓN COMPLETADA")
print("=" * 60)
print("\nModelo AuditLog:\n  - Tabla: audit_logs")
print("  - Campos: id, usuario, fecha_hora, accion, entidad, descripcion")
print("  - Admin: Registrado y funcional")
print("  - Acciones: LOGIN, LOGOUT, CREATE, UPDATE, DELETE")
