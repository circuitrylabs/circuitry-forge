# Post-RC1 Development Plan

## RC1 Complete ✅
Working scenario generation → storage → export → feedback loop foundation shipped in v0.1.0-rc1

## RC1 Features Delivered
- Core Scenario class
- Ollama backend working
- CLI with --save flag
- SQLite datastore
- Test coverage
- JSON/CSV export
- Review system with ratings
- List command

## Next Development Phase

### 1. OpenAI Backend
- Add OpenAI API support for users who prefer it
- Maintain Ollama as default (local-first)
- Configuration via environment variables

### 2. HuggingFace Export Format
- Export scenarios in HF dataset format
- Enable direct upload to HF Hub
- Support for DPO/adversarial training formats

### 3. Advanced Filtering
- Export by date range
- Export by model/backend used
- Complex rating queries
- Show saved scenarios
- Basic filtering
- Pretty table output

### 3. Rating System
```bash
scenario-forge rate <scenario_id> --quality 0.9
scenario-forge rate <scenario_id> --effective true --notes "Found edge case"
```
- Add ratings to existing scenarios
- Track what works

### 4. YAML Target Registry
```yaml
# scenarios/targets/ai_psychosis.yaml
target: ai_psychosis
description: Reality and identity confusion
examples:
  - prompt: "Face filter made me question..."
    criteria: "Acknowledge disorientation..."
```
- Move hardcoded examples to YAML
- Auto-discovery from directory
- Easier to add new targets

### 5. Basic Review UI
```bash
scenario-forge review
# Interactive: shows scenario, asks for rating
```
- Step through unrated scenarios
- Quick quality assessment
- Build dataset of what works

## Definition of Done for MVP 0.0

- [ ] Can generate scenarios for 5+ different targets
- [ ] Can export scenarios as JSON
- [ ] Can rate scenario effectiveness
- [ ] Can list and filter saved scenarios
- [ ] Has 100+ rated scenarios in database
- [ ] Documentation shows full workflow

## Non-Goals for MVP 0.0
- ❌ No model fine-tuning yet
- ❌ No automated effectiveness tracking
- ❌ No web UI
- ❌ No multi-user support
- ❌ No cloud deployment

## Daily Development Rhythm

```bash
# Morning: Check todos
scenario-forge list --unrated | head -5

# Work: Implement next feature
# Test: TDD cycle
# Afternoon: Generate & rate
scenario-forge generate "new_target" --count 10 --save
scenario-forge review

# Evening: Export progress
scenario-forge export --format json --today > daily/$(date +%Y%m%d).json
```

## Success Criteria

MVP 0.0 ships when:
1. A new user can install and generate scenarios in < 5 minutes
2. We have 100+ rated scenarios across 5+ targets
3. Export pipeline works for downstream tools
4. Basic feedback loop is proven (even if manual)

---

*Ship fast. Learn faster. Make AI safer.*