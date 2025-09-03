# Kroki Flask Generator - Déploiement Production

Instructions pour déployer rapidement Kroki Flask Generator en production.

## Installation rapide (Recommandée)

### Installation en une ligne

```bash
curl -sSL https://raw.githubusercontent.com/stef500/kroki-flask-generator/main/deploy/install.sh | bash
```

Cette commande va :
- ✅ Vérifier que Docker est installé
- ✅ Télécharger la configuration Docker Compose
- ✅ Récupérer les dernières images Docker
- ✅ Démarrer tous les services
- ✅ Vérifier que l'application est accessible

### Avec port personnalisé

```bash
APP_PORT=3000 curl -sSL https://raw.githubusercontent.com/stef500/kroki-flask-generator/main/deploy/install.sh | bash
```

## Installation manuelle

### Étape 1 : Récupérer la configuration

```bash
curl -L https://raw.githubusercontent.com/stef500/kroki-flask-generator/main/deploy/docker-compose.yml -o docker-compose.yml
```

### Étape 2 : Démarrer les services

```bash
docker-compose up -d
```

### Étape 3 : Vérifier l'installation

```bash
curl http://localhost:8080/health
```

## Configuration

### Variables d'environnement

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `APP_PORT` | `8080` | Port d'écoute de l'application |
| `FLASK_CONFIG` | `production` | Configuration Flask |
| `REQUEST_TIMEOUT` | `15` | Timeout des requêtes Kroki (secondes) |
| `MAX_BYTES` | `2000000` | Taille max des diagrammes (bytes) |

### Exemple avec configuration personnalisée

```bash
# Fichier .env
APP_PORT=3000
REQUEST_TIMEOUT=30
MAX_BYTES=5000000
```

```bash
docker-compose up -d
```

## Gestion des services

### Commandes utiles

```bash
# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Redémarrer
docker-compose restart

# Mettre à jour vers la dernière version
docker-compose pull && docker-compose up -d

# Voir le statut
docker-compose ps
```

### Résolution de problèmes

#### Port déjà utilisé

```bash
# Utiliser un autre port
APP_PORT=3000 docker-compose up -d

# Ou voir quel processus utilise le port
lsof -i :8080
```

#### Services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Redémarrer complètement
docker-compose down
docker-compose up -d
```

#### Images pas à jour

```bash
# Forcer le téléchargement
docker-compose pull
docker-compose up -d --force-recreate
```

## Utilisation

Une fois installé, accédez à l'application :
- **Interface web** : http://localhost:8080
- **Health check** : http://localhost:8080/health
- **API** : http://localhost:8080/api/generate

## Support

- **Documentation** : [README principal](../README.md)
- **Issues** : [GitHub Issues](https://github.com/stef500/kroki-flask-generator/issues)
- **Docker Hub** : [stef500/kroki-flask-generator](https://hub.docker.com/r/stef500/kroki-flask-generator)

## Désinstallation

```bash
# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer les images (optionnel)
docker rmi stef500/kroki-flask-generator:latest yuzutech/kroki:latest yuzutech/kroki-mermaid:latest

# Supprimer le fichier de configuration
rm docker-compose.yml
```