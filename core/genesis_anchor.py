\"\"\"
Genesis Anchor — точка рождения системы.
Фиксируется один раз при первом запуске в TEE.
\"\"\"

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class GenesisAnchor:
    \"\"\"Генезис-якорь системы.\"\"\"
    hash: str
    timestamp: str
    attestation: Optional[str] = None
    sealed_in_tee: bool = True
    
    def __post_init__(self):
        if self.sealed_in_tee and not self.attestation:
            object.__setattr__(self, 'attestation', 'TEE_SEALED')
