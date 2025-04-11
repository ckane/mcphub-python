from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseAdapter(ABC):

    @classmethod
    @abstractmethod
    def from_config(cls, config_path: str) -> "BaseAdapter":
        """Create an adapter instance from a configuration file."""
        pass
