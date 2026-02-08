"""Chat channels module with plugin architecture."""

from aegis.channels.base import BaseChannel
from aegis.channels.manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager"]
