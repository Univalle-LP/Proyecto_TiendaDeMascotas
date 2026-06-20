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
        print(f"Error auditoría: {e}")
        return None

def registrar_auditoria_login(usuario):
    return registrar_auditoria(usuario, 'LOGIN', 'Sesión', f'{usuario.nombre} inició sesión')

def registrar_auditoria_logout(usuario):
    return registrar_auditoria(usuario, 'LOGOUT', 'Sesión', f'{usuario.nombre} cerró sesión')

def registrar_auditoria_crear(usuario, entidad, nombre, detalles=""):
    desc = f'Se creó {entidad}: {nombre}'
    if detalles:
        desc += f' - {detalles}'
    return registrar_auditoria(usuario, 'CREATE', entidad, desc)

def registrar_auditoria_actualizar(usuario, entidad, nombre, cambios=""):
    desc = f'Se actualizó {entidad}: {nombre}'
    if cambios:
        desc += f' - {cambios}'
    return registrar_auditoria(usuario, 'UPDATE', entidad, desc)

def registrar_auditoria_eliminar(usuario, entidad, nombre, razon=""):
    desc = f'Se eliminó {entidad}: {nombre}'
    if razon:
        desc += f' - {razon}'
    return registrar_auditoria(usuario, 'DELETE', entidad, desc)
