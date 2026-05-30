from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_required_architecture_directories_exist() -> None:
    for relative in ["api/application", "api/domain", "api/infrastructure", "ui/src"]:
        assert (ROOT / relative).is_dir(), relative


def test_grok_uses_xai_openai_compatible_base_url() -> None:
    settings = (ROOT / "api/application/settings.py").read_text()
    client = (ROOT / "api/infrastructure/llm/grok_client.py").read_text()
    assert "https://api.x.ai/v1" in settings
    assert "OpenAI" in client
    assert "chat.completions.create" in client


def test_evals_cover_promotion_and_non_promotion() -> None:
    eval_file = (ROOT / "api/application/evals/rubric_eval.py").read_text()
    assert "expected_promotion: bool" in eval_file
    assert "True" in eval_file
    assert "False" in eval_file
