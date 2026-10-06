import os
import sys

# cho phep chay `pytest` ma khong can dat PYTHONPATH thu cong
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
