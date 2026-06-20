from django.db import models
from usuarios.models import Usuario

class AuditLog(models.Model):
    ACCIONES = (
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Crear'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
    )
    
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    entidad = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.entidad}"
