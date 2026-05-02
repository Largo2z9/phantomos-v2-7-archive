# contacts (operator scope) · example custom entity

Illustrative custom entity tracking les personnes que l'opérateur veut garder dans la conscience de son assistant. Operator scope means this lives at `operator/extensions/contacts/`, pas sous une marque spécifique. Copie ce dossier pour démarrer ton propre carnet de contacts ou lis-le pour comprendre la forme canonique d'une extension operator-scope.

## Purpose

Tracker chaque personne digne d'être présente dans la mémoire de ton assistant, à travers tes différents contextes. Pros, persos, famille, mentors, voisinage, médecins, partenaires de hobby, peu importe le registre. Une fiche par contact. Touch history append-only. L'agent compose des surfacings proactifs quand pertinent : *"Marc t'a contacté il y a 3 mois sur ce sujet, et tu as une initiative en cours pile dans son scope, on lui écrit ?"*. Ça marche pour un échange pro autant que pour un anniversaire de pote ou un suivi avec ton ostéo.

## Files

- **`schema.json`** : JSON Schema pour les instances de cette entité. Déclare `_version`, `_schema`, `_field_types` canon. Valide les champs requis au moment de l'écriture.
- **`marc-dubois.json`** : exemple d'instance avec trois entrées de touch.
- **`README.md`** : ce fichier.

## Cross-references vers d'autres entités

- **`brand_refs[]`** résout vers `brands/{slug}/`. Utilisé quand un contact est associé à une mission spécifique. Vide si le contact n'a aucun lien avec une mission encodée.
- **`activity_refs[]`** résout vers `operator/extensions/{type}/{slug}.json` si tu as d'autres extensions operator (opportunities, projects, learning, etc.). Permet d'ancrer un contact à une initiative en cours, peu importe qu'elle soit pro ou perso.

Les deux refs sont optionnelles. Beaucoup de contacts dans un réseau n'en ont aucune (relations purement humaines, pas attachées à un projet).

## Writing new touch entries

Les touch entries sont append-only via `write_to_context`, jamais éditées en place :

```
write_to_context(
  field_path="operator.contacts.marc-dubois.touch_history[]",
  value={
    observed_at: "2026-04-27T14:30:00Z",
    channel: "email",
    note: "échangé sur sa lecture en cours et le projet Y"
  },
  source="operator",
  confidence=0.95,
  mode="direct"
)
```

L'agent met à jour `last_touch` automatiquement à la lecture de `touch_history` (champ derived, jamais écrit manuellement).

## Index.json registration

Ajout une fois par entity type (pas par instance) :

```json
{
  "type": "contacts",
  "scope": "operator",
  "schema": "operator/extensions/contacts/schema.json",
  "cross_refs": [
    "brand_refs → brands/{slug}/",
    "activity_refs → operator/extensions/{type}/{slug}.json"
  ],
  "owner_skill": null
}
```

`owner_skill: null` parce que dans cet exemple l'opérateur maintient les contacts manuellement. Si tu construis un skill qui peuple (par exemple : import depuis un export LinkedIn, ou capture depuis tes signatures email), ajoute son nom ici avec le préfixe `custom:`.

## Compositions que l'agent peut faire une fois ça encodé

- *"Qui je n'ai pas relancé depuis 3 mois sur quelque chose d'en cours ?"* : l'agent walk `touch_history` par contact, croise avec `activity_refs` non-clos, surface les gaps.
- *"Qui je connais qui pourrait m'aider sur ce sujet ?"* : l'agent filtre `tags[]` et `notes` par domaine demandé, retourne top matches avec leur dernier touch.
- *"Pour ce projet, qui dans mon réseau pourrait apporter ?"* : l'agent croise contacts avec `brand_refs[]` et tags pertinents au domaine du projet.
- *"Anniversaires de mon entourage proche cette semaine ?"* : si tu as encodé birthday en field optionnel, l'agent surface.
- *"Mon ostéo m'a dit de revenir tous les 3 mois, c'est quand mon dernier RDV avec lui ?"* : l'agent walk le `touch_history` du contact ostéo et propose une relance.

Ces compositions ne sont pas hardcodées comme skills. Elles émergent du fait que l'encoding est propre et que l'agent lit cette extension comme il lirait n'importe quelle autre entité.

## Cloner cet exemple

Pour démarrer ton propre carnet de contacts :

```bash
cp -R operator/extensions/_EXAMPLE/contacts operator/extensions/contacts
```

Puis : ajuste `schema.json` si tu veux des champs différents (par exemple ajouter `birthday`, `referred_by`, taxonomie de tags propre à ton mode de classement, lieu géographique, langues parlées), supprime l'instance d'exemple, register dans `index.json`, commence à ajouter des contacts via langage naturel.
