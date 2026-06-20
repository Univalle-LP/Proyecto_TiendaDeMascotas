"""
Módulo de utilidades para facilitar el registro de auditoría en el proyecto.
Proporciona funciones helper para registrar acciones de usuarios.
"""
from auditoria.models import AuditLog


def registrar_auditoria(usuario, accion, entidad, descripcion):
    """
    Registra una acción en el log de auditoría.
    
    Args:
        usuario (Usuario): Instancia de Usuario que realizó la acción
        accion (str): Tipo de acción (CREATE, UPDATE, DELETE, VIEW, LOGIN, LOGOUT, ERROR, OTHER)
        entidad (str): Nombre del modelo/tabla afectada
        descripcion (str): Descripción detallada de la acción
    
    Returns:
        AuditLog: Instancia del registro de auditoría creado
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
        # Log del error pero no interrumpir el flujo de la aplicación
        print(f"Error al registrar auditoría: {str(e)}")
        return None


def registrar_auditoria_login(usuario):
    """
    Registra el inicio de sesión de un usuario.
    
    Args:
        usuario (Usuario): Usuario que inició sesión
    """
    return registrar_auditoria(
        usuario=usuario,
        accion='LOGIN',
        entidad='Sesión',
        descripcion=f'{usuario.nombre} inició sesión desde {usuario.email}'
    )


def registrar_auditoria_logout(usuario):
    """
    Registra el cierre de sesión de un usuario.
    
    Args:
        usuario (Usuario): Usuario que cerró sesión
    """
    return registrar_auditoria(
        usuario=usuario,
        accion='LOGOUT',
        entidad='Sesión',
        descripcion=f'{usuario.nombre} cerró sesión'
    )


def registrar_auditoria_crear(usuario, entidad, nombre_objeto, detalles=""):
    """
    Registra la creación de un objeto.
    
    Args:
        usuario (Usuario): Usuario que creó el objeto
        entidad (str): Tipo de entidad creada (ej: Producto, Usuario, Venta)
        nombre_objeto (str): Nombre o descripción del objeto creado
        detalles (str): Detalles adicionales opcionales
    """
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
    """
    Registra la actualización de un objeto.
    
    Args:
        usuario (Usuario): Usuario que actualizó el objeto
        entidad (str): Tipo de entidad actualizada
        nombre_objeto (str): Nombre o descripción del objeto actualizado
        cambios (str): Descripción de los cambios realizados
    """
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
    """
    Registra la eliminación de un objeto.
    
    Args:
        usuario (Usuario): Usuario que eliminó el objeto
        entidad (str): Tipo de entidad eliminada
        nombre_objeto (str): Nombre o descripción del objeto eliminado
        razon (str): Razón de la eliminación opcional
    """
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
    """
    Registra un error en el sistema.
    
    Args:
        usuario (Usuario): Usuario afectado por el error
        entidad (str): Entidad donde ocurrió el error
        error_msg (str): Mensaje de error
        detalles (str): Detalles adicionales del error
    """
    descripcion = f'Error en {entidad}: {error_msg}'
    if detalles:
        descripcion += f'. Detalles: {detalles}'
    
    return registrar_auditoria(
        usuario=usuario,
        accion='ERROR',
        entidad=entidad,
        descripcion=descripcion
    )
