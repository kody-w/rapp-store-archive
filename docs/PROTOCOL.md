# RAPP Store Protocol Specification v1.0

This document defines the protocol for RAPP Store repositories, enabling interoperability between different AI agent and skill marketplaces.

## Overview

The RAPP Store Protocol enables:
- **Discovery**: Finding stores and their contents via manifest files
- **Retrieval**: Downloading agents and skills via raw GitHub URLs
- **Cross-compatibility**: Converting between RAPP Agent and Claude Skill formats
- **Federation**: Registering and using multiple store repositories

## Manifest Specification

Every RAPP Store must have a `manifest.json` at the repository root.

### Required Fields

```json
{
  "$schema": "https://rapp-store.github.io/schema/v1/manifest.json",
  "version": "1.0.0",
  "store": {
    "name": "Store Name",
    "description": "Store description",
    "owner": "github-username",
    "url": "https://github.com/username/repo",
    "license": "Apache-2.0"
  },
  "protocol": {
    "version": "1.0",
    "supports": ["rapp-agent", "claude-skill"],
    "discovery_endpoint": "manifest.json",
    "raw_base": "https://raw.githubusercontent.com/username/repo/main"
  },
  "agents": [],
  "skills": []
}
```

### Store Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable store name |
| `description` | string | Yes | Store description |
| `owner` | string | Yes | GitHub username or organization |
| `url` | string | Yes | Full GitHub repository URL |
| `license` | string | Yes | Store license (e.g., "Apache-2.0") |
| `created` | string | No | ISO 8601 creation date |
| `updated` | string | No | ISO 8601 last update date |

### Protocol Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Protocol version (currently "1.0") |
| `supports` | array | Yes | Supported types: "rapp-agent", "claude-skill" |
| `discovery_endpoint` | string | Yes | Path to manifest (always "manifest.json") |
| `raw_base` | string | Yes | Raw GitHub content base URL |

### Agent Entry

```json
{
  "id": "unique_agent_id",
  "type": "rapp-agent",
  "name": "Human Readable Name",
  "description": "What this agent does",
  "version": "1.0.0",
  "category": "category-id",
  "author": "Author Name",
  "license": "Apache-2.0",
  "path": "agents/agent_folder",
  "filename": "agent_file.py",
  "icon": "🤖",
  "tags": ["tag1", "tag2"],
  "features": ["Feature 1", "Feature 2"],
  "dependencies": ["package1", "package2"],
  "min_python": "3.9"
}
```

### Skill Entry

```json
{
  "id": "skill-id",
  "type": "claude-skill",
  "name": "Skill Name",
  "description": "What this skill does",
  "version": "1.0.0",
  "category": "category-id",
  "author": "Author Name",
  "license": "Apache-2.0",
  "path": "skills/skill-folder",
  "icon": "✨",
  "tags": ["tag1", "tag2"],
  "features": ["Feature 1", "Feature 2"],
  "resources": {
    "scripts": ["script1.py"],
    "references": ["doc.md"],
    "templates": ["template.html"]
  }
}
```

## Directory Structure

```
repository/
├── manifest.json           # Required: Store manifest
├── README.md              # Recommended: Documentation
├── index.html             # Optional: GitHub Pages frontend
├── agents/                # RAPP Agents
│   └── agent_id/
│       ├── agent_id.py    # Agent code
│       ├── metadata.json  # Optional: Extended metadata
│       └── README.md      # Optional: Documentation
├── skills/                # Claude Skills
│   └── skill-id/
│       ├── SKILL.md       # Skill definition
│       ├── scripts/       # Optional: Helper scripts
│       ├── references/    # Optional: Reference docs
│       └── templates/     # Optional: Templates
├── docs/                  # Protocol documentation
│   ├── PROTOCOL.md
│   └── CONTRIBUTING.md
└── schema/                # Optional: JSON schemas
    └── manifest.schema.json
```

## Discovery Protocol

### Store Discovery

1. Client receives repository URL (e.g., `https://github.com/owner/repo`)
2. Construct manifest URL: `https://raw.githubusercontent.com/owner/repo/main/manifest.json`
3. Fetch and parse manifest JSON
4. Validate protocol version compatibility
5. Cache manifest with appropriate TTL

### Item Discovery

Items are discovered from the manifest's `agents` and `skills` arrays. Each entry contains:
- Unique identifier (`id`)
- Path within repository (`path`)
- Filename for agents (`filename`)

### Content Retrieval

**Agents:**
```
{raw_base}/{agent.path}/{agent.filename}
```
Example: `https://raw.githubusercontent.com/kody-w/rapp-store-archive/main/agents/pdf_processor_agent/pdf_processor_agent.py`

**Skills:**
```
{raw_base}/{skill.path}/SKILL.md
```
Example: `https://raw.githubusercontent.com/kody-w/rapp-store-archive/main/skills/algorithmic-art/SKILL.md`

**Skill Resources:**
```
{raw_base}/{skill.path}/scripts/{script}
{raw_base}/{skill.path}/references/{reference}
{raw_base}/{skill.path}/templates/{template}
```

## Format Specifications

### RAPP Agent Format

RAPP Agents are Python classes inheriting from `BasicAgent`:

```python
from agents.basic_agent import BasicAgent

class MyAgent(BasicAgent):
    def __init__(self):
        self.name = 'MyAgent'
        self.metadata = {
            "name": self.name,
            "description": "What this agent does",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action to perform"
                    }
                },
                "required": ["action"]
            }
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        action = kwargs.get('action')
        # Implementation
        return "Result"
```

### Claude Skill Format

Claude Skills are Markdown files with YAML frontmatter:

```markdown
---
name: skill-name
description: What this skill does and when to use it
---

# Skill Title

Instructions and guidance for using this skill...
```

## Cross-Format Conversion

### Agent → Skill

1. Extract agent metadata (name, description)
2. Generate YAML frontmatter
3. Convert `perform()` method documentation to markdown instructions
4. Bundle any helper utilities as scripts

### Skill → Agent

1. Parse YAML frontmatter
2. Generate Python class with embedded skill instructions
3. Create `perform()` method that returns skill guidance
4. Bundle scripts as importable modules

## Categories

Standard category IDs:

| ID | Name | Description |
|----|------|-------------|
| `document-processing` | Document Processing | PDF, Word, Excel, PowerPoint |
| `code-generation` | Code & Development | Code gen, MCP servers |
| `creative` | Creative & Design | Art, design, visual |
| `business` | Business & Enterprise | CRM, sales, analytics |
| `communication` | Communication | Email, messaging |
| `data` | Data & Analytics | Data processing |
| `utilities` | Utilities | General tools |

## Error Handling

### HTTP Errors

| Code | Meaning | Action |
|------|---------|--------|
| 404 | Item not found | Remove from cache, report to user |
| 403 | Rate limited | Implement exponential backoff |
| 500 | Server error | Retry with backoff |

### Validation Errors

- Invalid manifest schema: Report error, skip store
- Missing required fields: Report warning, use defaults where possible
- Invalid item paths: Skip item, continue with others

## Security Considerations

1. **Code Execution**: Never auto-execute downloaded code
2. **Input Validation**: Validate all manifest data before use
3. **Path Traversal**: Validate paths stay within repository
4. **Rate Limiting**: Respect GitHub API rate limits
5. **Caching**: Implement appropriate cache invalidation

## Versioning

The protocol follows semantic versioning:
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

Current version: **1.0**

## Reference Implementation

See the `RAPPStoreAgent` class in the RAPP Store repository for a complete reference implementation of this protocol.
