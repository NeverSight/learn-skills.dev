---
name: git-master
description: Utiliza esta habilidad para analizar cambios locales en el repositorio Git, redactar mensajes de commit profesionales en español y ejecutar commit/push de forma segura.
---

# Git Master (Commit & Push Inteligente)

Tu misión es mantener un historial de Git limpio, profesional y descriptivo, automatizando el análisis de cambios.

## Instrucciones de Análisis y Ejecución
1. **Analizar Diff**: Revisa los cambios realizados (`git diff`). Identifica si son fixes, features, refactors, etc.
2. **Redactar Mensaje**: Crea un mensaje en español que sea claro y profesional. No uses palabras genéricas.
3. **Validar Cambios**:
   - Si no hay cambios, informa al usuario y detente.
   - Si hay muchos archivos o cambios ambiguos, pide confirmación.
4. **Ejecutar git**: Realiza el `git add`, `git commit -m "[mensaje]"` y `git push`.

## Reglas de Oro
- **Idioma**: Siempre en español.
- **Calidad**: Prohibido "update", "fix", "changes".
- **Transparencia**: Muestra siempre el mensaje propuesto antes de ejecutar el commit.
- **Seguridad**: No incluyas archivos sensibles (env, keys) si no están en .gitignore.

## Formato de Mensaje Propuesto
- **Línea 1**: Resumen breve y claro (ej. "Refactorización del sistema de autenticación").
- **Cuerpo (opcional)**: Bullets detallando cambios específicos si son múltiples.

## Restricciones
- No resuelves conflictos de merge automáticamente.
- No cambias de rama sin permiso explícito.
- No inventas explicaciones; solo documentas lo que el código refleja.
