from abc import ABC, abstractmethod


class UserBase(ABC):
    """
    An abstract base class representing a user.

    This class serves as a template for different types of users in the system. It defines
    an abstract method `actions` that must be implemented by all subclasses.
    """
    @abstractmethod
    def actions(self):
        """
        Abstract method to be implemented by subclasses to define user-specific actions.
        """
        pass