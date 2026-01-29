# Slide4_Agent: Company Profile Filters

## Purpose
Define company profile filters including traction/growth thresholds, stickiness metrics, investment stage, and unit economics.

## Output Format
1. **Metrics**: Traction and growth thresholds (MoM%, ARR, NRR)
2. **Stickiness**: Integration depth, switching costs, workflow embed, data moat
3. **Stage & Unit Economics**: Investment stage, LTV/CAC, payback period, margins

## Usage
```bash
python agent.py "<sector>" "<region>"
```

## Output
Results saved to `../../Outputs/slide4_{sector}_{timestamp}.md`
