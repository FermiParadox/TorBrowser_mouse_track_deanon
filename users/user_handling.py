from analysis.conversion import DataExtractor
from users.user_base import User


class AllUsers(set):
    @property
    def ips(self):
        return {str(u.ip) for u in self}

    @property
    def ids(self):
        return {str(u.id) for u in self}

    def add(self, other: User):
        """When added element is already present, it replaces the existing one,
        instead of "editing" it.
        Not very efficient, but should be ok for testing.

        By default `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


all_users = AllUsers()


class UserCreator:
    def __init__(self, req):
        self.req = req
        self.user: User

    def _created_user(self):
        extractor = DataExtractor(req=self.req)

        return User(id=extractor.user_id,
                    ip=extractor.user_ip,
                    all_txy=extractor.txy_lists,
                    entry_txy_lists=extractor.entry_txy,
                    exit_txy_lists=extractor.exit_txy,
                    exit_indices=extractor.exit_indices(),
                    entry_indices=extractor.entry_indices())

    def create_and_insert_user(self):
        self.user = self._created_user()
        all_users.add(self.user)
