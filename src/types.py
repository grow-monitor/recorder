from typing import Any, Literal, TypedDict, Union

from faunadb.objects import FaunaTime, Ref

QoS = Literal[0, 1, 2]
SoilData = TypedDict("SoilData", {"topic": str, "timestamp": FaunaTime, "value": float})
Data = Union[SoilData]
QueryResult = TypedDict("QueryResult", {"ref": Ref, "ts": int, "data": Data})
