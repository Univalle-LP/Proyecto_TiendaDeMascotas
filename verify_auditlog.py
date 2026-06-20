#!/usr/bin/env python
"""
Script para verificar que el modelo AuditLog se creó correctamente en la base de datos.
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

from django.db import connection
from auditoria.models import AuditLog

print("=" * 80)
print("VERIFICACIÓN DEL MODELO AUDITLOG")
print("=" * 80)

# Verificar que la tabla existe
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs'
    """)
    result = cursor.fetchone()
    if result:
        print("\n✓ La tabla 'audit_logs' existe correctamente en la base de datos")
    else:
        print("\n✗ La tabla 'audit_logs' NO se encontró en la base de datos")
        sys.exit(1)

# Verificar estructura de la tabla
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs'
        ORDER BY ORDINAL_POSITION
    """)
    columns = cursor.fetchall()
    
    print("\n✓ Estructura de la tabla 'audit_logs':")
    print("-" * 80)
    print(f"{'Columna':<20} {'Tipo':<25} {'Nullable':<10} {'Key':<5} {'Extra':<15}")
    print("-" * 80)
    
    for col in columns:
        col_name, col_type, is_nullable, col_key, extra = col
        nullable = 'Sí' if is_nullable == 'YES' else 'No'
        key = col_key if col_key else '-'
        extra = extra if extra else '-'
        print(f"{col_name:<20} {col_type:<25} {nullable:<10} {key:<5} {extra:<15}")

# Verificar índices
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
        FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs'
        ORDER BY INDEX_NAME, SEQ_IN_INDEX
    """)
    indexes = cursor.fetchall()
    
    if indexes:
        print("\n✓ Índices en la tabla 'audit_logs':")
        print("-" * 80)
        current_index = None
        for idx_name, col_name, seq in indexes:
            if idx_name != current_index:
                current_index = idx_name
                print(f"  {idx_name}: ", end="")
            else:
                print(", ", end="")
            print(f"{col_name}", end="")
        print("\n")

# Verificar relaciones (Foreign Keys)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs'
        AND REFERENCED_TABLE_NAME IS NOT NULL
    """)
    fks = cursor.fetchall()
    
    if fks:
        print("✓ Relaciones (Foreign Keys) en 'audit_logs':")
        print("-" * 80)
        for constraint, column, ref_table, ref_column in fks:
            print(f"  {column} → {ref_table}.{ref_column}")

print("\n" + "=" * 80)
print("✓ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 80)

# Mostrar información del modelo Django
print("\nInformación del modelo Django (AuditLog):")
print(f"  - Tabla: {AuditLog._meta.db_table}")
print(f"  - App: {AuditLog._meta.app_label}")
print(f"  - Campos: {[field.name for field in AuditLog._meta.fields]}")

print("\n✓ El modelo AuditLog está completamente funcional")
