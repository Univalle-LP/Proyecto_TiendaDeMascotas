# 📋 Plantillas de GitHub

Este directorio contiene plantillas automáticas para Issues y Pull Requests.

---

## 📁 Contenido

### Templates de Issues

Elige el template más apropiado según tu necesidad:

#### 🐛 [bug_report.md](bug_report.md)
Para reportar bugs o errores.

**Incluye**:
- Descripción del bug
- Pasos para reproducir
- Resultado esperado vs actual
- Evidencias (capturas, logs)
- Prioridad y responsable

#### ✨ [feature_request.md](feature_request.md)
Para solicitar nuevas funcionalidades.

**Incluye**:
- Descripción de la feature
- Problema que resuelve
- Solución propuesta
- Criterios de aceptación
- Prioridad y responsable

#### 📝 [documentation.md](documentation.md)
Para reportar problemas o mejoras en documentación.

**Incluye**:
- Qué documentación necesita mejora
- Problema actual
- Solución propuesta
- Prioridad y responsable

#### 🔧 [general.md](general.md)
Para preguntas, discusiones u otro tipo de issue.

**Incluye**:
- Descripción
- Pasos para reproducir (si aplica)
- Resultado esperado/actual
- Contexto adicional
- Prioridad y responsable

### Configuración

#### [config.yml](config.yml)
Configuración global de templates para GitHub.

---

## 🚀 Cómo Usar

### Crear un Issue

1. Ve a **Issues** en GitHub
2. Haz clic en **New Issue**
3. Verás las opciones de templates disponibles:
   - 🐛 Bug Report
   - ✨ Feature Request
   - 📝 Documentation
   - 🔧 General Issue
4. Elige el que mejor se ajuste a tu necesidad
5. El template se auto-rellena
6. Completa los campos requeridos
7. Click en **Submit new issue**

---

## ✅ Campos Comunes

Todos los templates incluyen:

- ✅ **Descripción clara** del problema/solicitud
- ✅ **Pasos para reproducir** (si es aplicable)
- ✅ **Resultado esperado** vs actual
- ✅ **Prioridad**: Crítica, Alta, Media, Baja
- ✅ **Responsable**: Quién debería trabajar en esto
- ✅ **Contexto adicional** (evidencias, referencias)
- ✅ **Checklist** de verificación

---

## 📊 Estructura de Archivo

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.md          # Template para bugs
    ├── feature_request.md     # Template para features
    ├── documentation.md       # Template para docs
    ├── general.md             # Template general
    ├── config.yml             # Configuración
    └── README.md              # Este archivo
```

---

## 🔑 Metadata de Templates

Cada template incluye:

```yaml
---
name: "Nombre del Template"
about: "Descripción breve"
title: "[TIPO] "
labels: "label1, label2"
assignees: ""
---
```

Esto permite que GitHub reconozca y organize automáticamente los issues.

---

## 💡 Consejos

### Al Crear un Issue

1. **Sé específico**: Describe claramente qué es el problema
2. **Incluye contexto**: Más información = mejor entendimiento
3. **Adjunta evidencias**: Capturas, logs, URLs
4. **Usa el checklist**: Verifica antes de enviar
5. **Vincula issues**: Si está relacionado con otros

### Al Revisar Issues

1. **Verifica que sea un nuevo issue**: Busca antes de crear
2. **Usa el template correcto**: No todos los issues son bugs
3. **Llena todos los campos**: Especialmente pasos y prioridad
4. **Asigna responsable**: Quién lo va a trabajar

---

## 📚 Recursos Relacionados

- [GitHub Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Best Practices](https://docs.github.com/en/communities)
- [Cómo crear Issues efectivos](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue)

---

## ✨ Características

### Automáticas
- ✅ Auto-relleno al crear issues
- ✅ Labels automáticos según tipo
- ✅ Validación de campos
- ✅ Metadata consistente

### Organizadas
- ✅ Separadas por tipo
- ✅ Fáciles de encontrar
- ✅ Claras y estructuradas
- ✅ Profesionales

---

**Última actualización**: 2026-06-20  
**Versión**: 1.0  
**Mantenedor**: Equipo de Desarrollo
