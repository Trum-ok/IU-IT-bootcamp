class UserNotFoundError(Exception):
    pass


class UserExistsError(Exception):
    pass


class CompanyNotFoundError(Exception):
    pass


class SubscriptionNotFoundError(Exception):
    pass


class SubscriberNotFoundError(Exception):
    pass


class PublicationNotFoundError(Exception):
    pass


class SubscriptionExists(Exception):
    pass


class ModeratorIsNotAuthor(Exception):
    pass
