from talkcorner.common.exceptions.main import Talkcorner


class UnableUpdateSubforum(Talkcorner):
    pass


class UnableCreateSubforum(Talkcorner):
    pass


class ParentChildForumsAlreadyExists(UnableCreateSubforum):
    pass
