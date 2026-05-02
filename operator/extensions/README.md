# Operator extensions

Custom entities scoped à toi (l'opérateur), pas à une marque ou une mission spécifique. C'est la couche où vit **tout ce qui constitue ton écosystème opérationnel** au sens large, dès que tu décides de l'encoder : ton réseau de contacts (pros, persos, famille, mentors, voisinage), tes opportunités en cours (commerciales, formations, projets, partenariats), tes prestataires récurrents (freelances, artisans, professionnels de santé, conseillers), tes initiatives (side projects, hobbies, créations), ton domicile et sa gestion (domotique, agenda famille, ménage), ton suivi personnel (santé, finance, lecture, apprentissage, voyages), ton admin perso, et n'importe quelle autre dimension de ta vie que tu juges digne d'être systématisée.

## Pourquoi cette couche existe

PhantomOS ship aujourd'hui les entités DTC paid par défaut **par marque** (brand, product, offer, audience, angle, learnings, strategy). Ça couvre tes opérations paid acquisition. Ça ne couvre pas ce qui entoure tes missions ni ce qui n'a rien à voir avec tes opérations. Ton réseau humain élargi, tes prestataires hors-mission, tes opportunités pré-mission, ta domotique, ta santé, tes lectures, tes loisirs, tes obligations admin perso : tout ça vit ici.

La couche operator extensions a la même mécanique que les extensions brand (`brands/{slug}/custom/`), les mêmes règles de gouvernance, le même skill `scaffold-extension`. Juste scope=operator au lieu de scope=brand.

## Ce que tu peux encoder ici

Il n'y a pas de liste imposée. Le système n'a aucune opinion sur ce qui mérite d'être encodé ou pas. Quelques exemples qui correspondent naturellement à cette couche :

- **`contacts/`** : les personnes que tu veux que ton assistant garde en tête. Pros, persos, famille, mentors, voisinage, médecins, partenaires de hobby, peu importe. Ce qui compte c'est qu'au moment où tu en parles, l'assistant les connaît.
- **`opportunities/`** : tout ce qui est en cours mais pas encore tranché. Commercial (deals, retainers), perso (raise, formation, achat immobilier, vacances en réflexion), créatif (idée de projet, side initiative à explorer).
- **`vendors/`** : les prestataires que tu réutilises. Freelances pro, artisans, plombier, comptable, pédiatre, prof de yoga, jardinier, mécanicien, peu importe le domaine.
- **`projects/`** : tes initiatives en cours. Pro et perso mélangés. Lancement d'une marque, écriture d'un livre, rénovation maison, formation continue, projet open source, marathon en préparation.
- **`home/`** : ce qui touche à ton domicile. Domotique, agenda famille, courses récurrentes, entretien, événements, gestion vie quotidienne.
- **`admin/`** : trackers d'obligations administratives. Légal, fiscal, assurances, cotisations, renouvellements de pièces, échéances bancaires, abonnements.
- **`learning/`** : ton suivi intellectuel. Livres en cours, formations, cours, podcasts, recherches en cours, idées à creuser.
- **`health/`** : suivi médical et bien-être. RDV médecins, traitements, examens, sport, nutrition, sommeil si tu veux que ton assistant compose dessus.
- **`finance/`** : ta gestion financière perso. Investissements, comptes, échéances, objectifs d'épargne.
- **`creative/`** : tes projets créatifs. Musique, écriture, art, side projects sans visée business.

C'est juste une liste illustrative. Si demain tu veux encoder ton suivi de plantes d'intérieur, ta collection de vinyles, ton arbre généalogique ou les anniversaires de ton entourage, le système accueille pareil.

Le critère est simple : si tu veux que ton assistant compose avec cette dimension (te rappeler des choses, croiser, suggérer, écrire pour toi), encode. Si tu veux juste un stockage passif, garde ça dans Notion ou Sheets. Le système lui-même ne refuse rien, la question est si tu vas en tirer de la valeur en encodant plutôt qu'en stockant.

## Comment ajouter une extension ici

Même chemin que côté brand, juste scope=operator. Trois options :

1. **Skill `scaffold-extension`** (recommandé). Tu dis à l'agent en langage naturel : *"je veux scaffolder un carnet de contacts opérateur"*, *"crée une extension operator pour ma domotique"*, *"je veux suivre mes lectures"*, *"range mes RDV médicaux"*. Le skill fait le chemin canonique (capture intention, check naming, draft schema, validation, scaffolding, registry).
2. **Cloner l'exemple.** Copie `_EXAMPLE/contacts/` vers `operator/extensions/{ton-type}/`, ajuste schema et README, register dans `index.json`.
3. **Depuis une donnée en main** (mode data-first de `scaffold-extension`). Tu apportes un bloc structuré : *"voici ma liste de contacts, range-la proprement"*, *"voici l'export de mes lectures Kindle"*. Le skill parse, scaffolde, peuple en un seul flux.

## Composition cross-scope

Un même type peut coexister à plusieurs scopes. Exemple `vendors` :

- **Operator scope** (`operator/extensions/vendors/`) : tous les prestataires que tu as identifiés à un moment ou un autre, leur domaine, ton historique avec eux.
- **Brand scope** (`brands/{slug}/custom/vendors/`) : ceux assignés à une mission précise, avec contexte spécifique à cette mission.

L'agent croise les scopes quand pertinent. Tu lui demandes *"qui dans mon réseau pourrait m'aider sur ce sujet"*, il regarde les vendors operator-scope (qui je connais ?) et les vendors brand-scope si c'est lié à une mission active (qui bosse déjà ?), il propose l'intersection.

Pareil pour contacts : tes contacts opérateur peuvent référencer une marque sur laquelle ils interviennent (`brand_refs[]`), ce qui permet à l'agent de croiser *"contacts pertinents sur la mission X"* sans dupliquer.

## Règles de gouvernance

Identiques à brand-scope, voir `docs/system/extending.md` pour le canon complet :

1. **Schema déclaré.** Chaque extension ship un JSON Schema avec `_version`, `_schema`, `_field_types`. `validate-resources` refuse les extensions non-conformes.
2. **Registered dans `index.json`.** Chaque custom entity scope=operator ajoute une entrée sous `extensions[]` avec `scope: operator`. Les sidecars sur `operator/profile.json` (`profile.extensions.json`) sont convention-discovered, pas registered.
3. **README documentant le purpose.** Court doc expliquant ce que c'est, pourquoi tu l'as encodé, quelles autres entités ça référence, quelles skills consomment.

## Mutation gate, identique à brand-side

Toutes les écritures passent par `write_to_context()`. Convention de field path :

```
operator.{entity_type}.{instance_slug}.{field_name}
```

Exemple :

```
write_to_context(field_path="operator.contacts.marc-dubois.touch_history[]",
 value={observed_at: "2026-04-27T14:30:00Z", channel: "email", note: "discussion lecture en cours"},
 source="operator",
 confidence=0.95,
 mode="direct")
```

L'agent résout `operator.contacts.*` vers `operator/extensions/contacts/{slug}.json`. Même pattern pour n'importe quel autre type operator-scope.

## Sidecars sur `profile.json`

Si tu veux étendre `operator/profile.json` lui-même (champs additionnels sur toi qui ne rentrent pas dans le schema universel profile), utilise `operator/profile.extensions.json`. Même convention que les sidecars brand-side : append-only, jamais override le core, discovered par convention.

## Cross-references

- `docs/system/extending.md` : canon complet de la couche extension (trois scopes, gouvernance, mutation rules)
- `.skills/skills/scaffold-extension/SKILL.md` : orchestrator pour scaffolder n'importe quel scope
- `_EXAMPLE/contacts/` : exemple canonique à cloner
- `index.json` : registre central où les extensions operator-scope sont déclarées
