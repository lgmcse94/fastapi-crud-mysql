from typing import Optional

import uvicorn
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from starlette.requests import Request
from starlette.responses import JSONResponse

import request_body_mapping as req_mapping
from db import Session, models
from const import PREFIX_URL

import create_tables
create_tables.create() #This will create the tables automatically, first create database(create the schema within db if exists.)

app = FastAPI(debug=True)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# alldbs
@app.post(PREFIX_URL + "/alldbs")
async def create_alldbs(request_context: Request, alldbs: req_mapping.AllDBs, response: Response):
    session = None
    try:
        session = Session()
        db_type = alldbs.db_type
        db_name = alldbs.db_name
        db_endpoint = alldbs.db_endpoint
        password = alldbs.password
        db_ = models.AllDBs(db_type=db_type, db_name=db_name, db_endpoint=db_endpoint, password=password)
        session.add(db_)
        session.commit()
        session.refresh(db_)
        response.status_code = status.HTTP_201_CREATED
        return {"Status":"Success","data":db_}
    except Exception as err:
        print("Exception:", err)
        return JSONResponse({"error_code": "create_alldbs_api_failed",
                             "message": "Technical Error occurred while storing the all dbs info"}, status_code=500)
    finally:
        if session:
            session.close()

@app.get(PREFIX_URL + "/alldbs/{id}")
async def get_alldbs(request_context: Request, id):
    session = None
    try:
        session = Session()
        result_set = session.query(models.AllDBs).filter(models.AllDBs.id == id)
        result_set_count = result_set.count()
        result_set = result_set.all()
        if result_set_count > 0:
            return result_set
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        print("Exception:", err)
        return JSONResponse({"error_code": "get_alldbs_by_id_api_failed",
                             "message": "Technical Error occurred while retrieving the all dbs info"}, status_code=500)
    finally:
        if session:
            session.close()

@app.get(PREFIX_URL + "/alldbs")
async def get_alldbs_all(request_context: Request, page: Optional[int] = 0, size: Optional[int] = 20):
    session = None
    try:
        if page != 0:
            # index starts from zero,req page is 1 means index 0.
            page = page - 1
        session = Session()
        result_set = session.query(models.AllDBs).order_by(models.AllDBs.id).offset(
            page * size).limit(size).all()
        return {"alldbs": result_set}
    except Exception as err:
        print("Exception:", err)
        return JSONResponse({"error_code": "get_alldbs_api_failed",
                             "message": "Technical Error occurred while retrieving the all dbs info"}, status_code=500)
    finally:
        if session:
            session.close()

@app.put(PREFIX_URL + "/alldbs/{id}")
async def update_alldbs(request_context: Request, id, alldbs_update: req_mapping.UpdateStatus):
    session = None
    try:
        session = Session()
        result_set = session.query(models.AllDBs).filter(models.AllDBs.id == id)
        result_set_count = result_set.count()
        result_set = result_set.all()
        if result_set_count > 0:
            for db_ in result_set:
                db_.is_active = alldbs_update.status
                session.commit()
                session.refresh(db_)
            return result_set
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        print("Exception:", err)
        return JSONResponse({"error_code": "update_alldbs_api_failed",
                             "message": "Technical Error occurred while updating the alldbs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.delete(PREFIX_URL + "/alldbs/{id}")
async def delete_alldbs(request_context: Request, id):
    session = None
    try:
        session = Session()
        result_set = session.query(models.AllDBs).filter(models.AllDBs.id == id)
        if result_set.count() > 0:
            result_set.delete()
            session.commit()
            return JSONResponse({"detail": "success"})
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        print("Exception:", err)
        return JSONResponse({"error_code": "delete_alldbs_api_failed",
                             "message": "Technical Error occurred while deleting the alldbs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.delete(PREFIX_URL + "/alldbs")
async def delete_alldbs(request_context: Request):
    session = None
    try:
        session = Session()
        session.query(models.AllDBs).delete()
        session.commit()
        return JSONResponse({"detail": "success"})
    except Exception as err:
        print("Exception:", err)
        return JSONResponse({"error_code": "delete_alldbs_api_failed",
                             "message": "Technical Error occurred while deleting the alldbs"}, status_code=500)
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8200, log_level="debug")