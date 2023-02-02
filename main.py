import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai

openai.organization = '[YOUR ORGINIZATION]'
openai.api_key = '[YOUR API KEY]'
app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = {
    'todo': [{'title': 'sample todo', 'completed': False}]
}


@app.get("/gpt/{command}")
async def gpt(command: str):
    prompt = f'data is {json.dumps(db["todo"], ensure_ascii=False)} , {command}, json format'
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=256)
    try:
        db['todo'] = json.loads(response.choices[0].text.strip())
    except Exception as e:
        print(response.choices)
        raise e

    return db['todo']


@app.get("/todo")
async def get_todo():
    return db['todo']
