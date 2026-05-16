# `_EXAMPLE/` · cas pédagogique canon · read-only

**Tu n'es pas dans la brand active de l'opérateur.** Tu es dans le cas pédagogique partagé canon PhantomOS.

`_EXAMPLE/stepprs/` est utilisé comme cas illustratif pour rendre tangibles les concepts canon (compositional cartography, sub-audience hiérarchique, formula OTRB, investigation-posture, etc.). Stepprs · brand pédagogique cas canonique · cf `_EXAMPLE/README.md` pour contexte complet.

## Règles strictes pour tout agent

**READ-ONLY canon.** Tu peux LIRE n'importe quel fichier dans `_EXAMPLE/` pour comprendre les patterns canon et les citer comme exemple. Tu ne dois JAMAIS écrire dans `_EXAMPLE/` (mutation gate `write_to_context` refusé sur ce folder · NE-PAS bypass via Edit/Write direct).

**Référence pédagogique, pas runtime brand.** Si tu rencontres un cas où tu serais tenté de "lancer une production sur Stepprs", "scraper Stepprs", "produire un brief copy pour Stepprs", arrête-toi. Stepprs n'est pas une brand active. L'opérateur n'a pas demandé à travailler sur Stepprs · il travaille sur SA marque qui vit dans `brands/{son-slug}/`.

**Usage canon autorisé.**
- Lire les fichiers Stepprs pour comprendre la structure canon
- Citer Stepprs comme exemple dans `/breakdown stepprs {topic}` (la slash command vitrine pédagogique)
- Pointer un atome Stepprs spécifique à l'opérateur pour clarifier un concept (e.g. *"regarde `_EXAMPLE/audiences/workers-shifts/profile.json` pour voir le pattern parent/enfants canon"*)

**Usage anti-pattern.**
- Traiter Stepprs comme la brand active de l'opérateur
- Hallucination *"tes audiences workers-shifts...", "ton produit massage-insoles..."* (ce sont les audiences ET le produit de Stepprs, pas de l'opérateur)
- Lancer un skill production sur Stepprs (compose-creative, produce-copy-brief, etc.) sauf si l'opérateur a explicitement demandé *"montre-moi comment ça donnerait sur Stepprs"* en mode démo
- Écrire dans `_EXAMPLE/` (refused canon)

## Cross-refs

- Doctrine root · `CLAUDE.md` workspace-template section `_EXAMPLE/ folder · anti-hallucination canon`
- Slash command vitrine · `.claude/commands/breakdown.md`
- README local · `brands/_EXAMPLE/README.md` (ordre de lecture suggéré pour comprendre Stepprs comme exemple)
