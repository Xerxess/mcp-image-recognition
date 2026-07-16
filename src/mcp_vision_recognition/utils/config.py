import os

DEFAULT_MAX_TOKENS = 1024


def get_max_tokens() -> int:
    """Return the configured maximum number of response tokens."""
    raw_value = os.getenv("MAX_TOKENS")
    if raw_value is None:
        return DEFAULT_MAX_TOKENS

    try:
        max_tokens = int(raw_value)
    except ValueError as exc:
        raise ValueError("MAX_TOKENS must be a positive integer") from exc

    if max_tokens < 1:
        raise ValueError("MAX_TOKENS must be a positive integer")

    return max_tokens
