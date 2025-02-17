from pathlib import Path
from typing import Optional

def validate_gpx_file(file_path: Path) -> None:
    """
    Validate GPX file existence and format
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if file_path.suffix.lower() != '.gpx':
        raise ValueError(f"File must have .gpx extension: {file_path}")
        
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
        
    # Check if file is readable
    try:
        file_path.open('r').close()
    except Exception as e:
        raise ValueError(f"Cannot read file {file_path}: {str(e)}")

def validate_speed_threshold(speed: float) -> None:
    """
    Validate speed threshold value
    """
    if speed <= 0:
        raise ValueError("Speed threshold must be positive")
        
    if speed > 100:  # Reasonable upper limit for running
        raise ValueError("Speed threshold too high for running activity")
