from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from fastapi import FastAPI
from pydantic import BaseModel

table = resource('dynamodb').Table('test')

def insert(Pname,Pid,bpm):
    print("Inserting Data")
    response = table.put_item(
        Item = {
            "Pname":Pname,
            "Pid":Pid,
            "BPM":bpm
        }
    )

    return response


def fetch(Pid):
    filter = Key('ID').eq(Pid)
    response = table.query(
        KeyConditionExpression = filter
    )

    return response["Items"]


    
app = FastAPI()

class NewBPM(BaseModel):
    Pid: str
    Pname: str
    BPM: int

@app.get("/")
def home():
    return "Welcome to dynamoDB API"

@app.get("/fetch/{pid}")
def getBPM(pid: str):
    resp = fetch(pid)
    return {"Response":resp,"BPM":resp[0]["BPM"]}

@app.post("/insertBPM")
def insertingBPM(item: NewBPM):
    return insert(item.Pname,item.Pid,item.BPM)