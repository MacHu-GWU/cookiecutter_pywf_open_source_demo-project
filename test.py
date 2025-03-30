import tomllib
from pathlib import Path
from rich import print as rprint
p = Path("pyproject.toml")
data = tomllib.loads(p.read_text(encoding="utf-8"))
rprint(data)