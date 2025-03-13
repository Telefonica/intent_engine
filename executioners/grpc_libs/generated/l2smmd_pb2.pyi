from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Provider(_message.Message):
    __slots__ = ("name", "domain")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    name: str
    domain: str
    def __init__(self, name: _Optional[str] = ..., domain: _Optional[str] = ...) -> None: ...

class L2Network(_message.Message):
    __slots__ = ("name", "provider", "pod_cidr")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    POD_CIDR_FIELD_NUMBER: _ClassVar[int]
    name: str
    provider: Provider
    pod_cidr: str
    def __init__(self, name: _Optional[str] = ..., provider: _Optional[_Union[Provider, _Mapping]] = ..., pod_cidr: _Optional[str] = ...) -> None: ...

class CreateNetworkRequest(_message.Message):
    __slots__ = ("network",)
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    network: L2Network
    def __init__(self, network: _Optional[_Union[L2Network, _Mapping]] = ...) -> None: ...

class DeleteNetworkRequest(_message.Message):
    __slots__ = ("network_name",)
    NETWORK_NAME_FIELD_NUMBER: _ClassVar[int]
    network_name: str
    def __init__(self, network_name: _Optional[str] = ...) -> None: ...

class Cluster(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Link(_message.Message):
    __slots__ = ("endpointA", "endpointB")
    ENDPOINTA_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTB_FIELD_NUMBER: _ClassVar[int]
    endpointA: str
    endpointB: str
    def __init__(self, endpointA: _Optional[str] = ..., endpointB: _Optional[str] = ...) -> None: ...

class OverlayTopology(_message.Message):
    __slots__ = ("provider", "clusters", "links")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    provider: Provider
    clusters: _containers.RepeatedCompositeFieldContainer[Cluster]
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, provider: _Optional[_Union[Provider, _Mapping]] = ..., clusters: _Optional[_Iterable[_Union[Cluster, _Mapping]]] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class CreateOverlayRequest(_message.Message):
    __slots__ = ("overlay",)
    OVERLAY_FIELD_NUMBER: _ClassVar[int]
    overlay: OverlayTopology
    def __init__(self, overlay: _Optional[_Union[OverlayTopology, _Mapping]] = ...) -> None: ...

class AddClusterRequest(_message.Message):
    __slots__ = ("provider_name", "provider_domain", "overlay_name", "cluster")
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    OVERLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    provider_name: str
    provider_domain: str
    overlay_name: str
    cluster: Cluster
    def __init__(self, provider_name: _Optional[str] = ..., provider_domain: _Optional[str] = ..., overlay_name: _Optional[str] = ..., cluster: _Optional[_Union[Cluster, _Mapping]] = ...) -> None: ...

class RemoveClusterRequest(_message.Message):
    __slots__ = ("provider_name", "provider_domain", "overlay_name", "cluster_name")
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    OVERLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    provider_name: str
    provider_domain: str
    overlay_name: str
    cluster_name: str
    def __init__(self, provider_name: _Optional[str] = ..., provider_domain: _Optional[str] = ..., overlay_name: _Optional[str] = ..., cluster_name: _Optional[str] = ...) -> None: ...

class DeleteOverlayRequest(_message.Message):
    __slots__ = ("provider_name", "provider_domain", "overlay_name")
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    OVERLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    provider_name: str
    provider_domain: str
    overlay_name: str
    def __init__(self, provider_name: _Optional[str] = ..., provider_domain: _Optional[str] = ..., overlay_name: _Optional[str] = ...) -> None: ...

class CreateNetworkResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class DeleteNetworkResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CreateOverlayResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class AddClusterResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class RemoveClusterResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class DeleteOverlayResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
