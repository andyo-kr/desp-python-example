from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
from enum import Enum


class EnvironmentName(Enum):
    TEST = 'test'
    DEV = 'dev'


@dataclass_json
@dataclass
class Environment:
    broker_list: str
    name: EnvironmentName
    scheme_registry: str


@dataclass_json
@dataclass
class DespEnvironments:
    desp_environments: List[Environment]


env_file = f"etc/environments.json"


class DespEnvironment:
    def __init__(self):
        self.desp_environments = None
        self.current_environment: Environment = None
        with open(env_file, 'r') as file:
            data = file.read()
            self.desp_environments: DespEnvironments = DespEnvironments.from_json(data)
        self._set_environment(EnvironmentName.TEST)

    def _set_environment(self, environment: EnvironmentName):
        env = next((e for e in self.desp_environments.desp_environments if e.name == environment), None)
        if env is None:
            print (f"environment {environment} not defined in {env_file} ")
        else:
            self.current_environment = env
            print(self.current_environment.broker_list)





if __name__ == '__main__':
    de: DespEnvironment = DespEnvironment()
    print(de.desp_environments)
    print(de.current_environment)
