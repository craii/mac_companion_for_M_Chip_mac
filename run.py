import os
import sys
# from pathlib import Path
# sys.path.append(f"{Path(__file__).resolve().parent.parent}")

# os.system(f"{Path(__file__).resolve().parent}/venv/bin/python App.py")

file_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(file_dir)

sys.path.append(f"{file_dir}")
sys.path.append(f"{file_dir}/data_storage")
sys.path.append(f"{file_dir}/uikit")
print("==="*10, sys.path, file_dir, "==="*10 )
os.system(f"{file_dir}/venv/bin/python App.py")