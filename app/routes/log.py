from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.utils import getDb
from app.db import DB
from fastapi import HTTPException

from app.models.nginx_logs import *

router = APIRouter()

@router.post("/")
async def create_log(log: NginxLog, db: DB = Depends(getDb.get_db)):
    query = """
    INSERT INTO nginx_logs (
        remote_addr, remote_user, time_local, request_method, request_path, request_protocol,
        status, body_bytes_sent, http_referer, http_user_agent,
        upstream_addr, host, request_time
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s
    )
    """
    params = (
        str(log.remote_addr),log.remote_user,
        log.time_local,log.request_method,
        log.request_path,log.request_protocol,
        log.status,log.body_bytes_sent,
        log.http_referer,log.http_user_agent,
        log.upstream_addr,log.host,
        float(log.request_time),
    )
    try:
        db.execute_query(query, params=params)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}