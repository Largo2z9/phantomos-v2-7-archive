---
name: about
description: Documentation deep PhantomOS · vision, artefacts, mécanismes, termes canon, ce qui le rend singulier. Backup exhaustif de `/tour` (qui est l'explication conversationnelle guidée). Pour comprendre l'architecture et la philosophie d'un bloc.
version: v2.81.0
---

# /about · documentation deep PhantomOS

Documentation longue opt-in pour l'opérateur curieux qui veut comprendre profondément l'architecture, la philosophie et les mécanismes PhantomOS. Pour démarrage rapide, utiliser `/tour`.

**Cible** · opérateur curieux post-onboarding, prospect partenaire, contributeur skill, opérateur expert en recadrage.

**Registre** · institutionnel sérieux + accessible. Voix Vercel/GitHub product shipped. Zéro jargon plumbing (canon `output-clarity-doctrine.md` v2.79.2).

**Language** · adapter FR/EN selon language opérateur détecté (cf canon Language root CLAUDE.md). Output bilingue conditionnel sur premier signal opérateur. Defaults FR.

---

## Output pattern (à rendre tel quel · adapter FR/EN selon opérateur)

```
═══════════════════════════════════════════════════════════════════
PhantomOS · documentation deep
═══════════════════════════════════════════════════════════════════


## 1. Vision

PhantomOS est un workspace agentic pour opérateurs DTC.
Tu encodes ton métier une seule fois (marques, produits, audiences,
stratégies, process). Le système raisonne, exécute et apprend en
continu sur cet univers persistant.

L'environnement opérationnel devient ta fondation. Chaque session
s'appuie sur l'univers métier déjà encodé. Chaque output produit
enrichit la connaissance disponible pour les sessions suivantes.

  ─────────────────────────────────────────────────────────────────────

  Le principe
  · Ton univers métier est encodé une fois, pas re-décrit chaque session
  · Une marque vit dans son substrat · produits, audiences, stratégie
  · La connaissance s'enrichit cycle après cycle, elle ne se perd pas
  · L'agent raisonne sur cet univers, pas sur une question isolée


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 2. Pourquoi ça existe

Le métier DTC fonctionne sur trois friction structurelles.

  ─────────────────────────────────────────────────────────────────────

  Contexte client réinventé chaque session
  Tu re-brief ta conversation à chaque démarrage. Ce que tu as dit
  hier est perdu. La connaissance ne s'accumule jamais.

  Process fragmentés
  Ta connaissance métier vit éclatée entre un outil de doc, un de
  données, un de tâches, un de raisonnement. Aucun ne raisonne sur
  l'ensemble. Tu fais le pont à la main, à chaque fois.

  Capitalisation perdue sur les apprentissages
  Chaque test, chaque audit, chaque correction reste un signal isolé.
  Rien ne se canonise. Tu redécouvres les mêmes leçons six mois après.

  ─────────────────────────────────────────────────────────────────────

PhantomOS adresse les trois en un substrat unique · ton univers métier
encodé une fois, raisonné par l'agent, enrichi à chaque cycle.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 3. Les 4 artefacts de l'écosystème

PhantomOS s'organise autour de quatre artefacts canon. Comprendre les
quatre · comprendre comment ça raisonne.

  ─────────────────────────────────────────────────────────────────────

  Artefact      Définition                                Exemple concret
  ───────────   ─────────────────────────────────────     ───────────────
  Workspace     Environnement personnel persistant.       Ton dossier local
                Stockage local. Zéro lock-in.             avec tes brands,
                Tes données restent à toi.                operator, settings.

  Brand         Une marque encodée. Substrate complet     Stepprs encodée ·
                (specs produits, audiences, angles        atlas + skills
                paid, stratégie, learnings, roadmap).     opérables dessus.

  Skill         Outil opérationnel exécutable. 80         produce-paid-angles,
                shipped. Cartographier, produire,         audit-meta-account,
                auditer, scaler.                          decompose-ad.

  Doctrine      Principe architectural canon. 21          Investigation Posture,
                shipped. Guide le raisonnement            Output Clarity,
                système.                                  Onboarding Holistic.

  ─────────────────────────────────────────────────────────────────────

  Note · Atlas (cartographie stratégique complète d'une marque) est
  l'output canonique de Brand encodée · cf glossaire §7 pour définition.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 4. Comment ça raisonne

Quatre mécanismes structurent le raisonnement du système.

  ─────────────────────────────────────────────────────────────────────

  Mémoire métier persistante
  Ton univers encodé reste disponible session après session. Rien
  à re-briefer.

  Skill routing
  Tu décris ton intent en langage normal. L'agent route vers la
  bonne capacité, sans syntaxe à mémoriser (cf §7).

  Doctrines canon
  Des principes qui cadrent chaque raisonnement stratégique. Pas
  d'improvisation, une démarche reproductible.

  Réflexion montrée
  L'agent expose son raisonnement, pas seulement sa conclusion ·
  ce qu'il observe, ce qu'il déduit, ce qu'il ignore encore.

  ─────────────────────────────────────────────────────────────────────

La combinaison des quatre produit une intelligence métier opérable,
auditable, défendable, reproductible cross-session.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 5. Cycle opérationnel

Trois phases canon · Encode, Opère, Capitalise.

  ─────────────────────────────────────────────────────────────────────

  Phase          Fréquence              Démarche
  ────────       ───────────────        ──────────────────────────────
  Encode         1 fois par brand,      Brand setup, scrape produits,
                 ~30 min                cartographie audiences, atlas
                                        complet généré.

  Opère          Cycles quotidiens      Skills exécutent. Produire
                 5-30 min               angles paid, briefs copy,
                                        audits perf, adaptations créa.

  Capitalise     Continu                Learnings captés. Canon enrichi.
                                        Cycles propagés cross-brands.

  ─────────────────────────────────────────────────────────────────────

Encode est ponctuel. Opère est ton quotidien. Capitalise tourne en
arrière-plan sur chaque output validé.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 6. Ce qui le rend singulier

Quatre propriétés que PhantomOS tient ensemble, par conception.

  ─────────────────────────────────────────────────────────────────────

  Un univers métier qui persiste
  Ta marque est encodée et raisonnée d'une session à l'autre. Le
  contexte n'est pas un copier-coller à refaire.

  Un raisonnement cadré, pas improvisé
  Des doctrines structurent chaque sortie stratégique. La démarche
  est la même quel que soit l'opérateur ou le jour.

  De l'exécution, pas seulement du texte
  Le système produit des livrables opérables sur ta donnée · angles
  paid, briefs, audits, cartographies. Pas des notes à recopier.

  Une connaissance qui se capitalise
  Chaque correction, chaque apprentissage validé enrichit le canon.
  Tu ne redécouvres pas les mêmes leçons six mois plus tard.

  ─────────────────────────────────────────────────────────────────────

  PhantomOS est construit pour tenir ces quatre propriétés en même
  temps, par conception.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 7. Termes canon

Glossaire des 13 termes forts à connaître pour comprendre PhantomOS.
Ces termes structurent le système · les rencontrer dans la
documentation déclenche le bon mental model.

  ─────────────────────────────────────────────────────────────────────

  Workspace
  Environnement personnel persistant. Stockage local. Canon pour
  toutes tes marques. Tes données restent à toi, zéro lock-in
  (cf §3).

  Brand
  Marque encodée dans le système. Entité racine du raisonnement
  métier. Contient specs produits, audiences, angles, stratégie,
  learnings, roadmap (cf §3).

  Skill
  Outil opérationnel exécutable. Unité atomique d'action. 80
  disponibles cross 7 territoires métier (cf §3).

  Substrate
  Fondations stables encodées de ta marque. Atlas produits par
  build-atlas-complete. Ne change pas runtime, alimente toutes les
  productions downstream.

  Production
  Livrables runtime générés à la demande. Briefs copy, créas,
  matrices paid. Consomment le substrate, produisent un output
  daté et auditable.

  Atlas
  Cartographie stratégique complète d'une marque. Substrate.
  Contient brand identity, produits, audiences, angles, stratégie.
  Fondation pour toute production downstream.

  Investigation Posture
  5 sections obligatoires sur tout output stratégique · observé,
  déduit, inconnu, leviers, close ouvert. Doctrine racine
  anti-affirmation hallucinée.

  Decomposition Visibility
  L'agent MONTRE sa réflexion en matrices. 4 niveaux canon
  (décomposition produit, many-to-many, stage filter, méthode
  pédagogique).

  Mutation gate
  Toute écriture passe par un canon validé via write_to_context.
  Rien direct en JSON. Audit trail complet. Aucune corruption
  silencieuse possible.

  Skill routing
  Tu n'invoques pas un skill technique. Tu décris ton intent.
  L'agent route vers le bon skill canon depuis le manifest.

  Canon
  Règles métier intangibles encodées par doctrines. 21 doctrines
  shipped. Garantissent cohérence cross-session et cross-opérateur.

  Doctrine
  Principe architectural racine qui guide le raisonnement système.
  Pas un outil, un guide structurel pour tous les skills downstream.

  Panorama territoires
  Vue 360° des 7 métiers DTC sur pied d'égalité visuelle. Canon
  onboarding holistique. L'opérateur se reconnaît dans le panorama,
  choisit son entrée libre.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 8. Comment ça reste honnête

Six mécanismes structurels anti-hallucination et anti-improvisation.

  ─────────────────────────────────────────────────────────────────────

  Mécanisme                          Effet
  ────────────────────────────       ─────────────────────────────────
  Investigation Posture              5 sections obligatoires (observé,
                                     déduit, inconnu, leviers, close
                                     ouvert) sur tout output stratégique.

  Decomposition Visibility           4 niveaux matriciels canon. L'agent
                                     PROUVE qu'il a compris en MONTRANT
                                     sa réflexion visible.

  Sourcing tags                      Auto-tag observé / déduit / déclaré
                                     / incertain sur chaque fait encodé.
                                     Confidence chain explicit.

  Confidence chain                   Niveau forte / moyenne / faible /
                                     TRÈS faible explicit. Aucune
                                     hypothèse présentée comme fait.

  Mutation gate                      Écritures validées canon, pas direct
                                     JSON. Aucune corruption silencieuse.
                                     Audit trail complet.

  Skill routing systémique           Cf §7 glossaire pour définition.
                                     Garantit que tu invoques jamais
                                     freestyle prose par défaut.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 9. Les 7 territoires DTC

Panorama capabilities détaillé. Les 7 métiers DTC couverts ou en
backlog explicit.

  ─────────────────────────────────────────────────────────────────────

  Territoire                       Statut   Cycle       Capacités core
  ──────────────────────────       ──────   ─────────   ──────────────
  Creative & Copy Production        ✓       5-30 min    Paid angles,
                                                        copy briefs,
                                                        creative composition,
                                                        sales letters DR.

  Tracking & GTM                    ○       backlog     Pixels Meta/Google,
                                            v2.80       server-side, consent
                                                        mode, coverage audits.

  Media Buy & Performance           ✓       10-30 min   Campagnes Meta,
                                                        audits perf, score
                                                        matrices, brief-day.

  Brand Strategy                    ✓       20-45 min   Positioning canvas,
                                                        voice 4D, archetypes,
                                                        purpose.

  Ops & Workflow                    ◐       5-15 min    Todos, agendas,
                                                        onboarding, setup,
                                                        scripts.

  Business Pilotage                 ◐       backlog     Unit economics, WBR,
                                            v2.79.x     cohort retention,
                                                        roadmap.

  Lifecycle & CRO                   ◐       backlog     PDP, landing, email
                                            v2.81+      flows, upsell, LTV.

  ─────────────────────────────────────────────────────────────────────

Les territoires ○ open annoncent honnêtement l'invocation freestyle
prose disponible ou l'attente du skill canon backlog. Les territoires
◐ partial mixent skills shipped et NEW à venir. Pas de territoire
surévalué.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## 10. Pour démarrer

Trois commandes canon + setup pour entrer dans PhantomOS selon ton intent.

  ─────────────────────────────────────────────────────────────────────

  /tour       Explication conversationnelle guidée de PhantomOS
  /phantom    État du workspace
  /skills     Catalogue exécutable

  ─────────────────────────────────────────────────────────────────────

  Setup ta première marque · paste URL Shopify ou décris ce que tu
  opères. Le système cartographie en ~5 minutes.


═══════════════════════════════════════════════════════════════════
✓ shipped  ◐ partial  ○ open territoire  ✗ absent  ⚠ critique
═══════════════════════════════════════════════════════════════════
```

---

## Bilingual rule

Detect operator language at first turn (cf canon Language root CLAUDE.md). Output FR (default) OR EN according to detection. Adapter prose des 10 sections selon language. Termes canon section 7 restent identifiés tel quel (Substrate, Production, Atlas, etc.) avec définition adaptée language opérateur.

**EN equivalents indicatifs** (rendre selon detection, jamais codé en dur dans deux blocs distincts) ·

- "PhantomOS · documentation deep" → "PhantomOS · deep documentation"
- "Vision" / "Pourquoi ça existe" → "Vision" / "Why it exists"
- "Les 4 artefacts de l'écosystème" → "The 4 ecosystem artifacts"
- "Comment ça raisonne" → "How it reasons"
- "Cycle opérationnel" → "Operational cycle"
- "Ce qui le rend singulier" → "What makes it singular"
- "Termes canon" → "Canon terms"
- "Comment ça reste honnête" → "How it stays honest"
- "Les 7 territoires DTC" → "The 7 DTC territories"
- "Pour démarrer" → "To get started"

---

## Constraints (non-negotiable)

- **Registre institutionnel sérieux + accessible.** Pas direct response, pas hype, pas marketing mou. Voix Vercel/GitHub shipped product. Référence canon · memory `phantomos_pitch_posture`.
- **Zéro em-dash** (caractère long tiret U+2014) dans tout l'output. Substituer par parenthèses, virgule, point, deux-points ou middle dot `·` (canon `no_em_dash`).
- **Iconographie canon v2.79.2 unique** · ✓ shipped · ◐ partial · ○ open territoire · ✗ absent · ⚠ critique. Légende au pied. Pas d'emoji couleur (🔥🟢🟡🔴 banned).
- **Zéro jargon plumbing leak.** Pas exposer `write_to_context`, `Task tool`, `subagent_safe`, field paths internes. Termes canon section 7 SONT le jargon expliqué (autorisé).
- **Séparateurs cohérents** · `━━━` (sections H2) + `───` (sous-sections internes).
- **Headers FR sobres** par défaut (1. Vision, 2. Pourquoi ça existe, etc.) ou EN equivalents si détecté.
- **Format ~150-200 lignes total** rendu opérateur.
- **No menu fermé.** L'opérateur consulte la doc, peut ensuite drill ailleurs via free-text natif. Pas de questionnaire structuré post-doc.

---

## Related canon

- `docs/system/onboarding-holistic-discipline.md` · doctrine racine onboarding (v2.80.3 · arc substance guidé · `/about` backup)
- `docs/system/output-clarity-doctrine.md` · standards Vercel-grade opérateur-facing (v2.79.2)
- `docs/system/decomposition-visibility-discipline.md` · 4 niveaux matriciels canon (v2.79+)
- `docs/system/investigation-posture.md` · 5 sections obligatoires stratégique
- `docs/system/canonical-matrix-reasoning.md` · schema + matrice canon cohérence output
- `docs/system/skill-routing-discipline.md` · routing systémique + manifest fallback
- `.claude/commands/tour.md` · onboarding holistique court (panorama 360°)
- `.claude/commands/lexicon.md` · magic keywords prompting (10-15 termes canon)
- `.claude/commands/phantom.md` · cockpit workspace + brand
- `.claude/commands/skills.md` · catalogue navigable skills par intent
