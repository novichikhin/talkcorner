from talkcorner.common.settings.environments.app import AppSettings


class ProdAppSettings(AppSettings):
    debug: bool = False
