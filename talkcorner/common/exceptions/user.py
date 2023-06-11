from talkcorner.common.exceptions.main import Talkcorner


class UnableCreateUser(Talkcorner):
    pass


class UsernameAlreadyExists(UnableCreateUser):
    pass


class EmailAlreadyExists(UnableCreateUser):
    pass
