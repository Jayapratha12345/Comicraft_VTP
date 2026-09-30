import sys
from pathlib import Path

# make `import app...` work no matter where pytest is started from
CODE_DIR = Path(__file__).resolve().parents[2] / "05_Project_Development_Phase"
sys.path.insert(0, str(CODE_DIR))
