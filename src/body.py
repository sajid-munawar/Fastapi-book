from fastapi import FastAPI,Body


app=FastAPI()

@app.get('/')
def root():
  return {"message": "Hello World"}

@app.post("/todos")
def create_todo(title: str=Body(embed=True) ): 
  return {"title": title}
