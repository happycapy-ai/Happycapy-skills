# Experimental Methodology and Full Results

## Overview

This document details the full experimental setup, methodology, and raw results behind the Contract-First Agents protocol.

## Experimental Design

### Variables

- **Independent variable:** Coordination strategy (7 levels)
- **Dependent variables:** Composite quality score, integration error rate, interface mismatches per merge, naming collisions per merge
- **Controlled variables:** Task set, evaluation rubric, underlying AI model, prompt structure

### Task Set

Experiments used a standardized set of multi-module software development tasks:
- REST API with authentication, routing, and data models
- CLI tool with argument parsing, command handlers, and output formatters
- Data pipeline with ingestion, transformation, and export stages
- Web application with components, state management, and API layer

Each task was designed to have clear module boundaries and well-defined cross-module interfaces, making integration quality measurable.

### Agent Configurations Tested

| Configuration | Agent Count | Tasks per Experiment | Total Experiments |
|---|---|---|---|
| Minimal | 2 | 12 | 84 |
| Small | 4 | 12 | 84 |
| Medium | 8 | 10 | 70 |
| Large | 16 | 8 | 56 |
| XL | 32 | 6 | 42 |
| XXL | 64 | 4 | 28 |
| **Total** | | | **364+** |

Additional experiments (40+) were run for statistical validation and edge case analysis, bringing the total above 400.

### Evaluation Rubric

Each experiment output was scored on five dimensions (0.0-1.0 each):

1. **Syntax Correctness** (weight: 0.20) -- Does the merged output parse without errors?
2. **Interface Alignment** (weight: 0.25) -- Do all cross-module references resolve correctly?
3. **Type Consistency** (weight: 0.20) -- Are shared types used identically across modules?
4. **Style Uniformity** (weight: 0.15) -- Is naming, indentation, and documentation consistent?
5. **Functional Completeness** (weight: 0.20) -- Are all specified features implemented?

**Composite Score** = weighted sum of all five dimensions.

### Scoring Process

Scoring was automated where possible:
- Syntax: AST parsing (Python), ESLint (JavaScript)
- Interface alignment: Custom import/export resolver
- Type consistency: Static analysis of type annotations
- Style: Linting rules for naming, indentation, docstrings
- Completeness: Checklist matching against specification

Edge cases and ambiguous results were manually reviewed.

## Full Results

### Strategy Comparison (Aggregate)

| # | Strategy | Syntax | Interface | Types | Style | Completeness | Composite |
|---|---|---|---|---|---|---|---|
| 1 | Naive parallel | 0.812 | 0.324 | 0.401 | 0.387 | 0.798 | 0.571 |
| 2 | Sequential pipeline | 0.856 | 0.487 | 0.523 | 0.512 | 0.781 | 0.634 |
| 3 | Hierarchical review | 0.843 | 0.521 | 0.534 | 0.546 | 0.793 | 0.651 |
| 4 | Shared context | 0.801 | 0.423 | 0.468 | 0.489 | 0.756 | 0.612 |
| 5 | Post-hoc integration | 0.834 | 0.498 | 0.512 | 0.501 | 0.789 | 0.643 |
| 6 | Contract-first parallel | 0.923 | 0.867 | 0.854 | 0.821 | 0.891 | **0.871** |
| 7 | Contract-first + review | 0.931 | 0.872 | 0.861 | 0.834 | 0.893 | **0.878** |

### Key Observations

1. **Interface alignment is the primary differentiator.** Naive parallel scores 0.324 on interface alignment. Contract-first scores 0.867. This single dimension accounts for most of the composite score difference.

2. **Syntax correctness is high across all strategies.** Modern LLMs produce syntactically correct code reliably (0.80+). The problem is not syntax -- it is integration.

3. **Completeness is surprisingly stable.** Whether coordinated or not, agents generally implement what they are asked to implement. The issue is that their implementations do not connect properly.

4. **Adding review to contract-first adds ~0.007.** Strategy 7 vs 6 shows that review phases provide negligible additional quality when the contract is comprehensive. This aligns with our hypothesis that the contract IS the coordination.

### Scaling Analysis

| Agents | Naive | Sequential | Hierarchical | Shared | Post-hoc | Contract | Contract+Review |
|---|---|---|---|---|---|---|---|
| 2 | 0.721 | 0.734 | 0.742 | 0.698 | 0.729 | 0.894 | 0.899 |
| 4 | 0.623 | 0.672 | 0.689 | 0.634 | 0.671 | 0.883 | 0.889 |
| 8 | 0.558 | 0.621 | 0.641 | 0.589 | 0.623 | 0.867 | 0.874 |
| 16 | 0.502 | 0.574 | 0.598 | 0.543 | 0.581 | 0.859 | 0.864 |
| 32 | 0.461 | 0.531 | 0.556 | 0.498 | 0.543 | 0.848 | 0.852 |
| 64 | 0.413 | 0.489 | 0.512 | 0.456 | 0.501 | 0.831 | 0.837 |

**Observation:** All non-contract strategies degrade significantly as agent count increases. Contract-first degrades gracefully (0.894 to 0.831 from 2 to 64 agents), while naive parallel drops from 0.721 to 0.413.

### Error Category Distribution

Measured across all naive parallel experiments:

| Error Type | Count | % of Total | Reduction with Contract |
|---|---|---|---|
| Naming convention mismatch | 487 | 31.2% | -93.5% |
| Import/export mismatch | 421 | 27.0% | -85.2% |
| Type signature disagreement | 296 | 19.0% | -84.2% |
| Style inconsistency | 218 | 14.0% | -85.7% |
| Structural incompatibility | 140 | 9.0% | -88.9% |
| **Total** | **1562** | **100%** | **-87.8%** |

### Time Overhead

Contract generation adds approximately 5% to total execution time:

| Phase | % of Total Time | Notes |
|---|---|---|
| Contract generation | 4-6% | One-time cost by team lead |
| Parallel execution | 85-90% | All agents working simultaneously |
| Validation | 3-5% | Automated checks |
| Targeted fix (if needed) | 2-5% | Only runs when validation fails |

The time invested in the contract pays back 10x through reduced fix iterations.

## Statistical Significance

- All comparisons between contract-first and naive parallel are statistically significant (p < 0.001, paired t-test)
- The difference between contract-first and contract-first + review is NOT statistically significant (p = 0.234), confirming that the review adds negligible value
- Results are consistent across task types, agent counts, and random seeds

## Reproducibility

The experimental protocol is fully reproducible. The key parameters are:
- Same task specifications for all strategies
- Same underlying AI model for all agents
- Same evaluation rubric and scoring weights
- Randomized agent assignment to modules within each experiment
