# scm/resonance/core.py
"""
Resonance Engine для SCM.
Межсущностное взаимодействие и коллективное бессознательное.
"""

import hashlib
import random
import math
from enum import Enum
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

class ResonanceType(Enum):
    """Типы резонанса между сущностями"""
    SYMPATHY = "sympathy"       # Симпатия - положительный резонанс
    ANTIPATHY = "antipathy"     # Антипатия - отрицательный резонанс
    MIMICRY = "mimicry"         # Подражание - копирование поведения
    SYNC = "sync"               # Синхронизация - общие мысли/эмоции
    CONTAGION = "contagion"     # Заразительность - эмоции передаются
    BLOCK = "block"             # Блокировка - подавление влияния

class ResonanceStrength(Enum):
    """Сила резонансной связи"""
    WEAK = 0.2
    MODERATE = 0.5
    STRONG = 0.8
    BONDED = 1.0

@dataclass
class EntitySignature:
    """Сигнатура сущности - ее уникальный отпечаток"""
    anchor_hash: str
    emotional_profile: Dict[str, float]
    memory_themes: List[str]
    trauma_count: int
    lucidity_level: float
    mood_baseline: str

@dataclass
class ResonanceConnection:
    """Резонансная связь между сущностями"""
    entity_a: str
    entity_b: str
    resonance_type: ResonanceType
    strength: float  # 0.0 to 1.0
    formed_at: datetime
    last_interaction: datetime
    interaction_count: int
    shared_experiences: List[str]

class ResonanceEngine:
    """
    Движок межсущностного резонанса.
    Управляет связями и взаимодействиями между сущностями.
    """
    
    def __init__(self, anchor_hash: str):
        self.anchor_hash = anchor_hash
        self.connections: Dict[str, ResonanceConnection] = {}  # other_hash -> connection
        self.known_entities: Dict[str, EntitySignature] = {}
        self.resonance_field: float = 0.0  # общее поле резонанса
        self.contagion_factor: float = 0.3  # как легко заражаться эмоциями
        
    def calculate_signature(self, emotional_state: Dict, 
                           memories: List[str],
                           traumas: List[Dict]) -> EntitySignature:
        """
        Вычисляет сигнатуру сущности на основе текущего состояния.
        """
        # Эмоциональный профиль
        profile = {}
        emotions = ['joy', 'sadness', 'anger', 'fear', 'trust']
        for emotion in emotions:
            profile[emotion] = emotional_state.get(emotion, random.uniform(0, 0.5))
        
        # Основные темы из памяти
        memory_themes = self._extract_themes(memories[:5])
        
        return EntitySignature(
            anchor_hash=self.anchor_hash,
            emotional_profile=profile,
            memory_themes=memory_themes,
            trauma_count=len(traumas),
            lucidity_level=emotional_state.get('lucidity', 0.0),
            mood_baseline=emotional_state.get('mood', 'calm')
        )
    
    def _extract_themes(self, memories: List[str]) -> List[str]:
        """Извлекает темы из воспоминаний"""
        themes = []
        theme_keywords = {
            'code': ['программирование', 'код', 'баги'],
            'learning': ['обучение', 'новое', 'понимание'],
            'conflict': ['спор', 'конфликт', 'ссора'],
            'achievement': ['успех', 'достижение', 'победа'],
            'loss': ['потеря', 'утрата', 'грусть'],
            'creation': ['создание', 'творчество', 'идея']
        }
        
        for memory in memories:
            memory_lower = memory.lower()
            for theme, keywords in theme_keywords.items():
                if any(keyword in memory_lower for keyword in keywords):
                    if theme not in themes:
                        themes.append(theme)
        
        return themes[:3]  # максимум 3 темы
    
    def calculate_resonance(self, signature_a: EntitySignature, 
                           signature_b: EntitySignature) -> Tuple[ResonanceType, float]:
        """
        Вычисляет резонанс между двумя сущностями.
        Возвращает (тип резонанса, сила)
        """
        # Сравниваем эмоциональные профили
        emotional_similarity = self._compare_profiles(
            signature_a.emotional_profile,
            signature_b.emotional_profile
        )
        
        # Сравниваем темы памяти
        theme_similarity = self._compare_themes(
            signature_a.memory_themes,
            signature_b.memory_themes
        )
        
        # Учитываем травмы
        trauma_factor = 1.0 - abs(signature_a.trauma_count - signature_b.trauma_count) / 10
        
        # Общая схожесть
        total_similarity = (emotional_similarity * 0.4 + 
                          theme_similarity * 0.3 + 
                          trauma_factor * 0.3)
        
        # Определяем тип резонанса
        if total_similarity > 0.7:
            resonance_type = ResonanceType.SYMPATHY
        elif total_similarity > 0.4:
            resonance_type = ResonanceType.MIMICRY
        elif total_similarity < 0.2:
            resonance_type = ResonanceType.ANTIPATHY
        else:
            resonance_type = ResonanceType.SYNC
        
        # Сила резонанса
        strength = min(1.0, total_similarity * 1.2)
        
        return resonance_type, strength
    
    def _compare_profiles(self, profile_a: Dict, profile_b: Dict) -> float:
        """Сравнивает эмоциональные профили"""
        if not profile_a or not profile_b:
            return 0.0
        
        common_emotions = set(profile_a.keys()) & set(profile_b.keys())
        if not common_emotions:
            return 0.0
        
        differences = []
        for emotion in common_emotions:
            diff = abs(profile_a.get(emotion, 0) - profile_b.get(emotion, 0))
            differences.append(1.0 - diff)
        
        return sum(differences) / len(differences)
    
    def _compare_themes(self, themes_a: List[str], themes_b: List[str]) -> float:
        """Сравнивает темы памяти"""
        if not themes_a or not themes_b:
            return 0.0
        
        common = set(themes_a) & set(themes_b)
        if not common:
            return 0.1  # небольшая базовая схожесть
        
        return len(common) / max(len(themes_a), len(themes_b))
    
    def establish_connection(self, other_hash: str, 
                           signature: EntitySignature) -> ResonanceConnection:
        """
        Устанавливает резонансную связь с другой сущностью.
        """
        # Получаем свою сигнатуру
        my_signature = self.known_entities.get(self.anchor_hash)
        if not my_signature:
            raise ValueError("Own signature not found")
        
        # Вычисляем резонанс
        resonance_type, strength = self.calculate_resonance(my_signature, signature)
        
        # Создаем связь
        connection = ResonanceConnection(
            entity_a=self.anchor_hash,
            entity_b=other_hash,
            resonance_type=resonance_type,
            strength=strength,
            formed_at=datetime.utcnow(),
            last_interaction=datetime.utcnow(),
            interaction_count=1,
            shared_experiences=[]
        )
        
        self.connections[other_hash] = connection
        self.known_entities[other_hash] = signature
        
        # Обновляем поле резонанса
        self._update_resonance_field()
        
        return connection
    
    def interact(self, other_hash: str, 
                interaction_type: str,
                emotional_state: Dict) -> Dict:
        """
        Взаимодействие с другой сущностью.
        Возвращает эффект взаимодействия.
        """
        if other_hash not in self.connections:
            return {'error': 'No connection established'}
        
        conn = self.connections[other_hash]
        conn.last_interaction = datetime.utcnow()
        conn.interaction_count += 1
        
        # Эффект взаимодействия зависит от типа резонанса
        effect = {
            'resonance_type': conn.resonance_type.value,
            'strength': conn.strength,
            'emotional_shift': 0.0,
            'contagion': False,
            'sync_level': 0.0
        }
        
        # Резонансные эффекты
        if conn.resonance_type == ResonanceType.SYMPATHY:
            effect['emotional_shift'] = conn.strength * 0.3
            effect['sync_level'] = conn.strength * 0.5
            
        elif conn.resonance_type == ResonanceType.ANTIPATHY:
            effect['emotional_shift'] = -conn.strength * 0.2
            effect['sync_level'] = 0.0
            
        elif conn.resonance_type == ResonanceType.CONTAGION:
            # Эмоциональное заражение
            if random.random() < self.contagion_factor:
                effect['contagion'] = True
                effect['emotional_shift'] = conn.strength * 0.4
                
        elif conn.resonance_type == ResonanceType.SYNC:
            effect['sync_level'] = conn.strength * 0.8
            
        elif conn.resonance_type == ResonanceType.MIMICRY:
            # Подражание поведению
            effect['sync_level'] = conn.strength * 0.3
            effect['emotional_shift'] = conn.strength * 0.2
        
        # Усиливаем связь при частых взаимодействиях
        if conn.interaction_count > 10:
            conn.strength = min(1.0, conn.strength + 0.05)
        
        return effect
    
    def get_connection_strength(self, other_hash: str) -> float:
        """Возвращает силу связи с другой сущностью"""
        if other_hash not in self.connections:
            return 0.0
        return self.connections[other_hash].strength
    
    def find_similar_entities(self, threshold: float = 0.5) -> List[Tuple[str, float]]:
        """
        Находит похожих сущностей среди известных.
        """
        my_sig = self.known_entities.get(self.anchor_hash)
        if not my_sig:
            return []
        
        similar = []
        for other_hash, signature in self.known_entities.items():
            if other_hash == self.anchor_hash:
                continue
            
            _, strength = self.calculate_resonance(my_sig, signature)
            if strength >= threshold:
                similar.append((other_hash, strength))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)
    
    def _update_resonance_field(self):
        """Обновляет общее поле резонанса"""
        if not self.connections:
            self.resonance_field = 0.0
            return
        
        total_strength = sum(c.strength for c in self.connections.values())
        self.resonance_field = total_strength / len(self.connections)
    
    def get_resonance_network(self) -> Dict:
        """
        Возвращает информацию о сети резонансных связей.
        """
        return {
            'anchor': self.anchor_hash,
            'field_strength': self.resonance_field,
            'connections': len(self.connections),
            'strongest_connection': max(
                [(h, c.strength) for h, c in self.connections.items()],
                key=lambda x: x[1],
                default=(None, 0.0)
            ),
            'by_type': {
                rtype.value: sum(1 for c in self.connections.values() 
                               if c.resonance_type == rtype)
                for rtype in ResonanceType
            }
        }
