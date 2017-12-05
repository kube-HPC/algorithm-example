import ApakMain as apm
class AlgoWrapper(object):
    """docstring for ClassName."""
    def __init__(self):
        self._mcr = apm.initialize()
        self.data = None 
    def initialize(self,data):
        self.data = data
    def run(self):
        inputData = self.data
        self.output = self._mcr.ApakMain(r"/home/matyz/dev/source/Daniel_DISC1/example_input_output/test_files.csv",inputData["json_input"].encode('utf8'),inputData["output_file_path"].encode('utf8'))
    def stop(self):
        self._mcr.terminate()

def progress():
    return 0