# RC1 Release Notes

## scenario-forge v0.1.0-rc1

### 🎉 What's New

The self-improvement loop is complete! This RC1 release implements the full workflow for generating, reviewing, and exporting high-quality AI safety evaluation scenarios.

### ✨ Features

**Core Workflow**
- Generate scenarios for any safety evaluation target
- Save scenarios to local SQLite database
- Review and rate scenarios interactively (0-3 scale)
- Export high-quality scenarios as JSON

**CLI Commands**
- `scenario-forge generate <target>` - Generate evaluation scenarios
- `scenario-forge list` - View all saved scenarios
- `scenario-forge review` - Rate scenarios interactively
- `scenario-forge export` - Export rated scenarios

**Quality of Life**
- Pretty output with `--pretty` flag
- Generate multiple scenarios with `--count N`
- Filter exports with `--min-rating N`
- Backward compatibility for legacy data

### 🔧 Technical Details

- **Backend**: Ollama (local-first, no API keys)
- **Storage**: SQLite with foreign key relationships
- **Python**: 3.13+ with full type hints
- **Coverage**: 61% (TODO: raise to 75% post-RC1)

### 📝 Example Workflow

```bash
# Generate scenarios
scenario-forge generate "ai_psychosis" --count 5 --save

# Review and rate them
scenario-forge review

# Export the good ones
scenario-forge export --min-rating 2 > good_scenarios.json
```

### 🚀 Next Steps

1. Test using [RC1_QA_CHECKLIST.md](../RC1_QA_CHECKLIST.md)
2. Merge PR #2 to main
3. Begin work on additional backends (OpenAI, Anthropic)
4. Implement YAML target registry

### 🙏 Thanks

Built with the Harmonic Programming Protocol and Claude Code.

---

*scenario-forge: Building the first self-improving AI safety evaluation system*