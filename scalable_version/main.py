from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from tasks import process_request
import uvicorn

app = FastAPI()

class WebhookPayload(BaseModel):
    fields: list

@app.post("/webhook")
async def webhook(data: WebhookPayload, background_tasks: BackgroundTasks):
    field_map = {f['label']: f['value'] for f in data.fields}
    email = field_map.get("Hva er e-postadressen din?")
    tema = field_map.get("Hva handler innlegget om?")
    plattform = field_map.get("Hvilken plattform gjelder innlegget?")

    background_tasks.add_task(process_request, email, tema, plattform)
    return {"status": "queued"}