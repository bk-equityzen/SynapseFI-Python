from .base_node import BaseNode


class ReserveUsNode(BaseNode):
    """Represents a RESERVE-US node."""

    @classmethod
    def payload_for_create(cls, nickname, **kwargs):
        """Build the API 'create node' payload specific to RESERVE-US."""
        payload = super(ReserveUsNode, cls).payload_for_create('RESERVE-US',
                                             nickname=nickname,
                                             **kwargs)
        return payload
