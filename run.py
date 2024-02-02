import os
import sys
# from pathlib import Path
# sys.path.append(f"{Path(__file__).resolve().parent.parent}")

# os.system(f"{Path(__file__).resolve().parent}/venv/bin/python App.py")

file_dir = os.path.dirname(os.path.abspath(__file__))
# print(file_dir, type(file_dir))
os.system(f"{file_dir}/venv/bin/python App.py")