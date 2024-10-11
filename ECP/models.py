from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class User:
    id: int
    last_activity: datetime
    name: str
    role: str
    connections: List[str]
    password: str  # Поле password

@dataclass
class Login:
    id: int
    name: str
    login_time: datetime
    ip_address: str
    status: str  # Новое поле status
