from cryptography.fernet import Fernet
from pathlib import Path
from getpass import getpass

from decouple import config

from .sso_access_forums.constants import Names

class UpdateFunctions:
    @classmethod
    def _append_value(cls, env_file, key, value, env_file_is_ini):
        if env_file_is_ini and value is str:
            value = value.replace(r"%", r"%%")

        env_file.write(f"\n{key}={value}")

    @classmethod
    def _update_jsconnect_client_id(cls, env_file, key, env_file_is_ini):
        new_value = getpass(f"Please enter a value for '{key}': ")
        cls._append_value(env_file, key, new_value, env_file_is_ini)

    @classmethod
    def _update_jsconnect_secret(cls, env_file, key, env_file_is_ini):
        new_value = getpass(f"Please enter a value for '{key}': ")
        cls._append_value(env_file, key, new_value, env_file_is_ini)

    @classmethod
    def _update_encryption_secret(cls, env_file, key, env_file_is_ini):
        print(f"Generating a value for '{key}'...")
        new_value = Fernet.generate_key()
        cls._append_value(env_file, key, new_value, env_file_is_ini)

    @classmethod
    def get_update_functions(cls):
        return {
            Names.Vars.jsconnect_client_id: cls._update_jsconnect_client_id,
            Names.Vars.jsconnect_secret: cls._update_jsconnect_secret,
            Names.Vars.encryption_secret: cls._update_encryption_secret
        }

_update_functions = UpdateFunctions.get_update_functions()

class ModulePathFinder:
    @classmethod
    def run(cls):
        return cls._verify_module_location()

    @classmethod
    def _verify_module_location(cls):
        # This script expects that the repo is currently in an AA installation's `custom-plugins` folder. If not, it'll quit.
        module_location = Path(__file__).expanduser().resolve()
        expected_parent_folder = "custom-plugins"
        actual_parent_folder = module_location.parent.parent.name

        if actual_parent_folder != expected_parent_folder:
            print(f"This script should be run as a plugin within an Alliance Auth installation. Install the {Names.app_name_raw} plugin to an installation and try with that plugin's 'init_secrets.py'.")
            raise RuntimeError("Script is not in a plugin folder as expected")

        return module_location

class TargetFinder:
    @classmethod
    def run(cls):
        return cls._find_unset_values()

    @classmethod
    def _find_unset_values(cls):
        results = []

        for key in _update_functions:
            if not cls._key_already_set(key):
                results.append(key)

        return results

    @classmethod
    def _key_already_set(cls, key) -> bool:
        try:
            return config(key) is not None
        except:
            return False

class ValueUpdater:
    @classmethod
    def run(cls, module_location, unset_values):
        env_file_path = cls._get_env_file_path(module_location)
        env_file_is_ini = env_file_path.suffix == ".ini"
        with cls._get_env_file(module_location) as env_file:
            cls._update_unset_values(unset_values, env_file, env_file_is_ini)

    @classmethod
    def _get_env_file(cls, module_location: Path):
        env_file_path = cls._get_env_file_path(module_location)
        return env_file_path.open('a')

    @classmethod
    def _update_unset_values(cls, unset_values, env_file, env_file_is_ini):
        if not unset_values:
            cls._handle_all_values_already_set()
            return

        for key in unset_values:
            update_function = _update_functions[key]
            if not update_function:
                raise RuntimeError(f"Don't have update function for key '{key}'; set one in _update_functions")

            update_function(env_file, key, env_file_is_ini)

    @classmethod
    def _handle_all_values_already_set(cls):
        print(f"All values required for plugin {Names.app_name_raw} are already set, quitting")

    @classmethod
    def _get_env_file_path(cls, module_location: Path) -> Path:
        expected_installation_root = module_location.parent.parent.parent
        expected_env_file = expected_installation_root / ".env"
        expected_ini_file = expected_installation_root / "settings.ini"

        if not expected_env_file.exists():
            if not expected_ini_file.exists():
                raise RuntimeError(f"No '.env' or 'settings.ini' configuration file found at expected locations '{str(expected_env_file)}' or '{str(expected_ini_file)}'")

            return expected_ini_file
        return expected_env_file

def main():
    module_location = ModulePathFinder.run()
    unset_values = TargetFinder.run()
    ValueUpdater.run(module_location, unset_values)

if __name__ == "__main__":
    main()