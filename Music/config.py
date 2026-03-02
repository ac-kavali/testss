"""Configuration parsing and validation for maze generator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Config:
    """Parsed configuration values."""

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


class ConfigError(Exception):
    """Configuration parsing or validation error."""


def parse_bool(value: str, key_name: str) -> bool:
    """Parse a boolean string value."""

    v = value.strip().lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ConfigError(f"{key_name} must be True or False")


def parse_coord(value: str, key_name: str) -> Tuple[int, int]:
    """Parse a coordinate in the format x,y."""

    try:
        x, y = value.split(",", 1)
        return int(x.strip()), int(y.strip())
    except ValueError as exc:
        raise ConfigError(f"{key_name} must be in format x,y") from exc


def parse_config(file_name: str) -> Config:
    """Parse the config file and return a Config object."""

    confs: dict[str, str] = {}
    required = {
        "width",
        "height",
        "entry",
        "exit",
        "output_file",
        "perfect",
    }

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Line {line_num}: missing '='")

                key, value = line.split("=", 1)
                confs[key.lower().strip()] = value.strip()

    except FileNotFoundError as exc:
        raise ConfigError(
            f"Config file not found: {file_name}"
        ) from exc
    except OSError as exc:
        raise ConfigError(
            f"Failed to read config file: {file_name}"
        ) from exc

    missing = required - confs.keys()
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ConfigError(f"Missing required keys: {missing_str}")

    try:
        width = int(confs["width"])
        height = int(confs["height"])
    except ValueError as exc:
        raise ConfigError(
            "WIDTH and HEIGHT must be integers"
        ) from exc

    if width <= 1 or height <= 1:
        raise ConfigError("WIDTH and HEIGHT must be > 1")

    entry = parse_coord(confs["entry"], "ENTRY")
    ex_it = parse_coord(confs["exit"], "EXIT")

    if entry == ex_it:
        raise ConfigError("ENTRY and EXIT must be different")

    perfect = parse_bool(confs["perfect"], "PERFECT")

    output_file = confs["output_file"]
    if not output_file:
        raise ConfigError("OUTPUT_FILE must be non-empty")

    seed: Optional[int] = None
    if "seed" in confs:
        try:
            seed = int(confs["seed"])
        except ValueError as exc:
            raise ConfigError("SEED must be an integer") from exc

    for name, (x, y) in {"ENTRY": entry, "EXIT": ex_it}.items():
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} out of bounds")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=ex_it,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
