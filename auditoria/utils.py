from auditoria.models import AuditLog


def registrar_auditoria(usuario, accion, entidad, descripcion):
    try:
        return AuditLog.objects.create(
            usuario=usuario,
            accion=accion,
            entidad=entidad,
            descripcion=descripcion
        )
    except Exception as e:
        print(f"Error al registrar auditoría: {str(e)}")
        return None


def registrar_auditoria_login(usuario):
    return registrar_auditoria(
        usuario=usuario,
        accion='LOGIN',
        entidad='Sesión',
        descripcion=f'{usuario.nombre} inició sesión'
    )


def registrar_auditoria_logout(usuario):
    return registrar_auditoria(
        usuario=usuario,
        accion='LOGOUT',
        entidad='Sesión',
        descripcion=f'{usuario.nombre} cerró sesión'
    )


def registrar_auditoria_crear(usuario, entidad, nombre_objeto, detalles=""):
    descripcion = f'Se creó {entidad.lower()}: {nombre_objeto}'
    if detalles:
        descripcion += f'. Detalles: {detalles}'
    return registrar_auditoria(usuario, 'CREATE', entidad, descripcion)


def registrar_auditoria_actualizar(usuario, entidad, nombre_objeto, cambios=""):
    descripcion = f'Se actualizó {entidad.lower()}: {nombre_objeto}'
    if cambios:
        descripcion += f'. Cambios: {cambios}'
    return registrar_auditoria(usuario, 'UPDATE', entidad, descripcion)


def registrar_auditoria_eliminar(usuario, entidad, nombre_objeto, razon=""):
    descripcion = f'Se eliminó {entidad.lower()}: {nombre_objeto}'
    if razon:
        descripcion += f'. Razón: {razon}'
    return registrar_auditoria(usuario, 'DELETE', entidad, descripcion)


def registrar_auditoria_error(usuario, entidad, error_msg, detalles=""):
    descripcion = f'Error en {entidad}: {error_msg}'
    if detalles:
        descripcion += f'. Detalles: {detalles}'
    return registrar_auditoria(usuario, 'ERROR', entidad, descripcion)
