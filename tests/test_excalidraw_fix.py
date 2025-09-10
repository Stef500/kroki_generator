"""Tests pour le fix Excalidraw JSON avec section files."""

import pytest
import json
from src.kroki_client import KrokiClient, KrokiError


class TestExcalidrawJSONFix:
    """Tests pour vérifier le nettoyage des JSON Excalidraw complets."""

    def test_preprocess_excalidraw_with_files_section(self):
        """Test du nettoyage d'un JSON Excalidraw avec section files."""
        # JSON avec section 'files' problématique
        json_with_files = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": [
                {
                    "id": "test-id",
                    "type": "rectangle",
                    "x": 100,
                    "y": 200,
                    "width": 150,
                    "height": 80,
                }
            ],
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20},
            "files": {
                "file-id": {
                    "mimeType": "image/png",
                    "dataURL": "data:image/png;base64,iVBORw0KGgo...",
                    "created": 1690295874454,
                }
            },
        }

        client = KrokiClient()
        result = client._preprocess_excalidraw(json.dumps(json_with_files))

        # Vérifier que le résultat est un JSON valide
        cleaned_data = json.loads(result)

        # Vérifier que la section 'files' a été supprimée
        assert "files" not in cleaned_data

        # Vérifier que les autres sections sont préservées
        assert cleaned_data["type"] == "excalidraw"
        assert cleaned_data["version"] == 2
        assert cleaned_data["source"] == "https://excalidraw.com"
        assert len(cleaned_data["elements"]) == 1
        assert cleaned_data["elements"][0]["id"] == "test-id"
        assert "appState" in cleaned_data

    def test_preprocess_excalidraw_without_files_section(self):
        """Test avec un JSON Excalidraw sans section files (format Kroki standard)."""
        # JSON sans section 'files' (format Kroki standard)
        standard_json = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": [
                {
                    "id": "test-id-2",
                    "type": "text",
                    "x": 50,
                    "y": 100,
                    "text": "Hello World",
                }
            ],
            "appState": {"viewBackgroundColor": "#ffffff"},
        }

        client = KrokiClient()
        result = client._preprocess_excalidraw(json.dumps(standard_json))

        # Vérifier que le résultat est un JSON valide
        cleaned_data = json.loads(result)

        # Vérifier que le contenu est préservé
        assert cleaned_data["type"] == "excalidraw"
        assert len(cleaned_data["elements"]) == 1
        assert cleaned_data["elements"][0]["text"] == "Hello World"

    def test_preprocess_excalidraw_invalid_json(self):
        """Test avec un JSON invalide."""
        invalid_json = '{"type": "excalidraw", invalid syntax}'

        client = KrokiClient()

        with pytest.raises(KrokiError) as exc_info:
            client._preprocess_excalidraw(invalid_json)

        assert "Invalid Excalidraw JSON format" in str(exc_info.value)

    def test_preprocess_excalidraw_not_excalidraw_type(self):
        """Test avec un JSON qui n'est pas de type excalidraw."""
        other_json = {"type": "other", "data": "some data"}

        client = KrokiClient()
        result = client._preprocess_excalidraw(json.dumps(other_json))

        # Le JSON devrait être retourné tel quel
        assert result == json.dumps(other_json)

    def test_preprocess_excalidraw_missing_elements(self):
        """Test avec un JSON Excalidraw sans éléments."""
        minimal_json = {"type": "excalidraw", "version": 2}

        client = KrokiClient()
        result = client._preprocess_excalidraw(json.dumps(minimal_json))

        cleaned_data = json.loads(result)

        # Vérifier que les valeurs par défaut sont ajoutées
        assert cleaned_data["type"] == "excalidraw"
        assert cleaned_data["version"] == 2
        assert cleaned_data["source"] == "https://excalidraw.com"
        assert cleaned_data["elements"] == []
        assert cleaned_data["appState"]["viewBackgroundColor"] == "#ffffff"
        assert cleaned_data["appState"]["gridSize"] == 20

    def test_integration_with_preprocess_diagram_source(self):
        """Test d'intégration avec _preprocess_diagram_source."""
        json_with_files = {
            "type": "excalidraw",
            "version": 2,
            "elements": [{"id": "test", "type": "rectangle"}],
            "appState": {"viewBackgroundColor": "#ffffff"},
            "files": {"file1": {"dataURL": "data:image/png;base64,..."}},
        }

        client = KrokiClient()
        result = client._preprocess_diagram_source(
            "excalidraw", json.dumps(json_with_files)
        )

        # Vérifier que les files ont été supprimées via le preprocessing général
        cleaned_data = json.loads(result)
        assert "files" not in cleaned_data
        assert len(cleaned_data["elements"]) == 1
