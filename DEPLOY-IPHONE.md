# iPhone Safari deployment (GitHub + Render)

1. Register for a GitHub account at https://github.com/signup and verify your email.
2. Create a new **private** repository called `poker-ai-pro-v1` (do not add a README).
3. Extract this ZIP in the iPhone Files app. The repository root must contain `backend/`, `frontend/`, `requirements.txt`, and `render.yaml`. GitHub's web UI does not reliably upload directories on mobile; if you cannot upload the extracted folder, use a computer or GitHub Codespaces to copy files while retaining paths.
4. Upload files to the repository, preserving folder structure.
5. Create a Render account at https://dashboard.render.com/ using GitHub login. Authorize access to the repository.
6. Choose New > Blueprint and select this repository, or New > Web Service with: Python runtime; build `pip install -r requirements.txt`; start `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
7. After deploy finishes, open the `https://...onrender.com` URL in Safari. Use Share > Add to Home Screen.

Important: The service has no authentication. Use only for non-sensitive demonstrations until authentication and rate limits are added. Free service availability, pricing, and sleep behavior are subject to Render's current policies. This tool is a poker equity and simplified EV calculator, not a GTO solver.
