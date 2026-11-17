# Poker AI Pro — Advanced V1

A runnable 9-max Texas Hold'em cash-game **equity and simplified EV analysis** web app. The backend is FastAPI; the frontend is responsive HTML/CSS/JavaScript (no Node build required).

## Requirements
- Python 3.10+
- Internet access for first-time dependency installation

## Run locally

```bash
cd poker-ai-pro
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 . API docs: http://127.0.0.1:8000/docs .

## Test

```bash
pytest -q
```

## API

`POST /api/analyze`

```json
{
  "hero": ["As", "Kh"],
  "board": ["Qs", "Jh", "2d"],
  "ranges": ["QQ+,AKs,AKo", "random"],
  "pot": 100,
  "call": 25,
  "iterations": 2000,
  "seed": 42
}
```

The number of ranges is the number of active opponents (1–8). `hero` must contain two unique cards; `board` must contain 0, 3, 4, or 5 unique cards. Card notation: `A K Q J T 9 ... 2` + `s h d c` (spades, hearts, diamonds, clubs). Range notation supports `random`, exact pairs (`QQ`), pairs-plus (`TT+`), suited (`AKs`), offsuit (`AKo`), and same-first-rank plus (`AJs+`), comma-separated. `AK` means both suited and offsuit.

## Methodology / important limitations

- Hand evaluation: exhaustive enumeration of all 5-card combinations from the 7 cards; correct standard poker ranking, including wheel straight and split pots.
- Equity: Monte Carlo over opponent ranges and remaining board cards. Equity includes fractional split-pot outcomes. Random sampling produces statistical uncertainty.
- Opponent ranges: uniform weight over matching combinations, **not** an inferred opponent behavior model. For multiple opponents, sequential compatible-hand sampling is an approximation to joint uniform assignment, and may bias results when ranges overlap strongly.
- Call EV: `equity * (pot + call) - call` where pot **already includes the opponent's bet** but excludes hero's call. This assumes no further betting, no rake, and full equity realization; this is not a complete postflop decision solver.
- This is **not** a GTO solver, action recommendation engine, position-based solver, or automated camera reader. The 9-max UI supports up to eight opponents; it does not calculate preflop position strategy.
- Pure-Python evaluation is intended for a functional prototype, not sub-second heavy multiway simulations. Lower the iteration count if needed.
- Only use in environments whose rules permit electronic assistance. Do not expose the app publicly without HTTPS, authentication, rate limiting, and resource controls.

## Optional LAN access

On a trusted local network, change the host to `0.0.0.0` and open `http://YOUR_COMPUTER_LAN_IP:8000` on your phone. Check local firewall rules. Do not port-forward to the public internet.
