# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project named "create-graph" using Python 3.12+. The project is in its initial setup phase with minimal structure.

## Project Structure

```
create_graph/
├── pyproject.toml          # Python project configuration and dependencies
├── src/                    # Main source code directory
│   └── main.py            # Main entry point (currently empty)
└── .serena/               # Serena MCP server configuration
    └── project.yml        # Project settings for semantic code operations
```

## Development Commands

This project uses modern Python tooling with pyproject.toml configuration:

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (when added)
pip install -e .
```

### Running the Application
```bash
# Run main entry point
python src/main.py
```

## Dependencies

Currently no dependencies are specified in pyproject.toml. Dependencies should be added to the `dependencies` array as the project grows.

## Architecture Notes

- **Entry Point**: `src/main.py` serves as the main application entry point
- **Package Structure**: Source code is organized under `src/` directory following modern Python packaging conventions
- **Configuration**: Uses pyproject.toml for modern Python project configuration instead of setup.py

## Development Guidelines

- Follow Python 3.12+ syntax and features
- Add new modules under the `src/` directory
- Update pyproject.toml when adding dependencies
- Use the existing project structure for consistency

## Claude comportment
- quand tu finis une tâche, penses à mettre à jour le fichier TASKS.md
- prépare un message de commit clair et concis