from lib.github.GithubUser import GithubUser

class GithubOrganization(GithubUser):
    """
    GithubUser subclass representing an organisation.
    """
    def print_description(self):
        # Prints relevant information about the organization.
        return self.print_general_information()
