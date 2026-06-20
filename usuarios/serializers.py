from .models import Usuario


class UsuarioSerializer:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario

    def to_representation(self):
        return {
            'id': self.usuario.id,
            'nombre': self.usuario.nombre,
            'email': self.usuario.email,
            'telefono': self.usuario.telefono,
            'direccion': self.usuario.direccion,
            'estado': self.usuario.estado,
            'rol': self.usuario.rol.nombre if self.usuario.rol else None,
        }
