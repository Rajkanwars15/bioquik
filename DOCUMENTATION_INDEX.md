# Bioquik Documentation Index

This document provides an overview of all available documentation for the Bioquik project.

## 📚 Documentation Overview

Bioquik has comprehensive documentation organized by audience and purpose:

### For End Users
- **Getting Started**: How to install and use Bioquik
- **Tutorials**: Step-by-step guides for common tasks
- **API Reference**: Function and class documentation

### For Developers
- **Architecture**: System design and component overview
- **Module Reference**: Detailed documentation of each module
- **Developer Guide**: Contributing and extending Bioquik

---

## 📖 Documentation Files

### User-Facing Documentation

#### [README.md](README.md)
**Purpose**: Main project overview and quick start guide

**Contents**:
- Project description and features
- Installation instructions
- Basic usage examples
- Links to other documentation

**Audience**: All users (new and existing)

---

#### [docs/source/quickstart.md](docs/source/quickstart.md)
**Purpose**: Get started with Bioquik quickly

**Contents**:
- Command-line usage examples
- Python API usage
- Common workflows
- Parameter explanations

**Audience**: New users

---

#### [docs/source/validation.md](docs/source/validation.md)
**Purpose**: Understanding input validation

**Contents**:
- Pattern validation rules
- Directory validation
- Error messages and troubleshooting

**Audience**: Users encountering validation errors

---

#### [docs/source/reports.md](docs/source/reports.md)
**Purpose**: Understanding output formats

**Contents**:
- CSV format details
- JSON format details
- Plot descriptions
- Interpreting results

**Audience**: Users analyzing results

---

### Developer Documentation

#### [ARCHITECTURE.md](ARCHITECTURE.md)
**Purpose**: High-level system architecture and design decisions

**Contents**:
- System overview and data flow
- Component architecture
- Design patterns used
- Performance characteristics
- Extension points
- Future considerations

**Audience**: Developers, architects, contributors

**Key Sections**:
- High-Level Flow diagram
- Component descriptions
- Design decisions and rationale
- Performance analysis
- Glossary of terms

---

#### [MODULES.md](MODULES.md)
**Purpose**: Detailed reference for each module

**Contents**:
- Module-by-module documentation
- Function signatures and examples
- Usage patterns
- Extension examples
- Module dependencies

**Audience**: Developers working with specific modules

**Key Sections**:
- Complete module list with descriptions
- Function documentation with examples
- Usage patterns (basic, programmatic, low-level)
- Extension examples

---

#### [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
**Purpose**: Guide for contributing and extending Bioquik

**Contents**:
- Development setup
- Code structure
- Design principles
- Adding new features
- Testing strategy
- Debugging tips
- Code style guidelines
- Contributing workflow

**Audience**: Contributors, maintainers

**Key Sections**:
- Quick start for developers
- Core algorithms explained
- How to add features
- Testing and debugging
- Performance optimization

---

#### [docs/source/architecture.md](docs/source/architecture.md)
**Purpose**: In-depth technical architecture documentation

**Contents**:
- Detailed algorithm explanations
- Data structure internals
- Performance analysis
- Extension points
- Research references

**Audience**: Developers needing deep technical understanding

**Key Sections**:
- FM-Index deep dive
- Wavelet Tree implementation
- Parallel processing strategy
- Memory management
- Time/space complexity analysis

---

## 🗺️ Documentation Map

### By Task

**I want to...**

- **Use Bioquik**: Start with [README.md](README.md) → [quickstart.md](docs/source/quickstart.md)
- **Understand results**: Read [reports.md](docs/source/reports.md)
- **Fix validation errors**: Read [validation.md](docs/source/validation.md)
- **Understand the system**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
- **Work with specific modules**: Read [MODULES.md](MODULES.md)
- **Contribute code**: Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Deep technical dive**: Read [docs/source/architecture.md](docs/source/architecture.md)

### By Role

**I am a...**

- **New User**: [README.md](README.md) → [quickstart.md](docs/source/quickstart.md)
- **Regular User**: [reports.md](docs/source/reports.md), [validation.md](docs/source/validation.md)
- **Developer**: [ARCHITECTURE.md](ARCHITECTURE.md) → [MODULES.md](MODULES.md) → [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Researcher**: [docs/source/architecture.md](docs/source/architecture.md) → [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🔍 Quick Reference

### Key Concepts

| Concept | Documentation |
|---------|--------------|
| FM-Index | [ARCHITECTURE.md](ARCHITECTURE.md), [docs/source/architecture.md](docs/source/architecture.md) |
| Wavelet Tree | [ARCHITECTURE.md](ARCHITECTURE.md), [MODULES.md](MODULES.md) |
| Pattern Expansion | [MODULES.md](MODULES.md), [docs/source/architecture.md](docs/source/architecture.md) |
| Parallel Processing | [ARCHITECTURE.md](ARCHITECTURE.md), [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) |
| CLI Usage | [README.md](README.md), [docs/source/quickstart.md](docs/source/quickstart.md) |
| Python API | [MODULES.md](MODULES.md), [docs/source/quickstart.md](docs/source/quickstart.md) |

### Common Questions

**Q: How does Bioquik count motifs?**
- A: See [ARCHITECTURE.md](ARCHITECTURE.md) - "FM-Index: The Heart of Pattern Matching"

**Q: How do I add a new pattern type?**
- A: See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - "Adding New Features"

**Q: What's the time complexity?**
- A: See [ARCHITECTURE.md](ARCHITECTURE.md) - "Performance Characteristics"

**Q: How do I process a single file?**
- A: See [MODULES.md](MODULES.md) - "fasta_worker.py" section

**Q: How does parallel processing work?**
- A: See [ARCHITECTURE.md](ARCHITECTURE.md) - "Processing Orchestrator" and [docs/source/architecture.md](docs/source/architecture.md) - "Parallel Processing Strategy"

---

## 📊 Documentation Structure

```
Documentation
│
├── User Documentation
│   ├── README.md (overview)
│   ├── docs/source/
│   │   ├── index.md (docs homepage)
│   │   ├── quickstart.md (getting started)
│   │   ├── validation.md (input validation)
│   │   └── reports.md (output formats)
│   └── Online: https://bioquik.readthedocs.io/
│
└── Developer Documentation
    ├── ARCHITECTURE.md (system architecture)
    ├── MODULES.md (module reference)
    ├── DEVELOPER_GUIDE.md (contributing guide)
    └── docs/source/architecture.md (technical deep dive)
```

---

## 🔄 Documentation Maintenance

### When to Update Documentation

- **New Feature**: Update relevant user docs + architecture docs
- **API Change**: Update MODULES.md + quickstart.md
- **Architecture Change**: Update ARCHITECTURE.md + docs/source/architecture.md
- **Bug Fix**: Update relevant troubleshooting sections

### Documentation Standards

- Use clear, concise language
- Include code examples
- Link between related documents
- Keep examples up-to-date
- Use consistent formatting

---

## 📝 Contributing to Documentation

See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for:
- Documentation style guidelines
- How to build docs locally
- Pull request checklist

---

## 🌐 External Resources

- **Online Documentation**: [Read the Docs](https://bioquik.readthedocs.io/)
- **GitHub Repository**: [github.com/Rajkanwars15/bioquik](https://github.com/Rajkanwars15/bioquik)
- **Issue Tracker**: [GitHub Issues](https://github.com/Rajkanwars15/bioquik/issues)

---

## 📌 Summary

**Start Here**:
- Users → [README.md](README.md)
- Developers → [ARCHITECTURE.md](ARCHITECTURE.md)

**Deep Dive**:
- Users → [docs/source/](docs/source/)
- Developers → [MODULES.md](MODULES.md) + [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

**Reference**:
- All → [MODULES.md](MODULES.md) (function reference)
- Developers → [docs/source/architecture.md](docs/source/architecture.md) (algorithms)
