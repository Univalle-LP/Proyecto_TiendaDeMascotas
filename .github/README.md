# 🔧 Configuración de GitHub

Este directorio contiene configuraciones para mejorar el flujo de trabajo en GitHub.

---

## 📁 Estructura

```
.github/
├── PULL_REQUEST_TEMPLATE.md      ← Template obligatorio para PRs
├── PR_GUIDELINES.md               ← Guía de buenas prácticas
├── ISSUE_TEMPLATE/
│   ├── bug_report.md              ← Template para reportes de bugs
│   ├── feature_request.md         ← Template para solicitudes de features
│   ├── documentation.md           ← Template para mejoras de docs
│   └── config.yml                 ← Configuración de templates
└── README.md                      ← Este archivo
```

---

## 📋 Templates Disponibles

### PULL_REQUEST_TEMPLATE.md
**Cuándo se usa**: Automáticamente en todo nuevo PR

**Incluye**:
- Descripción del cambio
- Tipo de cambio (bug, feature, refactor, etc)
- Issue relacionado
- Evidencias (capturas, videos)
- Testing realizado
- Checklist de revisión completo

**Cómo**: Abre un PR → Se autocompleta el template

---

### ISSUE_TEMPLATE/bug_report.md
**Cuándo se usa**: Al reportar un bug

**Incluye**:
- Descripción del error
- Pasos para reproducir
- Comportamiento esperado vs actual
- Evidencias
- Información del sistema

**Cómo**: Issues → New Issue → "🐛 Reporte de Bug"

---

### ISSUE_TEMPLATE/feature_request.md
**Cuándo se usa**: Al solicitar una nueva funcionalidad

**Incluye**:
- Descripción de la feature
- Problema que resuelve
- Solución propuesta
- Criterios de aceptación
- Impacto y beneficios

**Cómo**: Issues → New Issue → "✨ Solicitud de Feature"

---

### ISSUE_TEMPLATE/documentation.md
**Cuándo se usa**: Al reportar problemas o mejoras en documentación

**Incluye**:
- Qué documentación necesita mejora
- Problema actual
- Solución propuesta
- Contenido sugerido

**Cómo**: Issues → New Issue → "📝 Mejora de Documentación"

---

## 🚀 Cómo Usar

### Abrir un PR

```bash
# Crea rama
git checkout -b feature/mi-funcionalidad

# Haz cambios, commits, push
git push origin feature/mi-funcionalidad

# Ve a GitHub
# → New Pull Request
# → El template se llena automáticamente
# → Solo completa las secciones
```

### Reportar un Problema

```
GitHub → Issues → New Issue
→ Elige el template apropiado
→ Completa los campos
→ Submit
```

---

## 📝 Guías Relacionadas

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Cómo contribuir al proyecto
- **[PR_GUIDELINES.md](./PR_GUIDELINES.md)** - Guía de buenas prácticas en PRs
- **[PULL_REQUEST_TEMPLATE.md](./PULL_REQUEST_TEMPLATE.md)** - Template de PR

---

## ✅ Checklist para Revisor

Al revisar configuración de GitHub:

- [ ] Templates están en la carpeta `.github/`
- [ ] PULL_REQUEST_TEMPLATE.md existe
- [ ] Carpeta ISSUE_TEMPLATE/ existe
- [ ] config.yml está configurado
- [ ] Nombres de archivos son correctos
- [ ] Contenido de templates es claro

---

## 📚 Recursos Útiles

- [GitHub PR Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [GitHub Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Best Practices](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)

---

## 🔄 Mantenimiento

### Cuándo Actualizar Templates

- Cuando cambien estándares del proyecto
- Cuando se agreguen/eliminen campos en DB
- Cuando cambien procesos de desarrollo
- Cuando feedback indique que falta algo

### Quién Actualiza

- Cualquier contributror puede sugerir cambios
- Lead/Arquitecto aprueba cambios
- Se documentan cambios en changelog

---

## 📊 Estadísticas

- **Templates PR**: 1
- **Templates Issues**: 3
- **Líneas de documentación**: 500+
- **Checklists incluidos**: 5+

---

**Última actualización**: 2026-06-20  
**Versión**: 1.0  
**Estado**: ✅ Completa
