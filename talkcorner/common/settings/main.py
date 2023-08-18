from typing import Dict, Type

from talkcorner.common.settings.environments.app import AppSettings
from talkcorner.common.settings.environments.base import AppEnvTypes
from talkcorner.common.settings.environments.development import DevAppSettings
from talkcorner.common.settings.environments.production import ProdAppSettings

environments: Dict[str, Type[AppSettings]] = {
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.dev: DevAppSettings
}


def get_app_settings(app_env: AppEnvTypes = AppEnvTypes.dev) -> AppSettings:
    return environments[app_env]()
