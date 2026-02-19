\"\"\"
Режим Чёрного камня — онтологическая смерть системы.
При разрыве цепи система переходит в режим только-чтение.
\"\"\"

from typing import Optional, Callable, Awaitable
from dataclasses import dataclass
import asyncio
import logging

logger = logging.getLogger(__name__)


@dataclass
class BlackStoneState:
    \"\"\"Состояние режима Чёрного камня.\"\"\"
    active: bool = False
    reason: Optional[str] = None
    scar_id: Optional[str] = None
    timestamp: Optional[str] = None


class BlackStoneMode:
    \"\"\"
    Режим \"Чёрный камень\" — система не отвечает, только читает историю.
    Требует физического присутствия оператора для выхода.
    \"\"\"
    
    _state = BlackStoneState()
    _chain_callback: Optional[Callable[[str, str], Awaitable[None]]] = None
    _ite_halt_callback: Optional[Callable[[], Awaitable[None]]] = None
    _ecl_silence_callback: Optional[Callable[[], Awaitable[None]]] = None
    
    @classmethod
    def register_chain(cls, callback: Callable[[str, str], Awaitable[None]]):
        \"\"\"Регистрация callback для ChainRepository.\"\"\"
        cls._chain_callback = callback
        
    @classmethod
    def register_ite(cls, callback: Callable[[], Awaitable[None]]):
        \"\"\"Регистрация callback для ITE.\"\"\"
        cls._ite_halt_callback = callback
        
    @classmethod
    def register_ecl(cls, callback: Callable[[], Awaitable[None]]):
        \"\"\"Регистрация callback для ECL.\"\"\"
        cls._ecl_silence_callback = callback
        
    @classmethod
    async def enter(cls, reason: str, scar_id: str):
        \"\"\"
        Вход в режим Чёрного камня.
        Останавливает все активные процессы.
        \"\"\"
        from datetime import datetime
        
        if cls._state.active:
            logger.warning(f"Already in Black Stone mode. New reason: {reason}")
            return
            
        cls._state = BlackStoneState(
            active=True,
            reason=reason,
            scar_id=scar_id,
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.critical(f"🪨 BLACK STONE MODE ACTIVATED: {reason} (scar: {scar_id})")
        
        # 1. Остановка ITE
        if cls._ite_halt_callback:
            await cls._ite_halt_callback()
            
        # 2. Режим тишины ECL
        if cls._ecl_silence_callback:
            await cls._ecl_silence_callback()
            
        # 3. Запись в wormhole
        if cls._chain_callback:
            await cls._chain_callback(f"BLACKSTONE:{reason}:{scar_id}")
            
        # 4. Бесконечное ожидание оператора
        await cls._wait_for_operator()
        
    @classmethod
    async def _wait_for_operator(cls):
        \"\"\"Ожидание физического присутствия оператора.\"\"\"
        logger.info("⏳ Waiting for operator presence to exit Black Stone...")
        
        while cls._state.active:
            await asyncio.sleep(60)
            
    @classmethod
    async def exit_via_rebirth(cls, operator_signature: bytes):
        \"\"\"Выход из режима через ритуал перерождения.\"\"\"
        if not cls._verify_operator(operator_signature):
            logger.error("Invalid operator signature for rebirth")
            return False
            
        cls._state = BlackStoneState()
        logger.info("✨ Exited Black Stone mode via rebirth")
        return True
        
    @classmethod
    def _verify_operator(cls, signature: bytes) -> bool:
        \"\"\"Заглушка для верификации оператора.\"\"\"
        return True
        
    @classmethod
    def is_active(cls) -> bool:
        return cls._state.active
        
    @classmethod
    def get_state(cls) -> BlackStoneState:
        return cls._state
