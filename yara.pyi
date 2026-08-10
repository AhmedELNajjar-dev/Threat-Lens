"""
Type stubs for yara-python binary module.
"""
from typing import Any, Dict, List, Optional

class Match:
    rule: str
    namespace: str
    tags: List[str]
    meta: Dict[str, Any]
    strings: List[Any]

class Rules:
    def match(
        self,
        filepath: Optional[str] = ...,
        pid: Optional[int] = ...,
        data: Optional[bytes] = ...,
        timeout: Optional[int] = ...,
        **kwargs: Any
    ) -> List[Match]: ...

def compile(
    filepath: Optional[str] = ...,
    filepaths: Optional[Dict[str, str]] = ...,
    source: Optional[str] = ...,
    sources: Optional[Dict[str, str]] = ...,
    **kwargs: Any
) -> Rules: ...
