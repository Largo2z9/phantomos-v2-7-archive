# Doctrine Candidates · Backlog

> Patterns identified as potential canon doctrines but not yet codified. Each entry includes identification date, revisit date, and acceptance criteria chiffrés. Aucun candidat n'est codifié en doctrine canon avant que ses critères d'acceptation soient atteints (cohérent memory canon `no_overengineer` + meta-pattern `doctrine_ripening_period` lui-même).

## Format canonique

```
### {pattern_name}

- **Identified** · YYYY-MM-DD
- **Revisit** · YYYY-MM-DD (T+N weeks/months)
- **Criteria** · acceptance criteria chiffrés (ex "5+ informal applications observed in sprint history")
- **Context** · brief 1-2 lignes · pourquoi identifié comme candidat
- **Applications tracker** · liste des observations informelles avec date
- **Status** · pending revisit | promoted to canon | rejected with rationale
```

---

## Active candidates

### doctrine_ripening_period

- **Identified** · 2026-05-19 (sprint v2.83.0)
- **Revisit** · 2026-06-09 (T+3 weeks)
- **Criteria** · 5+ informal applications observed where waiting 2-3 weeks before codification prevented over-engineering · OR 2+ doctrines codified prematurely that later required refactor (documenting the prevention value)
- **Context** · audit externe Claude Web v2 sur sprint v2.82.0/v2.83.0 a flag "réflexe de codification immédiate · chaque insight devient doctrine, chaque doctrine devient discipline, chaque discipline devient memory canon avec D# capture". Pattern de ralentissement proposé · 2-3 semaines de pratique informelle avant codification canon. Si à T+3 weeks le pattern est réutilisé 5+ fois sans y penser, alors mérite codification. Sinon doctrine prématurée qui pèse sur le contexte sans valeur prouvée. Ironie · codifier ce pattern immédiatement violerait le pattern lui-même · d'où entrée backlog avec revisit + criteria.
- **Applications tracker** ·
  - 2026-05-19 · pattern identifié (initial observation · sprint v2.83.0 acknowledged)
  - {prochaines applications à logger pendant la période de maturation}
- **Status** · pending revisit

---

## Rejected candidates

(none yet)

---

## Promoted to canon

(none yet)

---

## Discipline du fichier

- Mise à jour à chaque sprint où un pattern méta est observé · pas de codification réactive
- Revisit dates respectées strict · si revisit dépasse de >1 semaine, flag · soit promouvoir, soit rejeter, soit extend revisit avec justification
- Applications tracker maintenu honnête · chaque observation date + sprint/contexte · pas d'inflation artificielle pour atteindre criteria
- Cohérent `no_overengineer` memory canon · pas de doctrine canon sans valeur prouvée par usage réel
