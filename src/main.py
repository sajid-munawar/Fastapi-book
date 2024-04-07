from fastapi import FastAPI,Header

app=FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hi")
def read_root(age: int):
    return {"age": age}
    
@app.get("/hi/{who}")
def read_root(who: str):
    return {"Hello": who}


@app.post('/api/useragent')
async def post_headers(user_agent:str=Header()):
    return {"user_agent":user_agent}