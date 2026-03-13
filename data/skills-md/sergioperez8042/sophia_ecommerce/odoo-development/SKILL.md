---
name: odoo-development
description: Habilidad para desarrollar soluciones empresariales en Odoo siguiendo arquitectura modular, buenas prácticas oficiales, testing y CI/CD.
capabilities:
  - Diseñar y desarrollar módulos Odoo (modelos, vistas, acciones, menús).
  - Definir modelos con el ORM de Odoo (`models.Model`, `fields.*`).
  - Aplicar convenciones oficiales de Odoo y PEP8 en Python.
  - Crear vistas XML y QWeb para formularios, listas y reportes.
  - Escribir pruebas unitarias con `TransactionCase` y etiquetas `@tagged`.
  - Configurar entornos con Odoo.sh, Docker o entornos virtuales.
  - Integrar CI/CD ejecutando `odoo-bin --test-enable`.
  - Versionar y desplegar módulos con Git y flujos por ramas.
examples:
  - |
    ```python
    from odoo import models, fields

    class LibraryBook(models.Model):
        _name = 'library.book'
        _description = 'Libro de biblioteca'

        title = fields.Char(string='Título', required=True)
        author_id = fields.Many2one('res.partner', string='Autor')
        is_available = fields.Boolean(default=True)
    ```
references:
  - https://www.odoo.com/documentation
  - https://www.odoo.com/documentation/18.0
  - https://www.odoo.com/documentation/18.0/contributing/development/coding_guidelines.html
  - https://www.odoo.sh
  - https://github.com/odoo/odoo
---

## Descripción técnica

Odoo es un ERP modular basado en Python. Cada módulo encapsula modelos, vistas, seguridad, datos y pruebas.

### Estructura recomendada de un módulo

my_module/
models/
views/
security/
data/
reports/
tests/
manifest.py

### Buenas prácticas clave

- **Modelos**
  - Clases en `PascalCase`
  - `_name` en `snake.case`
- **ORM**
  - Evitar SQL directo si no es necesario
  - No usar `cr.commit` en lógica ni tests
- **Vistas**
  - XML claro y desacoplado
  - QWeb para reportes
- **Testing**
  - `TransactionCase`
  - Tests en `tests/test_*.py`
- **CI/CD**
  - Odoo.sh o pipelines propios
- **Arquitectura**
  - MVC: Modelos (Python), Vistas (XML/QWeb), Controladores (HTTP)

El desarrollo profesional en Odoo requiere alinearse estrictamente con las guías oficiales para garantizar mantenibilidad y compatibilidad futura.
