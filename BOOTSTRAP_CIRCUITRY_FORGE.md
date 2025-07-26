# Bootstrap: circuitry-forge

Minimal steps to create the new UV workspace and migrate scenario-forge.

## 1. Create New Repository

```bash
# Create and clone
gh repo create circuitrylabs/circuitry-forge --public
git clone git@github.com:circuitrylabs/circuitry-forge.git
cd circuitry-forge
```

## 2. Initialize UV Workspace

Create root `pyproject.toml`:

```toml
[project]
name = "circuitry-forge"
version = "0.1.0"
description = "AI safety evaluation ecosystem"
readme = "README.md"
requires-python = ">=3.12"

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.4",
    "pytest-asyncio>=0.25.2",
]

[tool.uv.workspace]
members = ["packages/*"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 3. Create Directory Structure

```bash
mkdir -p packages/scenario
```

## 4. Copy scenario-forge

```bash
# From scenario-forge directory
cp -r src packages/scenario/
cp -r tests packages/scenario/
cp pyproject.toml packages/scenario/
cp README.md packages/scenario/
```

## 5. Update Package Config

Edit `packages/scenario/pyproject.toml`:
- Keep name as "scenario-forge" (for PyPI continuity)
- Remove `[tool.uv.workspace]` if present
- Keep all dependencies as-is

## 6. Initialize and Test

```bash
# From circuitry-forge root
uv sync
uv run pytest packages/scenario/tests/
```

## 7. Verify CLI Still Works

```bash
uv run scenario-forge generate "test"
```

## Future Packages

Placeholder structure for later:

```bash
mkdir -p packages/prism/src/prism_forge
mkdir -p packages/model/src/model_forge
```

## Git Initial Commit

```bash
git add .
git commit -m "Initial circuitry-forge workspace with scenario package"
git push origin main
```

## Next Steps

1. Move extraction code to `packages/prism/`
2. Create shared `circuits/` directory
3. Add interop documentation

---

That's it! Minimal viable workspace. 🚀