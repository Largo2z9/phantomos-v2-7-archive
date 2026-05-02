---
name: skills
description: Navigable menu of all skills available in this workspace. Grouped by operator intent. Marks custom skills with [custom] tag. Drill into a category by typing its number or a keyword.
---

# /skills, navigable menu

Operator-facing browser for all skills available in this workspace. Read top to bottom before acting.

## Mode detection

Check the user's argument :

| Argument | Mode |
|---|---|
| empty (just `/skills`) | **menu** : show all categories with counts |
| number (e.g. `/skills 2`) | **drill** : show skills in category N |
| keyword (e.g. `/skills audit`) | **search** : show skills whose name or trigger matches keyword |

## Mode menu, default

1. Read `.skills/INDEX.md`. Parse the H2 headings (`## I want to...`) as categories.
2. For each category, count the skills listed in the markdown table below the heading.
3. Read `.skills/_manifest.json`. Mark each skill that has a path containing `/custom/` with a `[custom]` tag.
4. Render the menu :

```
SKILLS DISPONIBLES (N total, M custom)

CATÉGORIES
  [1] {category 1 name}     ({count} skills)
  [2] {category 2 name}     ({count} skills)
  ...
  [N] {category N name}     ({count} skills)

Tape /skills {numero} pour voir les skills d'une catégorie.
Tape /skills {mot-clé} pour chercher par nom ou intent.
```

Use the categories *exactly* as they appear in `.skills/INDEX.md` H2 headings. Do not invent. Do not reorder.

## Mode drill

1. Take the number from the argument.
2. Resolve to the Nth H2 in `.skills/INDEX.md`.
3. Render the skills in that category, with one-line description :

```
{Category name}, {count} skills

  {skill-name-1}     {operator-says-trigger}
  {skill-name-2}     {operator-says-trigger}
  ...
  {skill-name-N}     {operator-says-trigger}

Tape un nom de skill pour voir son trigger complet et son output.
```

For each skill, find the matching frontmatter block in `.skills/_manifest.json` (by `name` field). Add `[custom]` tag at the end of the line if `path` contains `/custom/`. Use the `triggers` field of the manifest entry, not the operator-says column from INDEX.md (the manifest is the source of truth for triggers, INDEX.md is the human bridge).

## Mode search

1. Take the keyword from the argument.
2. Filter skills in `.skills/_manifest.json` whose `name` or any element in `triggers` contains the keyword (case-insensitive).
3. Render matching skills in a flat list :

```
SKILLS MATCHING "{keyword}", {count} hits

  {skill-name-1}     {short trigger}     [{category from INDEX.md if findable}]
  {skill-name-2}     {short trigger}     [{category}]
  ...

Tape /skills {numero} pour browser par catégorie.
```

If no match, render :
```
Aucun skill ne match "{keyword}".

Catégories disponibles : ...
Tape /skills pour voir le menu complet.
```

## Constraints

- **Read-only.** This command never mutates anything. Just read INDEX.md and _manifest.json.
- **No agent invention.** Skill names, categories, triggers come from the source files. Never paraphrase or invent.
- **Custom skills first-class.** Skills under `.skills/skills/custom/` are listed alongside shipped skills, just tagged `[custom]`. Treat them as equally valid.
- **One screen output.** Aim for output that fits in one terminal screen. If a category has more than 15 skills, paginate or note "tape /skills {numero} {keyword}" pour filtrer.
