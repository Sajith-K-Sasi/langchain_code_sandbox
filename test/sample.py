# AUTO_INSTALL: numpy
import numpy as np

def execute_code():
    # Create a numpy array with 10 rows and 3 columns with random values
    arr = np.random.rand(10, 3)
    return f"Created numpy array with shape {arr.shape}:\n{arr}"

result = execute_code()