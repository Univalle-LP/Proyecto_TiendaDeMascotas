from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'entidad', 'fecha_hora', 'descripcion_corta')
    list_filter = ('accion', 'entidad', 'fecha_hora', 'usuario')
    search_fields = ('usuario__nombre', 'entidad', 'descripcion')
    ordering = ('-fecha_hora',)
    readonly_fields = ('usuario', 'fecha_hora', 'accion', 'entidad', 'descripcion')
    date_hierarchy = 'fecha_hora'

    def descripcion_corta(self, obj):
        """Muestra una versión truncada de la descripción"""
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

    def has_add_permission(self, request):
        """Evitar que se creen registros manualmente desde el admin"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Permitir borrado de registros (solo administradores)"""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Evitar que se editen registros"""
        return False
