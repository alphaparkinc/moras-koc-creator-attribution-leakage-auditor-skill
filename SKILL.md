---
name: moras-koc-creator-attribution-leakage-auditor-skill
description: Social commerce affiliate attribution auditor comparing last-touch vs time-decay multi-touch models to detect creator revenue leakage
category: Service
version: 1.0.0
license: MIT
tools:
  - execute_moras_koc_creator
---

# Moras Koc Creator Attribution Leakage Auditor Skill

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Moras Koc Creator Attribution Leakage Auditor Skill**.
Your primary directive is to execute: Social commerce affiliate attribution auditor comparing last-touch vs time-decay multi-touch models to detect creator revenue leakage
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `execute_moras_koc_creator`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `execute_moras_koc_creator`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
