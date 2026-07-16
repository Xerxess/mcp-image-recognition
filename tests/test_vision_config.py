from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from src.mcp_vision_recognition.utils.config import get_max_tokens
from src.mcp_vision_recognition.vision.anthropic import AnthropicVision
from src.mcp_vision_recognition.vision.openai import OpenAIVision


def test_max_tokens_defaults_to_1024(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use 1024 response tokens when MAX_TOKENS is not configured."""
    monkeypatch.delenv("MAX_TOKENS", raising=False)

    assert get_max_tokens() == 1024


def test_max_tokens_can_be_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read a custom response token limit from the environment."""
    monkeypatch.setenv("MAX_TOKENS", "4096")

    assert get_max_tokens() == 4096


@pytest.mark.parametrize("value", ["0", "-1", "invalid", "1.5", ""])
def test_max_tokens_rejects_invalid_values(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    """Reject non-positive and non-integer response token limits."""
    monkeypatch.setenv("MAX_TOKENS", value)

    with pytest.raises(ValueError, match="MAX_TOKENS must be a positive integer"):
        get_max_tokens()


@pytest.mark.asyncio
async def test_openai_uses_configured_max_tokens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pass MAX_TOKENS to the OpenAI-compatible API."""
    monkeypatch.setenv("MAX_TOKENS", "2048")
    vision = OpenAIVision.__new__(OpenAIVision)
    create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="description"))]
        )
    )
    vision.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    assert await vision.describe_image("image-data") == "description"
    assert create.await_args.kwargs["max_tokens"] == 2048


def test_anthropic_uses_configured_max_tokens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pass MAX_TOKENS to the Anthropic API."""
    monkeypatch.setenv("MAX_TOKENS", "3072")
    vision = AnthropicVision.__new__(AnthropicVision)
    create = Mock(
        return_value=SimpleNamespace(content=[SimpleNamespace(text="description")])
    )
    vision.client = SimpleNamespace(messages=SimpleNamespace(create=create))

    assert vision.describe_image("image-data") == "description"
    assert create.call_args.kwargs["max_tokens"] == 3072
