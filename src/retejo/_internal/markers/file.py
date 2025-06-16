from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import _Marker, is_marker_factory


class _File(_Marker):
    pass


if TYPE_CHECKING:
    type File[T] = T
else:

    class File:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, _File()]


is_file = is_marker_factory(_File)
