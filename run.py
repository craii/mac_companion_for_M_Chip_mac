import os
import sys
from pathlib import Path
sys.path.append(f"{Path(__file__).resolve().parent.parent}")

os.system(f"{Path(__file__).resolve().parent}/venv/bin/python App.py")