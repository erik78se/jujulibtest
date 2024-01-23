#!/usr/bin/env python3
import sys
from juju import jasyncio
from juju.model import Model

async def connect_to_my_model():
    """There are multiple ways of connecting to a model.
    The simples one is to just run connect() which will auto connect to the currently switched model

    You can also fully customize that connection like:

        await model.connect(endpoint=_CONTROLLER['endpoint'],
                            username=_CONTROLLER['username'],
                            password=_CONTROLLER['password'],
                            uuid=model_uuid,
			                cacert=_CONTROLLER['cacert'])
    
    """
    m = Model()
    await m.connect()
    return m

async def get_model_state():
    m = connect_to_my_model()

    print(f"############ Model Status ({m.name}) ############")
    print("## Cloud tag: ", m.info['cloud-tag'] )
    print("## Cloud region : ", m.info['cloud-region'] )

    print("Deploying the ubuntu charm (see 'juju info ubuntu')")
    await m.deploy('ubuntu')

    # You can check out some stuff while it's being deployed
    apps = m.applications
    units = apps['ubuntu'].units
    unit = units[0]
    machines = m.machines

    await jasyncio.sleep(5)

    print(f"""You can check out some stuff while it's being deployed:
          apps: {apps}
          units: {units}
          my-unit: {unit}
          machines: {machines} <-- this may come up as empty because the container's not created yet
          """)

    # unit status will probably be pending or allocating (during deploy stages)
    print(f"Unit agent status: {unit.agent_status}")
    # workload status will probably be waiting
    print(f"Unit workload status: {unit.workload_status}")

    print("Wait until the application ubuntu is ready to go (active and idle)")
    await m.wait_for_idle()
    print("ready!")

    print(f"Unit agent status after wait_for_idle should be idle: {unit.agent_status}")
    print(f"Unit workload status after wait_for_idle should be active: {unit.workload_status}")

    machine = unit.machine
    print(f"""Get some info about the machine of that unit:
                machine status: {machine.status}
                machine status message: {machine.status_message}
                machine agent status: {machine.agent_status}
                machine series: {machine.series}
                machine dns_name: {machine.dns_name}
          """)

    print("Let's run an action on that unit:")
    action = await unit.run('unit-get public-address')
    print(f"action results: {action.results}")

    print("Cleaning up.")
    await m.remove_application('ubuntu')
    print("Disconnecting.")
    await m.disconnect()
    print("Example successful.")

if __name__ == '__main__':
    jasyncio.run(get_model_state())
