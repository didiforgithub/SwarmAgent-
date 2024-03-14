## Usage
To use SwarmAgent, follow these simple steps:

1. Define Your Scene: Use the --idea argument to describe the scene you wish to simulate. This field is required for the simulation to proceed.

2. Choose Configuration Mode: Decide whether you want to use the default automatic configuration (--config auto) or load a pre-existing configuration (--config load). The default mode is auto.

3. Select Update Rules: Specify the update rules for your agents with the --update_rule argument. You can choose from IM, PC, or BEST. The default rule is BEST.

4. Set Agent Counts: Determine the number of agents involved in the simulation with the --agent_counts argument. The default count is 3.

5. Intervene in Simulation: If you wish to intervene in the simulation, set the --intervene argument to True. By default, it is set to False.

6. Specify Version Name: Provide a name for your simulation version using the --version_name argument. The default name is temp.

### Example Command Line
Here's an example of how to run a simulation with SwarmAgent:
```bash
pip install -r requirements.txt
export OPENAI_API_KEY = "your key"
export BASE_URL = "base url if you use service other than openai"
```

```bash
python run.py --idea "Your Scene Description" --config auto --update_rule BEST --agent_counts 3 --intervene False --version_name temp
```
### 
Functions
auto_config: This function generates a simulation environment based on the provided idea and version name. It saves the configuration locally and runs the simulation.

load_config: This function loads a pre-configured simulation from local storage and runs it with the specified update rules and intervention settings.