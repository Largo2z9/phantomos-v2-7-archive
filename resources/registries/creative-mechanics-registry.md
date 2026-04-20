# Creative Mechanics Registry

> **TYPE:** Taxonomie — registre vivant
> **CONSOMMÉ PAR:** hooks-generator, script-writer, brief-generator, creative-strategist, pattern-extractor
> **SOURCE:** Retro-engineering 522 créas statiques (10 batches, 9 brands, 6 niches)
> **DÉPEND DE:** `templates/creative-formula.md` (§5.1)
> **FORMAT:** 1 fiche taggée par mécanique. Champs parsables par agent.

---

## Format fiche

```
### [ID] — [Nom]
- **Définition:** [prose, 1-2 phrases]
- **Curseur:** [min, max]
- **Mode:** CONCEPT | TEMPLATE | ASSET
- **Stop scroller:** hook_dominant | visual_dominant | co_dominant
- **Angles:** [array — ref angle-registry.md]
- **Proofs:** [array — ref proof-registry.md]
- **Awareness:** [array — awareness levels compatibles]
- **Conditions:** [array — tags de contexte requis]
- **Anti-conditions:** [array — red flags, ne pas utiliser si]
- **Variantes:** [array — sous-types si applicable]
- **Template signals:** [array — éléments visuels/textuels non-persuasifs. TEMPLATE/ASSET only, optionnel]
- **Piège:** [prose, 1 phrase — erreur courante]
- **Batches:** [array]
```

---

## Claim Niches (curseur 5-10)

### versus — Comparaison

- **Définition:** Confrontation directe produit vs concurrent, workaround, ou statu quo. La comparaison EST le concept.
- **Curseur:** [6, 10]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [efficiency, price-value, innovation, parasitic-positioning]
- **Proofs:** [cost-calculator, clinical-trial, social-proof-number]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [avantage_mesurable, referent_connu, audience_compare_deja]
- **Anti-conditions:** [zero_avantage_objectif, risque_legal_comparaison, audience_unaware]
- **Variantes:** [vs_concurrent_nomme, vs_categorie_workaround, vs_statu_quo, vs_ancienne_version]
- **Piège:** Sans avantage objectif démontrable, le versus se retourne contre la brand.
- **Batches:** [B01, B05, B08]

---

### diagnostic — Quiz / Symptom Check

- **Définition:** Créa qui simule ou invite à un diagnostic personnalisé. CTA = "faire le test". L'engagement via la personnalisation.
- **Curseur:** [5, 8]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [simplicity, expertise, transformation]
- **Proofs:** [social-proof-number, badge-tech]
- **Awareness:** [problem_aware, solution_aware]
- **Conditions:** [personnalisation_valorisee, funnel_quiz_amont, multi_sku]
- **Anti-conditions:** [mono_sku_sans_personnalisation, audience_most_aware]
- **Variantes:** [quiz_interactif, symptom_checklist, identitaire_quel_X_es_tu]
- **Piège:** Sur audience most_aware, le diagnostic ralentit la conversion au lieu de l'accélérer.
- **Batches:** [B02, B05]

---

### ugc — User Generated Content

- **Définition:** Contenu généré (ou simulé) par l'utilisateur comme device principal. L'authenticité perçue EST le mécanisme de persuasion.
- **Curseur:** [4, 9]
- **Mode:** CONCEPT
- **Stop scroller:** co_dominant
- **Angles:** [transformation, community, security, emotional-identity]
- **Proofs:** [customer-review, social-proof-number, sponsoring-disclosure]
- **Awareness:** [problem_aware, solution_aware, product_aware]
- **Conditions:** [trust_barrier_medium_high, audience_mefie_brand_content, resultat_visible]
- **Anti-conditions:** [zero_ugc_disponible, resultat_non_demonstrable]
- **Variantes:** [selfie_mirror, story_repost, conversationnel_qa, ugc_founder, founder_client_chat, testimonial_quote_brand, avis_citation]
- **Piège:** Un UGC trop "propre" (éclairage studio, script visible) détruit l'authenticité perçue.
- **Batches:** [B03, B05, B08]

→ Sous-types hiérarchisés par authenticité : voir `creative-formula.md` §5.5

---

### celebrity — Celebrity Endorsement

- **Définition:** Personnalité connue recommande/utilise le produit. Capital de notoriété transféré au produit.
- **Curseur:** [5, 9]
- **Mode:** CONCEPT
- **Stop scroller:** visual_dominant
- **Angles:** [expertise, community, emotional-identity, transformation]
- **Proofs:** [celebrity-endorsement, press-logos, social-proof-number]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [association_authentique, audience_admire_personne, celebrity_effect_superieur_product_first]
- **Anti-conditions:** [association_artificielle, budget_droits_insuffisant, audience_sceptique_endorsement]
- **Variantes:** [endorsement_direct, co_creation, investment_ownership, mention_passive]
- **Piège:** Celebrity fatigue — une célébrité qui endorse 15 marques perd en crédibilité. Exclusivité catégorielle renforce.
- **Batches:** [B04, B05]

---

### launch-narrative — Annonce / Upgrade

- **Définition:** Annonce nouveau produit ou upgrade. La nouveauté + la narration "pourquoi maintenant" = le device.
- **Curseur:** [5, 8]
- **Mode:** CONCEPT
- **Stop scroller:** co_dominant
- **Angles:** [innovation, efficiency, transformation]
- **Proofs:** [badge-tech, press-logos, clinical-trial, social-proof-number]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [lancement_reel, upgrade_substantiel, audience_existante_a_reactiver]
- **Anti-conditions:** [fausse_nouveaute, audience_unaware_ne_connait_pas_v1]
- **Variantes:** [launch_produit, upgrade_v1_v2, extension_gamme, restock]
- **Piège:** Sans vraie nouveauté, le "NEW" badge est du bruit — l'audience détecte.
- **Batches:** [B01, B02, B04, B05, B08]

---

### offer-breakdown — Déballage de l'Offre

- **Définition:** Décomposition structurée de l'offre — chaque élément nommé, valorisé. Perception de valeur par accumulation.
- **Curseur:** [6, 9]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [price-value, efficiency, security]
- **Proofs:** [cost-calculator, risk-reversal, social-proof-number, best-seller-badge]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [offre_multi_produit, pricing_competitif, audience_compare_deals]
- **Anti-conditions:** [mono_produit_simple, audience_unaware, audience_problem_aware]
- **Variantes:** [welcome_kit, bundle_decompose, free_gift_highlight, subscription_breakdown]
- **Piège:** Sur audience pas encore convaincue du problème, l'offre n'a aucun sens.
- **Batches:** [B05, B08]

---

### before-after — Contraste Avant/Après

- **Définition:** Juxtaposition état "avant" (douleur) et état "après" (résultat). Le contraste visuel ou textuel EST la persuasion.
- **Curseur:** [5, 9]
- **Mode:** CONCEPT
- **Stop scroller:** co_dominant
- **Angles:** [transformation, efficiency, emotional-identity]
- **Proofs:** [customer-review, social-proof-number, clinical-trial, claim-science]
- **Awareness:** [problem_aware, solution_aware, product_aware]
- **Conditions:** [resultat_visible, ecart_avant_apres_dramatique, preuve_reelle]
- **Anti-conditions:** [resultat_invisible_abstrait, risque_reglementaire_ba, plateforme_interdit_ba]
- **Variantes:** [ba_visuel_2_photos, ba_emotionnel_2_etats, ba_3_plus_etapes, ba_textuel]
- **Piège:** Meta health ads restreint les BA visuels — vérifier les policies avant.
- **Batches:** [B02, B03, B09]

---

### testimonial-quote — Citation Client Brand

- **Définition:** Verbatim client dans un design brand. Hybride UGC/brand — voix authentique, packaging contrôlé.
- **Curseur:** [6, 8]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [transformation, security, community]
- **Proofs:** [customer-review, social-proof-number, press-logos]
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [verbatims_forts_disponibles, trust_barrier_medium]
- **Anti-conditions:** [zero_temoignages_reels, audience_unaware]
- **Variantes:** [quote_seule, quote_plus_photo, quote_plus_trustpilot, quote_plus_badge_verifie]
- **Piège:** Un verbatim trop parfait semble fake. Garder les imperfections de langage.
- **Batches:** [B05, B08]

---

### cost-calculator — Démonstration Mathématique

- **Définition:** La créa fait le calcul pour le prospect. Preuve par les chiffres que le deal est objectivement supérieur.
- **Curseur:** [7, 10]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [price-value, efficiency, parasitic-positioning]
- **Proofs:** [cost-calculator, risk-reversal, social-proof-number]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [cout_objectivement_inferieur, calcul_simple_verifiable, audience_rationnelle]
- **Anti-conditions:** [calcul_trompeur, audience_desire_driven, positionnement_premium]
- **Variantes:** [savings_annuels, cout_par_jour, comparaison_panier, breakdown_vrai_cout]
- **Piège:** Le calcul doit résister à 5 secondes de réflexion critique — sinon l'effet se retourne.
- **Batches:** [B05]

---

### analogie — Bridge Externe

- **Définition:** Élément externe surprenant bridgé vers le produit. Pattern interrupt par l'incongru, puis pont logique.
- **Curseur:** [6, 9]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [counter-intuitive, innovation, efficiency]
- **Proofs:** [claim-science, social-proof-number]
- **Awareness:** [problem_aware, solution_aware]
- **Conditions:** [analogie_surprenante, bridge_logique, audience_saturee_hooks_directs]
- **Anti-conditions:** [bridge_force_confus, analogie_noie_produit]
- **Variantes:** [analogie_objet, analogie_stat, analogie_culturelle]
- **Piège:** Si le bridge prend plus de 3 secondes à comprendre, l'audience a déjà scrollé.
- **Batches:** [B01]

---

### trending-fake-natif — Contenu Pseudo-Natif

- **Définition:** Créa qui mime un format organique (Notes, story, Google, tweet) pour bypass les ad filters mentaux.
- **Curseur:** [4, 8]
- **Mode:** CONCEPT
- **Stop scroller:** visual_dominant
- **Angles:** [counter-intuitive, transformation, community]
- **Proofs:** [social-proof-number, press-logos, customer-review]
- **Awareness:** [problem_aware, solution_aware, product_aware]
- **Conditions:** [audience_ad_fatigued, message_integre_naturellement, format_pas_surexploite]
- **Anti-conditions:** [format_grille, message_force_dans_format, risque_confusion_brand]
- **Variantes:** [format_app, format_social, format_trend_meme, format_editorial, format_search, format_whiteboard]
- **Piège:** Les formats fake natif se grillent vite — durée de vie courte. Renouveler régulièrement.
- **Batches:** [B01, B02, B05, B06, B08]

→ Sous-types détaillés : voir `creative-formula.md` §5.6

---

### direct-benefit — Bénéfice Brut

- **Définition:** Le bénéfice produit EST le concept entier. 2-5 mots, zéro device. Minimalisme textuel comme arme.
- **Curseur:** [8, 10]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [efficiency, barrier-removal, transformation]
- **Proofs:** [press-logos, clinical-trial, regulatory-disclaimer]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [benefice_universellement_compris, marche_mature, zero_education_requise]
- **Anti-conditions:** [benefice_necessite_explication, audience_unaware, benefice_nuance]
- **Variantes:** [benefice_seul, benefice_plus_visual, benefice_plus_prix]
- **Piège:** Fonctionne uniquement si le bénéfice est instantanément compris — sinon ça tombe à plat.
- **Batches:** [B09]

---

### press-quote — Citation Presse

- **Définition:** Citation presse verbatim = concept créatif entier. La crédibilité du média porte la persuasion.
- **Curseur:** [7, 10]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [expertise, security, parasitic-positioning]
- **Proofs:** [press-quote, press-logos, clinical-trial]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [citation_reelle_media_reconnu, citation_forte_porte_seule, trust_barrier_haute]
- **Anti-conditions:** [citation_tronquee, media_non_reconnu, citation_fade]
- **Variantes:** [quote_seule_logo, quote_packshot, quote_lien_article, multi_quotes]
- **Piège:** Citation cherry-picked qui ne reflète pas l'article = bombe à retardement si le prospect vérifie.
- **Batches:** [B09]

---

### format-menu — Menu de Formats Produit

- **Définition:** Présentation des options format/variant comme un menu. Auto-segmentation de l'audience par le choix.
- **Curseur:** [6, 8]
- **Mode:** CONCEPT
- **Stop scroller:** co_dominant
- **Angles:** [simplicity, price-value, innovation]
- **Proofs:** [best-seller-badge, social-proof-number, risk-reversal]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [multi_sku, naming_distinctif_par_format, audience_hesite_sur_format]
- **Anti-conditions:** [mono_sku, formats_non_differencies]
- **Variantes:** [menu_horizontal, menu_lifestyle, menu_comparatif]
- **Piège:** Si les formats ne sont pas suffisamment différents, le menu crée de la confusion, pas du choix.
- **Batches:** [B09]

---

### price-primary — Prix comme Concept

- **Définition:** Le prix EST la créa entière. Le chiffre seul porte le message. Arme ultime pour audiences price-driven.
- **Curseur:** [8, 10]
- **Mode:** CONCEPT
- **Stop scroller:** hook_dominant
- **Angles:** [price-value, urgency, parasitic-positioning]
- **Proofs:** [cost-calculator, risk-reversal, parasitic-positioning]
- **Awareness:** [most_aware]
- **Conditions:** [prix_objectivement_disruptif, audience_price_sensitive, chiffre_genere_surprise]
- **Anti-conditions:** [prix_pas_competitif, positionnement_premium, audience_unaware]
- **Variantes:** [prix_seul, prix_barre, prix_per_month, prix_starting_at]
- **Piège:** Sans contexte catégorie, le prix seul ne dit rien. L'audience doit connaître le prix de référence.
- **Batches:** [B09]

---

### diagnostic-service — Diagnostic comme Produit

- **Définition:** Le produit vendu = un test/screening, pas un traitement. Vend l'acte de savoir, pas l'acte de soigner.
- **Curseur:** [7, 9]
- **Mode:** CONCEPT
- **Stop scroller:** co_dominant
- **Angles:** [security, expertise, simplicity, barrier-removal]
- **Proofs:** [claim-science, risk-reversal, regulatory-disclaimer]
- **Awareness:** [problem_aware, solution_aware]
- **Conditions:** [offre_est_test_screening, peur_ne_pas_savoir_superieure_peur_savoir]
- **Anti-conditions:** [produit_est_traitement, audience_veut_solution_pas_question]
- **Variantes:** [test_medical, screening_digital, diagnostic_en_personne]
- **Piège:** Si l'audience veut agir et pas comprendre, le diagnostic freine la conversion.
- **Batches:** [B09]

---

### founder-chat — Conversation Fondateur-Client

- **Définition:** Créa simulant une conversation (DM, iMessage) entre fondateur et client. Intimité du format + transparence = persuasion.
- **Curseur:** [6, 8]
- **Mode:** CONCEPT
- **Stop scroller:** visual_dominant
- **Angles:** [security, expertise, community, emotional-identity]
- **Proofs:** [customer-review, sponsoring-disclosure]
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [fondateur_personal_brand, audience_valorise_proximite, marche_dtc]
- **Anti-conditions:** [fondateur_invisible, grand_groupe_corporate, intimite_forcee]
- **Variantes:** [dm_instagram, imessage, whatsapp, email_screenshot]
- **Piège:** L'intimité simulée doit être crédible — si le fondateur n'a aucune présence publique, ça sonne faux.
- **Batches:** [B08]

---

### recipe-instructions — Mode d'Emploi comme Ad

- **Définition:** Mode d'emploi, recette, ou rituel d'utilisation présenté comme créa. Montre la simplicité/le plaisir d'usage.
- **Curseur:** [5, 7]
- **Mode:** CONCEPT
- **Stop scroller:** visual_dominant
- **Angles:** [simplicity, efficiency, expertise]
- **Proofs:** [best-seller-badge, customer-review, social-proof-number]
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [rituel_usage_existe, usage_correct_impacte_resultat, audience_hesite_praticite]
- **Anti-conditions:** [usage_trivial, audience_most_aware_connait_deja]
- **Variantes:** [step_by_step, recette_food, routine_matin_soir, video_how_to]
- **Piège:** Si l'usage est trop complexe (>5 étapes), la créa crée de la friction au lieu de l'éliminer.
- **Batches:** [B08]

---

### bundle-duo — Regroupement Structuré

- **Définition:** 2+ produits regroupés avec structure narrative (jour/nuit, him/her). Complémentarité racontée comme système.
- **Curseur:** [5, 8]
- **Mode:** CONCEPT
- **Stop scroller:** co_dominant
- **Angles:** [efficiency, simplicity, price-value]
- **Proofs:** [cost-calculator, best-seller-badge, customer-review]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [produits_complementaires, aov_push_strategique, histoire_duo_evidente]
- **Anti-conditions:** [produits_pas_complementaires, bundle_pretexte_discount]
- **Variantes:** [duo_jour_nuit, duo_him_her, duo_starter_maintenance, trio_routine]
- **Piège:** Un bundle sans logique narrative = discount déguisé. L'audience sent la manœuvre.
- **Batches:** [B01, B08]

---

## Visual Niches (curseur 0-4)

### category-showcase — Vitrine Catégorie

- **Définition:** Template : photo modèle + titre catégorie + badge attribut. Navigation produit, pas persuasion.
- **Curseur:** [2, 3]
- **Mode:** TEMPLATE
- **Stop scroller:** visual_dominant
- **Angles:** []
- **Proofs:** []
- **Template signals:** [badge_attribut, prix, prix_club]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [fashion_retail, objectif_traffic_collection, audience_browse]
- **Anti-conditions:** [objectif_conversion_directe, audience_besoin_persuasion]
- **Variantes:** [mono_produit, multi_produit_grille, lookbook_lifestyle]
- **Piège:** Sans aucun élément textuel distinctif, les category-showcases se ressemblent toutes.
- **Batches:** [B06]

---

### collection — Univers Thématique

- **Définition:** Univers créatif (nom + palette + motifs) justifiant N produits. Cohérence esthétique = désir par immersion.
- **Curseur:** [1, 3]
- **Mode:** TEMPLATE
- **Stop scroller:** visual_dominant
- **Angles:** [emotional-identity, community]
- **Proofs:** []
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [marque_lifestyle_drops_reguliers, univers_visuel_fort, audience_achete_esthetique]
- **Anti-conditions:** [marque_sans_identite_visuelle, produit_utilitaire, audience_rationnelle]
- **Variantes:** [collection_saisonniere, collab_co_brand, thematique_motif]
- **Piège:** Sans identité visuelle forte, la collection ressemble à un catalogue — pas à un univers.
- **Batches:** [B06]

---

### season-campaign — Campagne Saisonnière

- **Définition:** Photo contexte saisonnier + slogan saison + CTA. Le moment calendaire comme déclencheur d'achat.
- **Curseur:** [2, 4]
- **Mode:** TEMPLATE
- **Stop scroller:** visual_dominant
- **Angles:** [urgency, emotional-identity]
- **Proofs:** []
- **Template signals:** [prix, offre_saisonniere]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [produit_saisonnier, moment_calendaire_fort, image_contexte_declenche_besoin]
- **Anti-conditions:** [produit_evergreen_sans_saison, saison_pretexte_faible]
- **Variantes:** [saison_pure, moment_rentree_holidays, meteo]
- **Piège:** La saisonnalité doit être réelle — forcer un lien saison/produit = pub générique.
- **Batches:** [B06]

---

### loyalty-campaign — Campagne Fidélité

- **Définition:** Photo + nom campagne fidélité + prix club. Exclusivité du prix réservé aux membres.
- **Curseur:** [2, 3]
- **Mode:** TEMPLATE
- **Stop scroller:** visual_dominant
- **Angles:** [price-value, scarcity, community]
- **Proofs:** []
- **Template signals:** [prix_club, badge_fidelite]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [programme_fidelite_actif, ecart_prix_significatif, reactivation_membres]
- **Anti-conditions:** [pas_programme_fidelite, ecart_prix_negligeable]
- **Variantes:** [prix_club_vs_public, early_access, vente_privee]
- **Piège:** Si l'écart de prix est insignifiant, la mécanique "membre exclusif" sonne creux.
- **Batches:** [B06]

---

### guide-listicle — Guide / Checklist

- **Définition:** Titre éditorial + checklist/listicle. Format éditorial qui attire par l'utilité, pas la vente directe.
- **Curseur:** [3, 5]
- **Mode:** TEMPLATE
- **Stop scroller:** co_dominant
- **Angles:** [expertise, simplicity]
- **Proofs:** [best-seller-badge]
- **Template signals:** [badge_attribut]
- **Awareness:** [problem_aware, solution_aware]
- **Conditions:** [contenu_educatif_mene_au_produit, funnel_top_of_funnel]
- **Anti-conditions:** [guide_pretexte_pub_transparent, audience_most_aware]
- **Variantes:** [x_essentiels_saison, guide_activite, checklist_occasion, fake_search]
- **Piège:** Si le guide est un prétexte publicitaire transparent, l'audience le détecte et la confiance chute.
- **Batches:** [B06]

---

### packshot-solo — Packshot Studio

- **Définition:** 1 modèle, fond studio, produit porté, logo seul. Zéro texte. L'image parle seule.
- **Curseur:** [0, 1]
- **Mode:** ASSET
- **Stop scroller:** visual_dominant
- **Angles:** []
- **Proofs:** []
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [brand_forte_equity_visuelle, dpa_daba, retargeting]
- **Anti-conditions:** [brand_inconnue, objectif_acquisition_cold]
- **Variantes:** [portrait, full_body, flat_lay]
- **Piège:** Sur brand inconnue, le visual seul ne communique rien — il faut au minimum un hook textuel.
- **Batches:** [B07]

---

### packshot-contextuel — Packshot en Contexte

- **Définition:** 1 modèle en contexte d'usage (gym, outdoor, bureau), produit porté, logo seul. Le contexte remplace le copy.
- **Curseur:** [0, 1]
- **Mode:** ASSET
- **Stop scroller:** visual_dominant
- **Angles:** []
- **Proofs:** []
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [contexte_usage_aspirationnel, audience_sidentifie_au_decor, dpa_enrichissement_lifestyle]
- **Anti-conditions:** [contexte_generique, brand_sans_identite_lifestyle]
- **Variantes:** [gym_sport, outdoor_nature, urbain, domestique, travel]
- **Piège:** Un contexte trop générique (fond blanc + gym random) n'ajoute rien par rapport au packshot studio.
- **Batches:** [B07]

---

### squad-group — Groupe / Communauté

- **Définition:** 3-5 modèles ensemble, diversité visible. La communauté comme message : "tu as ta place ici."
- **Curseur:** [0, 2]
- **Mode:** ASSET
- **Stop scroller:** visual_dominant
- **Angles:** [community, emotional-identity]
- **Proofs:** []
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [positionnement_inclusif, image_groupe_renforce_brand, campagne_branding]
- **Anti-conditions:** [segment_narrow, objectif_conversion_directe]
- **Variantes:** [studio_fond_uni, lifestyle_exterieur, action_sport]
- **Piège:** Le groupe dilue le ciblage — si la brand vise un segment narrow, la diversité brouille le message.
- **Batches:** [B07]

---

### ugc-selfie — Selfie Authentique

- **Définition:** Selfie miroir, format smartphone, zéro texte/branding. Le format brut = le message. L'anti-pub comme pub.
- **Curseur:** [0, 1]
- **Mode:** ASSET
- **Stop scroller:** visual_dominant
- **Angles:** [community, transformation]
- **Proofs:** []
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [vraie_communaute_ugc, produit_visible_dans_selfie, authenticite_pure_est_strategie]
- **Anti-conditions:** [produit_pas_visible_selfie, selfie_trop_parfait]
- **Variantes:** [miroir_gym, miroir_chambre, selfie_exterieur, selfie_avant_apres]
- **Piège:** Un selfie trop parfait (éclairage pro, cadrage composé) = pas authentique. Le "défaut" est le signal.
- **Batches:** [B07]

---

## Méta-règles

- **1 mécanique par créa.** Si 2 devices coexistent → identifier primaire (structure layout) et secondaire (enrichit).
- **Mécanique ≠ Angle.** Mécanique = COMMENT (structure). Angle = POURQUOI (psychologie). Dimensions orthogonales.
- **Mécanique ≠ Hook.** Mécanique = device structurel global. Hook = élément textuel stop-scroll. Un `before-after` peut utiliser un hook `question` ou `confession`.
- **Curseur ≠ catégorie figée.** Curseur évalué par créa, pas par mécanique. Un `UGC` peut être curseur 4 ou curseur 9.
- **CONCEPT > TEMPLATE > ASSET.** Hiérarchie de complexité persuasive, pas de qualité.
- **Visual niches ≠ visuels uniquement.** Texte possible (badge, prix, catégorie) mais fonctionnel, pas persuasif.
- **H4 (à valider).** Chaque brand semble avoir 1-2 mécaniques core dominant >40% output. Observé 9/9 brands, échantillon limité.

---

## Extension

1. Fiche au format taggé ci-dessus
2. Classifier : claim niche [5, 10] ou visual niche [0, 4]
3. Mode : CONCEPT | TEMPLATE | ASSET
4. Test : device structurel unique ? (pas de chevauchement)
5. Valider ≥ 2 batches ou ≥ 5 créas
6. Ajouter dans `creative-formula.md` §5.1

---

*Dernière mise à jour : 2026-03-17 (Session 11 — 28 fiches taggées, 19 claim + 9 visual)*


---

## Proposed — F5 Sandbox Batch 2026-04-10

> Source : `research/f5-sandbox-promotion-batch.md` | Injected : 2026-04-13T20:29:22Z | Status : **_proposed** (review required)

---

### annonce-upgrade — [PROPOSED] Launch d'une V2 / nouvelle formule / évolution produit posit

- **Définition:** Launch d'une V2 / nouvelle formule / évolution produit positionnée comme amélioration explicite du précédent
- **Catégorie:** announcement
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [innovation, expertise]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [im8, im8-extended, unbottled]
- **Sample count:** 9
- **Confidence:** 0.85
- **Source:** sandbox/batch-04-im8, batch-05-im8-extended, batch-02-unbottled
- **Notes:** Pattern fort supplément / beauté quand le produit a une V1 identifiable. Souvent couplé avec testimonial quote (anciens users valident upgrade).
- **DTC era:** 2024-2026
- **Proposal ID:** prop_mech_01
- **_proposed:** true


---

### cross-sell-companion — [PROPOSED] Mise en avant d'un produit B comme compagnon nécessaire du p

- **Définition:** Mise en avant d'un produit B comme compagnon nécessaire du produit A (stack logique, pas un simple upsell)
- **Catégorie:** bundle
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [efficacité, expertise]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [hims-hers]
- **Sample count:** 8
- **Confidence:** 0.8
- **Source:** sandbox/batch-09-10-hims-hers
- **Notes:** Hims/Hers: GLP-1 + hair loss prevention, GLP-1 + nausée management. Le second produit répond à un side-effect du premier = bundle logique non-forcé.
- **DTC era:** 2024-2026
- **Proposal ID:** prop_mech_02
- **_proposed:** true


---

### testimonial-quote — [PROPOSED] Citation texte d'un utilisateur (vs vidéo UGC), format copy-

- **Définition:** Citation texte d'un utilisateur (vs vidéo UGC), format copy-heavy
- **Catégorie:** social-proof
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [transformation, expertise]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [im8, unbottled, spotminders, pilot-skincare-sub, hims-hers]
- **Sample count:** 5
- **Confidence:** 0.9
- **Source:** sandbox cross-batch
- **Notes:** À distinguer de UGC-testimonial (format vidéo face-cam). Testimonial quote = copy statique ou motion text.

- **Proposal ID:** prop_mech_03
- **_proposed:** true


---

### benefit-direct — [PROPOSED] Mise en avant d'un bénéfice produit sans passer par un pain

- **Définition:** Mise en avant d'un bénéfice produit sans passer par un pain (positive framing pur)
- **Catégorie:** product-focus
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [transformation, efficacité]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [spotminders, im8]
- **Sample count:** 3
- **Confidence:** 0.75
- **Source:** sandbox cross-batch
- **Notes:** Complémentaire de 'benefit vs pain' : celui-ci assume que l'audience est desire-driven, pas pain-driven.

- **Proposal ID:** prop_mech_04
- **_proposed:** true


---

### promo-shipping — [PROPOSED] Free shipping / shipping upgrade utilisé comme hook principa

- **Définition:** Free shipping / shipping upgrade utilisé comme hook principal d'une creative
- **Catégorie:** offer-framing
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [prix-valeur]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [spotminders, pilot-skincare-sub]
- **Sample count:** 3
- **Confidence:** 0.7
- **Source:** sandbox cross-batch
- **Notes:** Souvent combiné à un seuil d'order minimum. Plus efficace sur produits à CAC tendu / AOV mid-range.

- **Proposal ID:** prop_mech_05
- **_proposed:** true


---

### promo-occasion — [PROPOSED] Promo saisonnière / calendrier (Black Friday, Summer Sale, a

- **Définition:** Promo saisonnière / calendrier (Black Friday, Summer Sale, anniversaire brand, fête spécifique)
- **Catégorie:** offer-framing
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [prix-valeur]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [unbottled, tao]
- **Sample count:** 3
- **Confidence:** 0.8
- **Source:** sandbox cross-batch
- **Notes:** Déclencheur = date externe, pas état produit. À différencier de promo-launch et promo-shipping.

- **Proposal ID:** prop_mech_06
- **_proposed:** true


---

### before-after — [PROPOSED] Split-screen ou séquence montrant état initial (problème) pu

- **Définition:** Split-screen ou séquence montrant état initial (problème) puis état final (résolu)
- **Catégorie:** transformation-proof
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [transformation]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [unbottled]
- **Sample count:** 2
- **Confidence:** 0.9
- **Source:** sandbox/batch-02-unbottled
- **Notes:** Classique beauté/cosmétique. Efficace sur pain-driven avec preuve visuelle. Risque compliance sur supplément/health.

- **Proposal ID:** prop_mech_07
- **_proposed:** true


---

### ugc-testimonial — [PROPOSED] User-generated content format : face-cam, setting informel,

- **Définition:** User-generated content format : face-cam, setting informel, authentic tone
- **Catégorie:** social-proof
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [transformation, contre-intuitif]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [naali, hims-hers]
- **Sample count:** 2
- **Confidence:** 0.85
- **Source:** sandbox cross-batch
- **Notes:** Distinct de testimonial-quote (text-only) et de celebrity-endorsement (scripted). UGC = feel unscripted, même si dirigé.

- **Proposal ID:** prop_mech_08
- **_proposed:** true


---

### focus-produit — [PROPOSED] Creative centrée sur le produit lui-même (hero shot, packagi

- **Définition:** Creative centrée sur le produit lui-même (hero shot, packaging, features visuelles), sans narrative
- **Catégorie:** product-focus
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [innovation, expertise]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [spotminders, im8]
- **Sample count:** 2
- **Confidence:** 0.75
- **Source:** sandbox cross-batch
- **Notes:** Mécanique basique mais omise du registry actuel. Souvent utilisée en scaling sur produits visually distinctive.

- **Proposal ID:** prop_mech_09
- **_proposed:** true


---

### annonce-launch — [PROPOSED] Moment-driven creative : 'now available', 'launching today',

- **Définition:** Moment-driven creative : 'now available', 'launching today', 'back in stock', amplifiant un événement produit
- **Catégorie:** announcement
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [innovation, urgence]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [im8, spotminders]
- **Sample count:** 2
- **Confidence:** 0.8
- **Source:** sandbox cross-batch
- **Notes:** À distinguer de annonce-upgrade (V2) : annonce-launch = premier drop ou re-stock, pas évolution.

- **Proposal ID:** prop_mech_10
- **_proposed:** true


---

### diagnostic-service — [PROPOSED] CTA creative axée sur un diagnostic / consultation gratuite

- **Définition:** CTA creative axée sur un diagnostic / consultation gratuite comme first step, pas sur le produit directement
- **Catégorie:** service-led
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [expertise, sécurité]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [hims-hers]
- **Sample count:** 2
- **Confidence:** 0.85
- **Source:** sandbox/batch-09-10-hims-hers
- **Notes:** Pattern telehealth spécifique. Diagnostic = lead magnet, produit = downstream. Creative cache le produit derrière le funnel service.

- **Proposal ID:** prop_mech_11
- **_proposed:** true


---

### diagnostic — [PROPOSED] Creative qui éduque sur le problème sans révéler immédiateme

- **Définition:** Creative qui éduque sur le problème sans révéler immédiatement la solution — fait émerger la conscience du pain
- **Catégorie:** education
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [expertise, contre-intuitif]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [im8-extended]
- **Sample count:** 21
- **Confidence:** 0.9
- **Source:** sandbox/batch-05-im8-extended
- **Notes:** LA mécanique la plus fréquente du batch im8-extended. À vérifier si déjà dans le registry sous un autre nom. Si absent, c'est un trou majeur.

- **Proposal ID:** prop_mech_12
- **_proposed:** true


---

### versus-old-new — [PROPOSED] Side-by-side de l'ancienne manière vs la nouvelle (avec le p

- **Définition:** Side-by-side de l'ancienne manière vs la nouvelle (avec le produit)
- **Catégorie:** comparison
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [innovation, contre-intuitif]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [spotminders]
- **Sample count:** 2
- **Confidence:** 0.75
- **Source:** sandbox/batch-01-spotminders
- **Notes:** Différent de before-after : versus = comparaison de méthode, before-after = comparaison d'état.

- **Proposal ID:** prop_mech_13
- **_proposed:** true


---

### celebrity-endorsement — [PROPOSED] Figure publique reconnue valide ou utilise le produit de man

- **Définition:** Figure publique reconnue valide ou utilise le produit de manière scripted
- **Catégorie:** social-proof
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [expertise, transformation]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [im8]
- **Sample count:** 6
- **Confidence:** 0.9
- **Source:** sandbox/batch-04-im8, batch-05-im8-extended
- **Notes:** À distinguer de UGC / testimonial-quote. Celebrity = scripted, brand-funded, production value visible. Compliance à surveiller (disclosure).

- **Proposal ID:** prop_mech_14
- **_proposed:** true


---

### safety-risk-mitigation — [PROPOSED] Messaging explicite sur la sécurité d'usage, certifications,

- **Définition:** Messaging explicite sur la sécurité d'usage, certifications, tests cliniques
- **Catégorie:** reassurance
- **Curseur:** [TBD]
- **Mode:** TBD
- **Stop scroller:** TBD
- **Angles:** [sécurité, expertise]
- **Proofs:** [TBD]
- **Awareness:** [TBD]
- **Conditions:** [TBD]
- **Anti-conditions:** [TBD]
- **Variantes:** [TBD]
- **Piège:** TBD
- **Batches:** [spotminders]
- **Sample count:** 3
- **Confidence:** 0.7
- **Source:** sandbox/batch-01-spotminders
- **Notes:** Particulièrement pertinent sur wearable, supplément, beauté active ingredient. Tag sur angle sécurité observé 3x batch.

- **Proposal ID:** prop_mech_15
- **_proposed:** true
