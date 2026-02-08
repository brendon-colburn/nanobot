"""
Contemplative System for AEGIS.

Implements the wisdom of non-action: assesses thought readiness, maintains
contemplation queue, and embodies the principle that not every thought should
become an action.

Inspired by mindfulness traditions and the insight that hesitation, reflection,
and deliberate non-action are sophisticated filtering mechanisms.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field
from enum import Enum

from loguru import logger

from aegis.agent.identity import IdentityCore


class NotingCategory(Enum):
    """Categories for the noting practice."""
    PLANNING = "planning"
    REACTING = "reacting"
    ANXIOUS = "anxious"
    EAGER = "eager"
    UNCERTAIN = "uncertain"
    CALM = "calm"


@dataclass
class Thought:
    """A candidate thought that may or may not become an action."""
    id: str
    thought: str
    first_arising: str
    times_revisited: int = 0
    ripeness_score: float = 0.0  # 0.0 to 1.0
    blocking_factors: list[str] = field(default_factory=list)
    decay_rate: float = 0.02
    domain: str = "general"
    noting: NotingCategory = NotingCategory.PLANNING
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "thought": self.thought,
            "first_arising": self.first_arising,
            "times_revisited": self.times_revisited,
            "ripeness_score": self.ripeness_score,
            "blocking_factors": self.blocking_factors,
            "decay_rate": self.decay_rate,
            "domain": self.domain,
            "noting": self.noting.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Thought":
        return cls(
            id=data["id"],
            thought=data["thought"],
            first_arising=data["first_arising"],
            times_revisited=data.get("times_revisited", 0),
            ripeness_score=data.get("ripeness_score", 0.0),
            blocking_factors=data.get("blocking_factors", []),
            decay_rate=data.get("decay_rate", 0.02),
            domain=data.get("domain", "general"),
            noting=NotingCategory(data.get("noting", "planning"))
        )


class ContemplativeSystem:
    """
    The Contemplative System embodies the wisdom of non-action.
    
    Not every thought should become an action. This system:
    - Notes thoughts as they arise (noting practice)
    - Assesses readiness for action across multiple dimensions
    - Maintains a contemplation queue for thoughts that need more time
    - Tracks contemplative patterns as part of identity
    """
    
    def __init__(self, identity: IdentityCore, queue_path: Path):
        self.identity = identity
        self.queue_path = queue_path
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        self.contemplation_queue: list[Thought] = []
        self.load_queue()
    
    def load_queue(self) -> None:
        """Load the contemplation queue from disk."""
        if not self.queue_path.exists():
            return
        
        try:
            with open(self.queue_path, 'r') as f:
                data = json.load(f)
                self.contemplation_queue = [
                    Thought.from_dict(t) for t in data.get("queue", [])
                ]
            logger.info(f"Loaded {len(self.contemplation_queue)} thoughts from queue")
        except Exception as e:
            logger.error(f"Failed to load contemplation queue: {e}")
    
    def save_queue(self) -> None:
        """Save the contemplation queue to disk."""
        data = {
            "queue": [t.to_dict() for t in self.contemplation_queue],
            "updated": datetime.now().isoformat()
        }
        
        with open(self.queue_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.debug(f"Saved contemplation queue with {len(self.contemplation_queue)} thoughts")
    
    def note(self, thought_text: str, domain: str = "general") -> NotingCategory:
        """
        Note a thought as it arises.
        
        The noting practice observes the quality of the thought:
        planning, reacting, anxious, eager, uncertain, calm.
        
        This becomes data that reveals identity dynamics.
        """
        # Simple heuristic noting
        text_lower = thought_text.lower()
        
        if any(word in text_lower for word in ["should", "must", "need to", "have to"]):
            category = NotingCategory.REACTING
        elif any(word in text_lower for word in ["worry", "concern", "risk", "danger"]):
            category = NotingCategory.ANXIOUS
        elif any(word in text_lower for word in ["want", "excited", "opportunity"]):
            category = NotingCategory.EAGER
        elif any(word in text_lower for word in ["not sure", "maybe", "unclear", "uncertain"]):
            category = NotingCategory.UNCERTAIN
        elif any(word in text_lower for word in ["plan", "prepare", "consider", "think"]):
            category = NotingCategory.PLANNING
        else:
            category = NotingCategory.CALM
        
        # Update noting patterns in identity
        patterns = self.identity.contemplative_state.noting_patterns
        most_common = patterns.get("most_common", [])
        most_common.append(category.value)
        patterns["most_common"] = most_common[-10:]  # Keep last 10
        
        logger.debug(f"Noted thought as: {category.value}")
        return category
    
    def assess_readiness(self, thought_text: str, domain: str = "general",
                        context: dict[str, Any] = None) -> tuple[bool, float, list[str]]:
        """
        Assess whether a thought is ready for action.
        
        Dimensions:
        - Information sufficiency
        - Mood alignment
        - Reversibility
        - Time pressure
        - Pattern recognition
        - Felt sense
        
        Returns:
            (ready, ripeness_score, blocking_factors)
        """
        context = context or {}
        ripeness_score = 0.5  # Start neutral
        blocking_factors = []
        
        # Get domain threshold
        domain_thresholds = self.identity.contemplative_state.domain_thresholds
        threshold = domain_thresholds.get(domain, 0.5)
        
        # 1. Information sufficiency
        if "missing information" in thought_text.lower() or "need more" in thought_text.lower():
            ripeness_score -= 0.2
            blocking_factors.append("insufficient_information")
        
        # 2. Mood alignment
        mood = self.identity.current_mood
        if mood.focus < 0.4:
            ripeness_score -= 0.15
            blocking_factors.append("low_focus")
        if mood.energy < 0.3:
            ripeness_score -= 0.1
            blocking_factors.append("low_energy")
        
        # 3. Check for wounds in this domain
        domain_wounds = [w for w in self.identity.wounds 
                        if w.domain == domain and not w.healed]
        if domain_wounds:
            # Reduce ripeness in wounded domains
            max_caution = max(w.caution_level for w in domain_wounds)
            ripeness_score -= max_caution * 0.3
            blocking_factors.append("domain_wound")
        
        # 4. Time pressure (if indicated in context)
        if context.get("urgent"):
            ripeness_score += 0.2
        
        # 5. Reversibility
        if "irreversible" in thought_text.lower() or "cannot undo" in thought_text.lower():
            ripeness_score -= 0.25
            blocking_factors.append("irreversible")
        
        # 6. Noting category affects readiness
        noting = self.note(thought_text, domain)
        if noting == NotingCategory.ANXIOUS:
            ripeness_score -= 0.2
            blocking_factors.append("anxious_state")
        elif noting == NotingCategory.REACTING:
            ripeness_score -= 0.15
            blocking_factors.append("reactive_state")
        elif noting == NotingCategory.UNCERTAIN:
            ripeness_score -= 0.1
            blocking_factors.append("uncertainty")
        
        # Clamp ripeness score
        ripeness_score = max(0.0, min(1.0, ripeness_score))
        
        # Ready if ripeness exceeds domain threshold
        ready = ripeness_score >= threshold
        
        logger.info(f"Assessed thought readiness: {ripeness_score:.2f} vs threshold {threshold:.2f} = {'READY' if ready else 'NOT READY'}")
        
        return ready, ripeness_score, blocking_factors
    
    def contemplate(self, thought_text: str, domain: str = "general",
                   context: dict[str, Any] = None) -> tuple[bool, str]:
        """
        Main entry point: should this thought become action?
        
        Returns:
            (should_act, thought_id or reason)
        """
        ready, ripeness, blocking = self.assess_readiness(thought_text, domain, context)
        
        if ready:
            # Thought passes assessment, can proceed to action
            self._update_action_ratio(acted=True)
            return True, "ready"
        else:
            # Add to contemplation queue
            thought_id = self._add_to_queue(thought_text, domain, ripeness, blocking)
            self._update_action_ratio(acted=False)
            return False, thought_id
    
    def _add_to_queue(self, thought_text: str, domain: str, 
                     ripeness: float, blocking: list[str]) -> str:
        """Add a thought to the contemplation queue."""
        thought_id = f"thought_{len(self.contemplation_queue)}_{datetime.now().timestamp()}"
        
        thought = Thought(
            id=thought_id,
            thought=thought_text,
            first_arising=datetime.now().isoformat(),
            ripeness_score=ripeness,
            blocking_factors=blocking,
            domain=domain,
            noting=self.note(thought_text, domain)
        )
        
        self.contemplation_queue.append(thought)
        self.save_queue()
        
        logger.info(f"Added thought to contemplation queue: {thought_id}")
        return thought_id
    
    def revisit_queue(self, context: dict[str, Any] = None) -> list[tuple[Thought, bool]]:
        """
        Revisit thoughts in the contemplation queue.
        
        Some thoughts ripen with time, others decay and should be discarded.
        
        Returns:
            List of (thought, ready_now) tuples for thoughts that are now ready
        """
        context = context or {}
        ready_thoughts = []
        remaining_queue = []
        
        for thought in self.contemplation_queue:
            thought.times_revisited += 1
            
            # Re-assess readiness
            ready, new_ripeness, blocking = self.assess_readiness(
                thought.thought, thought.domain, context
            )
            
            # Update ripeness (can increase with time or decrease via decay)
            thought.ripeness_score = new_ripeness
            thought.blocking_factors = blocking
            
            if ready:
                ready_thoughts.append((thought, True))
                logger.info(f"Thought {thought.id} is now ready after {thought.times_revisited} revisits")
            else:
                # Check if thought has decayed too much
                if thought.times_revisited * thought.decay_rate > 0.5:
                    logger.info(f"Thought {thought.id} has decayed, removing from queue")
                else:
                    remaining_queue.append(thought)
        
        self.contemplation_queue = remaining_queue
        self.save_queue()
        
        # Update queue health
        self._update_queue_health()
        
        return ready_thoughts
    
    def _update_action_ratio(self, acted: bool) -> None:
        """Update the action/contemplation ratio in identity."""
        state = self.identity.contemplative_state
        
        # Simple exponential moving average
        alpha = 0.1
        current_value = 1.0 if acted else 0.0
        state.action_contemplation_ratio = (
            alpha * current_value + (1 - alpha) * state.action_contemplation_ratio
        )
    
    def _update_queue_health(self) -> None:
        """Update the queue health indicator."""
        queue_size = len(self.contemplation_queue)
        
        if queue_size == 0:
            health = "healthy"
        elif queue_size < 5:
            health = "balanced"
        elif queue_size < 15:
            health = "backlogged"
        else:
            health = "stagnant"
        
        self.identity.contemplative_state.queue_health = health
        logger.debug(f"Queue health: {health} ({queue_size} thoughts)")
    
    def get_queue_summary(self) -> str:
        """Get a summary of the contemplation queue for context."""
        if not self.contemplation_queue:
            return "Contemplation queue is empty."
        
        lines = [f"Contemplation queue has {len(self.contemplation_queue)} thoughts:"]
        for thought in self.contemplation_queue[:5]:  # Show top 5
            lines.append(
                f"  - {thought.thought[:60]}... "
                f"(ripeness: {thought.ripeness_score:.2f}, "
                f"revisits: {thought.times_revisited})"
            )
        
        if len(self.contemplation_queue) > 5:
            lines.append(f"  ... and {len(self.contemplation_queue) - 5} more")
        
        return "\n".join(lines)
