\"\"\"
Интерфейс к TEE (Trusted Execution Environment).
Поддерживает soft-mode для разработки.
\"\"\"

import os
import warnings
from typing import Dict, Optional


class AccumulatorEnclave:
    \"\"\"Интерфейс к TEE с fallback на soft-mode.\"\"\"
    
    def __init__(self):
        self.soft_mode = not self._check_nitro_available()
        if self.soft_mode:
            warnings.warn(
                "⚠️  TEE unavailable. Running in SOFT MODE - phi(N) exposed in RAM!",
                RuntimeWarning
            )
            
    def _check_nitro_available(self) -> bool:
        \"\"\"Проверка наличия AWS Nitro Enclaves.\"\"\"
        # В реальности: проверка /dev/nitro_enclaves
        # Для тестов возвращаем False
        return False
        
    def create_accumulator(self) -> Dict:
        \"\"\"Создаёт новый аккумулятор.\"\"\"
        if self.soft_mode:
            # Генерируем локально (НЕБЕЗОПАСНО!)
            from Crypto.PublicKey import RSA
            key = RSA.generate(2048)
            return {
                'N': key.n,
                'g': 65537,
                'phi': (key.p - 1) * (key.q - 1),
                'attestation': 'SOFT_MODE_NO_ATTESTATION'
            }
        else:
            # В реальности: вызов enclave
            return {
                'N': 12345,  # заглушка
                'g': 65537,
                'attestation': 'aws-nitro:enclave-12345678'
            }
            
    def store_genesis(self, anchor):
        \"\"\"Сохраняет genesis в TEE.\"\"\"
        if not self.soft_mode:
            # Вызов enclave для сохранения
            pass
