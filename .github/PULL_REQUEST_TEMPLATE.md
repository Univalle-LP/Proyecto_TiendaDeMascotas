## 📝 Descripción

<!-- Describe brevemente qué cambios realizas y por qué -->

### Tipo de cambio
- [ ] 🐛 Bug fix (cambio que corrige un problema)
- [ ] ✨ Nueva funcionalidad (cambio que añade funcionalidad)
- [ ] 📝 Documentación (cambio solo en documentación)
- [ ] 🔄 Refactoring (cambio de código sin nueva funcionalidad)
- [ ] ⚡ Mejora de rendimiento
- [ ] 🔒 Seguridad
- [ ] 🗄️ Base de datos

---

## 🔗 Issue Relacionado

<!-- Vincula el issue que este PR resuelve -->

Closes #123
<!-- O usa "Related to #456" si no cierra completamente -->

---

## 🎯 Cambios Principales

<!-- Lista específica de cambios realizados -->

- [ ] Cambio 1
- [ ] Cambio 2
- [ ] Cambio 3

---

## 📸 Evidencias

### Capturas de pantalla / Video
<!-- Sube capturas o video demostrando el cambio -->

<!-- Para cambios visuales:
- Antes: [Captura anterior]
- Después: [Captura nueva]
-->

### Pruebas locales
<!-- Describe cómo probaste los cambios -->

**Pasos reproducidos:**
```
1. Paso 1
2. Paso 2
3. Paso 3
```

**Resultado esperado:**
<!-- Qué debería suceder -->

**Resultado obtenido:**
<!-- Qué sucedió realmente -->

---

## 🧪 Testing

### Tests creados/modificados
- [ ] Tests unitarios añadidos/actualizados
- [ ] Tests de integración añadidos/actualizados
- [ ] Coverage ≥ 80%

**Comando para ejecutar tests:**
```bash
python manage.py test
```

**Resultado de tests:**
<!-- Pega output de tests -->
```

```

---

## 📋 Checklist de Revisión

### Código
- [ ] El código sigue las convenciones del proyecto
- [ ] Se removieron comentarios de debug/console.log
- [ ] Se removieron líneas de código innecesarias
- [ ] Las variables tienen nombres descriptivos
- [ ] Las funciones están documentadas (docstrings)

### Seguridad
- [ ] No se exponen credenciales o API keys
- [ ] Se validan los inputs del usuario
- [ ] Se manejan excepciones correctamente
- [ ] Se implementa CSRF protection si es necesario

### Base de datos
- [ ] Se crearán migraciones si hay cambios en modelos
- [ ] Las migraciones fueron testadas
- [ ] Se añadieron índices si es necesario
- [ ] No hay queries N+1 o ineficientes

### Performance
- [ ] El código no degrada el performance
- [ ] Se reutiliza código existente
- [ ] Las llamadas a API son minimizadas
- [ ] Los archivos estáticos son optimizados

### Documentación
- [ ] Se actualizó documentación relevante
- [ ] Se documentó el cambio en README si aplica
- [ ] Se documentaron cambios en API (si aplica)
- [ ] Se agregó docstring a nuevas funciones

### Frontend (si aplica)
- [ ] UI es responsive en móvil/tablet/desktop
- [ ] Se probó en navegadores principales
- [ ] Accesibilidad (WCAG A) cumplida
- [ ] No hay warnings en consola

### Backend (si aplica)
- [ ] Se probó con datos de prueba variados
- [ ] Se validaron edge cases
- [ ] Se probó error handling
- [ ] Logs son adecuados

### Auditoría (si aplica)
- [ ] Se registran acciones en AuditLog
- [ ] Se capturan cambios importantes
- [ ] Usuario y timestamp están registrados

---

## 🔄 Reviewers Sugeridos

<!-- Sugiere quién debería revisar este PR -->

- @username1
- @username2

---

## 📦 Deploy Notes

### Cambios que afectan producción
- [ ] Requires database migration
- [ ] Requires new environment variables
- [ ] Requires service restart
- [ ] Requires cache clear

**Variables de entorno necesarias:**
```
NEW_VAR=value
ANOTHER_VAR=value
```

**Instrucciones de deployment:**
```bash
# Paso 1
git pull origin branch-name

# Paso 2
python manage.py migrate

# Paso 3
python manage.py collectstatic

# Paso 4
systemctl restart gunicorn
```

---

## 🎓 Notas Adicionales

<!-- Cualquier información adicional útil para los reviewers -->

### Links útiles
- [Issue #123](link-a-issue)
- [Documentación relacionada](link)

### Dependencias
- Depende de PR #456 (menciona si este PR debe aplicarse después de otro)

### Breaking Changes
- [ ] Este PR introduce cambios que rompen la API/funcionalidad existente
- [ ] Si es sí, describe los cambios necesarios

---

## ✅ Confirmación Final

- [ ] He probado mi código localmente
- [ ] He actualizado la documentación
- [ ] He añadido/actualizado tests
- [ ] He revisado mi propio código antes de solicitar review
- [ ] No hay conflictos de merge

---

**Fecha**: YYYY-MM-DD  
**Rama**: `nombre-rama`  
**Commits**: X cambios
