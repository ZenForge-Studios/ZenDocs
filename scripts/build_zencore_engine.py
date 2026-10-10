import os
import re
import json

def clean_emojis(text):
    emoji_pattern = re.compile(
        r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\u2300-\u23ff\u2b50\u2b55\u200d\ufe0f]'
    )
    return emoji_pattern.sub('', text)

print("--- 1. Building General Pages ---")
os.makedirs("content/docs/general", exist_ok=True)

with open("content/docs/general/index.mdx", "w", encoding="utf-8") as f:
    f.write('''---
title: "ZenCore Engine"
description: "Motor central declarativo de efectos, disparadores, condiciones y mutadores para el ecosistema de plugins ZenForge."
---

import { Card, Cards } from 'fumadocs-ui/components/card';
import { Callout } from 'fumadocs-ui/components/callout';

**ZenCore** es el motor declarativo central que potencia todo el ecosistema de plugins de ZenForge (incluyendo **ZenCustomItems**, **ZenEnchants**, y futuros sistemas). Inspirado en la arquitectura modular de estándares como *Libreforge / Eco*, unifica la lógica de ejecución de habilidades, mecánicas de combate, cálculo de variables y sincronización de eventos de Minecraft.

---

## Módulos del Motor

<Cards>
  <Card title="Effects (Efectos)" href="/docs/effects" description="Acciones y habilidades ejecutables: daño, partículas, pociones, empuje, sonidos y utilidades." />
  <Card title="Conditions (Condiciones)" href="/docs/conditions" description="Validaciones lógicas y requisitos de contexto: salud, biomas, permisos y variables." />
  <Card title="Triggers (Disparadores)" href="/docs/triggers" description="Eventos de Minecraft que inician la ejecución de habilidades del jugador o entorno." />
  <Card title="Filters (Filtros)" href="/docs/filters" description="Filtros precisos de entidades, bloques y orígenes de daño." />
  <Card title="Mutators (Mutadores)" href="/docs/mutators" description="Operaciones matemáticas y cinemáticas para transformar valores de daño y variables." />
  <Card title="Placeholders y Expresiones" href="/docs/general/placeholders" description="Placeholders universales y soporte de fórmulas matemáticas evaluadas en tiempo real." />
</Cards>

---

## Filosofía de Diseño

1. **Rendimiento de Grado Servidor**: Cada efecto y condición está compilado para ejecutarse sin demoras en el hilo principal de Paper y Folia.
2. **Sintaxis Declarativa YAML**: Escribe habilidades avanzadas directamente en archivos de configuración sin necesidad de programar en Java.
3. **Persistencia PDC Nativa**: Los datos de variables e instancias se almacenan de forma segura en el `PersistentDataContainer` de Minecraft.
4. **Formato MiniMessage**: Soporte completo para degradados, colores HEX y estilos enriquecidos en mensajes, títulos y barras de acción.
''')

with open("content/docs/general/arquitectura.mdx", "w", encoding="utf-8") as f:
    f.write('''---
title: "Arquitectura del Motor"
description: "Estructura del ciclo de ejecución declarativo: Triggers -> Filters -> Conditions -> Mutators -> Effects."
---

import { Callout } from 'fumadocs-ui/components/callout';

El motor ZenCore procesa cada habilidad mediante una cadena de ejecución modular y determinista.

---

## Flujo de Ejecución

```text
[ Evento en Minecraft ]
          │
          ▼
     1. TRIGGER      -> El evento activa el disparador registrado.
          │
          ▼
     2. FILTERS      -> Comprueba si las entidades o bloques objetivo coinciden.
          │
          ▼
    3. CONDITIONS    -> Evalúa si se cumplen todos los requisitos y probabilidades.
          │
          ▼
     4. MUTATORS     -> Altera matemáticamente valores de contexto (daño, vectores).
          │
          ▼
     5. EFFECTS      -> Ejecuta la lista secuencial de acciones finales.
```

---

## Contexto de Ejecución (`TriggerContext`)

Cada trigger genera un objeto de contexto que viaja a través de la cadena con acceso seguro a:

- **`player`**: El jugador que inició la acción (si aplica).
- **`targetEntity`**: La entidad objetivo atacada o afectada.
- **`targetBlock`**: El bloque roto, colocado o interactuado.
- **`damage`**: El valor numérico del daño en curso.
- **`variables`**: Variables de instancia personalizadas asociadas al ítem o jugador.
''')

with open("content/docs/general/placeholders.mdx", "w", encoding="utf-8") as f:
    f.write('''---
title: "Placeholders y Expresiones"
description: "Variables dinámicas de contexto y fórmulas matemáticas soportadas en ZenCore."
---

ZenCore permite el uso de placeholders dinámicos y fórmulas matemáticas en cualquier parámetro numérico o de texto.

---

## Placeholders Universales

| Placeholder | Descripción |
| :--- | :--- |
| `%player%` / `%player_name%` | Nombre del jugador que ejecuta la acción. |
| `%player_health%` | Salud actual del jugador. |
| `%player_max_health%` | Salud máxima del jugador. |
| `%target%` / `%target_name%` | Nombre o tipo de la entidad objetivo. |
| `%target_health%` | Salud actual del objetivo. |
| `%damage%` | Valor numérico del daño en curso. |
| `%variable_<nombre>%` | Valor de una variable persistente guardada en el ítem. |

---

## Expresiones Matemáticas

Puedes emplear operadores matemáticos estándar (`+`, `-`, `*`, `/`, `^`, `%`) y funciones (`min`, `max`, `abs`, `round`) en valores numéricos:

```yaml
effects:
  - type: DEAL_DAMAGE
    amount: "10 + (%player_health% * 0.2)"
```
''')

with open("content/docs/general/meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": "General",
        "pages": [
            "index",
            "arquitectura",
            "placeholders"
        ]
    }, f, indent=2)

print("--- 2. Building Effects Section ---")
os.makedirs("content/docs/effects", exist_ok=True)

# Collect all effect markdown files from DOCS/ZenCore/effects, content/docs/zenenchants/effects, content/docs/zencustomitems/effects
effects_dict = {}

# 1. From DOCS/ZenCore/effects
if os.path.exists("DOCS/ZenCore/effects"):
    for f in os.listdir("DOCS/ZenCore/effects"):
        if f.endswith(".md"):
            slug = f[:-3].lower()
            with open(os.path.join("DOCS/ZenCore/effects", f), "r", encoding="utf-8", errors="ignore") as fp:
                raw = fp.read()
            # Wrap as MDX with frontmatter
            lines = raw.strip().split("\n")
            title = slug
            desc = f"Efecto {slug} del motor ZenCore."
            # parse title and desc if present
            for l in lines:
                if l.startswith("# "):
                    title = l.replace("# ", "").replace("`", "").strip()
                elif "**Descripción:**" in l or "- **Descripción:**" in l:
                    desc = l.split(":**")[1].strip()
            
            mdx_content = f"""---
title: "{title}"
description: "{desc}"
---

{clean_emojis(raw)}
"""
            effects_dict[slug] = (title, desc, mdx_content)

# 2. From content/docs/zenenchants/effects (to get full 185 enriched effects)
if os.path.exists("content/docs/zenenchants/effects"):
    for f in os.listdir("content/docs/zenenchants/effects"):
        if f.endswith(".mdx") and f != "index.mdx":
            slug = f[:-4].lower()
            with open(os.path.join("content/docs/zenenchants/effects", f), "r", encoding="utf-8", errors="ignore") as fp:
                raw = fp.read()
            # extract title and desc
            title = slug
            desc = f"Efecto {slug} del motor ZenCore."
            m_title = re.search(r'title:\s*["\']([^"\']+)["\']', raw)
            if m_title:
                title = m_title.group(1)
            m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', raw)
            if m_desc:
                desc = m_desc.group(1)
            effects_dict[slug] = (title, desc, clean_emojis(raw))

# 3. From content/docs/zencustomitems/effects
if os.path.exists("content/docs/zencustomitems/effects"):
    for f in os.listdir("content/docs/zencustomitems/effects"):
        if f.endswith(".mdx") and f != "index.mdx":
            slug = f[:-4].lower()
            if slug not in effects_dict:
                with open(os.path.join("content/docs/zencustomitems/effects", f), "r", encoding="utf-8", errors="ignore") as fp:
                    raw = fp.read()
                title = slug
                desc = f"Efecto {slug} del motor ZenCore."
                m_title = re.search(r'title:\s*["\']([^"\']+)["\']', raw)
                if m_title:
                    title = m_title.group(1)
                m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', raw)
                if m_desc:
                    desc = m_desc.group(1)
                effects_dict[slug] = (title, desc, clean_emojis(raw))

print(f"Total unique effects to write: {len(effects_dict)}")

# Write all individual effect files
sorted_effect_slugs = sorted(effects_dict.keys())
for slug in sorted_effect_slugs:
    title, desc, content = effects_dict[slug]
    with open(f"content/docs/effects/{slug}.mdx", "w", encoding="utf-8") as fp:
        fp.write(content)

# Write effects/index.mdx with Cards
effects_cards = "\n".join([
    f'  <Card title="{effects_dict[slug][0]}" href="/docs/effects/{slug}" description="{effects_dict[slug][1]}" />'
    for slug in sorted_effect_slugs
])

with open("content/docs/effects/index.mdx", "w", encoding="utf-8") as f:
    f.write(f'''---
title: "Effects (Efectos)"
description: "Catálogo completo de los {len(sorted_effect_slugs)} efectos declarativos ejecutables del motor ZenCore."
---

import {{ Card, Cards }} from 'fumadocs-ui/components/card';
import {{ Callout }} from 'fumadocs-ui/components/callout';

Los **Efectos** son las acciones que se ejecutan cuando se activa un disparador (Trigger) y se satisfacen los filtros y condiciones. Soportan expresiones dinámicas, parámetros de contexto y formateo MiniMessage.

---

## Catálogo de Efectos ({len(sorted_effect_slugs)})

<Cards>
{effects_cards}
</Cards>
''')

with open("content/docs/effects/meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": "Effects",
        "pages": ["index"] + sorted_effect_slugs
    }, f, indent=2)

print("Effects section complete.")

print("--- 3. Building Conditions Section ---")
os.makedirs("content/docs/conditions", exist_ok=True)

conditions_dict = {}

# 1. From content/docs/zencustomitems/conditions
if os.path.exists("content/docs/zencustomitems/conditions"):
    for f in os.listdir("content/docs/zencustomitems/conditions"):
        if f.endswith(".mdx") and f != "index.mdx":
            slug = f[:-4].lower()
            with open(os.path.join("content/docs/zencustomitems/conditions", f), "r", encoding="utf-8", errors="ignore") as fp:
                raw = fp.read()
            title = slug
            desc = f"Condición {slug} del motor ZenCore."
            m_title = re.search(r'title:\s*["\']([^"\']+)["\']', raw)
            if m_title:
                title = m_title.group(1)
            m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', raw)
            if m_desc:
                desc = m_desc.group(1)
            conditions_dict[slug] = (title, desc, clean_emojis(raw))

# 2. From content/docs/zenenchants/conditions
if os.path.exists("content/docs/zenenchants/conditions"):
    for f in os.listdir("content/docs/zenenchants/conditions"):
        if f.endswith(".mdx") and f != "index.mdx":
            slug = f[:-4].lower()
            if slug not in conditions_dict:
                with open(os.path.join("content/docs/zenenchants/conditions", f), "r", encoding="utf-8", errors="ignore") as fp:
                    raw = fp.read()
                title = slug
                desc = f"Condición {slug} del motor ZenCore."
                m_title = re.search(r'title:\s*["\']([^"\']+)["\']', raw)
                if m_title:
                    title = m_title.group(1)
                m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', raw)
                if m_desc:
                    desc = m_desc.group(1)
                conditions_dict[slug] = (title, desc, clean_emojis(raw))

print(f"Total unique conditions to write: {len(conditions_dict)}")

sorted_cond_slugs = sorted(conditions_dict.keys())
for slug in sorted_cond_slugs:
    title, desc, content = conditions_dict[slug]
    with open(f"content/docs/conditions/{slug}.mdx", "w", encoding="utf-8") as fp:
        fp.write(content)

cond_cards = "\n".join([
    f'  <Card title="{conditions_dict[slug][0]}" href="/docs/conditions/{slug}" description="{conditions_dict[slug][1]}" />'
    for slug in sorted_cond_slugs
])

with open("content/docs/conditions/index.mdx", "w", encoding="utf-8") as f:
    f.write(f'''---
title: "Conditions (Condiciones)"
description: "Catálogo completo de las {len(sorted_cond_slugs)} condiciones lógicas de evaluación de ZenCore."
---

import {{ Card, Cards }} from 'fumadocs-ui/components/card';
import {{ Callout }} from 'fumadocs-ui/components/callout';

Las **Condiciones** evalúan el contexto del evento y determinan si los efectos deben o no ejecutarse. Soportan inversión booleana añadiendo `inverted: true` (actuando como operador `NOT`).

---

## Catálogo de Condiciones ({len(sorted_cond_slugs)})

<Cards>
{cond_cards}
</Cards>
''')

with open("content/docs/conditions/meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": "Conditions",
        "pages": ["index"] + sorted_cond_slugs
    }, f, indent=2)

print("Conditions section complete.")

print("--- 4. Building Triggers Section ---")
os.makedirs("content/docs/triggers", exist_ok=True)

triggers_dict = {}

# 1. From content/docs/zenenchants/triggers
if os.path.exists("content/docs/zenenchants/triggers"):
    for f in os.listdir("content/docs/zenenchants/triggers"):
        if f.endswith(".mdx") and f != "index.mdx":
            slug = f[:-4].lower()
            with open(os.path.join("content/docs/zenenchants/triggers", f), "r", encoding="utf-8", errors="ignore") as fp:
                raw = fp.read()
            title = slug
            desc = f"Disparador {slug} del motor ZenCore."
            m_title = re.search(r'title:\s*["\']([^"\']+)["\']', raw)
            if m_title:
                title = m_title.group(1)
            m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', raw)
            if m_desc:
                desc = m_desc.group(1)
            triggers_dict[slug] = (title, desc, clean_emojis(raw))

# 2. From content/docs/zencustomitems/triggers
if os.path.exists("content/docs/zencustomitems/triggers"):
    for f in os.listdir("content/docs/zencustomitems/triggers"):
        if f.endswith(".mdx") and f != "index.mdx":
            slug = f[:-4].lower()
            if slug not in triggers_dict:
                with open(os.path.join("content/docs/zencustomitems/triggers", f), "r", encoding="utf-8", errors="ignore") as fp:
                    raw = fp.read()
                title = slug
                desc = f"Disparador {slug} del motor ZenCore."
                m_title = re.search(r'title:\s*["\']([^"\']+)["\']', raw)
                if m_title:
                    title = m_title.group(1)
                m_desc = re.search(r'description:\s*["\']([^"\']+)["\']', raw)
                if m_desc:
                    desc = m_desc.group(1)
                triggers_dict[slug] = (title, desc, clean_emojis(raw))

print(f"Total unique triggers to write: {len(triggers_dict)}")

sorted_trig_slugs = sorted(triggers_dict.keys())
for slug in sorted_trig_slugs:
    title, desc, content = triggers_dict[slug]
    with open(f"content/docs/triggers/{slug}.mdx", "w", encoding="utf-8") as fp:
        fp.write(content)

trig_cards = "\n".join([
    f'  <Card title="{triggers_dict[slug][0]}" href="/docs/triggers/{slug}" description="{triggers_dict[slug][1]}" />'
    for slug in sorted_trig_slugs
])

with open("content/docs/triggers/index.mdx", "w", encoding="utf-8") as f:
    f.write(f'''---
title: "Triggers (Disparadores)"
description: "Catálogo completo de los {len(sorted_trig_slugs)} eventos y disparadores nativos soportados por ZenCore."
---

import {{ Card, Cards }} from 'fumadocs-ui/components/card';
import {{ Callout }} from 'fumadocs-ui/components/callout';

Los **Triggers** son los eventos de Minecraft que activan la ejecución de las habilidades. Cada disparador provee un contexto seguro con acceso al jugador, objetivo, vector de daño y variables.

---

## Catálogo de Triggers ({len(sorted_trig_slugs)})

<Cards>
{trig_cards}
</Cards>
''')

with open("content/docs/triggers/meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": "Triggers",
        "pages": ["index"] + sorted_trig_slugs
    }, f, indent=2)

print("Triggers section complete.")

print("--- 5. Building Filters Section ---")
os.makedirs("content/docs/filters", exist_ok=True)

# Parse filters from DOCS/ZenCustomItems/FILTERS_AND_MUTATORS.md
with open("DOCS/ZenCustomItems/FILTERS_AND_MUTATORS.md", "r", encoding="utf-8") as f:
    fm_raw = f.read()

# Extract Filter blocks
lines = fm_raw.split("\n")
filter_blocks = {}
current_sec = None
current_key = None
current_body = []

for line in lines:
    if line.startswith("## "):
        if "Filtro" in line:
            current_sec = "filters"
        elif "Mutador" in line:
            current_sec = "mutators"
        else:
            current_sec = None
    elif line.startswith("### `") and current_sec:
        if current_key and current_sec == "filters":
            filter_blocks[current_key] = "\n".join(current_body)
        current_key = line.split("`")[1].strip().lower().replace(" ", "_")
        current_body = [line]
    elif current_key and current_sec == "filters":
        current_body.append(line)

if current_key and current_sec == "filters":
    filter_blocks[current_key] = "\n".join(current_body)

sorted_filter_slugs = sorted(filter_blocks.keys())
for slug in sorted_filter_slugs:
    body = filter_blocks[slug]
    title = slug.upper()
    desc = f"Filtro {title} del motor ZenCore."
    # parse first description sentence
    for l in body.split("\n"):
        if l and not l.startswith("#") and not l.startswith("```"):
            desc = l.strip()
            break
    mdx_text = f"""---
title: "{title}"
description: "{desc}"
---

import {{ Callout }} from 'fumadocs-ui/components/callout';

{clean_emojis(body)}
"""
    with open(f"content/docs/filters/{slug}.mdx", "w", encoding="utf-8") as fp:
        fp.write(mdx_text)

filter_cards = "\n".join([
    f'  <Card title="{slug.upper()}" href="/docs/filters/{slug}" description="Filtro de contexto {slug.upper()}." />'
    for slug in sorted_filter_slugs
])

with open("content/docs/filters/index.mdx", "w", encoding="utf-8") as f:
    f.write(f'''---
title: "Filters (Filtros)"
description: "Catálogo completo de filtros de entidades, bloques y daño de ZenCore."
---

import {{ Card, Cards }} from 'fumadocs-ui/components/card';
import {{ Callout }} from 'fumadocs-ui/components/callout';

Los **Filtros** permiten restringir de forma limpia qué entidades o bloques se ven afectados por una habilidad sin necesidad de anidar condicionales complejos.

---

## Catálogo de Filtros ({len(sorted_filter_slugs)})

<Cards>
{filter_cards}
</Cards>
''')

with open("content/docs/filters/meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": "Filters",
        "pages": ["index"] + sorted_filter_slugs
    }, f, indent=2)

print("Filters section complete.")

print("--- 6. Building Mutators Section ---")
os.makedirs("content/docs/mutators", exist_ok=True)

mutator_blocks = {}
current_sec = None
current_key = None
current_body = []

for line in lines:
    if line.startswith("## "):
        if "Filtro" in line:
            current_sec = "filters"
        elif "Mutador" in line:
            current_sec = "mutators"
        else:
            current_sec = None
    elif line.startswith("### `") and current_sec:
        if current_key and current_sec == "mutators":
            mutator_blocks[current_key] = "\n".join(current_body)
        current_key = line.split("`")[1].strip().lower().replace(" ", "_")
        current_body = [line]
    elif current_key and current_sec == "mutators":
        current_body.append(line)

if current_key and current_sec == "mutators":
    mutator_blocks[current_key] = "\n".join(current_body)

sorted_mutator_slugs = sorted(mutator_blocks.keys())
for slug in sorted_mutator_slugs:
    body = mutator_blocks[slug]
    title = slug.upper()
    desc = f"Mutador matemático {title} del motor ZenCore."
    for l in body.split("\n"):
        if l and not l.startswith("#") and not l.startswith("```"):
            desc = l.strip()
            break
    mdx_text = f"""---
title: "{title}"
description: "{desc}"
---

import {{ Callout }} from 'fumadocs-ui/components/callout';

{clean_emojis(body)}
"""
    with open(f"content/docs/mutators/{slug}.mdx", "w", encoding="utf-8") as fp:
        fp.write(mdx_text)

mutator_cards = "\n".join([
    f'  <Card title="{slug.upper()}" href="/docs/mutators/{slug}" description="Mutador {slug.upper()} para transformación de variables." />'
    for slug in sorted_mutator_slugs
])

with open("content/docs/mutators/index.mdx", "w", encoding="utf-8") as f:
    f.write(f'''---
title: "Mutators (Mutadores)"
description: "Catálogo completo de mutadores matemáticos y cinemáticos de ZenCore."
---

import {{ Card, Cards }} from 'fumadocs-ui/components/card';
import {{ Callout }} from 'fumadocs-ui/components/callout';

Los **Mutadores** alteran y transforman matemáticamente valores de contexto (como el daño infligido o variables de instancia) antes de que los efectos se ejecuten.

---

## Catálogo de Mutadores ({len(sorted_mutator_slugs)})

<Cards>
{mutator_cards}
</Cards>
''')

with open("content/docs/mutators/meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": "Mutators",
        "pages": ["index"] + sorted_mutator_slugs
    }, f, indent=2)

print("Mutators section complete.")

print("--- 7. Updating content/docs/meta.json ---")
with open("content/docs/meta.json", "r", encoding="utf-8") as f:
    root_meta = json.load(f)

# The user explicitly requested:
# Top: General, Effects, Conditions, Filters, Mutators, Triggers (like Libreforge in Eco)
# Then separator
# Bottom: The plugins
plugins_list = [
    "zenafkzone",
    "zenauctions",
    "zenbank",
    "zenchat",
    "zenchatgames",
    "zencosmetics",
    "zencustomitems",
    "zeneconomy",
    "zenenchants",
    "zenfairy",
    "zenmilestone",
    "zenorbs",
    "zenpvpcore",
    "zenrankups",
    "zenrewards",
    "zenstorage"
]

root_meta["pages"] = [
    "general",
    "effects",
    "conditions",
    "filters",
    "mutators",
    "triggers",
    "---PLUGINS---"
] + plugins_list

with open("content/docs/meta.json", "w", encoding="utf-8") as f:
    json.dump(root_meta, f, indent=2)

print("content/docs/meta.json updated!")
