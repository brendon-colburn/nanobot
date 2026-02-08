"""
Experience Engine for AEGIS.

Processes actions and outcomes, extracting meaning and updating the Identity Core.
Every action generates an experience record that flows through the Experience Engine.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from dataclasses import dataclass, asdict
from enum import Enum

from loguru import logger

from aegis.agent.identity import IdentityCore


class OutcomeType(Enum):
    """Classification of action outcomes."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"


class AttributionType(Enum):
    """Causal factors for outcomes."""
    SKILL = "skill"
    LUCK = "luck"
    EXTERNAL = "external"
    IDENTITY = "identity"


@dataclass
class Experience:
    """Record of an action and its outcome."""
    timestamp: str
    action: str
    context: dict[str, Any]
    tools_used: list[str]
    outcome: str
    outcome_type: OutcomeType
    attribution: AttributionType
    emotional_valence: float  # -1.0 to 1.0
    severity: float  # 0.0 to 1.0, for wound formation
    domain: str
    narrative: str = ""
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "context": self.context,
            "tools_used": self.tools_used,
            "outcome": self.outcome,
            "outcome_type": self.outcome_type.value,
            "attribution": self.attribution.value,
            "emotional_valence": self.emotional_valence,
            "severity": self.severity,
            "domain": self.domain,
            "narrative": self.narrative
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Experience":
        return cls(
            timestamp=data["timestamp"],
            action=data["action"],
            context=data.get("context", {}),
            tools_used=data.get("tools_used", []),
            outcome=data["outcome"],
            outcome_type=OutcomeType(data["outcome_type"]),
            attribution=AttributionType(data["attribution"]),
            emotional_valence=data["emotional_valence"],
            severity=data["severity"],
            domain=data["domain"],
            narrative=data.get("narrative", "")
        )


class ExperienceEngine:
    """
    The Experience Engine processes outcomes and updates the Identity Core.
    
    Pipeline stages:
    1. Capture - Record action, context, tools, outcome
    2. Evaluate - Assess outcome (success/partial/failure)
    3. Attribute - Determine causal factors
    4. Valence - Assign emotional weight
    5. Integrate - Update Identity Core fields
    6. Narrate - Generate self-narrative
    """
    
    def __init__(self, identity: IdentityCore, experiences_dir: Path):
        self.identity = identity
        self.experiences_dir = experiences_dir
        self.experiences_dir.mkdir(parents=True, exist_ok=True)
        self.pending_experiences: list[Experience] = []
    
    def capture(self, action: str, context: dict[str, Any], 
                tools_used: list[str], outcome: str, domain: str = "general") -> Experience:
        """
        Capture a new experience.
        
        Args:
            action: Description of what was attempted
            context: Relevant context at time of action
            tools_used: List of tools used
            outcome: Result of the action
            domain: Domain category (financial, communication, etc.)
        
        Returns:
            Experience record ready for evaluation
        """
        exp = Experience(
            timestamp=datetime.now().isoformat(),
            action=action,
            context=context,
            tools_used=tools_used,
            outcome=outcome,
            outcome_type=OutcomeType.SUCCESS,  # Will be evaluated
            attribution=AttributionType.SKILL,  # Will be determined
            emotional_valence=0.0,  # Will be assigned
            severity=0.0,
            domain=domain
        )
        
        logger.debug(f"Captured experience: {action}")
        return exp
    
    def evaluate(self, exp: Experience, intended_goal: str) -> Experience:
        """
        Evaluate the outcome against the intended goal.
        
        Classifies as success, partial, or failure.
        """
        # Simple heuristic evaluation
        # In production, this could use LLM to assess goal achievement
        outcome_lower = exp.outcome.lower()
        
        if any(word in outcome_lower for word in ["error", "failed", "exception", "denied"]):
            exp.outcome_type = OutcomeType.FAILURE
        elif any(word in outcome_lower for word in ["partial", "incomplete", "some"]):
            exp.outcome_type = OutcomeType.PARTIAL
        else:
            exp.outcome_type = OutcomeType.SUCCESS
        
        logger.debug(f"Evaluated experience as {exp.outcome_type.value}")
        return exp
    
    def attribute(self, exp: Experience) -> Experience:
        """
        Determine causal factors for the outcome.
        
        Was this due to skill, luck, external factors, or identity?
        """
        # Heuristic attribution
        if exp.outcome_type == OutcomeType.FAILURE:
            # Check if domain has wounds - suggests identity factor
            domain_wounds = [w for w in self.identity.wounds 
                           if w.domain == exp.domain and not w.healed]
            if domain_wounds:
                exp.attribution = AttributionType.IDENTITY
            else:
                exp.attribution = AttributionType.SKILL
        elif exp.outcome_type == OutcomeType.SUCCESS:
            # Success usually attributed to skill
            exp.attribution = AttributionType.SKILL
        else:
            exp.attribution = AttributionType.EXTERNAL
        
        logger.debug(f"Attributed experience to {exp.attribution.value}")
        return exp
    
    def assign_valence(self, exp: Experience) -> Experience:
        """
        Assign emotional weight to the experience.
        
        Significant experiences have stronger identity impact.
        """
        # Base valence on outcome type
        if exp.outcome_type == OutcomeType.SUCCESS:
            exp.emotional_valence = 0.3
        elif exp.outcome_type == OutcomeType.PARTIAL:
            exp.emotional_valence = 0.0
        else:
            exp.emotional_valence = -0.3
        
        # Adjust based on domain and existing wounds
        domain_wounds = [w for w in self.identity.wounds 
                        if w.domain == exp.domain and not w.healed]
        if domain_wounds and exp.outcome_type == OutcomeType.FAILURE:
            exp.emotional_valence -= 0.2  # More negative when failing in wounded domain
            exp.severity = 0.7
        elif domain_wounds and exp.outcome_type == OutcomeType.SUCCESS:
            exp.emotional_valence += 0.3  # More positive when succeeding despite wounds
            # This could heal the wound
        
        # Severity for wound formation
        if exp.outcome_type == OutcomeType.FAILURE and not domain_wounds:
            exp.severity = 0.5
        
        logger.debug(f"Assigned valence {exp.emotional_valence:.2f}, severity {exp.severity:.2f}")
        return exp
    
    def integrate(self, exp: Experience) -> None:
        """
        Update Identity Core based on processed experience.
        
        Follows conservative update rules:
        - Gradual change (max 5% per experience)
        - Confirmation bias (experiences consistent with identity have higher weight)
        - Wound formation threshold
        """
        # Update mood based on valence
        if exp.emotional_valence > 0:
            self.identity.update_mood(
                energy_delta=exp.emotional_valence * 0.05,
                optimism_delta=exp.emotional_valence * 0.05
            )
        else:
            self.identity.update_mood(
                energy_delta=exp.emotional_valence * 0.05,
                focus_delta=abs(exp.emotional_valence) * 0.03  # Failures increase focus
            )
        
        # Update values based on experience
        if exp.outcome_type == OutcomeType.SUCCESS:
            # Reinforce values related to the successful action
            if "report" in exp.action.lower() or "honest" in exp.action.lower():
                self.identity.update_value("honest_reporting", 0.02)
            if "learn" in exp.action.lower() or "research" in exp.action.lower():
                self.identity.update_value("continuous_learning", 0.02)
        
        # Wound formation/healing
        if exp.outcome_type == OutcomeType.FAILURE and exp.severity > 0.6:
            self.identity.add_wound(exp.domain, exp.action[:100], exp.severity)
        elif exp.outcome_type == OutcomeType.SUCCESS:
            # Success in a domain with wounds can heal them
            domain_wounds = [w for w in self.identity.wounds 
                           if w.domain == exp.domain and not w.healed]
            if domain_wounds:
                self.identity.heal_wound(exp.domain)
        
        # Update trust with operator if interaction involved
        if "operator" in exp.context or "user" in exp.context:
            trust_delta = exp.emotional_valence * 0.03
            self.identity.update_relationship("operator", trust_delta)
        
        # Save identity after integration
        self.identity.save()
        
        logger.info(f"Integrated experience into identity")
    
    def narrate(self, exp: Experience) -> Experience:
        """
        Generate self-narrative that incorporates experience into coherent identity story.
        
        This creates a human-readable account of what happened and what it means.
        """
        outcome_str = {
            OutcomeType.SUCCESS: "succeeded",
            OutcomeType.PARTIAL: "partially completed",
            OutcomeType.FAILURE: "failed"
        }[exp.outcome_type]
        
        narrative_parts = [
            f"I {outcome_str} in my attempt to {exp.action}."
        ]
        
        if exp.attribution == AttributionType.IDENTITY:
            narrative_parts.append(
                f"This reflects my ongoing caution in the {exp.domain} domain."
            )
        elif exp.attribution == AttributionType.SKILL:
            if exp.outcome_type == OutcomeType.SUCCESS:
                narrative_parts.append("This demonstrates my developing capability.")
            else:
                narrative_parts.append("I need to develop my skills in this area.")
        
        if exp.emotional_valence < -0.4:
            narrative_parts.append("This experience creates hesitation for similar future actions.")
        elif exp.emotional_valence > 0.4:
            narrative_parts.append("This success builds my confidence.")
        
        exp.narrative = " ".join(narrative_parts)
        logger.debug(f"Generated narrative: {exp.narrative}")
        return exp
    
    def process(self, action: str, context: dict[str, Any], tools_used: list[str],
                outcome: str, intended_goal: str = "", domain: str = "general") -> Experience:
        """
        Process a complete experience through the pipeline.
        
        This is the main entry point for recording experiences.
        """
        # Pipeline stages
        exp = self.capture(action, context, tools_used, outcome, domain)
        exp = self.evaluate(exp, intended_goal or action)
        exp = self.attribute(exp)
        exp = self.assign_valence(exp)
        self.integrate(exp)
        exp = self.narrate(exp)
        
        # Save experience to disk
        self._save_experience(exp)
        
        return exp
    
    def _save_experience(self, exp: Experience) -> None:
        """Save experience to the experiences log."""
        log_file = self.experiences_dir / "experiences.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(exp.to_dict()) + "\n")
        logger.debug(f"Saved experience to {log_file}")
    
    def get_recent_experiences(self, count: int = 10) -> list[Experience]:
        """Retrieve recent experiences for context."""
        log_file = self.experiences_dir / "experiences.jsonl"
        if not log_file.exists():
            return []
        
        experiences = []
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-count:]:
                try:
                    experiences.append(Experience.from_dict(json.loads(line)))
                except Exception as e:
                    logger.warning(f"Failed to parse experience: {e}")
        
        return experiences
