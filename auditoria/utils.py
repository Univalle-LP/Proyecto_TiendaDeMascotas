"""
Módulo de utilidades para facilitar el registro de auditoría en el proyecto.
Proporciona funciones helper para registrar acciones de usuarios.
"""
from auditoria.models import AuditLog


def registrar_auditoria(usuario, accion, entidad, descripcion):
    """
    Registra una acción en el log de auditoría.
    """
    try:
        audit_log = AuditLog.objects.create(
            usuario=usuario,
            accion=accion,
            entidad=entidad,
            descripcion=descripcion
        )
        return audit_log
    except Exception as e:
        print(f"Error al registrar auditoría: {str(e)}")
        return None


def registrar_auditoria_login(usuario):
    """Registra el inicio de sesión de un usuario."""
    return registrar_auditoria(
        usuario=usuario,
        accion='LOGIN',
        entidad='Sesión',
        descripcion=f'{usuario.nombre} inició sesión desde {usuario.email}'
    )


def registrar_auditoria_logout(usuario):
    """Registra el cierre de sesión de un usuario."""
    return registrar_auditoria(
        usuario=usuario,
        accion='LOGOUT',
        entidad='Sesión',
        descripcion=f'{usuario.nombre} cerró sesión'
    )


def registrar_auditoria_crear(usuario, entidad, nombre_objeto, detalles=""):
    """Registra la creación de un objeto."""
    descripcion = f'Se creó {entidad.lower()}: {nombre_objeto}'
    if detalles:
        descripcion += f'. Detalles: {detalles}'
    
    return registrar_auditoria(
        usuario=usuario,
        accion='CREATE',
        entidad=entidad,
        descripcion=descripcion
    )


def registrar_auditoria_actualizar(usuario, entidad, nombre_objeto, cambios=""):
    """Registra la actualización de un objeto."""
    descripcion = f'Se actualizó {entidad.lower()}: {nombre_objeto}'
    if cambios:
        descripcion += f'. Cambios: {cambios}'
    
    return registrar_auditoria(
        usuario=usuario,
        accion='UPDATE',
        entidad=entidad,
        descripcion=descripcion
    )


def registrar_auditoria_eliminar(usuario, entidad, nombre_objeto, razon=""):
    """Registra la eliminación de un objeto."""
    descripcion = f'Se eliminó {entidad.lower()}: {nombre_objeto}'
    if razon:
        descripcion += f'. Razón: {razon}'
    
    return registrar_auditoria(
        usuario=usuario,
        accion='DELETE',
        entidad=entidad,
        descripcion=descripcion
    )


def registrar_auditoria_error(usuario, entidad, error_msg, detalles=""):
    """Registra un error en el sistema."""
    descripcion = f'Error en {entidad}: {error_msg}'
    if detalles:
        descripcion += f'. Detalles: {detalles}'
    
    return registrar_auditoria(
        usuario=usuario,
        accion='ERROR',
        entidad=entidad,
        descripcion=descripcion
    )
