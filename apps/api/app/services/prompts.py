import re
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

_VERSION_RE = re.compile(r"^#\s*prompt:\s*(.+?)\s+v(\S+)$")


def load_prompt(name: str) -> tuple[str, str, str]:
    """Load a prompt template by name.

    Searches for <name>_v*.txt in the prompts directory.
    Returns (template, prompt_name, prompt_version).
    First line must match: # prompt: <name> v<version>
    """
    matches = sorted(PROMPTS_DIR.glob(f"{name}_v*.txt"))
    if not matches:
        raise FileNotFoundError(f"No prompt template found for '{name}' in {PROMPTS_DIR}")
    path = matches[-1]
    text = path.read_text(encoding="utf-8")
    first_line = text.splitlines()[0]
    m = _VERSION_RE.match(first_line)
    if not m:
        raise ValueError(f"Prompt file {path} missing version header. Expected: # prompt: <name> v<version>")
    prompt_name = m.group(1)
    prompt_version = m.group(2)
    return text, prompt_name, prompt_version


def substitute(template: str, vars: dict[str, str]) -> str:
    result = template
    for key, value in vars.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result
