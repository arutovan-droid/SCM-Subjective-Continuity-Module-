# tests/test_resonance/test_core.py
"""
Tests for Resonance Engine
"""

import pytest
import random
from datetime import datetime, timedelta
from scm.resonance.core import (
    ResonanceEngine, ResonanceType, ResonanceStrength,
    EntitySignature, ResonanceConnection
)

class TestResonanceEngine:
    """Testing resonance engine"""
    
    def test_initialization(self):
        """Test: engine initialization"""
        engine = ResonanceEngine("test_anchor_1")
        
        assert engine.anchor_hash == "test_anchor_1"
        assert len(engine.connections) == 0
        assert len(engine.known_entities) == 0
        assert engine.resonance_field == 0.0
    
    def test_calculate_signature(self):
        """Test: entity signature calculation"""
        engine = ResonanceEngine("test_anchor")
        
        emotional = {
            'joy': 0.8,
            'sadness': 0.1,
            'mood': 'happy',
            'lucidity': 0.3
        }
        memories = ['сегодня писал код', 'вчера была ссора', 'нашел решение']
        traumas = [{'emotion': 'fear'}, {'emotion': 'anger'}]
        
        sig = engine.calculate_signature(emotional, memories, traumas)
        
        assert sig.anchor_hash == "test_anchor"
        assert len(sig.emotional_profile) > 0
        assert len(sig.memory_themes) <= 3
        assert sig.trauma_count == 2
        assert sig.lucidity_level == 0.3
        assert sig.mood_baseline == 'happy'
    
    def test_resonance_calculation(self):
        """Test: resonance between entities"""
        engine = ResonanceEngine("test_1")
        
        # Создаем две разные сигнатуры
        sig1 = EntitySignature(
            anchor_hash="test_1",
            emotional_profile={'joy': 0.8, 'trust': 0.7},
            memory_themes=['code', 'achievement'],
            trauma_count=1,
            lucidity_level=0.3,
            mood_baseline='happy'
        )
        
        sig2 = EntitySignature(
            anchor_hash="test_2",
            emotional_profile={'joy': 0.7, 'trust': 0.6},
            memory_themes=['code', 'learning'],
            trauma_count=1,
            lucidity_level=0.2,
            mood_baseline='happy'
        )
        
        rtype, strength = engine.calculate_resonance(sig1, sig2)
        
        assert rtype in ResonanceType
        assert 0.0 <= strength <= 1.0
    
    def test_establish_connection(self):
        """Test: establishing resonance connection"""
        engine = ResonanceEngine("test_1")
        
        # Добавляем свою сигнатуру
        my_sig = EntitySignature(
            anchor_hash="test_1",
            emotional_profile={'joy': 0.8},
            memory_themes=['code'],
            trauma_count=0,
            lucidity_level=0.0,
            mood_baseline='calm'
        )
        engine.known_entities["test_1"] = my_sig
        
        # Сигнатура другой сущности
        other_sig = EntitySignature(
            anchor_hash="test_2",
            emotional_profile={'joy': 0.6},
            memory_themes=['code'],
            trauma_count=0,
            lucidity_level=0.0,
            mood_baseline='calm'
        )
        
        conn = engine.establish_connection("test_2", other_sig)
        
        assert conn.entity_a == "test_1"
        assert conn.entity_b == "test_2"
        assert conn.interaction_count == 1
        assert "test_2" in engine.connections
    
    def test_interaction_effects(self):
        """Test: interaction effects between entities"""
        engine = ResonanceEngine("test_1")
        
        # Настраиваем связь
        my_sig = EntitySignature("test_1", {'joy': 0.8}, ['code'], 0, 0.0, 'happy')
        engine.known_entities["test_1"] = my_sig
        
        other_sig = EntitySignature("test_2", {'joy': 0.6}, ['code'], 0, 0.0, 'happy')
        engine.establish_connection("test_2", other_sig)
        
        # Взаимодействие
        effect = engine.interact("test_2", "chat", {'valence': 0.5})
        
        assert 'resonance_type' in effect
        assert 'strength' in effect
        assert 'emotional_shift' in effect
    
    def test_find_similar_entities(self):
        """Test: finding similar entities"""
        engine = ResonanceEngine("test_1")
        
        # Добавляем несколько сущностей
        my_sig = EntitySignature("test_1", {'joy': 0.8}, ['code'], 0, 0.0, 'happy')
        engine.known_entities["test_1"] = my_sig
        
        entities = [
            ("test_2", {'joy': 0.7}, ['code'], 0),
            ("test_3", {'joy': 0.3}, ['sadness'], 2),
            ("test_4", {'joy': 0.6}, ['code', 'learning'], 1),
        ]
        
        for h, prof, themes, traumas in entities:
            sig = EntitySignature(h, prof, themes, traumas, 0.0, 'calm')
            engine.known_entities[h] = sig
        
        similar = engine.find_similar_entities(threshold=0.5)
        
        assert len(similar) >= 0
        for h, strength in similar:
            assert strength >= 0.5
    
    def test_resonance_network(self):
        """Test: resonance network info"""
        engine = ResonanceEngine("test_1")
        
        # Добавляем свою сигнатуру
        my_sig = EntitySignature("test_1", {'joy': 0.8}, ['code'], 0, 0.0, 'happy')
        engine.known_entities["test_1"] = my_sig
        
        # Создаем несколько связей
        for i in range(3):
            other_sig = EntitySignature(
                f"test_{i+2}",
                {'joy': random.uniform(0.5, 0.9)},
                ['code'],
                random.randint(0, 2),
                0.0,
                'calm'
            )
            engine.establish_connection(f"test_{i+2}", other_sig)
        
        network = engine.get_resonance_network()
        
        assert network['anchor'] == "test_1"
        assert network['connections'] == 3
        assert 'field_strength' in network
        assert 'by_type' in network
