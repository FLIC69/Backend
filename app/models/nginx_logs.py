from pydantic import BaseModel, HttpUrl, conint, condecimal
from typing import Optional
from datetime import datetime
from ipaddress import IPv4Address

class NginxLog(BaseModel):
    remote_addr: IPv4Address
    remote_user: Optional[str] = None
    time_local: datetime
    request_method: str
    request_path: str
    request_protocol: str
    status: conint(ge=100, le=599)
    body_bytes_sent: int
    http_referer: Optional[str] = None
    http_user_agent: Optional[str] = None
    upstream_addr: Optional[str] = None
    host: str
    request_time: condecimal(max_digits=10, decimal_places=5)
