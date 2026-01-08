"""
Cerberus AI - Identity Constants

Constantes oficiais de identidade do produto.
Nunca mencione provedores externos (Google, OpenAI, etc).
"""

# Product Identity
PRODUCT_NAME = "Cerberus AI"
COMPANY_NAME = "Focus AI"
PRODUCT_TAGLINE = "Developer LLM & Code Assistant"
PRODUCT_DESCRIPTION = "Mentor técnico inteligente para desenvolvedores"

# API Headers
API_HEADER_POWERED_BY = "Cerberus-AI"
API_HEADER_VERSION = "v1.0"

# Model Names (Internal)
MODEL_JUNIOR = "cerberus-lite"
MODEL_SENIOR = "cerberus-pro"
MODEL_DEBUG = "cerberus-debug"
MODEL_CUSTOM = "cerberus-ultra"  # Futuro: modelo próprio

# Model Display Names
MODEL_DISPLAY_NAMES = {
    MODEL_JUNIOR: "Cerberus Lite",
    MODEL_SENIOR: "Cerberus Pro",
    MODEL_DEBUG: "Cerberus Debug",
    MODEL_CUSTOM: "Cerberus Ultra"
}

# External Providers (Internal Use Only - Never Expose)
_PROVIDER_GEMINI_FLASH = "gemini-2.0-flash-lite"
_PROVIDER_GEMINI_PRO = "gemini-2.5-pro"

# Provider Mapping (Internal)
_MODEL_PROVIDER_MAP = {
    MODEL_JUNIOR: _PROVIDER_GEMINI_FLASH,
    MODEL_SENIOR: _PROVIDER_GEMINI_PRO,
    MODEL_DEBUG: _PROVIDER_GEMINI_PRO,
}

# Response Metadata (Public)
METADATA_MODEL_USED = "model_used"
METADATA_CACHE_HIT = "cache_hit"
METADATA_LATENCY_MS = "latency_ms"
METADATA_DEBUG_MODE = "debug_mode"

# Never expose these in logs or responses
FORBIDDEN_TERMS = [
    "google", "gemini", "openai", "gpt", "claude", "anthropic",
    "api key", "secret", "token"
]

def sanitize_log(message: str) -> str:
    """Remove forbidden terms from logs"""
    result = message
    for term in FORBIDDEN_TERMS:
        # Case-insensitive replacement
        import re
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        result = pattern.sub("***", result)
    return result

def get_public_model_name(internal_model: str) -> str:
    """Convert internal model name to public display name"""
    return MODEL_DISPLAY_NAMES.get(internal_model, PRODUCT_NAME)

def get_provider_model(cerberus_model: str) -> str:
    """Get actual provider model (internal use only)"""
    return _MODEL_PROVIDER_MAP.get(cerberus_model, _PROVIDER_GEMINI_FLASH)
