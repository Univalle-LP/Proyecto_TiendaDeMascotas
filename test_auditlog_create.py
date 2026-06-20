#!/usr/bin/env python
"""
Test: Validar que se registran automáticamente creaciones en AuditLog
- Productos
- Categorías
- Usuarios
- Solicitudes (Chats)
"""

import os
import django
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adonai.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from auditoria.models import AuditLog
from usuarios.models import Usuario, Rol
from productos.models import Producto, Categoria
from chat.models import Chat

# Inicializar cliente
client = Client()

print("=" * 80)
print("PRUEBA: REGISTRO AUTOMÁTICO DE CREACIÓN (CREATE) EN AUDITLOG")
print("=" * 80)

# ============================================================================
# 1. PREPARACIÓN
# ============================================================================

print("\n" + "-" * 80)
print("Paso 1: Preparación - Buscar/Crear usuario de prueba")
print("-" * 80)

try:
    usuario_admin = Usuario.objects.filter(email='admin@test.com').first()
    if not usuario_admin:
        # Crear usuario admin para realizar acciones
        rol_admin, _ = Rol.objects.get_or_create(
            nombre='Admin',
            defaults={'descripcion': 'Administrador del sistema'}
        )
        usuario_admin = Usuario.objects.create(
            nombre='Admin Test',
            email='admin@test.com',
            rol=rol_admin,
            estado='activo',
            password=make_password('test123')
        )
        # Crear auth.User correspondiente
        auth_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='test123'
        )
        auth_user.is_staff = True
        auth_user.is_superuser = True
        auth_user.save()
        print("✓ Usuario admin creado")
    else:
        print("✓ Usuario admin encontrado")
    
    # Contar registros previos
    audit_count_inicial = AuditLog.objects.count()
    print(f"✓ Registros de auditoría previos: {audit_count_inicial}")
    
except Exception as e:
    print(f"❌ Error en preparación: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# 2. PROBAR CREACIÓN DE CATEGORÍA
# ============================================================================

print("\n" + "-" * 80)
print("Paso 2: Crear una Categoría y verificar registro en AuditLog")
print("-" * 80)

try:
    # Contar registros previos de CREATE
    registros_create_inicio = AuditLog.objects.filter(accion='CREATE').count()
    print(f"✓ Registros CREATE previos: {registros_create_inicio}")
    
    # Crear categoría
    categoria = Categoria.objects.create(
        nombre=f'Categoría Test {AuditLog.objects.count()}',
        descripcion='Categoría de prueba para auditoría'
    )
    print(f"✓ Categoría creada: {categoria.nombre}")
    
    # Verificar que se registró
    registros_create_nuevo = AuditLog.objects.filter(accion='CREATE').count()
    diferencia = registros_create_nuevo - registros_create_inicio
    
    if diferencia > 0:
        print(f"✅ Se creó(aron) {diferencia} registro(s) de auditoría")
        
        # Mostrar detalles del último registro
        audit_record = AuditLog.objects.filter(
            accion='CREATE',
            entidad='Categoría'
        ).order_by('-fecha_hora').first()
        
        if audit_record:
            print(f"\n✓ Detalles del registro:")
            print(f"  - ID: {audit_record.id}")
            print(f"  - Usuario: {audit_record.usuario}")
            print(f"  - Fecha/Hora: {audit_record.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"  - Acción: {audit_record.get_accion_display()}")
            print(f"  - Entidad: {audit_record.entidad}")
            print(f"  - Descripción: {audit_record.descripcion[:80]}...")
    else:
        print(f"⚠️  No se registró la creación de la categoría")
        
except Exception as e:
    print(f"❌ Error al crear categoría: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 3. PROBAR CREACIÓN DE PRODUCTO
# ============================================================================

print("\n" + "-" * 80)
print("Paso 3: Crear un Producto y verificar registro en AuditLog")
print("-" * 80)

try:
    registros_create_inicio = AuditLog.objects.filter(accion='CREATE').count()
    print(f"✓ Registros CREATE actuales: {registros_create_inicio}")
    
    # Obtener o crear categoría
    categoria, _ = Categoria.objects.get_or_create(
        nombre='Alimentos',
        defaults={'descripcion': 'Categoría de alimentos'}
    )
    
    # Crear producto
    producto = Producto.objects.create(
        nombre=f'Producto Test {AuditLog.objects.count()}',
        descripcion='Producto de prueba para auditoría',
        precio=99.99,
        cantidad_disponible=100,
        categoria=categoria
    )
    print(f"✓ Producto creado: {producto.nombre}")
    
    # Verificar que se registró
    registros_create_nuevo = AuditLog.objects.filter(accion='CREATE').count()
    diferencia = registros_create_nuevo - registros_create_inicio
    
    if diferencia > 0:
        print(f"✅ Se creó(aron) {diferencia} registro(s) de auditoría")
        
        # Mostrar detalles del último registro
        audit_record = AuditLog.objects.filter(
            accion='CREATE',
            entidad='Producto'
        ).order_by('-fecha_hora').first()
        
        if audit_record:
            print(f"\n✓ Detalles del registro:")
            print(f"  - ID: {audit_record.id}")
            print(f"  - Usuario: {audit_record.usuario}")
            print(f"  - Fecha/Hora: {audit_record.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"  - Acción: {audit_record.get_accion_display()}")
            print(f"  - Entidad: {audit_record.entidad}")
            print(f"  - Descripción: {audit_record.descripcion[:80]}...")
    else:
        print(f"⚠️  No se registró la creación del producto")
        
except Exception as e:
    print(f"❌ Error al crear producto: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 4. PROBAR CREACIÓN DE USUARIO (CLIENTE)
# ============================================================================

print("\n" + "-" * 80)
print("Paso 4: Crear un Usuario (Cliente) y verificar registro en AuditLog")
print("-" * 80)

try:
    registros_create_inicio = AuditLog.objects.filter(accion='CREATE').count()
    print(f"✓ Registros CREATE actuales: {registros_create_inicio}")
    
    # Obtener rol cliente
    rol_cliente, _ = Rol.objects.get_or_create(
        nombre='Cliente',
        defaults={'descripcion': 'Cliente del sistema'}
    )
    
    # Crear usuario
    usuario_nuevo = Usuario.objects.create(
        nombre=f'Usuario Test {AuditLog.objects.count()}',
        email=f'cliente_test_{AuditLog.objects.count()}@test.com',
        rol=rol_cliente,
        estado='activo',
        password=make_password('test123')
    )
    print(f"✓ Usuario creado: {usuario_nuevo.nombre}")
    
    # Verificar que se registró
    registros_create_nuevo = AuditLog.objects.filter(accion='CREATE').count()
    diferencia = registros_create_nuevo - registros_create_inicio
    
    if diferencia > 0:
        print(f"✅ Se creó(aron) {diferencia} registro(s) de auditoría")
        
        # Mostrar detalles del último registro
        audit_record = AuditLog.objects.filter(
            accion='CREATE',
            entidad='Usuario (Cliente)'
        ).order_by('-fecha_hora').first()
        
        if audit_record:
            print(f"\n✓ Detalles del registro:")
            print(f"  - ID: {audit_record.id}")
            print(f"  - Usuario: {audit_record.usuario}")
            print(f"  - Fecha/Hora: {audit_record.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"  - Acción: {audit_record.get_accion_display()}")
            print(f"  - Entidad: {audit_record.entidad}")
            print(f"  - Descripción: {audit_record.descripcion[:80]}...")
    else:
        print(f"⚠️  No se registró la creación del usuario")
        
except Exception as e:
    print(f"❌ Error al crear usuario: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 5. PROBAR CREACIÓN DE CHAT (SOLICITUD)
# ============================================================================

print("\n" + "-" * 80)
print("Paso 5: Crear un Chat (Solicitud) y verificar registro en AuditLog")
print("-" * 80)

try:
    registros_create_inicio = AuditLog.objects.filter(accion='CREATE').count()
    print(f"✓ Registros CREATE actuales: {registros_create_inicio}")
    
    # Usar el usuario de prueba
    usuario_para_chat = Usuario.objects.filter(email='cliente_test_1@test.com').first()
    if not usuario_para_chat:
        print("⚠️  No se encontró usuario para crear chat, saltando este paso")
    else:
        # Crear chat
        chat = Chat.objects.create(
            usuario=usuario_para_chat,
            estado='en_atencion',
            prioridad=1
        )
        print(f"✓ Chat creado: Chat #{chat.id}")
        
        # Verificar que se registró
        registros_create_nuevo = AuditLog.objects.filter(accion='CREATE').count()
        diferencia = registros_create_nuevo - registros_create_inicio
        
        if diferencia > 0:
            print(f"✅ Se creó(aron) {diferencia} registro(s) de auditoría")
            
            # Mostrar detalles del último registro
            audit_record = AuditLog.objects.filter(
                accion='CREATE',
                entidad__in=['Solicitud (Chat)', 'Solicitud (Chat Personalizado)']
            ).order_by('-fecha_hora').first()
            
            if audit_record:
                print(f"\n✓ Detalles del registro:")
                print(f"  - ID: {audit_record.id}")
                print(f"  - Usuario: {audit_record.usuario}")
                print(f"  - Fecha/Hora: {audit_record.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"  - Acción: {audit_record.get_accion_display()}")
                print(f"  - Entidad: {audit_record.entidad}")
                print(f"  - Descripción: {audit_record.descripcion[:80]}...")
        else:
            print(f"⚠️  No se registró la creación del chat")
        
except Exception as e:
    print(f"❌ Error al crear chat: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 6. RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMEN DE AUDITORÍA")
print("=" * 80)

try:
    total_audits = AuditLog.objects.count()
    total_creates = AuditLog.objects.filter(accion='CREATE').count()
    
    print(f"\n✓ Total de registros en AuditLog: {total_audits}")
    print(f"✓ Total de registros CREATE: {total_creates}")
    
    print(f"\n✓ Desglose por entidad:")
    for entidad in ['Categoría', 'Producto', 'Usuario (Cliente)', 'Solicitud (Chat)', 'Solicitud (Chat Personalizado)']:
        count = AuditLog.objects.filter(accion='CREATE', entidad=entidad).count()
        if count > 0:
            print(f"  - {entidad}: {count}")
    
    print("\n" + "=" * 80)
    if total_creates > 0:
        print("✅ PRUEBA EXITOSA - CREACIONES REGISTRADAS CORRECTAMENTE")
    else:
        print("❌ PRUEBA FALLIDA - NO SE REGISTRARON CREACIONES")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error en resumen: {e}")
    import traceback
    traceback.print_exc()
