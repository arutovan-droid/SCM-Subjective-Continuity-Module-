\"\"\"
Тесты для режима Чёрного камня.
\"\"\"

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock

from core.black_stone import BlackStoneMode


@pytest_asyncio.fixture
async def reset_black_stone():
    \"\"\"Сброс состояния BlackStone перед каждым тестом.\"\"\"
    # Сохраняем оригинальные коллбеки
    old_chain = BlackStoneMode._chain_callback
    old_ite = BlackStoneMode._ite_halt_callback
    old_ecl = BlackStoneMode._ecl_silence_callback
    
    # Сбрасываем
    BlackStoneMode._chain_callback = None
    BlackStoneMode._ite_halt_callback = None
    BlackStoneMode._ecl_silence_callback = None
    BlackStoneMode._state.active = False
    
    yield
    
    # Восстанавливаем
    BlackStoneMode._chain_callback = old_chain
    BlackStoneMode._ite_halt_callback = old_ite
    BlackStoneMode._ecl_silence_callback = old_ecl


@pytest.mark.asyncio
async def test_black_stone_activation(reset_black_stone):
    \"\"\"Проверка активации режима Чёрного камня.\"\"\"
    
    # Создаём мок-коллбеки
    chain_callback = AsyncMock()
    ite_callback = AsyncMock()
    ecl_callback = AsyncMock()
    
    # Регистрируем
    BlackStoneMode.register_chain(chain_callback)
    BlackStoneMode.register_ite(ite_callback)
    BlackStoneMode.register_ecl(ecl_callback)
    
    # Активируем
    await BlackStoneMode.enter("test_reason", "scar-123")
    
    # Проверяем состояние
    assert BlackStoneMode.is_active() == True
    state = BlackStoneMode.get_state()
    assert state.reason == "test_reason"
    assert state.scar_id == "scar-123"
    
    # Проверяем вызовы коллбеков
    chain_callback.assert_awaited_once_with("BLACKSTONE:test_reason:scar-123")
    ite_callback.assert_awaited_once()
    ecl_callback.assert_awaited_once()


@pytest.mark.asyncio
async def test_black_stone_exit(reset_black_stone):
    \"\"\"Проверка выхода из режима через rebirth.\"\"\"
    
    await BlackStoneMode.enter("test", "scar-123")
    assert BlackStoneMode.is_active() == True
    
    # Выход с подписью
    await BlackStoneMode.exit_via_rebirth(b"fake_signature")
    
    assert BlackStoneMode.is_active() == False
    assert BlackStoneMode.get_state().active == False
