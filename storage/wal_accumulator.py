\"\"\"
Write-Ahead Log для атомарных операций аккумулятора.
Использует aiofiles для неблокирующей записи.
\"\"\"

import os
import asyncio
import aiofiles
from typing import Tuple, Optional
from datetime import datetime


class AccumulatorWAL:
    \"\"\"Write-Ahead Log с async/await поддержкой.\"\"\"
    
    def __init__(self, path: str):
        self.path = path
        self._cached_seq = 0
        self._cached_value = 0
        self._lock = asyncio.Lock()
        self._ensure_file()
        
    def _ensure_file(self):
        \"\"\"Создаёт файл WAL, если его нет.\"\"\"
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write("# ACCUMULATOR WAL\n")
                f.write("# seq:operation:value:timestamp:scar_id\n")
                
    async def initialize_cache(self):
        \"\"\"Инициализация кэша из WAL при старте.\"\"\"
        seq, value, _ = await self.recover()
        self._cached_seq = seq
        self._cached_value = value
        
    async def append(self, operation: str, value: int, scar_id: str) -> bool:
        \"\"\"
        Атомарная запись операции с async fsync.
        Использует asyncio.Lock для потокобезопасности.
        \"\"\"
        async with self._lock:
            timestamp = datetime.utcnow().isoformat()
            self._cached_seq += 1
            entry = f"{self._cached_seq}:{operation}:{value}:{timestamp}:{scar_id}\n"
            
            # Асинхронная запись
            async with aiofiles.open(self.path, 'a') as f:
                await f.write(entry)
                await f.flush()
                # fsync в отдельном потоке
                await asyncio.to_thread(os.fsync, f.fileno())
            
            self._cached_value = value
            return True
            
    async def recover(self) -> Tuple[int, int, Optional[str]]:
        \"\"\"
        Восстановление последнего значения и seq после сбоя.
        Возвращает (seq, value, last_scar_id)
        \"\"\"
        if not os.path.exists(self.path):
            return 0, 0, None
            
        async with aiofiles.open(self.path, 'r') as f:
            content = await f.read()
            
        lines = content.strip().split('\n')
        # Пропускаем комментарии
        data_lines = [l for l in lines if l and not l.startswith('#')]
        
        if not data_lines:
            return 0, 0, None
            
        last = data_lines[-1].strip().split(':')
        seq = int(last[0])
        value = int(last[2])
        scar_id = last[4] if len(last) > 4 else None
        
        return seq, value, scar_id
        
    @property
    def current_value(self) -> int:
        return self._cached_value
        
    @property
    def current_seq(self) -> int:
        return self._cached_seq
