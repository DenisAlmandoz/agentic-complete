from __future__ import annotations

from api.domain.models import CefrLevel, LevelAssessment, SkillScore

PROMOTION_THRESHOLD = 0.82
CONFIDENCE_THRESHOLD = 0.72
_LEVEL_ORDER = [CefrLevel.A1, CefrLevel.A2, CefrLevel.B1, CefrLevel.B2, CefrLevel.C1, CefrLevel.C2]

CEFR_RUBRICS: dict[CefrLevel, str] = {
    CefrLevel.A1: "Can use simple phrases, introduce themselves, and answer concrete personal questions.",
    CefrLevel.A2: "Can communicate in routine tasks about familiar topics using simple connected language.",
    CefrLevel.B1: "Can handle travel situations, narrate experiences, and explain opinions in familiar contexts.",
    CefrLevel.B2: "Can interact with fluency, understand main ideas of complex text, and argue viewpoints.",
    CefrLevel.C1: "Can express ideas fluently, flexibly, and effectively for social, academic, and professional purposes.",
    CefrLevel.C2: "Can understand virtually everything and express themselves precisely with nuanced meaning.",
}


def next_level(level: CefrLevel) -> CefrLevel:
    index = _LEVEL_ORDER.index(level)
    return _LEVEL_ORDER[min(index + 1, len(_LEVEL_ORDER) - 1)]


def decide_promotion(current_level: CefrLevel, scores: SkillScore, confidence: float, rationale: str) -> LevelAssessment:
    can_promote = scores.average >= PROMOTION_THRESHOLD and confidence >= CONFIDENCE_THRESHOLD
    recommended = next_level(current_level) if can_promote else current_level
    next_steps = [
        "Complete a short oral exam with topic changes.",
        "Review mistakes from the last three sessions.",
        "Practice spontaneous answers without translation.",
    ]
    if can_promote:
        next_steps.insert(0, f"Start bridge lessons for {recommended}.")
    return LevelAssessment(
        current_level=current_level,
        recommended_level=recommended,
        can_promote=can_promote,
        confidence=confidence,
        scores=scores,
        rationale=rationale,
        next_steps=next_steps,
    )
