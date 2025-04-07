from packaging.version import Version
from importlib.metadata import version
import sempy.fabric as fabric

sempy_version = version('semantic-link-sempy')

if Version(sempy_version) < Version("0.9.3"):
    get_ipython().run_line_magic('pip', 'install semantic-link==0.9.3')

dataset = "Dev Tracker Dashboard" 
workspace = "Global - APAC - LA Development"

# Memory Analyser
fabric.model_memory_analyzer(dataset=dataset, workspace=workspace)

# Best Practice Analyser
fabric.run_model_bpa(dataset=dataset, workspace=workspace)

