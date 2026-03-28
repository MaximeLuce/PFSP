## security of number of core
import os
os.environ["OMP_NUM_THREADS"] = "1" # OpenMP
os.environ["OPENBLAS_NUM_THREADS"] = "1" # OpenBLAS
os.environ["MKL_NUM_THREADS"] = "1" # MKL
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" # Accelerate
os.environ["NUMEXPR_NUM_THREADS"] = "1" # NumExpr


from app.Utilities.ComparisonRunner import ComparisonRunner
from app.Utilities.SAParameters import SAParameters
from app.Utilities.EAParameters import EAParameters

if __name__ == "__main__":
    #runner = EAParameters()
    #runner = SAParameters()
    runner = ComparisonRunner()
    runner.run_all()