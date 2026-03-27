from app.Utilities.ExperimentRunner import ExperimentRunner
from app.Utilities.SAParameters import SAParameters
from app.Utilities.EAParameters import EAParameters

if __name__ == "__main__":
    runner = EAParameters()
    #runner = SAParameters()
    #runner = ExperimentRunner()
    runner.run_all()