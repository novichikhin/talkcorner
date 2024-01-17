from typing import Dict, Type

from talkcorner.settings.environments.app import AppSettings
from talkcorner.settings.environments.base import AppEnvTypes
from talkcorner.settings.environments.development import DevAppSettings
from talkcorner.settings.environments.production import ProdAppSettings

environments: Dict[str, Type[AppSettings]] = {
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.dev: DevAppSettings
}


def get_app_settings(app_env: AppEnvTypes = AppEnvTypes.dev) -> AppSettings:
    return environments[app_env]()
