# PRD — App Flask Kroki PNG Generator

# 1) Contexte & problème
- Besoin : générer **des PNG (et SVG)** de diagrammes à partir d’une **description textuelle** (Mermaid, PlantUML, Graphviz, etc.) en **local**, via Kroki.
- Cas d’usage : coller du texte → cliquer **Générer** → récupérer l’image (et via **API**).
- Contrainte clé : **simplicité**, **maintenabilité**, **dockerisable**, **tests unitaires & intégration**.

# 2) Vision & valeur
- « **Paste → Generate → Download** » local et fiable, basé sur **Kroki**.
- S’appuie sur **Kroki local** pour supporter plusieurs langages de diagrammes.
- Fournit aussi une **API REST** simple (`/api/generate`) pour automatiser depuis scripts/CI.

# 3) Public cible
- Dev/DS/Docs engineers ; environnement interne (poste dev, CI locale, VM).
- Langues : FR/EN (UI minimaliste, labels FR par défaut).

# 4) Portée MVP
## Fonctionnel
- Page Flask : **textarea**, champs **diagram type** (Mermaid, PlantUML, Graphviz), **format** (png/svg), bouton **“Générer le PNG”**.
- Appelle Kroki (URL configurable) en **`POST` text/plain** ou via fichier temporaire si gros payload.
- Affiche l’image retournée + bouton **Télécharger**.
- Endpoint **`POST /api/generate`** (JSON ou text/plain) pour usage programmatique.

## Non-fonctionnel
- Performances : génération rapide pour diagrammes courants.
- Robustesse : **timeouts**, messages d’erreur clairs (Kroki down, format invalide, payload trop grand).
- Sécurité : pas de stockage persistant du contenu ; logs **sans** données sensibles.
- Config via .env par exemple : `KROKI_URL` (défaut `http://localhost:8000`), `REQUEST_TIMEOUT`, `MAX_BYTES`.

# 5) User stories & critères d’acceptation
- **US1** En tant qu’utilisateur, je colle un diagramme Mermaid et je récupère un **PNG**.
  - _AC_: champ texte, select “Mermaid”, bouton “Générer”, image s’affiche, **téléchargement OK**.
- **US2** Je peux choisir **PlantUML** ou **Graphviz** et **SVG** au lieu de PNG (MVP).
  - _AC_: select diagram type et format ; réponse correcte ou message d’erreur utile.
- **US2bis** (Post-MVP) Support types étendus : BlockDiag, Ditaa, Excalidraw, SeqDiag, etc.
  - _AC_: Extension progressive selon demande utilisateur, priorisée par fréquence d'usage.
- **US3** Via script, je **POST** sur `/api/generate` et je reçois l’image binaire.
  - _AC_: endpoint accepte JSON `{diagram_type, output_format, diagram_source}` **ou** `text/plain` + `Accept`.
- **US4** Si Kroki est indisponible, l’UI me l’indique sans crasher.
  - _AC_: bannière d’erreur et code HTTP 502 côté API + log erreur

# 6) KPIs
- Taux de succès des générations ≥ **99%** (hors erreurs de syntaxe).
- Temps médian de génération **< 3 s**.
- Couverture tests unitaires **≥ 80%** ; intégration (smoke) **OK**.
- Lint CI **zéro** erreurs (Black/Ruff).

# 7) Données & intégrations
- Entrée : texte du diagramme (Mermaid/PlantUML/Graphviz…).
- Sortie : image (PNG/SVG).
- Intégration : **Kroki** (gateway + mermaid companion).

# 8) Contraintes légales & sécurité
- Local-only ; pas de données personnelles stockées.
- Limiter la taille d’entrée (`MAX_BYTES`).
- Journalisation sobre (erreurs/metrics sans payload), logs sobres.

# 9) Risques & mitigations
- **Indispo Kroki** → message clair + healthcheck au démarrage.
- **Payload volumineux** → chemin “fichier temporaire” + taille max.
- **Syntaxe invalide** → surfacer l’erreur retournée par Kroki.

# 10) Roadmap (extrait)
- MVP : UI minimale + API + Dockerfile + tests.