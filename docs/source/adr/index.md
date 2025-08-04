# 📋 Architecture Decision Records (ADRs)

This section contains Architecture Decision Records (ADRs) that document the design decisions made during the development of the Seedling template.

## What are ADRs?

Architecture Decision Records are documents that capture important architectural decisions made during a project. They provide context for why certain decisions were made and help future maintainers understand the reasoning behind the current architecture.

## ADR Structure

Each ADR follows this structure:

1. **Title**: Clear, descriptive title
2. **Status**: Current status (Proposed, Accepted, Deprecated, etc.)
3. **Context**: The situation that led to the decision
4. **Decision**: The decision that was made
5. **Consequences**: The consequences of the decision
6. **Alternatives**: Alternatives that were considered

## ADR List

```{toctree}
:maxdepth: 1

0001-template-design
0002-technology-stack
0003-architecture-decisions
```

## ADR-0001: Template Design Philosophy

**Status**: Accepted  
**Date**: 2024-01-01

Documents the core design philosophy and principles behind the Seedling template, including the choice of Copier as the template engine and the focus on modern Python development practices.

[Read ADR-0001](0001-template-design.md)

## ADR-0002: Technology Stack Rationale

**Status**: Accepted  
**Date**: 2024-01-01

Explains the technology choices made for the template, including uv for package management, modern Python features, and the selection of development tools.

[Read ADR-0002](0002-technology-stack.md)

## ADR-0003: Architecture Decisions and Project Structure

**Status**: Accepted  
**Date**: 2024-01-01

Details the architectural decisions regarding project structure, file organization, and the patterns used throughout the template.

[Read ADR-0003](0003-architecture-decisions.md)

## Contributing to ADRs

When making significant architectural decisions:

1. **Create a new ADR**: Use the template in `docs/adr/0001-template-design.md`
2. **Number sequentially**: Use the next available number
3. **Update this index**: Add the new ADR to the list above
4. **Get review**: Have the ADR reviewed by the team
5. **Update status**: Mark as Accepted once approved

## ADR Template

When creating a new ADR, use this template:

```markdown
# ADR-XXXX: [Title]

## Status

[Proposed/Accepted/Deprecated/Superseded]

## Date

YYYY-MM-DD

## Context

[Describe the situation that led to this decision]

## Decision

[Describe the decision that was made]

## Consequences

[Describe the consequences of this decision]

## Alternatives

[Describe alternatives that were considered]
```

## References

- [ADR GitHub Repository](https://github.com/joelparkerhenderson/architecture_decision_record)
- [ADR Documentation](https://adr.github.io/)
- [ADR Template](https://github.com/joelparkerhenderson/architecture_decision_record/blob/main/adr_template_by_michael_nygard.md) 