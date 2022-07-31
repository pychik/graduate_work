from dataclasses import dataclass
from typing import Dict


@dataclass
class HTTPResponse:
    body: Dict
    headers: Dict
    status: int
