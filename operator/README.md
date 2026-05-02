# Operator · contexte macro transversal

Ce dossier contient le profil **opérateur** (toi, l'utilisateur du workspace), pas un profil brand.

## Fichiers

- `profile.json` : qui tu es, tes préférences, ton historique d'outils, tes attentes, tes anti-patterns perso.
- `awareness.json` : état de ta connaissance actuelle du système (ce que tu as déjà vu, ce qui n'a pas besoin d'être ré-introduit).
- `installation.json` : métadonnées de ton installation workspace.
- `profile.extensions.json` (sidecar, optionnel) : champs additionnels sur toi qui ne rentrent pas dans le schema universel `profile.json`. Convention-discovered, pas registered.
- `extensions/` : couche d'extensions custom scopées à toi, transversales à toutes tes missions. Carnet de contacts pro et perso, opportunités, prestataires, projets, domotique, suivi santé, lectures, hobbies, admin perso, n'importe quoi que tu juges digne d'être systématisé. Voir `extensions/README.md` pour le canon complet.

## Comment ça se remplit

**Jamais en questionnaire.** Le fichier est populé progressivement à travers les sessions par `learn-from-session`, quand tu laisses tomber une info :

- *"J'ai testé Lindy, abandonné après 3 semaines"* → ajouté dans `stack_history`.
- *"Je réponds toujours en bullets, pas en prose"* → ajouté dans `preferences.communication_style`.
- *"Je déteste les outils qui demandent 15 questions avant de produire quoi que ce soit"* → ajouté dans `anti_patterns_perso`.

Tu n'as jamais à ouvrir ce fichier toi-même.

## À quoi ça sert

L'agent consulte `profile.json` en début de session pour calibrer son registre. Plus le fichier est riche, plus les outputs te ressemblent.

**Distinction critique** : les infos qui concernent *toi* vivent ici (dans `profile.json`, son sidecar `profile.extensions.json`, ou les custom entities sous `extensions/`). Les infos qui concernent *une marque ou une mission précise* vivent dans `brands/{slug}/learnings.json` ou `brands/{slug}/custom/`. Le routing est fait par `learn-from-session` et par le skill `scaffold-extension` (qui détecte le scope automatiquement à partir de l'intention).

**Trois scopes possibles** pour les custom entities :

- **brand-scope** (`brands/{slug}/custom/`) : lié à une mission précise.
- **operator-scope** (`operator/extensions/`) : transversal à toi, peu importe le registre (pro, perso, famille, hobby, santé, domotique, peu importe).
- **workspace-scope** (`resources/extensions/`) : partagé entre toutes tes marques.

Voir `docs/system/extending.md § Three scopes` pour le canon complet.
