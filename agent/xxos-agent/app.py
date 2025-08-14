from fastapi import FastAPI, Request
import uvicorn, os, uuid, json
app = FastAPI(title="xxos-agent", version="0.1-beta")
os.makedirs('/etc/xxos', exist_ok=True)
NODE_ID_FILE='/etc/xxos/node_id'
if not os.path.exists(NODE_ID_FILE):
    with open(NODE_ID_FILE,'w') as f: f.write(str(uuid.uuid4()))
@app.get('/status')
def status():
    with open(NODE_ID_FILE) as f: nid=f.read().strip()
    return {'node_id': nid, 'version':'0.1-beta', 'status':'ok'}
@app.post('/assist')
async def assist(req: Request):
    data = await req.json()
    # simple echo assistant stub - in future load local model
    return {'reply': 'Assistant (stub) received', 'payload': data}
if __name__=='__main__':
    uvicorn.run(app, host='127.0.0.1', port=5050)
