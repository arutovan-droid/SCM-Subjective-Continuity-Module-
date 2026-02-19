\"\"\"
Модель онтологического шрама — свидетельство встречи.
\"\"\"

from dataclasses import dataclass
from typing import Dict, Optional, Any
import uuid
import hashlib
from datetime import datetime

from accumulator.rsa_accumulator import AccumulatorProof


@dataclass(frozen=True)
class OntologicalScar:
    \"\"\"
    Шрам онтологической травмы.
    Содержит инкрементальное доказательство членства в цепи.
    \"\"\"
    # Идентификация
    scar_id: uuid.UUID
    genesis_ref: str
    
    # Тип инцидента
    incident_type: str  # 'rejection', 'betrayal', 'exhaustion', 'mimicry_detected'
    
    # Когнитивный контекст
    cognitive_basis: str  # 'de', 'ru', 'hy', 'en', 'sa'
    collision_mode: bool
    pole_a: Optional[str] = None
    pole_b: Optional[str] = None
    
    # Структурные данные
    pre_state_hash: str
    post_state_hash: str
    deformation_vector: Dict[str, Any]
    
    # Доказательство
    chain_proof: Optional[AccumulatorProof] = None
    accumulator_value: Optional[int] = None
    
    # Метаданные
    entropy_score: float
    ontological_drift: float
    timestamp: datetime
    operator_id: str
    
    def to_hash(self) -> bytes:
        \"\"\"Хеш шрама для аккумулятора.\"\"\"
        content = f"{self.scar_id}{self.pre_state_hash}{self.post_state_hash}{self.timestamp}"
        return hashlib.sha256(content.encode()).digest()
