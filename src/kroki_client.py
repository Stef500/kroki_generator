"""Kroki HTTP client for diagram generation.

Ce module fournit un client HTTP robuste pour interagir avec le service
de génération de diagrammes Kroki, supportant plusieurs types de diagrammes,
formats de sortie et fonctionnalités avancées comme les thèmes.
"""

import tempfile
import requests
import json
from typing import Tuple, Optional
from flask import current_app


class KrokiError(Exception):
    """Exception levée pour les erreurs liées à Kroki.

    Classe d'exception personnalisée pour gérer les différentes erreurs
    qui peuvent survenir lors de la génération de diagrammes, incluant
    les problèmes réseau, syntaxe invalide et échecs de service.
    """

    pass


class KrokiClient:
    """Client HTTP pour le service Kroki.

    Fournit une interface haut niveau pour générer des diagrammes via
    le service Kroki avec support pour plusieurs types de diagrammes,
    formats de sortie, thèmes et gestion d'erreurs robuste.

    Attributes:
        base_url (str): URL du point de terminaison Kroki
        timeout (int): Délai d'expiration des requêtes HTTP en secondes
        max_bytes (int): Taille max du source avant utilisation de fichiers temporaires

    Types de diagrammes supportés:
        - mermaid: Organigrammes, diagrammes de séquence, diagrammes de Gantt
        - plantuml: Diagrammes UML, diagrammes de séquence, diagrammes de classe
        - graphviz: Graphes dirigés, diagrammes de réseau

    Formats de sortie supportés:
        - png: Format d'image raster
        - svg: Graphiques vectoriels évolutifs
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_bytes: Optional[int] = None,
    ) -> None:
        """Initialise le client Kroki.

        Args:
            base_url: URL du service Kroki. Si None, utilise la configuration
                     ou par défaut http://localhost:8000
            timeout: Délai d'expiration des requêtes HTTP en secondes. Si None,
                    utilise la configuration ou par défaut 10 secondes
            max_bytes: Taille maximum du source en octets avant utilisation
                      de fichiers temporaires. Si None, utilise la configuration
                      ou par défaut 1MB
        """
        self.base_url = base_url or (
            current_app.config["KROKI_URL"] if current_app else "http://localhost:8000"
        )
        self.timeout = timeout or (
            current_app.config["REQUEST_TIMEOUT"] if current_app else 10
        )
        self.max_bytes = max_bytes or (
            current_app.config["MAX_BYTES"] if current_app else 1000000
        )

    def generate_diagram(
        self, diagram_type: str, output_format: str, diagram_source: str
    ) -> Tuple[bytes, str]:
        """Génère un diagramme en utilisant le service Kroki.

        Valide les paramètres d'entrée, préprocesse le code source du diagramme
        pour appliquer les thèmes, puis envoie une requête HTTP au service Kroki
        pour générer l'image du diagramme.

        Args:
            diagram_type: Type de diagramme (mermaid, plantuml, graphviz)
            output_format: Format de sortie (png, svg)
            diagram_source: Code source du diagramme

        Returns:
            Tuple[bytes, str]: Tuple contenant (données_image_binaires, content_type)

        Raises:
            KrokiError: Si la génération échoue (syntaxe invalide, service indisponible,
                       timeout, etc.)

        Example:
            >>> client = KrokiClient()
            >>> image_data, content_type = client.generate_diagram(
            ...     "mermaid", "png", "graph TD\\nA --> B"
            ... )
            >>> with open("diagram.png", "wb") as f:
            ...     f.write(image_data)
        """
        # Validate inputs
        self._validate_inputs(diagram_type, output_format, diagram_source)

        # Preprocess diagram source based on type and theme
        diagram_source = self._preprocess_diagram_source(diagram_type, diagram_source)

        # Prepare request
        url = f"{self.base_url}/{diagram_type}/{output_format}"
        headers = {
            "Content-Type": "text/plain",
            "Accept": (
                f"image/{output_format}" if output_format != "svg" else "image/svg+xml"
            ),
        }

        try:
            # Handle large payloads with temporary files
            if len(diagram_source.encode("utf-8")) > self.max_bytes:
                return self._generate_with_tempfile(
                    url, headers, diagram_source, output_format
                )
            else:
                return self._generate_direct(
                    url, headers, diagram_source, output_format
                )

        except requests.exceptions.Timeout:
            raise KrokiError("Request timeout - Kroki service is taking too long")
        except requests.exceptions.ConnectionError:
            raise KrokiError("Connection error - Cannot reach Kroki service")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                # Check if the response is actually a valid image (PNG/SVG)
                content = e.response.content
                if (output_format == "png" and content.startswith(b"\x89PNG")) or (
                    output_format == "svg" and b"<svg" in content[:100]
                ):
                    # This is actually a successful generation, return it
                    content_type = (
                        f"image/{output_format}"
                        if output_format != "svg"
                        else "image/svg+xml"
                    )
                    return content, content_type
                else:
                    # This is a real error
                    error_text = (
                        e.response.text[:200] if e.response.text else "Unknown error"
                    )
                    raise KrokiError(f"Invalid diagram syntax: {error_text}")
            elif e.response.status_code >= 500:
                raise KrokiError("Kroki service error - Please try again later")
            else:
                raise KrokiError(
                    f"HTTP error {e.response.status_code}: {e.response.text}"
                )

    def _preprocess_diagram_source(self, diagram_type: str, diagram_source: str) -> str:
        """Prétraite le code source du diagramme pour appliquer les thèmes et le styling.

        Args:
            diagram_type: Type de diagramme (mermaid, plantuml, graphviz, blockdiag,
                         excalidraw, ditaa, seqdiag, actdiag, bpmn)
            diagram_source: Code source original du diagramme

        Returns:
            str: Code source modifié avec les configurations de thème appliquées
        """
        if diagram_type == "mermaid":
            return self._preprocess_mermaid(diagram_source)
        elif diagram_type == "plantuml":
            return self._preprocess_plantuml(diagram_source)
        elif diagram_type in ["blockdiag", "seqdiag", "actdiag"]:
            return self._preprocess_blockdiag_family(diagram_type, diagram_source)
        elif diagram_type == "ditaa":
            return self._preprocess_ditaa(diagram_source)
        elif diagram_type == "excalidraw":
            return self._preprocess_excalidraw(diagram_source)
        # bpmn doesn't need preprocessing
        return diagram_source

    def _preprocess_mermaid(self, source: str) -> str:
        """Ajoute la configuration de thème aux diagrammes Mermaid.

        Injecte la configuration de thème Mermaid au début du code source
        si aucune configuration n'est déjà présente.

        Args:
            source: Code source Mermaid original

        Returns:
            str: Code source avec configuration de thème ajoutée si nécessaire
        """
        # Get theme from config or default to base (light theme)
        theme = (
            current_app.config.get("DIAGRAM_THEME", "base") if current_app else "base"
        )

        # Map our theme names to Mermaid theme names
        mermaid_themes = {
            "default": "base",
            "light": "base",
            "dark": "dark",
            "neutral": "neutral",
            "forest": "forest",
        }

        mermaid_theme = mermaid_themes.get(theme, "base")

        # Check if the source already contains theme configuration
        if "%%{init:" in source or "theme:" in source:
            return source

        # Add theme configuration at the beginning
        theme_config = f"%%{{init: {{'theme': '{mermaid_theme}'}}}}%%\n"
        return theme_config + source

    def _preprocess_plantuml(self, source: str) -> str:
        """Ajoute le styling aux diagrammes PlantUML.

        Injecte des paramètres de thème PlantUML pour un fond clair
        après la directive @startuml si elle est présente.

        Args:
            source: Code source PlantUML original

        Returns:
            str: Code source avec paramètres de style ajoutés si nécessaire
        """
        # For PlantUML, we can add skinparams for light background
        if not source.strip().startswith("@startuml"):
            return source

        # Insert skinparam after @startuml
        lines = source.split("\n")
        if len(lines) > 0 and lines[0].strip().startswith("@startuml"):
            # Add light theme skinparams
            skinparams = [
                "!theme plain",
                "skinparam backgroundColor white",
                "skinparam defaultFontColor black",
            ]
            # Insert after @startuml line
            lines = lines[:1] + skinparams + lines[1:]
            return "\n".join(lines)
        return source

    def _preprocess_blockdiag_family(self, diagram_type: str, source: str) -> str:
        """Ajoute le styling aux diagrammes BlockDiag family (blockdiag, seqdiag, actdiag).

        Args:
            diagram_type: Type de diagramme blockdiag specifique
            source: Code source original du diagramme

        Returns:
            str: Code source avec paramètres de style ajoutés si nécessaire
        """
        # Add default styling if not present
        lines = source.strip().split("\n")
        if lines and not any("default_" in line for line in lines[:5]):
            # Add styling options
            style_lines = [
                "    default_node_color = lightblue;",
                "    default_linecolor = black;",
                "    default_textcolor = black;",
                "    node_width = 128;",
                "    node_height = 40;",
                "    default_shape = box;",
            ]

            # Insert after opening brace if present
            if lines and "{" in lines[0]:
                lines = lines[:1] + style_lines + lines[1:]
            else:
                # Insert at beginning
                lines = style_lines + lines

        return "\n".join(lines)

    def _preprocess_ditaa(self, source: str) -> str:
        """Prétraite les diagrammes Ditaa pour un styling cohérent.

        Ditaa est un outil de diagrammes ASCII art qui convertit les
        diagrammes texte en images. Pas de preprocessing spécifique nécessaire.

        Args:
            source: Code source Ditaa original

        Returns:
            str: Code source inchangé (Ditaa n'a pas besoin de preprocessing)
        """
        return source

    def _preprocess_excalidraw(self, source: str) -> str:
        """Nettoie et prétraite les diagrammes Excalidraw.

        Supprime la section 'files' contenant les données d'images base64
        qui ne sont pas supportées par Kroki. Conserve uniquement les
        éléments essentiels : type, version, source, elements, appState.

        Args:
            source: Code source Excalidraw original (JSON complet d'export)

        Returns:
            str: Code source nettoyé compatible avec Kroki

        Raises:
            KrokiError: Si le JSON est malformé et ne peut pas être parsé
        """
        try:
            # Tentative de parsing du JSON
            data = json.loads(source.strip())

            # Vérifier que c'est bien un JSON Excalidraw
            if not isinstance(data, dict) or data.get("type") != "excalidraw":
                return source  # Pas un JSON Excalidraw, retourner tel quel

            # Créer un JSON nettoyé avec seulement les clés essentielles
            cleaned_data = {
                "type": data.get("type", "excalidraw"),
                "version": data.get("version", 2),
                "source": data.get("source", "https://excalidraw.com"),
                "elements": data.get("elements", []),
                "appState": data.get(
                    "appState", {"viewBackgroundColor": "#ffffff", "gridSize": 20}
                ),
            }

            # Retourner le JSON nettoyé
            return json.dumps(cleaned_data, separators=(",", ":"))

        except json.JSONDecodeError as e:
            # Le source n'est pas un JSON valide
            raise KrokiError(f"Invalid Excalidraw JSON format: {str(e)}")
        except Exception as e:
            # Autres erreurs de traitement
            raise KrokiError(f"Error processing Excalidraw diagram: {str(e)}")

    def _validate_inputs(
        self, diagram_type: str, output_format: str, diagram_source: str
    ) -> None:
        """Valide les paramètres d'entrée.

        Args:
            diagram_type: Type de diagramme à valider
            output_format: Format de sortie à valider
            diagram_source: Code source du diagramme à valider

        Raises:
            KrokiError: Si l'un des paramètres est invalide
        """
        valid_types = [
            "mermaid",
            "plantuml",
            "graphviz",
            "blockdiag",
            "excalidraw",
            "ditaa",
            "seqdiag",
            "actdiag",
            "bpmn",
        ]
        valid_formats = ["png", "svg"]

        if diagram_type not in valid_types:
            raise KrokiError(
                f"Invalid diagram type: {diagram_type}. Must be one of {valid_types}"
            )

        if output_format not in valid_formats:
            raise KrokiError(
                f"Invalid output format: {output_format}. Must be one of {valid_formats}"
            )

        if not diagram_source or not diagram_source.strip():
            raise KrokiError("Diagram source cannot be empty")

    def _generate_direct(
        self, url: str, headers: dict, diagram_source: str, output_format: str
    ) -> Tuple[bytes, str]:
        """Génère un diagramme avec une requête HTTP directe.

        Méthode optimisée pour les petits diagrammes qui peuvent être
        envoyés directement dans le corps de la requête HTTP.

        Args:
            url: URL complète de l'endpoint Kroki
            headers: Headers HTTP pour la requête
            diagram_source: Code source du diagramme
            output_format: Format de sortie (png, svg)

        Returns:
            Tuple[bytes, str]: Données binaires de l'image et content-type

        Raises:
            requests.exceptions.HTTPError: En cas d'erreur HTTP
            KrokiError: Si Kroki retourne une image d'erreur
        """
        response = requests.post(
            url,
            data=diagram_source.encode("utf-8"),
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        # If we reach here, the HTTP request was successful (status 200)
        # The response content is the generated diagram image

        content_type = (
            f"image/{output_format}" if output_format != "svg" else "image/svg+xml"
        )
        return response.content, content_type

    def _generate_with_tempfile(
        self, url: str, headers: dict, diagram_source: str, output_format: str
    ) -> Tuple[bytes, str]:
        """Génère un diagramme en utilisant un fichier temporaire pour les gros payloads.

        Méthode optimisée pour les diagrammes volumineux qui dépassent la limite
        max_bytes. Écrit le code source dans un fichier temporaire et l'envoie
        via une requête HTTP multipart.

        Args:
            url: URL complète de l'endpoint Kroki
            headers: Headers HTTP pour la requête
            diagram_source: Code source du diagramme
            output_format: Format de sortie (png, svg)

        Returns:
            Tuple[bytes, str]: Données binaires de l'image et content-type

        Raises:
            requests.exceptions.HTTPError: En cas d'erreur HTTP
            OSError: En cas d'erreur lors de la gestion du fichier temporaire
            KrokiError: Si Kroki retourne une image d'erreur
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as tmp_file:
            tmp_file.write(diagram_source)
            tmp_file_path = tmp_file.name

        try:
            with open(tmp_file_path, "rb") as f:
                response = requests.post(
                    url, data=f, headers=headers, timeout=self.timeout
                )
            response.raise_for_status()

            # Check if Kroki returned an error image (PNG with error text)
            if output_format == "png" and response.content.startswith(b"\x89PNG"):
                # Try to extract error message from PNG content
                content_str = response.content.decode("utf-8", errors="ignore")
                if any(
                    error_word in content_str
                    for error_word in ["error", "invalid", "syntax", "failed"]
                ):
                    # Extract readable error message
                    lines = content_str.split("\n")
                    error_lines = [
                        line.strip()
                        for line in lines
                        if line.strip() and len(line.strip()) > 3
                    ]
                    if error_lines:
                        error_msg = error_lines[0][
                            :100
                        ]  # First meaningful line, truncated
                        raise KrokiError(f"Diagram generation failed: {error_msg}")
                    else:
                        raise KrokiError(
                            "Diagram generation failed - invalid diagram syntax"
                        )

            content_type = (
                f"image/{output_format}" if output_format != "svg" else "image/svg+xml"
            )
            return response.content, content_type

        finally:
            # Cleanup temporary file
            import os

            try:
                os.unlink(tmp_file_path)
            except OSError:
                pass
