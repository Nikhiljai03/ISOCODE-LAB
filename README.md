# ARANYA

Illustrative direct-booking and reservations intelligence platform for a premium coffee-estate retreat.

## Backend setup

```powershell
cd apps/api
python -m pip install -e ".[test]"
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/aranya"
uvicorn aranya_api.main:app --reload
```

The backend domain is implemented first. Frontend implementation intentionally follows backend review and migration validation.
