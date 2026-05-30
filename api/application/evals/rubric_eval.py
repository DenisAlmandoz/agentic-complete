from __future__ import annotations

from dataclasses import dataclass

from api.domain.models import CefrLevel, SkillScore
from api.domain.rubrics import decide_promotion


@dataclass(frozen=True)
class EvalCase:
    name: str
    level: CefrLevel
    scores: SkillScore
    confidence: float
    expected_promotion: bool


EVAL_CASES = [
    EvalCase("strong_a1_to_a2", CefrLevel.A1, SkillScore(grammar=0.9, vocabulary=0.86, fluency=0.84, comprehension=0.88), 0.85, True),
    EvalCase("weak_a1_stays", CefrLevel.A1, SkillScore(grammar=0.5, vocabulary=0.62, fluency=0.58, comprehension=0.7), 0.8, False),
    EvalCase("low_confidence_stays", CefrLevel.A1, SkillScore(grammar=0.95, vocabulary=0.9, fluency=0.88, comprehension=0.9), 0.6, False),
]


def run_promotion_evals() -> dict[str, bool]:
    return {
        case.name: decide_promotion(case.level, case.scores, case.confidence, "eval").can_promote == case.expected_promotion
        for case in EVAL_CASES
    }
