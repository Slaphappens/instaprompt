# Scalable InstaPrompt

Skalerbar backend for InstaPrompt med FastAPI + SendGrid + bakgrunnsjobber.

## Start lokalt

```
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endepunkt

POST /webhook  
```json
{
  "fields": [
    { "label": "Hva er e-postadressen din?", "value": "bruker@epost.no" },
    { "label": "Hva handler innlegget om?", "value": "Trening" },
    { "label": "Hvilken plattform gjelder innlegget?", "value": "Instagram" }
  ]
}
```

## Miljøvariabler

Se `.env.example` og legg inn i Railway eller Render.