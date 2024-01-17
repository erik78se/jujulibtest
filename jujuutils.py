from juju import jasyncio
from pprint import pprint
import os
from juju.model import Model
import yaml


def get_controller_cacert(controller_name):
  """
  Reads a controller cacert from the effective unix user home.
  
  ~/.local/share/juju/controllers.yaml
  
  """
    # Define the path to the controllers.yaml file
    controllers_yaml_path = os.path.expanduser("~/.local/share/juju/controllers.yaml")

    try:
        with open(controllers_yaml_path, 'r') as file:
            controllers_yaml = yaml.safe_load(file)

            # Check if the specified controller exists in the YAML
            if controller_name in controllers_yaml.get('controllers', {}):
                # Retrieve and return the CA certificate for the specified controller
                return controllers_yaml['controllers'][controller_name].get('ca-cert', '')
            else:
                return f"Controller '{controller_name}' not found in controllers.yaml"

    except FileNotFoundError:
        return "controllers.yaml file not found"
    except Exception as e:
        return f"An error occurred: {e}"
