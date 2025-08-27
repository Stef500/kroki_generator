# Configuration DockerHub pour CI/CD

## Prérequis

1. **Compte DockerHub** : Avoir un compte sur [hub.docker.com](https://hub.docker.com)
2. **Repository DockerHub** : Créer un repository public ou privé pour `kroki-flask-generator`
3. **Access Token** : Générer un Personal Access Token DockerHub

## Configuration des Secrets GitHub

### 1. Générer un Access Token DockerHub

1. Connectez-vous à [hub.docker.com](https://hub.docker.com)
2. Allez dans **Account Settings** > **Security**
3. Cliquez sur **New Access Token**
4. Nom : `github-actions-kroki-flask`
5. Permissions : **Read, Write, Delete**
6. Copiez le token généré (il ne sera plus affiché)

### 2. Configurer les Secrets GitHub

Dans votre repository GitHub :

1. Allez dans **Settings** > **Secrets and variables** > **Actions**
2. Cliquez sur **New repository secret**
3. Ajoutez les secrets suivants :

```
DOCKERHUB_USERNAME: votre-nom-utilisateur-dockerhub
DOCKERHUB_TOKEN: le-token-généré-à-l-étape-1
```

### 3. Repository DockerHub

Créez un repository sur DockerHub avec le nom : `kroki-flask-generator`

URL finale : `https://hub.docker.com/r/VOTRE-USERNAME/kroki-flask-generator`

## Tags Docker Générés

Le pipeline CI génère automatiquement plusieurs tags :

- `latest` : Dernière version de la branche main
- `main-SHA` : Version spécifique avec hash du commit
- `main` : Branche main

## Architecture Multi-plateforme

L'image Docker est construite pour :
- `linux/amd64` (Intel/AMD)
- `linux/arm64` (Apple Silicon, ARM64)

## Utilisation

Après configuration, l'image sera disponible sur :
```bash
docker pull VOTRE-USERNAME/kroki-flask-generator:latest
docker run -p 8080:8080 VOTRE-USERNAME/kroki-flask-generator:latest
```

## Vérification

1. Push un commit sur la branche `main`
2. Vérifiez l'exécution du workflow dans **Actions**
3. Confirmez la présence de l'image sur DockerHub
4. Testez le pull de l'image : `docker pull VOTRE-USERNAME/kroki-flask-generator:latest`

## Troubleshooting

### Erreur d'authentification
- Vérifiez que `DOCKERHUB_USERNAME` correspond exactement à votre nom d'utilisateur DockerHub
- Régénérez le `DOCKERHUB_TOKEN` si nécessaire
- Confirmez que le token a les bonnes permissions

### Repository non trouvé
- Créez le repository `kroki-flask-generator` sur DockerHub
- Vérifiez que le nom correspond exactement dans le workflow

### Build multi-architecture échoue
- Les builds ARM64 peuvent être plus longs
- Vérifiez les logs détaillés dans Actions > Build job