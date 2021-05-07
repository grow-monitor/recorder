from typing import Any, Literal, TypedDict, Union

from faunadb.objects import FaunaTime

QoS = Literal[0, 1, 2]
Ref = TypedDict("Ref", {"@ref": str})
SoilData = TypedDict("SoilData", {"timestamp": FaunaTime, "value": float, "topic": str})
Data = Union[SoilData]
QueryResult = TypedDict(
    "QueryResult", {"ref": Ref, "class": Ref, "ts": int, "data": Data}
)
