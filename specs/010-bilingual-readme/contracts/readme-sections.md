# README Section Contracts

**Feature**: 010-bilingual-readme
**Date**: 2026-01-20

## Header Section Contract

```markdown
<div align="center">

# LegalDocs Manager

🇺🇸 [English](#english) | 🇪🇸 [Español](#español)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Coverage](https://img.shields.io/badge/Coverage-98%25-brightgreen.svg)
![Tests](https://img.shields.io/badge/Tests-163%20passing-brightgreen.svg)

</div>
```

## Table of Contents Contract

Each language section must include a TOC immediately after the section header.

### English TOC Template
```markdown
## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running Tests](#running-tests)
- [Demo Data](#demo-data)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
```

### Spanish TOC Template
```markdown
## Tabla de Contenidos

- [Características](#características)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Stack Tecnológico](#stack-tecnológico)
- [Inicio Rápido](#inicio-rápido)
- [Instalación](#instalación)
- [Variables de Entorno](#variables-de-entorno)
- [Configuración de Base de Datos](#configuración-de-base-de-datos)
- [Ejecutar Tests](#ejecutar-tests)
- [Datos de Demostración](#datos-de-demostración)
- [Referencia API](#referencia-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
```

## Features Section Contract

Each feature must follow this format:

```markdown
- 👥 **[Feature Name]**: [One-line description]
```

### Features List (English)
| Icon | Feature | Description |
|------|---------|-------------|
| 👥 | Client Management | Track client information, contact details, and associated cases |
| ⚖️ | Case Management | Handle legal cases with status tracking, priorities, and automatic case number generation |
| 📄 | Document Management | Upload, organize, and manage legal documents with confidentiality controls |
| 📊 | Dashboard | Real-time statistics and overview of active cases |
| 🔍 | Search | Global search across clients, cases, and documents |
| 🔐 | User Authentication | Token-based authentication with registration, login, and profile management |
| 📚 | API Documentation | Interactive Swagger UI documentation |

### Features List (Spanish)
| Icon | Feature | Description |
|------|---------|-------------|
| 👥 | Gestión de Clientes | Seguimiento de información de clientes, datos de contacto y casos asociados |
| ⚖️ | Gestión de Casos | Manejo de casos legales con seguimiento de estado, prioridades y generación automática de número de caso |
| 📄 | Gestión de Documentos | Carga, organización y gestión de documentos legales con controles de confidencialidad |
| 📊 | Panel de Control | Estadísticas en tiempo real y resumen de casos activos |
| 🔍 | Búsqueda | Búsqueda global en clientes, casos y documentos |
| 🔐 | Autenticación de Usuarios | Autenticación basada en token con registro, inicio de sesión y gestión de perfil |
| 📚 | Documentación API | Documentación interactiva con Swagger UI |

## Screenshot Gallery Contract

Use collapsible section with organized categories:

```markdown
<details>
<summary>📸 View Screenshots / Ver Capturas</summary>

### Category Name / Nombre de Categoría

![Image Description](path/to/image.png)

*English caption / Descripción en español*

</details>
```

### Screenshot Categories
1. Swagger API Documentation / Documentación API Swagger
2. Authentication / Autenticación
3. Client Management / Gestión de Clientes
4. Case Management / Gestión de Casos
5. Document Management / Gestión de Documentos
6. Dashboard & Search / Panel y Búsqueda
7. Django Admin / Administración Django

## API Reference Contract

Each resource group follows this table format:

```markdown
### Resource Name / Nombre del Recurso

| Endpoint | Method | Description EN | Descripción ES |
|----------|--------|----------------|----------------|
| `/api/v1/path/` | GET | Description | Descripción |
```

## Quick Start Contract

Minimal 5-step setup with copy-paste commands:

```markdown
## Quick Start / Inicio Rápido

```bash
# 1. Clone / Clonar
git clone https://github.com/hooperits/LegalDocs-Manager.git
cd LegalDocs-Manager

# 2. Virtual environment / Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install / Instalar
pip install -r requirements.txt

# 4. Setup / Configurar
cd legaldocs
python manage.py migrate
python manage.py createsuperuser

# 5. Run / Ejecutar
python manage.py runserver
```

Visit / Visitar: http://localhost:8000/api/v1/docs/
```

## Environment Variables Contract

Table format with all variables:

```markdown
| Variable | Description EN | Descripción ES | Default |
|----------|----------------|----------------|---------|
| `SECRET_KEY` | Django secret key | Clave secreta de Django | Required |
```

## Divider Contract

Use horizontal rule with language indicator:

```markdown
---

<div align="center">

# 🇪🇸 Español

[🇺🇸 Switch to English](#english)

</div>
```

## Link References

All external links should be documented:

- Repository: `https://github.com/hooperits/LegalDocs-Manager`
- API Docs: `API_DOCS.md`
- Deployment Guide: `DEPLOYMENT.md`
- Screenshots Gallery: `docs/screenshots/README.md`
- Issues: `https://github.com/hooperits/LegalDocs-Manager/issues`
