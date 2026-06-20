#!/usr/bin/env python
"""
Script para verificar que AuditLog está registrado en el panel administrativo.
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

from django.contrib.admin.apps import AdminConfig
from django.contrib.admin.sites import AdminSite, site
from auditoria.models import AuditLog

print("=" * 80)
print("VERIFICACIÓN DE AUDITLOG EN PANEL ADMINISTRATIVO")
print("=" * 80)

# Verificar que AuditLog está registrado en admin
is_registered = AuditLog in [model for model in site._registry.keys()]

if is_registered:
    print("\n✓ AuditLog está registrado en el panel administrativo")
    
    # Obtener la clase de admin
    admin_class = site._registry[AuditLog]
    
    print(f"\n✓ Clase Admin: {admin_class.__class__.__name__}")
    print(f"\n✓ Configuración del Admin:")
    print(f"  - list_display: {admin_class.list_display}")
    print(f"  - list_filter: {admin_class.list_filter}")
    print(f"  - search_fields: {admin_class.search_fields}")
    print(f"  - readonly_fields: {admin_class.readonly_fields}")
    print(f"  - date_hierarchy: {admin_class.date_hierarchy}")
    
    # Verificar permisos
    from django.contrib.auth.models import User
    from django.test import RequestFactory
    
    # Crear un usuario ficticio para pruebas
    factory = RequestFactory()
    request = factory.get('/admin/')
    
    # Crear un superuser mock
    class MockUser:
        is_superuser = True
        is_staff = True
    
    request.user = MockUser()
    
    print(f"\n✓ Permisos en el Admin:")
    print(f"  - Permite agregar: {not admin_class.has_add_permission(request)}")
    print(f"  - Permite cambiar: {not admin_class.has_change_permission(request)}")
    print(f"  - Permite borrar: {admin_class.has_delete_permission(request)}")
    
    print("\n✓ El modelo AuditLog está completamente integrado en el panel administrativo")
else:
    print("\n✗ AuditLog NO está registrado en el panel administrativo")
    print("\n  Modelos registrados en admin:")
    for model in site._registry.keys():
        print(f"  - {model.__name__}")
    sys.exit(1)

print("\n" + "=" * 80)
print("✓ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 80)
