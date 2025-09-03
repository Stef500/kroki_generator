# Bug Excalidraw - Session de Correction

## Problème Initial
Template Excalidraw retournait des données PNG corrompues au lieu de générer le diagramme.

## Diagnostic
- Erreur: "Invalid diagram syntax: �PNG..." avec données binaires
- Cause racine: Conteneur compagnon Excalidraw manquant dans Docker Compose
- Excalidraw nécessite un service compagnon comme Mermaid (yuzutech/kroki-excalidraw)

## Solution Implémentée

### 1. Configuration Docker Mise à Jour
**Fichiers modifiés:**
- `docker-compose.yml`: Ajout service excalidraw + variables env Kroki
- `deploy/docker-compose.yml`: Ajout service excalidraw + variables env Kroki

**Services ajoutés:**
```yaml
excalidraw:
  image: yuzutech/kroki-excalidraw:latest
  expose:
    - "8004"
  networks:
    - kroki-network
  restart: unless-stopped
```

**Variables Kroki:**
```yaml
environment:
  - KROKI_EXCALIDRAW_HOST=excalidraw
  - KROKI_EXCALIDRAW_PORT=8004
```

### 2. Améliorations Code
**src/kroki_client.py:**
- Amélioré détection d'erreur PNG dans `_generate_direct()` et `_generate_with_tempfile()`
- Extrait messages d'erreur lisibles depuis images PNG d'erreur
- Conservé preprocessing simple pour Excalidraw (pas de validation JSON spéciale)

### 3. Tests
- 6 nouveaux tests pour validation Excalidraw (puis supprimés - pas nécessaires)
- 34/34 tests passent
- Couverture 83% maintenue
- Code formaté avec black + ruff

## État Actuel du Problème
**Problème persistant:** Image Docker `stef500/kroki-flask-generator:latest` contient l'ancien code sans mes corrections.

**Solutions possibles:**
1. Utiliser build local dans docker-compose.yml au lieu de l'image published
2. Reconstruire et publier nouvelle image Docker
3. Utiliser mode développement local

## Architecture Excalidraw Confirmée
- ✅ Service excalidraw configuré correctement  
- ✅ Connectivité réseau Docker fonctionnelle
- ✅ Variables d'environnement Kroki correctes
- ❌ Code application pas mis à jour dans l'image Docker

## Prochaines Étapes
Pour résoudre complètement:
1. Modifier docker-compose.yml pour build local OU
2. Publier nouvelle image avec corrections OU  
3. Tester en mode dev local

## Apprentissages
- Excalidraw = conteneur compagnon obligatoire (comme Mermaid)
- Images Docker published peuvent être obsolètes vs code local
- Erreurs PNG de Kroki = conteneur manquant ou problème config