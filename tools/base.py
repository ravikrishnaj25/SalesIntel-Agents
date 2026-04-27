import logging
from pathlib import Path
from datetime import datetime

# Create outputs directory for generated files
OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

def get_logger(name="BattleCardPipeline"):
    return logging.getLogger(name)

def clean_markdown_response(content: str, lang: str = "html") -> str:
    """Clean up markdown wrapping if present."""
    if f"``` {lang}" in content:
        start = content.find(f"``` {lang}") + len(f"``` {lang}")
        end = content.rfind("```")
        return content[start:end].strip()
    elif f"```{lang}" in content:
        start = content.find(f"```{lang}") + len(f"```{lang}")
        end = content.rfind("```")
        return content[start:end].strip()
    elif "```" in content:
        start = content.find("```") + 3
        end = content.rfind("```")
        return content[start:end].strip()
    return content

def get_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_to_outputs(filename: str, content: bytes, is_text: bool = True):
    filepath = OUTPUTS_DIR / filename
    if is_text:
        filepath.write_text(content.decode('utf-8'), encoding='utf-8')
    else:
        filepath.write_bytes(content)
