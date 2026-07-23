# DEDA_Spatial_Algo_Pricing

> **Algorithmic pricing in a 2-D spatial (Hotelling) grocery market — Q-learning incumbents and an LLM "CEO" agent, calibrated on real Berlin inner-Ringbahn spatial data.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Seminar project for **DEDA (Digital Economy and Decision Analytics)**. This is a
lean, data-free publication copy of the working repository: it contains all code,
configs and notebooks needed to regenerate the datasets and reproduce the runs,
but **no data files** (see [Data](#data)).

---

## Overview

A two-dimensional Hotelling model of spatial competition on a real geographic grid.
Grocery stores set prices period by period; consumers on a population-weighted
100 m grid choose stores via a logit demand system with travel-time disutility.
Two agent layers interact:

- **Q-learning incumbents** — per-store tabular Q-policies over a relative price
  action space (Calvano et al. 2020 style calibration). This is the *baseline*.
- **LLM "CEO" agent** — an optional strategic layer that, after a Q-learning
  burn-in, periodically re-parameterises the chain's stores via structured LLM
  calls. This is the *strategic* game.

The economic environment (transport cost, logit scale, outside option, marginal
costs, quality ladder) is structurally calibrated to the **Berlin inner-Ringbahn**
study area (S41/S42 ring).

---

## Installation

```bash
# From inside the repository folder:
pip install -e .            # core package (src layout)
pip install -e ".[all]"     # all extras: spatial, viz, rl, llm, db, cli, notebooks
```

Development was done on **Python 3.11** (a `conda` environment named `py314` is
referenced in the run scripts; any 3.11+ interpreter works). Install extras
selectively if you only need part of the pipeline — e.g. `pip install -e ".[spatial,viz]"`
to regenerate data and plot, or `pip install -e ".[rl]"` to run the Q-learning
baseline. See `pyproject.toml` for the full extras matrix.

---

## Data

**The repository ships with no data.** All processed datasets the simulations read
(`data/processed/demand_grid.parquet`, `supermarkets.parquet`, `travel_times.parquet`,
`simulation_grid.parquet`) must be regenerated locally.

### 1. Automatic download + processing

Most sources (Zensus 2022 population grid, OSM boundaries and supermarket POIs,
LOR shapes, VBB/GTFS transit times, Berlin GDI social-structure indices) are
downloaded and processed **programmatically** by the `hotelling.spatial` pipeline:

```bash
pip install -e ".[spatial]"

# Run the full Berlin inner-Ringbahn pipeline (download → filter → grid → assemble):
hotelling-spatial                     # console script, or:
python -m hotelling.spatial.exe

# Equivalently, from Python:
python -c "from hotelling.spatial import run_default_data_pipeline; run_default_data_pipeline()"
```

This writes the simulation-ready parquet files into `data/processed/`.
The `notebooks/GEO_00 … GEO_07` series documents each stage of this pipeline
(download, sanity checks, preparation, preliminary maps) and is the best reference
if a step needs debugging.

### 2. Two files must be placed manually

Two sources are not publicly downloadable and must be obtained separately and
dropped into `data/raw/` **before** running the pipeline:

| File | Put in | Description |
|------|--------|-------------|
| `2023_12_IHK_Berlin_Gewerbedaten.csv` | `data/raw/` | IHK Berlin business microdata (employment enrichment) |
| `Medianeinkommen_Berlin-2023.xlsx` | `data/raw/` | Berlin median-income table (demand calibration) |

If these are absent the pipeline logs a warning and skips the corresponding
enrichment step rather than failing.

---

## Running the simulations

Activate your environment first (e.g. `conda activate py314` or `source .venv/bin/activate`).
All runs write a timestamped folder under `results/runs/` (baseline) or
`results/strategic_runs/runs/` (strategic), indexed in `results/index.csv`.

### Baseline — Q-learning burn-in

```bash
# Default calibrated config:
python scripts/run_baseline.py

# Common overrides:
python scripts/run_baseline.py --env-config configs/env/berlin_inner_ring_calibrated.yaml \
    --T-burnin 1000000 --seed 42

# Long run, minimal disk footprint (price animation only):
python scripts/run_baseline.py --T-burnin 2000000 --lean --seed 42

# Print the calibrated λ without running a simulation:
python scripts/run_baseline.py --calibrate-only
```

Reports the Calvano collusion index Δ = (p̄ − p_Nash) / (p_Mono − p_Nash),
converged prices vs Bertrand-Nash and joint-monopoly benchmarks, and steps to
convergence.

### Strategic — LLM CEO game

Requires a Google AI Studio key for the CEO calls:

```bash
export GEMINI_API_KEY=...

# Mechanics check with NO API calls (matched control):
python scripts/run_strategic.py --T-burnin 5000 --T-game 1000 --no-ceo

# CEO run, single envelope per chain:
python scripts/run_strategic.py --T-burnin 200000 --T-game 5000 --T-CEO 100 --groups no_groups

# With a group division (richer local state):
python scripts/run_strategic.py --groups competition_only --local-sum-d
```

`--groups` selects a config from `configs/groups/` (`no_groups`,
`competition_only`, `neighbourhood_only`, `competition_neighbourhood`).

### Visualising a run

```bash
# By run directory, repo-relative path, or bare run id:
python scripts/visualize_run.py results/runs/20260625_211444_811193ee
python scripts/visualize_run.py 20260625_211444_811193ee

# Only specific artefacts:
python scripts/visualize_run.py <run_id> --only price_trajectory store_price_animation

# For a run stored outside the repo (e.g. external SSD):
python scripts/visualize_run.py --abs-path "/Volumes/Data/.../<run_id>" --format mov
```

Output is written to `<run>/figures/run_report/`.

---

## Repository layout

```text
DEDA_Spatial_Algo_Pricing/
├── src/hotelling/        # Installable package (src layout)
│   ├── core/             # City, firms, logit demand, equilibrium/Nash & monopoly solvers
│   ├── agents/           # Q-learning, deep-Q, myopic, random, LLM agents
│   ├── env/              # PettingZoo HotellingMarketEnv
│   ├── spatial/          # Data pipeline: census, OSM, boundaries, distances, assembly
│   ├── simulation/       # Simulation engine, batch runner, recorder
│   ├── envelope/         # Group/chain envelopes and division registry
│   ├── calibration/      # Structural calibration (FOC inversion, moments)
│   ├── analysis/         # Results DB (DuckDB), metrics, IRF
│   ├── viz/              # Static / interactive / run-report visualisation
│   └── llm/              # LiteLLM client, Pydantic schemas, Jinja2 prompts
├── configs/              # YAML configs (env, agents, groups, calibration, sweep, viz)
├── scripts/              # run_baseline.py, run_strategic.py, visualize_run.py, calibration & diagnostics
├── notebooks/            # GEO_00–07 data pipeline + q_table / presentation analysis
├── report/               # Figures and figure-generation scripts
├── tests/                # unit/ and integration/ tests
├── data/                 # Empty — populated by the spatial pipeline (see Data)
├── results/              # Empty run indices — populated by simulations
├── pyproject.toml        # Package metadata, deps, extras, tooling
├── requirements.txt      # Core runtime pins (extras live in pyproject.toml)
└── Makefile              # install / test / lint shortcuts
```

---

## Tests & tooling

```bash
make test            # or: pytest tests/ -v
make lint            # ruff check
make format          # ruff format
```

---

## References

- Hotelling, H. (1929). *Stability in Competition*. The Economic Journal, 39(153), 41–57.
- d'Aspremont, C., Gabszewicz, J. J., & Thisse, J.-F. (1979). *On Hotelling's "Stability in Competition"*. Econometrica.
- Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2020). *Artificial intelligence, algorithmic pricing, and collusion*. American Economic Review, 110(10), 3267–3297.
- Anderson, S., de Palma, A., & Thisse, J.-F. (1992). *Discrete Choice Theory of Product Differentiation*. MIT Press.
- Terry, J. et al. (2021). *PettingZoo: Gym for Multi-Agent Reinforcement Learning*.

---

## License

[MIT](LICENSE)
