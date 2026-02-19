# scm/cli/resonance.py
"""
CLI commands for testing Resonance Engine
"""

import click
import random
from datetime import datetime
from scm.resonance.core import ResonanceEngine, EntitySignature

@click.group()
def resonance():
    """Commands for inter-entity resonance"""
    pass

@resonance.command()
@click.argument('anchor')
def init(anchor):
    """Initialize resonance engine"""
    engine = ResonanceEngine(anchor)
    click.echo(f"🔄 Resonance engine initialized for {anchor}")
    click.echo(f"   Field strength: {engine.resonance_field}")

@resonance.command()
@click.argument('anchor')
@click.argument('other')
@click.option('--joy', default=0.5, type=float)
@click.option('--trust', default=0.5, type=float)
def connect(anchor, other, joy, trust):
    """Establish connection with another entity"""
    engine = ResonanceEngine(anchor)
    
    # Добавляем свою сигнатуру
    my_sig = EntitySignature(
        anchor_hash=anchor,
        emotional_profile={'joy': joy, 'trust': trust},
        memory_themes=['code', 'learning'],
        trauma_count=random.randint(0, 3),
        lucidity_level=random.random(),
        mood_baseline='calm'
    )
    engine.known_entities[anchor] = my_sig
    
    # Сигнатура другой сущности
    other_sig = EntitySignature(
        anchor_hash=other,
        emotional_profile={'joy': random.uniform(0.3, 0.9), 
                          'trust': random.uniform(0.3, 0.9)},
        memory_themes=['code', 'problems'],
        trauma_count=random.randint(0, 2),
        lucidity_level=random.random(),
        mood_baseline='neutral'
    )
    
    conn = engine.establish_connection(other, other_sig)
    
    click.echo(f"\n🔄 CONNECTION ESTABLISHED")
    click.echo("=" * 40)
    click.echo(f"Between: {anchor} ↔ {other}")
    click.echo(f"Type: {conn.resonance_type.value}")
    click.echo(f"Strength: {conn.strength:.2%}")
    click.echo(f"Formed: {conn.formed_at}")

@resonance.command()
@click.argument('anchor')
@click.argument('other')
def interact(anchor, other):
    """Simulate interaction with connected entity"""
    engine = ResonanceEngine(anchor)
    
    if other not in engine.connections:
        click.echo(f"❌ No connection with {other}")
        return
    
    effect = engine.interact(
        other,
        "communication",
        {'valence': random.uniform(-1, 1)}
    )
    
    click.echo(f"\n💬 INTERACTION EFFECT")
    click.echo("=" * 40)
    click.echo(f"With: {other}")
    click.echo(f"Resonance: {effect['resonance_type']}")
    click.echo(f"Strength: {effect['strength']:.2%}")
    
    if effect['emotional_shift'] != 0:
        direction = "positive" if effect['emotional_shift'] > 0 else "negative"
        click.echo(f"Emotional shift: {direction} ({effect['emotional_shift']:.2f})")
    
    if effect.get('contagion'):
        click.echo("🦠 Emotional contagion!")
    
    if effect['sync_level'] > 0:
        click.echo(f"Sync level: {effect['sync_level']:.2%}")

@resonance.command()
@click.argument('anchor')
def network(anchor):
    """Show resonance network"""
    engine = ResonanceEngine(anchor)
    network = engine.get_resonance_network()
    
    click.echo(f"\n🌐 RESONANCE NETWORK for {anchor}")
    click.echo("=" * 40)
    click.echo(f"Field strength: {network['field_strength']:.2%}")
    click.echo(f"Total connections: {network['connections']}")
    
    strongest = network['strongest_connection']
    if strongest[0]:
        click.echo(f"Strongest connection: {strongest[0]} ({strongest[1]:.2%})")
    
    click.echo(f"\n📊 By type:")
    for rtype, count in network['by_type'].items():
        if count > 0:
            click.echo(f"  {rtype:12}: {count}")

@resonance.command()
@click.argument('anchor')
def similar(anchor):
    """Find similar entities"""
    engine = ResonanceEngine(anchor)
    
    # Добавляем тестовые сущности если их нет
    if anchor not in engine.known_entities:
        my_sig = EntitySignature(
            anchor_hash=anchor,
            emotional_profile={'joy': 0.7, 'trust': 0.6},
            memory_themes=['code', 'learning'],
            trauma_count=1,
            lucidity_level=0.3,
            mood_baseline='happy'
        )
        engine.known_entities[anchor] = my_sig
    
    similar = engine.find_similar_entities(threshold=0.4)
    
    if not similar:
        click.echo("🔍 No similar entities found")
        return
    
    click.echo(f"\n🔍 SIMILAR ENTITIES")
    click.echo("=" * 40)
    for entity, strength in similar:
        click.echo(f"{entity:20} similarity: {strength:.2%}")

@resonance.command()
@click.argument('anchor')
@click.option('--count', default=3, help='Number of entities to simulate')
def simulate(anchor, count):
    """Simulate a network of entities"""
    engine = ResonanceEngine(anchor)
    
    # Создаем свою сигнатуру
    my_sig = EntitySignature(
        anchor_hash=anchor,
        emotional_profile={'joy': 0.8, 'trust': 0.7},
        memory_themes=['code', 'creation'],
        trauma_count=0,
        lucidity_level=0.5,
        mood_baseline='happy'
    )
    engine.known_entities[anchor] = my_sig
    
    click.echo(f"\n🌐 SIMULATING NETWORK with {count} entities")
    click.echo("=" * 50)
    
    # Создаем другие сущности
    for i in range(count):
        other = f"entity_{i+1}"
        
        # Случайная сигнатура
        other_sig = EntitySignature(
            anchor_hash=other,
            emotional_profile={
                'joy': random.uniform(0.2, 0.9),
                'trust': random.uniform(0.2, 0.9),
                'anger': random.uniform(0.0, 0.5)
            },
            memory_themes=random.sample(['code', 'learning', 'conflict', 'loss'], 2),
            trauma_count=random.randint(0, 3),
            lucidity_level=random.random(),
            mood_baseline=random.choice(['happy', 'sad', 'calm'])
        )
        
        conn = engine.establish_connection(other, other_sig)
        
        # Эмодзи для типа связи
        type_emoji = {
            'sympathy': '❤️',
            'antipathy': '💢',
            'mimicry': '🦜',
            'sync': '🔄',
            'contagion': '🦠',
            'block': '🚫'
        }
        
        emoji = type_emoji.get(conn.resonance_type.value, '🔗')
        
        click.echo(f"{emoji} {other:12} | "
                  f"{conn.resonance_type.value:12} | "
                  f"strength: {conn.strength:.0%} | "
                  f"traumas: {other_sig.trauma_count}")
    
    network = engine.get_resonance_network()
    click.echo(f"\n📊 Network stats:")
    click.echo(f"   Field strength: {network['field_strength']:.2%}")
