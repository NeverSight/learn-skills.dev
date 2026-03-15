---
name: project-estimator
description: Skill para estimar proyectos de software y generar documentos Word profesionales. Genera estimaciones con tiempo en meses, equipo propuesto (rol y porcentaje de dedicación), consideraciones técnicas, y warnings/riesgos. Incluye template .docx corporativo. Usar cuando el usuario pida estimar un proyecto, calcular tiempos, definir equipo necesario, generar documento de estimación, o frases como "cuánto tiempo llevaría", "qué equipo necesito", "estimar proyecto", "presupuesto de tiempo", "planificar desarrollo", "documento de estimación".
---

# Project Estimator

Genera estimaciones de proyectos de software profesionales y estructuradas.

## Workflow de Estimación

### 1. Recopilar Información

Antes de estimar, obtener estos datos esenciales:

**Preguntas obligatorias:**
- ¿Qué tipo de proyecto es? (web app, mobile, API, plataforma, etc.)
- ¿Qué funcionalidades core necesita?
- ¿Hay integraciones con terceros? (pagos, auth, APIs externas)
- ¿Existe algo ya construido o es desde cero?
- ¿Hay restricciones de fecha/presupuesto?

**Preguntas según contexto:**
- ¿Qué stack tecnológico se usará o prefiere?
- ¿Cuántos usuarios concurrentes se esperan?
- ¿Requisitos de compliance? (KYC, PCI-DSS, GDPR)
- ¿Nivel de calidad requerido? (MVP vs producción enterprise)

### 2. Categorizar Complejidad

| Categoría | Características | Multiplicador Base |
|-----------|-----------------|-------------------|
| **Simple** | CRUD básico, pocas entidades, sin integraciones complejas | 1x |
| **Moderado** | Múltiples módulos, 1-2 integraciones, auth estándar | 1.5x |
| **Complejo** | Integraciones múltiples, tiempo real, compliance | 2x |
| **Muy Complejo** | Sistemas distribuidos, alta concurrencia, múltiples plataformas | 2.5-3x |

### 3. Estructura del Output

Generar la estimación en el siguiente formato:

```markdown
# Estimación: [Nombre del Proyecto]

## Resumen Ejecutivo
- **Duración estimada:** X-Y meses
- **Equipo requerido:** N personas (X FTE equivalentes)
- **Complejidad:** [Simple/Moderada/Compleja/Muy Compleja]

## Desglose por Fases

### Fase 1: [Nombre] (X semanas)
- Descripción breve
- Entregables específicos

### Fase 2: [Nombre] (X semanas)
...

## Equipo Propuesto

| Rol | Dedicación | Duración | Responsabilidades |
|-----|------------|----------|-------------------|
| Tech Lead | 100% | Todo el proyecto | Arquitectura, code review, decisiones técnicas |
| Backend Developer | 100% | Meses 1-N | APIs, lógica de negocio, integraciones |
| Frontend Developer | 80% | Meses 2-N | UI/UX implementation |
| QA Engineer | 50% | Meses 2-N | Testing, automatización |
| DevOps | 30% | Todo el proyecto | CI/CD, infraestructura |

### Notas sobre el Equipo
- Justificación de cada rol
- Posibles combinaciones alternativas

## Consideraciones Técnicas

### Stack Recomendado
- Backend: [tecnología] - razón
- Frontend: [tecnología] - razón
- Base de datos: [tecnología] - razón
- Infraestructura: [cloud/on-premise] - razón

### Integraciones
- [Integración 1]: Complejidad X, tiempo estimado Y
- [Integración 2]: ...

### Dependencias Externas
- [Dependencia]: Impacto si no está disponible

## ⚠️ Warnings y Riesgos

### 🔴 Riesgos Altos
- **[Riesgo]:** Descripción y mitigación
  - Impacto: [tiempo/costo/alcance]
  - Probabilidad: [alta/media/baja]
  - Mitigación: [acción propuesta]

### 🟡 Riesgos Medios
- **[Riesgo]:** ...

### 🟢 Riesgos Bajos
- **[Riesgo]:** ...

## Supuestos

Esta estimación asume:
1. [Supuesto 1]
2. [Supuesto 2]
3. ...

## Escenarios

| Escenario | Tiempo | Equipo | Condiciones |
|-----------|--------|--------|-------------|
| Optimista | X meses | N personas | Todo sale bien, sin cambios de alcance |
| Realista | Y meses | N personas | Algunos ajustes menores |
| Pesimista | Z meses | N+1 personas | Cambios de alcance, problemas técnicos |
```

## Reglas de Estimación

### Tiempos Base por Módulo

| Módulo | Simple | Con complejidad |
|--------|--------|-----------------|
| Auth básico (email/pass) | 1 semana | 2 semanas |
| Auth con OAuth/Social | 2 semanas | 3 semanas |
| CRUD simple | 3-5 días | 1-2 semanas |
| CRUD con relaciones complejas | 1-2 semanas | 3-4 semanas |
| Integración de pagos | 2-3 semanas | 4-6 semanas |
| Dashboard/reportes | 2-3 semanas | 4-6 semanas |
| Notificaciones (email/push) | 1 semana | 2-3 semanas |
| Chat/tiempo real | 2-3 semanas | 4-6 semanas |
| Upload/procesamiento archivos | 1 semana | 2-3 semanas |
| API externa (por integración) | 1-2 semanas | 2-4 semanas |
| Mobile app (por plataforma) | 1.5x del tiempo web | 2x si es nativa |

### Factores Multiplicadores

Aplicar estos factores al tiempo base:

| Factor | Multiplicador |
|--------|--------------|
| Primer proyecto con el stack | 1.2x |
| Compliance (KYC, PCI) | 1.3-1.5x |
| Multi-idioma | 1.15x |
| Alta disponibilidad (99.9%+) | 1.3x |
| Equipo distribuido/remoto | 1.1x |
| Sin documentación de sistemas legacy | 1.3x |
| Requisitos ambiguos | 1.2-1.4x |

### Buffer Recomendado

- **MVP/PoC:** +15-20% buffer
- **Proyecto estándar:** +25-30% buffer
- **Proyecto complejo:** +35-40% buffer
- **Proyecto con dependencias externas:** +40-50% buffer

## Composición de Equipos por Tamaño

### Proyecto Pequeño (1-3 meses)
- 1 Full-stack Developer (100%)
- 1 QA (25-50%, puede ser compartido)

### Proyecto Mediano (3-6 meses)
- 1 Tech Lead (100%)
- 1-2 Backend Developers (100%)
- 1 Frontend Developer (100%)
- 1 QA (50-100%)
- 1 DevOps (25-50%)

### Proyecto Grande (6-12 meses)
- 1 Tech Lead (100%)
- 2-3 Backend Developers (100%)
- 2 Frontend Developers (100%)
- 1-2 Mobile Developers si aplica (100%)
- 1-2 QA (100%)
- 1 DevOps (50-100%)
- 1 Product Owner/BA (50-100%)

### Proyecto Enterprise (12+ meses)
- 1 Architect (50-100%)
- 1-2 Tech Leads (100%)
- 4+ Developers (100%)
- 2+ QA (100%)
- 1-2 DevOps/SRE (100%)
- 1 Product Owner (100%)
- 1 Scrum Master/PM (50-100%)

## Warnings Comunes

### 🔴 Siempre incluir si aplica:
- **Integraciones con terceros:** APIs pueden cambiar, documentación puede ser incorrecta
- **Dependencias de otros equipos:** Bloqueos potenciales
- **Requisitos de compliance:** Auditorías pueden demorar
- **Primera vez con tecnología:** Curva de aprendizaje

### 🟡 Evaluar según contexto:
- **Scope creep:** Si el cliente tiene historial de cambios frecuentes
- **Deuda técnica:** Si se hereda código existente
- **Performance:** Si los requisitos de carga no están claros
- **Seguridad:** Penetration testing puede revelar issues

### 🟢 Mencionar para awareness:
- **Vacaciones/feriados:** Considerar en el timeline
- **Onboarding:** Tiempo para que nuevos miembros sean productivos
- **Documentación:** A menudo se subestima

## Generación de Documento Word

El skill incluye un template Word en `assets/template-estimacion.docx` que debe usarse como base.

### Proceso de Generación

1. **Copiar el template** al directorio de trabajo:
   ```bash
   cp /path/to/skill/assets/template-estimacion.docx /home/claude/estimacion-[proyecto].docx
   ```

2. **Desempaquetar** usando el skill docx:
   ```bash
   python /mnt/skills/public/docx/scripts/unpack.py estimacion-[proyecto].docx unpacked/
   ```

3. **Editar** `unpacked/word/document.xml` reemplazando los placeholders:

| Placeholder | Reemplazar con |
|-------------|----------------|
| `18/12/2025` | Fecha actual |
| `[NOMBRE_CLIENTE_PROYECTO]` | Nombre del cliente/proyecto |
| `[DATO_CONTACTO_CLIENTE]` | Información de contacto |
| `[JIRA_ASOCIADO]` | Ticket de Jira si aplica |
| `[ANALISTA_QUE_REALIZA_ESTIMACION]` | Nombre del analista |

4. **Completar tablas** de tiempo y equipo editando las celdas vacías en el XML

5. **Agregar sección de Warnings** después de Consideraciones si hay riesgos importantes

6. **Reempaquetar**:
   ```bash
   python /mnt/skills/public/docx/scripts/pack.py unpacked/ output.docx --original estimacion-[proyecto].docx
   ```

### Estructura del Template

El template tiene estas secciones:
- **Cabecera**: Fecha, Cliente/Proyecto, Contacto, Jira, Analista
- **Equipo y tiempos**: Tiempo estimado (meses) + tabla de equipo con Rol, Cantidad, Ocupación %, Observaciones
- **Consideraciones/Observaciones**: Texto libre

### Agregar Filas a Tablas

Para agregar filas de equipo, copiar el bloque `<w:tr>...</w:tr>` de una fila existente y modificar el contenido.

### Agregar Sección de Warnings

Insertar antes del `</w:body>` un nuevo Heading1 con lista de warnings:

```xml
<w:p>
  <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
  <w:r><w:rPr><w:rtl w:val="0"/></w:rPr>
    <w:t xml:space="preserve">Warnings / Riesgos</w:t>
  </w:r>
</w:p>
```

## Output Formats Adicionales

Ver `references/` para templates markdown:
- `estimation-template.md` - Template completo de estimación
- `executive-summary.md` - Resumen ejecutivo para stakeholders
- `team-matrix.md` - Matriz detallada de roles y dedicación
- `risk-catalog.md` - Catálogo de riesgos comunes
