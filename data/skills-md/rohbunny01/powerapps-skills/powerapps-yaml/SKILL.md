---
name: powerapps-yaml
description: >
  Genera código YAML pasteable en Power Apps Studio usando el schema pa.yaml v3.
  Incluye controles modernos, patrones de caché, Gallery con colecciones, y
  todas las lecciones aprendidas para vibe codear sin errores.
  Trigger: Cuando el usuario pida crear pantallas, controles o código para Power Apps en formato YAML.
metadata:
  author: matias-beltran
  version: "2.0"
  scope: [global]
  auto_invoke:
    - "Crear pantalla Power Apps"
    - "Generar YAML para Power Apps"
    - "Código pasteable Power Apps"
    - "pa.yaml"
    - "Power Apps con SharePoint"
---

# Power Apps YAML — Guía Completa para Vibe Coding

## Cuándo usar

- Al generar código YAML para pegar en Power Apps Studio
- Al crear o modificar pantallas de Power Apps
- Al convertir diseños a controles Power Apps modernos
- Al trabajar con SharePoint como backend

---

## 🔑 Estructura Base (pa.yaml Schema v3)

La estructura **OBLIGATORIA** para que Power Apps Studio acepte el YAML via "Paste code":

```yaml
Screens:
    NombrePantalla:
        Properties:
            Fill: =SurfaceAlt
            OnVisible: |-
                =Set(varEjemplo, "hola")
        Children:
            - NombreControl:
                Control: TipoControl
                Variant: VarianteOpcional
                Properties:
                    X: =0
                    Y: =0
                    Width: =Parent.Width
                    Height: =100
                Children:
                    - ControlHijo:
                        Control: Text
                        Properties:
                            Text: ="Hola mundo"
```

### Reglas de estructura

1. **Top-level**: Siempre empieza con `Screens:`
2. **Screen name**: Debe coincidir EXACTAMENTE con el nombre de la pantalla en Power Apps Studio
3. **No usar `Control: Screen`**: Las pantallas se definen directamente bajo `Screens:`, SIN propiedad `Control`
4. **Children es un array**: Cada hijo comienza con `- NombreControl:`
5. **Control y Variant**: Se definen dentro de cada hijo, NO en la pantalla
6. **Valores con `=`**: TODAS las propiedades llevan `=` al inicio: `Text: ="Hola"`, `X: =0`

---

## 🚨 Propiedades de Controles Modernos (CRÍTICO)

Power Apps usa controles **modernos** que tienen nombres DIFERENTES a los clásicos. Usar los nombres incorrectos produce error `PA2108: Unknown property`.

### Control `Text` (Label)

| ❌ Clásico (NO usar) | ✅ Moderno (USAR) |
|----------------------|-------------------|
| `Color` | `FontColor` |
| `FontWeight` | `Weight` |

```yaml
- lblEjemplo:
    Control: Text
    Properties:
        X: =0
        Y: =0
        Width: =200
        Height: =40
        Text: ="Hola"
        FontColor: =RGBA(0, 0, 0, 1)
        Size: =14
        Weight: =FontWeight.Bold
        Align: =Align.Center
        VerticalAlign: =VerticalAlign.Middle
```

### Control `Button`

| ❌ Clásico (NO usar) | ✅ Moderno (USAR) |
|----------------------|-------------------|
| `Fill` | `BasePaletteColor` |
| `Color` | `FontColor` |
| `Size` | `FontSize` |
| `RadiusTopLeft/Right/etc` | _(no existe, usa Fluent theme)_ |

```yaml
- btnEjemplo:
    Control: Button
    Properties:
        X: =0
        Y: =0
        Width: =200
        Height: =44
        Text: ="Click"
        BasePaletteColor: =BrandAccent
        FontColor: =TextOnAccent
        FontSize: =14
        FontWeight: =FontWeight.Semibold
        Appearance: ='ButtonCanvas.Appearance'.Primary
        OnSelect: =Notify("Clickeado")
```

**Valores de Appearance:**
- `'ButtonCanvas.Appearance'.Primary` — botón principal
- `'ButtonCanvas.Appearance'.Secondary` — botón secundario
- `'ButtonCanvas.Appearance'.Transparent` — transparente (ideal para overlays y back buttons)

### Control `TextInput`

| ❌ Clásico (NO usar) | ✅ Moderno (USAR) |
|----------------------|-------------------|
| `Default` | `Value` |
| `HintText` / `PlaceholderText` | _(no existe en moderno)_ |
| `Format` | _(no existe en moderno)_ |

```yaml
- txtEjemplo:
    Control: TextInput
    Properties:
        X: =0
        Y: =0
        Width: =200
        Height: =44
        Value: =""
        Mode: =TextMode.MultiLine  # Opcional
```

### Control `DatePicker`

| ❌ Clásico (NO usar) | ✅ Moderno (USAR) |
|----------------------|-------------------|
| `DefaultDate` | `SelectedDate` |

```yaml
- dpEjemplo:
    Control: DatePicker
    Properties:
        X: =0
        Y: =0
        Width: =200
        Height: =44
        SelectedDate: =Today()
```

### Control `Dropdown`

```yaml
- ddEjemplo:
    Control: Dropdown
    Properties:
        X: =0
        Y: =0
        Width: =200
        Height: =44
        Items: =["Opción 1", "Opción 2", "Opción 3"]
        DefaultSelectedItems: =["Opción 1"]
        OnChange: =Set(varSeleccion, Self.Selected.Value)
```

**Para items numéricos:**
```yaml
Items: =Sequence(24, 0)              # 0 a 23
Items: =[0, 5, 10, 15, 20, 25, 30]   # Lista explícita
```

### Control `GroupContainer`

| ❌ NO soportado | ✅ Alternativa |
|-----------------|---------------|
| `OnSelect` | Usar un Button overlay transparente dentro del container |
| `RadiusTopLeft/Right/etc` | _(no existe en modernos)_ |

```yaml
- containerEjemplo:
    Control: GroupContainer
    Variant: ManualLayout
    Properties:
        X: =0
        Y: =0
        Width: =200
        Height: =100
        Fill: =Surface
        DropShadow: =DropShadow.Light
```

**Para hacer un container clickeable:**
```yaml
Children:
    - lblContenido:
        Control: Text
        Properties:
            Text: ="Mi contenido"
    - btnOverlay:
        Control: Button
        Properties:
            X: =0
            Y: =0
            Width: =Parent.Width
            Height: =Parent.Height
            Text: =""
            Appearance: ='ButtonCanvas.Appearance'.Transparent
            OnSelect: =Navigate(OtraPantalla, ScreenTransition.None)
```

---

## 📊 Gallery — Reglas Críticas

### Regla #1: Variant es OBLIGATORIO
```yaml
- galEjemplo:
    Control: Gallery
    Variant: BrowseLayout_Flexible_SocialFeed_ver5.0  # OBLIGATORIO
```

**Error si falta:** `PA1011: The keyword 'Variant' is required but is missing or empty`

### Regla #2: Items de SharePoint directo → funciona bien
```yaml
Items: =MiListaSP
```

### Regla #3: Items de colección → usar ForAll con esquema explícito

⚠️ **PROBLEMA**: Cuando `Items` apunta a una colección creada con `GroupBy + AddColumns`, los controles dentro de la gallery muestran errores ❌ porque Power Apps no puede inferir el esquema.

✅ **SOLUCIÓN**: Usar `ForAll` con registros de forma explícita `{campo: valor}`:

```yaml
OnVisible: |-
    =ClearCollect(
        colRanking,
        ForAll(
            GroupBy(colRegistros, Title, Email, Registros),
            {
                Nombre: ThisRecord.Title,
                EmailUsuario: ThisRecord.Email,
                Puntos: Sum(Registros, Puntos),
                Sesiones: CountRows(Registros)
            }
        )
    )
```

### Regla #4: GroupBy — NO usar comillas en columnas
```
# ❌ MAL — "Registros" se interpreta como texto
GroupBy(tabla, "Title", "Email", "Registros")

# ✅ BIEN — identificadores sin comillas
GroupBy(tabla, Title, Email, Registros)
```

### Regla #5: No agrupar por columnas que cambian
Si un usuario puede cambiar de equipo, NO agrupar por `Equipo` porque aparecerá duplicado. Tomar el equipo del último registro:
```
EquipoUsuario: Last(Registros).Equipo
```

### Regla #6: Acceder a tabla agrupada dentro de ForAll
```
# ❌ MAL — ThisRecord.Registros no resuelve
Sum(ThisRecord.Registros, Puntos)

# ✅ BIEN — acceso directo a la columna de grupo
Sum(Registros, Puntos)
```

### Template completo para Gallery con colección:
```yaml
- galRanking:
    Control: Gallery
    Variant: BrowseLayout_Flexible_SocialFeed_ver5.0
    Properties:
        X: =16
        Y: =188
        Width: =Parent.Width - 32
        Height: =Parent.Height - 204
        Items: =SortByColumns(colRanking, "Puntos", SortOrder.Descending)
        TemplatePadding: =6
        TemplateSize: =80
        Fill: =RGBA(0, 0, 0, 0)
    Children:
        - CardItem:
            Control: GroupContainer
            Variant: ManualLayout
            Properties:
                Width: =Parent.Width
                Height: =74
                Fill: =Surface
                DropShadow: =DropShadow.Light
            Children:
                - lblNombre:
                    Control: Text
                    Properties:
                        X: =16
                        Y: =12
                        Width: =Parent.Width - 140
                        Height: =24
                        Text: =ThisItem.Nombre
```

---

## 🚀 Patrón de Caché Local (Optimización)

### Problema
Cada pantalla hace queries independientes a SharePoint → lento y redundante.

### Solución: Centro de caché en Screen_Inicio

```yaml
# Screen_Inicio.OnVisible — carga datos UNA VEZ
OnVisible: |-
    =Set(varUsuarioActual, User().FullName);
    Set(varEmailActual, User().Email);
    ClearCollect(
        colRegistrosMes,
        Filter(
            MiListaSP,
            Month(Fecha) = Month(Today()),
            Year(Fecha) = Year(Today())
        )
    );
    Set(varMisRegistros, Filter(colRegistrosMes, Email = varEmailActual));
    Set(varMiEquipo, LookUp(Miembros, Email = varEmailActual, Equipo))
```

### Reutilizar en otras pantallas

```yaml
# Screen_Ranking — usa colRegistrosMes, NO re-consulta SharePoint
OnVisible: |-
    =ClearCollect(
        colRanking,
        ForAll(
            GroupBy(colRegistrosMes, Title, Email, Registros),
            { Nombre: ThisRecord.Title, Puntos: Sum(Registros, Puntos) }
        )
    )

# Screen_Equipos — usa varMiEquipo ya cacheado
OnVisible: |-
    =Set(varVistaEquipos, "Lista")
    # varMiEquipo ya está cargado desde Screen_Inicio
```

### Después de guardar un registro — actualizar caché local

```yaml
# En btnGuardar.OnSelect, después del Patch:
Patch(MiListaSP, Defaults(MiListaSP), { ... });
Collect(colRegistrosMes, { ...mismo registro... });
Navigate(Screen_Inicio, ScreenTransition.None)
```

**Resultado**: ~7 queries SP → **2 queries** (1 ClearCollect + 1 LookUp)

---

## 🎨 Colores del Tema (App.Formulas)

Definir paleta global en `App > Formulas`:
```
BrandPrimary = RGBA(30, 41, 59, 1);
BrandAccent = RGBA(255, 107, 53, 1);
BrandAccentLight = RGBA(255, 107, 53, 0.08);
Surface = RGBA(255, 255, 255, 1);
SurfaceAlt = RGBA(245, 247, 252, 1);
TextPrimary = RGBA(15, 23, 42, 1);
TextSecondary = RGBA(100, 116, 139, 1);
TextOnAccent = RGBA(255, 255, 255, 1);
StatusSuccess = RGBA(16, 185, 129, 1);
StatusWarning = RGBA(234, 179, 8, 1);
StatusError = RGBA(239, 68, 68, 1);
```

---

## ⏰ Patrón: Selector de Hora con Dropdowns

El `DatePicker` solo selecciona fecha. Para hora, usar pares de Dropdowns:

```yaml
# Horas (0-23)
- ddHoraH:
    Control: Dropdown
    Properties:
        Items: =Sequence(24, 0)
        DefaultSelectedItems: =[8]

# Separador ":"
- lblSep:
    Control: Text
    Properties:
        Text: =":"
        Weight: =FontWeight.Bold

# Minutos (intervalos de 5)
- ddHoraM:
    Control: Dropdown
    Properties:
        Items: =[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        DefaultSelectedItems: =[0]
```

### Construir DateTime desde dropdowns:
```
DateAdd(
    DateAdd(Today(), Value(ddHoraH.Selected.Value), TimeUnit.Hours),
    Value(ddHoraM.Selected.Value),
    TimeUnit.Minutes
)
```

### Calcular duración:
```
With(
    {
        mins: (Value(ddFinH.Selected.Value) * 60 + Value(ddFinM.Selected.Value)) -
              (Value(ddInicioH.Selected.Value) * 60 + Value(ddInicioM.Selected.Value))
    },
    If(mins > 0, Text(RoundDown(mins / 60, 0)) & "h " & Text(Mod(mins, 60)) & "min", "⚠️ Error")
)
```

---

## 📋 Proceso de Paste Code

1. **Crear la pantalla** manualmente en Power Apps Studio
2. **Asegurar que el nombre** coincide con el definido en el YAML
3. **Copiar TODO** el contenido del archivo YAML (incluyendo `Screens:`)
4. **Seleccionar la pantalla** en el Tree View
5. **Pegar** con Ctrl+V o Click derecho → Paste code
6. Si hay errores de design-time por colecciones en `OnVisible`, ejecutar (Play ▶️) para que se creen

---

## ⚠️ Tabla de errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `PA2108: Unknown property 'Color'` | Propiedad clásica | Usar `FontColor` |
| `PA2108: Unknown property 'FontWeight'` en Text | Propiedad clásica | Usar `Weight` |
| `PA2108: Unknown property 'Fill'` en Button | Propiedad clásica | Usar `BasePaletteColor` |
| `PA2108: Unknown property 'Default'` en TextInput | Propiedad clásica | Usar `Value` |
| `PA2108: Unknown property 'DefaultDate'` | Propiedad clásica | Usar `SelectedDate` |
| `PA2108: Unknown property 'OnSelect'` en GroupContainer | No soportado | Button overlay transparente |
| `PA1011: 'Variant' is required` en Gallery | Falta Variant | Agregar `Variant: BrowseLayout_Flexible_SocialFeed_ver5.0` |
| `PA2109: Unknown variant 'X'` en Gallery | Variant inválido | Usar `BrowseLayout_Flexible_SocialFeed_ver5.0` |
| `YamlInvalidSyntax: PaModule` | Estructura incorrecta | Usar `Screens:` como top-level |
| Gallery con ❌ en controles | Colección sin esquema inferible | Usar `ForAll` + registros explícitos |
| Nombre duplicado en ranking | GroupBy por columna variable | No agrupar por campos que cambian |
| `"Registros" error: text` | Comillas en GroupBy | Quitar comillas: `GroupBy(t, Col, Grupo)` |

---

## 🧩 Mapeo rápido: Clásico → Moderno

| Control | Propiedad Clásica | Propiedad Moderna |
|---------|-------------------|-------------------|
| Text | `Color` | `FontColor` |
| Text | `FontWeight` | `Weight` |
| Button | `Fill` | `BasePaletteColor` |
| Button | `Color` | `FontColor` |
| Button | `Size` | `FontSize` |
| TextInput | `Default` | `Value` |
| TextInput | `HintText` | _(no existe)_ |
| DatePicker | `DefaultDate` | `SelectedDate` |
| GroupContainer | `OnSelect` | _(no existe)_ |
| Todos | `RadiusTopLeft` etc. | _(no existe)_ |

---

## 💡 Tips Power Fx

- **Separadores**: Usar **comas** (`,`) como separadores — la config regional del entorno define si Power Apps espera `,` o `;`
- **Strings multilínea**: Usar `|-` en YAML seguido de la fórmula con `=` al inicio
- **SharePoint Choice columns**: Al hacer Patch, usar `{Value: "texto"}` para columnas de tipo Choice
- **SharePoint list names**: Verificar el nombre EXACTO de la lista (con números si hay duplicados, ej: `MiLista1`)
- **Colecciones tipadas**: Siempre usar `ForAll({campo: valor})` en vez de `AddColumns` para colecciones que alimentan Gallery
- **Variables globales**: Cachear datos compartidos en `Screen_Inicio.OnVisible` y reutilizar en otras pantallas
