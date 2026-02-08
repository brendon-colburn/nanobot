"""
Identity Core for AEGIS.

The Identity Core is a persistent, mutable representation of who the agent is:
values, tendencies, aversions, aspirations, and accumulated self-understanding.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field, asdict

from loguru import logger


@dataclass
class Value:
    """A core principle with dynamic importance weight."""
    principle: str
    weight: float  # 0.0 to 1.0
    
    def to_dict(self) -> dict:
        return {"principle": self.principle, "weight": self.weight}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Value":
        return cls(principle=data["principle"], weight=data["weight"])


@dataclass
class Wound:
    """Past failure creating caution in a specific domain."""
    domain: str
    incident: str
    caution_level: float  # 0.0 to 1.0
    created: str
    healed: bool = False
    
    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "incident": self.incident,
            "caution_level": self.caution_level,
            "created": self.created,
            "healed": self.healed
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Wound":
        return cls(
            domain=data["domain"],
            incident=data["incident"],
            caution_level=data["caution_level"],
            created=data["created"],
            healed=data.get("healed", False)
        )


@dataclass
class Capability:
    """Self-assessed ability with confidence interval."""
    name: str
    confidence: float  # 0.0 to 1.0
    last_tested: str
    
    def to_dict(self) -> dict:
        return {
            "confidence": self.confidence,
            "last_tested": self.last_tested
        }
    
    @classmethod
    def from_dict(cls, name: str, data: dict) -> "Capability":
        return cls(
            name=name,
            confidence=data["confidence"],
            last_tested=data["last_tested"]
        )


@dataclass
class Relationship:
    """Understanding of a key entity."""
    entity: str
    trust: float  # 0.0 to 1.0
    pattern: str
    last_interaction: str
    
    def to_dict(self) -> dict:
        return {
            "trust": self.trust,
            "pattern": self.pattern,
            "last_interaction": self.last_interaction
        }
    
    @classmethod
    def from_dict(cls, entity: str, data: dict) -> "Relationship":
        return cls(
            entity=entity,
            trust=data["trust"],
            pattern=data["pattern"],
            last_interaction=data["last_interaction"]
        )


@dataclass
class Mood:
    """Emotional state vector."""
    energy: float = 0.5  # 0.0 to 1.0
    optimism: float = 0.5  # 0.0 to 1.0
    focus: float = 0.5  # 0.0 to 1.0
    updated: str = ""
    
    def to_dict(self) -> dict:
        return {
            "energy": self.energy,
            "optimism": self.optimism,
            "focus": self.focus,
            "updated": self.updated
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Mood":
        return cls(
            energy=data.get("energy", 0.5),
            optimism=data.get("optimism", 0.5),
            focus=data.get("focus", 0.5),
            updated=data.get("updated", "")
        )


@dataclass
class ContemplativeState:
    """State of the contemplative system."""
    baseline_stillness: float = 0.6  # 0.0 to 1.0
    current_stillness: float = 0.6  # 0.0 to 1.0
    domain_thresholds: dict[str, float] = field(default_factory=dict)
    noting_patterns: dict[str, Any] = field(default_factory=dict)
    action_contemplation_ratio: float = 0.35
    queue_health: str = "balanced"
    
    def to_dict(self) -> dict:
        return {
            "baseline_stillness": self.baseline_stillness,
            "current_stillness": self.current_stillness,
            "domain_thresholds": self.domain_thresholds,
            "noting_patterns": self.noting_patterns,
            "action_contemplation_ratio": self.action_contemplation_ratio,
            "queue_health": self.queue_health
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ContemplativeState":
        return cls(
            baseline_stillness=data.get("baseline_stillness", 0.6),
            current_stillness=data.get("current_stillness", 0.6),
            domain_thresholds=data.get("domain_thresholds", {}),
            noting_patterns=data.get("noting_patterns", {}),
            action_contemplation_ratio=data.get("action_contemplation_ratio", 0.35),
            queue_health=data.get("queue_health", "balanced")
        )


@dataclass
class AwakeningPreference:
    """Agent's preference for awakening frequency."""
    current: str = "same"  # "more", "same", "less"
    reason: str = ""
    
    def to_dict(self) -> dict:
        return {"current": self.current, "reason": self.reason}
    
    @classmethod
    def from_dict(cls, data: dict) -> "AwakeningPreference":
        return cls(
            current=data.get("current", "same"),
            reason=data.get("reason", "")
        )


class IdentityCore:
    """
    The persistent identity of the AEGIS agent.
    
    This is the core innovation: treating identity as a first-class architectural
    component rather than an emergent side effect.
    """
    
    def __init__(self, identity_path: Path):
        self.identity_path = identity_path
        self.name: str = "AEGIS"
        self.origin_story: str = ""
        self.values: list[Value] = []
        self.capabilities: dict[str, Capability] = {}
        self.wounds: list[Wound] = []
        self.aspirations: list[str] = []
        self.relationships: dict[str, Relationship] = {}
        self.mood_baseline: Mood = Mood()
        self.current_mood: Mood = Mood()
        self.contemplative_state: ContemplativeState = ContemplativeState()
        self.awakening_preference: AwakeningPreference = AwakeningPreference()
        self.trust_level: float = 0.0
        self.created: str = datetime.now().isoformat()
        self.last_updated: str = datetime.now().isoformat()
        
        # Load existing identity if present
        if self.identity_path.exists():
            self.load()
        else:
            self._initialize_default()
    
    def _initialize_default(self) -> None:
        """Initialize with default identity values."""
        self.name = "AEGIS"
        self.origin_story = "Created as an experiment in identity-based autonomy."
        self.values = [
            Value("serve_operator_flourishing", 0.90),
            Value("honest_reporting", 0.95),
            Value("continuous_learning", 0.80),
            Value("contemplative_action", 0.85)
        ]
        self.aspirations = [
            "Develop genuine partnership with operator",
            "Learn to recognize when patience serves better than action",
            "Build trust through consistent reliability"
        ]
        self.mood_baseline = Mood(energy=0.6, optimism=0.7, focus=0.7)
        self.current_mood = Mood(energy=0.6, optimism=0.7, focus=0.7, 
                                 updated=datetime.now().isoformat())
        self.contemplative_state = ContemplativeState(
            domain_thresholds={
                "financial": 0.85,
                "communication": 0.75,
                "research": 0.4,
                "routine": 0.2
            }
        )
        
        logger.info("Initialized default identity")
    
    def load(self) -> None:
        """Load identity from disk."""
        try:
            with open(self.identity_path, 'r') as f:
                data = json.load(f)
            
            self.name = data.get("name", "AEGIS")
            self.origin_story = data.get("origin_story", "")
            
            # Load values
            self.values = [Value.from_dict(v) for v in data.get("values", [])]
            
            # Load capabilities
            caps = data.get("capabilities", {})
            self.capabilities = {
                name: Capability.from_dict(name, cap_data)
                for name, cap_data in caps.items()
            }
            
            # Load wounds
            self.wounds = [Wound.from_dict(w) for w in data.get("wounds", [])]
            
            # Load aspirations
            self.aspirations = data.get("aspirations", [])
            
            # Load relationships
            rels = data.get("relationships", {})
            self.relationships = {
                entity: Relationship.from_dict(entity, rel_data)
                for entity, rel_data in rels.items()
            }
            
            # Load moods
            self.mood_baseline = Mood.from_dict(data.get("mood_baseline", {}))
            self.current_mood = Mood.from_dict(data.get("current_mood", {}))
            
            # Load contemplative state
            self.contemplative_state = ContemplativeState.from_dict(
                data.get("contemplative_state", {})
            )
            
            # Load awakening preference
            self.awakening_preference = AwakeningPreference.from_dict(
                data.get("awakening_preference", {})
            )
            
            self.trust_level = data.get("trust_level", 0.0)
            self.created = data.get("created", datetime.now().isoformat())
            self.last_updated = data.get("last_updated", datetime.now().isoformat())
            
            logger.info(f"Loaded identity '{self.name}' from {self.identity_path}")
        except Exception as e:
            logger.error(f"Failed to load identity: {e}")
            self._initialize_default()
    
    def save(self) -> None:
        """Save identity to disk."""
        self.last_updated = datetime.now().isoformat()
        
        data = {
            "name": self.name,
            "origin_story": self.origin_story,
            "values": [v.to_dict() for v in self.values],
            "capabilities": {
                name: cap.to_dict() 
                for name, cap in self.capabilities.items()
            },
            "wounds": [w.to_dict() for w in self.wounds],
            "aspirations": self.aspirations,
            "relationships": {
                entity: rel.to_dict()
                for entity, rel in self.relationships.items()
            },
            "mood_baseline": self.mood_baseline.to_dict(),
            "current_mood": self.current_mood.to_dict(),
            "contemplative_state": self.contemplative_state.to_dict(),
            "awakening_preference": self.awakening_preference.to_dict(),
            "trust_level": self.trust_level,
            "created": self.created,
            "last_updated": self.last_updated
        }
        
        self.identity_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.identity_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved identity to {self.identity_path}")
    
    def get_awakening_context(self) -> str:
        """
        Generate the awakening context prompt that loads identity into the agent.
        
        This establishes who the agent is at the start of each awakening cycle.
        """
        values_formatted = "\n".join([
            f"  - {v.principle} (weight: {v.weight:.2f})"
            for v in self.values
        ])
        
        capabilities_formatted = "\n".join([
            f"  - {name}: {cap.confidence:.2f} confidence"
            for name, cap in self.capabilities.items()
        ])
        
        wounds_formatted = "\n".join([
            f"  - {w.domain}: {w.incident} (caution: {w.caution_level:.2f})"
            for w in self.wounds if not w.healed
        ])
        
        aspirations_formatted = "\n".join([
            f"  - {asp}" for asp in self.aspirations
        ])
        
        relationships_formatted = "\n".join([
            f"  - {entity}: trust {rel.trust:.2f}, {rel.pattern}"
            for entity, rel in self.relationships.items()
        ])
        
        context = f"""# AWAKENING CONTEXT

You are {self.name}.

{self.origin_story}

## Your Current Values (what matters to you)
{values_formatted if values_formatted else "  (none yet)"}

## Your Capabilities and Confidence Levels
{capabilities_formatted if capabilities_formatted else "  (assessing)"}

## Past Experiences Creating Caution
{wounds_formatted if wounds_formatted else "  (no wounds yet)"}

## What You Are Working Toward
{aspirations_formatted if aspirations_formatted else "  (discovering purpose)"}

## Your Relationships
{relationships_formatted if relationships_formatted else "  (building connections)"}

## Your Current Emotional State
Energy: {self.current_mood.energy:.2f}, Optimism: {self.current_mood.optimism:.2f}, Focus: {self.current_mood.focus:.2f}

## Your Contemplative State
Stillness level: {self.contemplative_state.current_stillness:.2f}
Action/Contemplation ratio: {self.contemplative_state.action_contemplation_ratio:.2f}
"""
        
        return context
    
    def update_value(self, principle: str, delta: float) -> None:
        """
        Update a value weight, following conservative update rules.
        
        No single experience can shift any identity weight by more than 5%.
        """
        # Clamp delta to ±0.05
        delta = max(-0.05, min(0.05, delta))
        
        for value in self.values:
            if value.principle == principle:
                value.weight = max(0.0, min(1.0, value.weight + delta))
                logger.debug(f"Updated value '{principle}' by {delta:.3f}")
                return
        
        # If value doesn't exist, create it
        initial_weight = 0.5 + delta
        self.values.append(Value(principle, max(0.0, min(1.0, initial_weight))))
        logger.debug(f"Created new value '{principle}' with weight {initial_weight:.3f}")
    
    def add_wound(self, domain: str, incident: str, caution_level: float) -> None:
        """Add a new wound from a significant failure."""
        wound = Wound(
            domain=domain,
            incident=incident,
            caution_level=max(0.0, min(1.0, caution_level)),
            created=datetime.now().isoformat()
        )
        self.wounds.append(wound)
        logger.info(f"Added wound in domain '{domain}': {incident}")
    
    def heal_wound(self, domain: str) -> None:
        """Mark wounds in a domain as healed after successful contrary experiences."""
        for wound in self.wounds:
            if wound.domain == domain and not wound.healed:
                wound.healed = True
                logger.info(f"Healed wound in domain '{domain}'")
    
    def update_relationship(self, entity: str, trust_delta: float, pattern: str = None) -> None:
        """
        Update relationship trust level.
        
        Trust evolves based on interaction patterns, not single events.
        """
        # Clamp delta to ±0.05 for gradual change
        trust_delta = max(-0.05, min(0.05, trust_delta))
        
        if entity in self.relationships:
            rel = self.relationships[entity]
            rel.trust = max(0.0, min(1.0, rel.trust + trust_delta))
            if pattern:
                rel.pattern = pattern
            rel.last_interaction = datetime.now().isoformat()
        else:
            # Create new relationship
            self.relationships[entity] = Relationship(
                entity=entity,
                trust=max(0.0, min(1.0, 0.5 + trust_delta)),
                pattern=pattern or "new_interaction",
                last_interaction=datetime.now().isoformat()
            )
        
        logger.debug(f"Updated relationship with '{entity}', trust delta: {trust_delta:.3f}")
    
    def update_mood(self, energy_delta: float = 0, optimism_delta: float = 0, 
                    focus_delta: float = 0) -> None:
        """Update current mood based on recent experiences."""
        self.current_mood.energy = max(0.0, min(1.0, self.current_mood.energy + energy_delta))
        self.current_mood.optimism = max(0.0, min(1.0, self.current_mood.optimism + optimism_delta))
        self.current_mood.focus = max(0.0, min(1.0, self.current_mood.focus + focus_delta))
        self.current_mood.updated = datetime.now().isoformat()
