#!/usr/bin/env python3
import sys
from juju import jasyncio
from pprint import pprint
import jujuutils
from juju.model import Model
from juju.status import formatted_status

# Store some controller connection details.
_CONTROLLER1={'endpoint': '192.168.1.1:17070',
       'username': 'my-service',
       'password': '12345678910111213',
       'cacert': jujuutils.get_controller_cacert('my-controller') } 

# Store some other connection details.
_CONTROLLER2={'endpoint': '192.168.2.1:17070',
       'username': 'my-service',
       'password': '123456789101112131415',
       'cacert': jujuutils.get_controller_cacert('dwellir2-pionen') }

# Use one of the controllers
_CONTROLLER=_CONTROLLER1


async def get_model_state(model_uuid):
    """
    Retrieves the current state of a Juju model and returns a dictionary
    See: https://github.com/juju/python-libjuju/blob/2581b0ced1df6201c6b7fd8cc0b20dcfa9d97c51/juju/model.py
   
    See also: https://github.com/juju/python-libjuju/blob/2581b0ced1df6201c6b7fd8cc0b20dcfa9d97c51/juju/client/_client7.py
    for schema definition example
 
    The state contains: model, charm, application, unit, and machine information (dict)

    The FullStatus is static where the state.<thing> is updated automatically....
    
    """
    # print(_CONTROLLER)
    model = Model()
    await model.connect(endpoint=_CONTROLLER['endpoint'],
                        username=_CONTROLLER['username'],
                        password=_CONTROLLER['password'],
                        uuid=model_uuid,
			cacert=_CONTROLLER['cacert'])

    # Gets a <juju.client._definitions.FullStatus>
    # 'applications', 'branches', 'connect', 
    # 'controller_timestamp', 'from_json', 'get', 
    # 'machines', 'model', 'offers', 'relations', 
    # 'remote_applications', 'rpc', 'serialize', 
    # 'splitEntries', 'to_json', 'unknown_fields'
    fullstatus = await model.get_status()

    # Gets a juju.client._definitions.ModelStatusInfo
    modelstatus = fullstatus.model
    
    print()

    # Print the status for the model as json
    print(f"############ Model Status ({model.name}) ############")
    j = modelstatus.to_json()
    print("## Cloud tag: ", model.info['cloud-tag'] )
    print("## Cloud region : ", model.info['cloud-region'] )
    print("## Model status json: ", modelstatus.to_json())

    # Gets applications from this model as <Application>s
    applications = model.applications
    for idx, a in applications.items():
        print(f"## Application: {a.name} ({a.charm_name}) {a.status}")

        # Get the units for this application as <Unit>
        for u in a.units:
            print(f"##  Unit: {u.name} ({u.public_address}) Message: {u.workload_status_message}")
            m = u.machine
            print(f"##     Machine Hostname: {m.hostname} instance-id: {m.safe_data['instance-id']} is {m.status}")

    # Gets machines as a tuples of <index>,juju.client._definitions.MachineStatus
    # 'agent_status', 'base', 'connect', 'constraints', 
    # 'containers', 'display_name', 'dns_name', 'from_json', 'get', 
    # 'hardware', 'has_vote', 'hostname', 'id_', 'instance_id', 'instance_status', 
    # 'ip_addresses', 'jobs', 'lxd_profiles', 'modification_status', 'network_interfaces', 
    # 'primary_controller_machine', 'rpc', 'serialize', 'series', 'splitEntries', 
    # 'to_json', 'unknown_fields', 'wants_vote'
    machines = fullstatus.machines

    # for idx, m in machines.items():
    #    print(f"### Machine: {m.instance_id} {m.ip_addresses[0]}")
    #    pprint(m.to_json())
 
    await model.disconnect()
    return model.state.state


async def main(model_uuid):
    model_state = await get_model_state(model_uuid)
    # pprint(model_state)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <model_uuid>")
        sys.exit(1)

    model_uuid_arg = sys.argv[1]
    jasyncio.run(main(model_uuid_arg))
