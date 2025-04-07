%pip install semantic-link-labs

from packaging.version import Version
from importlib.metadata import version
import sempy.fabric as fabric
import sempy_labs as labs

labs.backup_semantic_model
labs.copy_semantic_model_backup_file
labs.restore_semantic_model

sempy_version = version('semantic-link-sempy')

if Version(sempy_version) < Version("0.9.3"):
    get_ipython().run_line_magic('pip', 'install semantic-link==0.9.3')

dataset = "Dev Tracker Dashboard" 
workspace = "Global - APAC - LA Development"

# Memory Analyser
fabric.model_memory_analyzer(dataset=dataset, workspace=workspace)

# Best Practice Analyser
fabric.run_model_bpa(dataset=dataset, workspace=workspace)


# Refresh model
dataset = '' # Enter your dataset name
workspace = None # Enter your workspace name (if set to None it will use the workspace in which the notebook is running)
labs.refresh_semantic_model(dataset=dataset, workspace=workspace) # Refresh Entire Model
labs.refresh_semantic_model(dataset=dataset, workspace=workspace, tables=['Sales', 'Geography']) # Refresh Specific tables
labs.refresh_semantic_model(dataset=dataset, workspace=workspace, partitions=["'Sales'[Sales FY20]", "'Sales'[Sales FY21]"]) # Refresh specific partitions
labs.get_semantic_model_refresh_history(dataset=dataset, workspace=workspace) # View refresh History





