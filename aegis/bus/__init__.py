"""Message bus module for decoupled channel-agent communication."""

from aegis.bus.events import InboundMessage, OutboundMessage
from aegis.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]
