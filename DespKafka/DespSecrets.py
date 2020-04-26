from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class Secret:
    name: str
    user: str
    password: str


@dataclass_json
@dataclass
class Secrets:
    secrets: List[Secret]


secrets_file = f"secrets/secrets.json"
orig_secrets_file = f"secrets/rename_me.json"


class DespSecrets:
    def __init__(self):
        self.secrets = None
        try:
            with open(secrets_file, 'r') as file:
                data = file.read()
                self.secrets: Secrets = Secrets.from_json(data)
        except IOError:
            print(f"Secrets file '{secrets_file}' does not exist.  "
                  f"Did you rename '{orig_secrets_file}' to '{secrets_file}' ?")
            exit(1)

    def get_secret(self, name='default'):
        secret = next((s for s in self.secrets.secrets if s.name == name), None)
        if secret is None:
            print(f"No secret named '{name}' could be found in '{secrets_file}'")
            exit(1)
        return secret


if __name__ == '__main__':
    de: DespSecrets = DespSecrets()
    de.get_secret()
    print(de.secrets)
