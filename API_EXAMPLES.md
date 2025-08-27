# API Usage Examples

This document provides comprehensive curl examples for interacting with the Kroki Flask Generator API.

## Base URL
```bash
BASE_URL="http://localhost:8080"
```

## Health Check

### Basic Health Check
```bash
curl -X GET "${BASE_URL}/health" | jq
```

**Expected Response:**
```json
{
  "service": "kroki-flask-generator",
  "version": "0.1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "healthy",
  "checks": {
    "service": {
      "status": "healthy",
      "message": "Flask service running"
    },
    "kroki": {
      "status": "healthy",
      "message": "Kroki service accessible at http://localhost:8000",
      "response_time_ms": 45
    }
  }
}
```

## Generate Diagrams

### Mermaid Flowchart (JSON)

```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "png",
    "diagram_source": "graph TD\n    A[Start] --> B{Decision}\n    B -->|Yes| C[Action 1]\n    B -->|No| D[Action 2]\n    C --> E[End]\n    D --> E"
  }' \
  --output mermaid_flowchart.png
```

### Mermaid Sequence Diagram with Dark Theme
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "svg",
    "diagram_source": "sequenceDiagram\n    participant A as Alice\n    participant B as Bob\n    A->>+B: Hello Bob, how are you?\n    B-->>-A: Great!",
    "diagram_theme": "dark"
  }' \
  --output mermaid_sequence_dark.svg
```

### PlantUML Class Diagram (JSON)
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "plantuml",
    "output_format": "png",
    "diagram_source": "@startuml\nclass User {\n  +String name\n  +String email\n  +login()\n  +logout()\n}\nclass Admin {\n  +manageUsers()\n}\nUser <|-- Admin\n@enduml"
  }' \
  --output plantuml_class.png
```

### PlantUML Sequence Diagram (Text/Plain)
```bash
curl -X POST "${BASE_URL}/api/generate?diagram_type=plantuml&output_format=svg" \
  -H "Content-Type: text/plain" \
  -d "@startuml
participant User
participant System
participant Database

User -> System: Request data
activate System

System -> Database: Query
activate Database
Database --> System: Result
deactivate Database

System --> User: Response
deactivate System
@enduml" \
  --output plantuml_sequence.svg
```

### Graphviz Network Diagram
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "graphviz",
    "output_format": "png",
    "diagram_source": "digraph G {\n  rankdir=LR;\n  node [shape=box];\n  \n  A [label=\"Web Server\"];\n  B [label=\"Database\"];\n  C [label=\"Cache\"];\n  D [label=\"Load Balancer\"];\n  \n  D -> A;\n  A -> B;\n  A -> C;\n}"
  }' \
  --output graphviz_network.png
```

### Complex Mermaid Gantt Chart
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "svg",
    "diagram_source": "gantt\n    title Project Timeline\n    dateFormat YYYY-MM-DD\n    section Planning\n    Requirements    :done, req, 2024-01-01, 2024-01-07\n    Design         :done, des, after req, 5d\n    section Development\n    Backend        :active, backend, 2024-01-15, 10d\n    Frontend       :frontend, after backend, 8d\n    section Testing\n    Unit Tests     :testing, after frontend, 3d\n    Integration    :integration, after testing, 2d"
  }' \
  --output mermaid_gantt.svg
```

## Error Handling Examples

### Invalid Diagram Type
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "invalid_type",
    "output_format": "png",
    "diagram_source": "graph TD\nA --> B"
  }'
```

**Expected Response:**
```json
{
  "error": "Invalid diagram type: invalid_type. Must be one of ['mermaid', 'plantuml', 'graphviz']"
}
```

### Missing Required Fields
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid"
  }'
```

**Expected Response:**
```json
{
  "error": "Missing required fields: output_format, diagram_source"
}
```

### Invalid Content Type
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: text/html" \
  -d "some data"
```

**Expected Response:**
```json
{
  "error": "Content-Type must be application/json or text/plain"
}
```

### Invalid Diagram Syntax
```bash
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "png",
    "diagram_source": "invalid mermaid syntax here"
  }'
```

**Expected Response:**
```json
{
  "error": "Invalid diagram syntax: [Kroki error details]"
}
```

## Advanced Usage

### Large Diagram with File Input
```bash
# Create a large PlantUML file
cat > large_diagram.puml << 'EOF'
@startuml
!theme plain
skinparam backgroundColor white

package "Web Layer" {
  class WebController
  class AuthController
  class UserController
}

package "Service Layer" {
  class UserService
  class AuthService
  class EmailService
}

package "Data Layer" {
  class UserRepository
  class SessionRepository
  interface DatabaseConnection
}

WebController --> UserService
AuthController --> AuthService
UserController --> UserService
UserService --> UserRepository
AuthService --> SessionRepository
UserRepository --> DatabaseConnection
SessionRepository --> DatabaseConnection

@enduml
EOF

# Send the file content
curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d "{
    \"diagram_type\": \"plantuml\",
    \"output_format\": \"svg\",
    \"diagram_source\": \"$(cat large_diagram.puml | sed 's/"/\\"/g' | tr '\n' '\\n')\"
  }" \
  --output large_diagram.svg

# Cleanup
rm large_diagram.puml
```

### Using Text/Plain with Complex Diagrams
```bash
curl -X POST "${BASE_URL}/api/generate?diagram_type=mermaid&output_format=png" \
  -H "Content-Type: text/plain" \
  --data-binary @- << 'EOF' \
  --output complex_mermaid.png
graph TB
    subgraph "Frontend"
        A[React App]
        B[Redux Store]
        C[Components]
    end
    
    subgraph "Backend"
        D[API Gateway]
        E[Auth Service]
        F[User Service]
        G[Data Service]
    end
    
    subgraph "Database"
        H[(PostgreSQL)]
        I[(Redis Cache)]
    end
    
    A --> B
    B --> C
    A --> D
    D --> E
    D --> F
    D --> G
    F --> H
    G --> H
    E --> I
EOF
```

### Performance Testing
```bash
# Test response time
time curl -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "png",
    "diagram_source": "graph LR\nA --> B --> C --> D --> E"
  }' \
  --output performance_test.png

# Concurrent requests (requires GNU parallel)
seq 10 | parallel -j5 'curl -X POST "${BASE_URL}/api/generate" -H "Content-Type: application/json" -d '\''{"diagram_type": "mermaid", "output_format": "png", "diagram_source": "graph TD\nA{} --> B{}"}'\'' --output test_{}.png'
```

## Response Headers Analysis

```bash
# Inspect response headers
curl -I -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "png", 
    "diagram_source": "graph TD\nA --> B"
  }'
```

**Expected Headers:**
```
HTTP/1.1 200 OK
Content-Type: image/png
Content-Disposition: inline; filename=diagram.png
Cache-Control: no-cache, no-store, must-revalidate
Content-Length: 12345
```

## Batch Processing Script

```bash
#!/bin/bash
# batch_generate.sh - Generate multiple diagrams

BASE_URL="http://localhost:8080"

# Array of diagram configurations
declare -A diagrams=(
    ["flowchart"]='{"diagram_type": "mermaid", "output_format": "png", "diagram_source": "graph TD\nA[Start] --> B[End]"}'
    ["sequence"]='{"diagram_type": "plantuml", "output_format": "svg", "diagram_source": "@startuml\nA -> B\n@enduml"}'
    ["network"]='{"diagram_type": "graphviz", "output_format": "png", "diagram_source": "digraph G { A -> B; }"}'
)

# Generate all diagrams
for name in "${!diagrams[@]}"; do
    echo "Generating ${name}..."
    curl -s -X POST "${BASE_URL}/api/generate" \
        -H "Content-Type: application/json" \
        -d "${diagrams[$name]}" \
        --output "${name}.${diagrams[$name]//.*output_format.*:.*\"([^\"]*)\".*/\1}"
    
    if [ $? -eq 0 ]; then
        echo "✓ ${name} generated successfully"
    else
        echo "✗ ${name} generation failed"
    fi
done
```

## Testing Different Themes

```bash
# Test all Mermaid themes
themes=("default" "light" "dark" "neutral" "forest")

for theme in "${themes[@]}"; do
    curl -X POST "${BASE_URL}/api/generate" \
        -H "Content-Type: application/json" \
        -d "{
            \"diagram_type\": \"mermaid\",
            \"output_format\": \"png\",
            \"diagram_source\": \"graph TD\n    A[Start] --> B[Process]\n    B --> C[End]\",
            \"diagram_theme\": \"${theme}\"
        }" \
        --output "theme_${theme}.png"
    echo "Generated theme_${theme}.png"
done
```