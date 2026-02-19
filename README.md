# Symbion Space Core v2026.1

## Онтологический аккумулятор

Замена ZK-SNARK на инкрементальные RSA-аккумуляторы для O(1) верификации цепочки шрамов.

### Быстрый старт

`ash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация genesis
python scripts/init_genesis.py

# Запуск тестов
pytest tests/
Genesis Anchor
    ↓
[Scar 1] ← proof₁
    ↓
[Scar 2] ← proof₂
    ↓
[Scar 3] ← proof₃
    ↓
... (верификация O(1))
Безопасность
RSA 2048-bit modulus

Phi(N) генерируется и хранится только в TEE

Write-Ahead Log для атомарности

Режим "Чёрного камня" при разрыве цепи
