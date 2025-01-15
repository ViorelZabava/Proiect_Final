
import sys
from importlib import util
def load_file_as_module(name, location):
    sys.path.insert(0,location.rsplit('/', 1)[0])
    spec = util.spec_from_file_location(name, location)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
sys.argv = [ "/home/viorel/Proiect_History/Sniper/scripts/Perceptron_predictor.py", "10000:1000:4096:4096" ]
load_file_as_module("Perceptron_predictor","/home/viorel/Proiect_History/Sniper/scripts/Perceptron_predictor.py")

