# Descripción

<!-- Describe brevemente los cambios realizados en este PR -->
<!-- Sé específico: qué fue cambiado y por qué -->

---

## 🎯 Tipo de Cambio

- [ ] 🐛 **BUG FIX** - Corregir un problema existente
- [ ] ✨ **FEATURE** - Agregar nueva funcionalidad
- [ ] 📝 **DOCUMENTATION** - Actualizar documentación
- [ ] 🔄 **REFACTOR** - Mejora de código sin cambiar funcionalidad
- [ ] ⚡ **PERFORMANCE** - Mejoras de performance
- [ ] 🔐 **SECURITY** - Cambios de seguridad
- [ ] 🗄️ **DATABASE** - Cambios en estructura de BD
- [ ] 🧪 **TESTING** - Agregar o mejorar tests

---

## 🔗 Issue Relacionado

Cierra #<!-- (número del issue) -->

<!-- Ejemplos:
Closes #123
Closes #123, #124, #125
Related to #456
Fixes #789
-->

---

## 🎯 Cambios Principales

<!-- Lista los cambios principales de forma clara -->

- Cambio 1: descripción
- Cambio 2: descripción
- Cambio 3: descripción

---

## 📸 Evidencias

<!-- Adjunta evidencias de que los cambios funcionan -->

### Para cambios visuales
```
Antes:
[Captura 1]

Después:
[Captura 2]
```

### Para cambios en API
```json
Endpoint: POST /api/nuevo/
Parámetros: { "param": "value" }
Respuesta: { "id": 1, "status": "success" }
```

### Para cambios de BD
```
Migración: 0001_initial.py
- Agregado campo: descripcion (TextField)
```

---

## 🧪 Testing

### Tests Realizados
- [ ] Tests unitarios creados/modificados
- [ ] Tests de integración pasando
- [ ] Cobertura ≥ 80%
- [ ] Validé casos de error
- [ ] Validé edge cases

### Paso a Paso (Manual Testing)
```
1. Ir a [URL]
2. Hacer [acción]
3. Validar [resultado]
4. Verificar [aspecto]
```

---

## 📋 Checklist de Revisión

### Código
- [ ] El código sigue estándares del proyecto
- [ ] No hay código muerto o comentarios innecesarios
- [ ] Nombres de variables son claros
- [ ] Funciones tienen docstrings
- [ ] No hay duplicación de código

### Seguridad
- [ ] No hay credenciales hardcodeadas
- [ ] Se validan inputs del usuario
- [ ] No hay vulnerabilidades SQL injection
- [ ] Está implementado CSRF protection

### Base de Datos
- [ ] Migraciones están versionadas
- [ ] No se rompen migraciones antiguas
- [ ] Se actualizaron indexes si es necesario
- [ ] Validé integridad de relaciones

### Performance
- [ ] No hay N+1 queries
- [ ] Se usan indexes apropiadamente
- [ ] Queries están optimizadas
- [ ] Validé consumo de memoria

### Documentación
- [ ] README actualizado si aplica
- [ ] Docstrings en funciones nuevas
- [ ] Cambios en API están documentados
- [ ] Comments explican código complejo

### Frontend
- [ ] Responsive en mobile
- [ ] Validé en navegadores principales
- [ ] Accesibilidad (a11y) verificada
- [ ] No hay console errors/warnings

### Backend
- [ ] No hay logging sensible
- [ ] Error handling es apropiado
- [ ] Validé comportamiento con BD vacía
- [ ] Testeé con datos realistas

### Auditoría
- [ ] Se registra en audit_logs (si aplica)
- [ ] Usuario queda registrado
- [ ] Descripción es clara
- [ ] No hay comportamientos no auditados

---

## 👥 Reviewers Sugeridos

<!-- Sugiere personas que deberían revisar (opcional) -->

@usuario1 @usuario2

---

## 📦 Deploy Notes

### Variables de Entorno Necesarias
```
[Si es necesario agregar vars de entorno]
```

### Migraciones
```bash
python manage.py migrate
```

### Instrucciones Especiales
```
[Cualquier paso especial para deploy]
```

---

## 🎓 Notas Adicionales

<!-- Información adicional que el reviewer debería saber -->

---

## ✅ Confirmación Final

Confirmo que:

- [ ] Este PR resuelve el issue completamente
- [ ] No hay código incompleto
- [ ] Todos los tests pasan localmente
- [ ] He revisado mis propios cambios
- [ ] Estoy listo para code review

---

**Fecha**: 2026-06-20  
**Rama**: <!-- Tu rama aquí -->  
**Commits**: <!-- Cantidad de commits -->
