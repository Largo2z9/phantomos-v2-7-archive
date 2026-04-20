# Operator — contexte macro transversal

Ce dossier contient le profil **opérateur** (toi, l'utilisateur du workspace), pas un profil brand.

## Fichiers

- `profile.json` — qui tu es, tes préférences, ton historique d'outils, tes attentes, tes anti-patterns perso.

## Comment ça se remplit

**Jamais en questionnaire.** Le fichier est populé progressivement à travers les sessions par `learn-from-session`, quand tu laisses tomber une info :

- *"J'ai testé Lindy, abandonné après 3 semaines"* → ajouté dans `stack_history`.
- *"Je réponds toujours en bullets, pas en prose"* → ajouté dans `preferences.communication_style`.
- *"Je déteste les outils qui demandent 15 questions avant de produire quoi que ce soit"* → ajouté dans `anti_patterns_perso`.

Tu n'as jamais à ouvrir ce fichier toi-même.

## À quoi ça sert

L'agent consulte `profile.json` en début de session pour calibrer son registre. Plus le fichier est riche, plus les outputs te ressemblent.

**Distinction critique** : les infos qui concernent *toi* vivent ici. Les infos qui concernent *une marque* vivent dans `brands/{slug}/learnings.json`. Le routing est fait par `learn-from-session`.
