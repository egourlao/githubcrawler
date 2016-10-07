import re

from lib.github.GithubHumanUser import GithubHumanUser
from lib.github.GithubOrganization import GithubOrganization
from lib.github.GithubRepository import GithubRepository
from lib.github.NotConnectedException import NotConnectedException


class GithubObjectFactory():
    """
    Factory taking into input on a GitHub URL to render a repo, an org or a human user.
    It takes during construction a PyGitHub client.
    """
    def __init__(self, client, connected=False):
        self.client = client
        self.connected = connected

    github_radical = '(?:\s)*http(?:s)?://(?:www.)?github.com/'
    regex_repo = github_radical + '([\d\w\-\_]+)/(\w+)(?:/)?(?:\s)*\Z'
    regex_user = github_radical + '([\d\w\-\_]+)(?:/)?(?:\s)*\Z'

    def get_github_repo(self, username, repo):
        """
        :param username: string
        :param repo: string
        :return: GithubRepository
        """
        if not self.connected:
            raise NotConnectedException()
        repo = self.client.get_user(username).get_repo(repo)
        return GithubRepository(repo)

    def get_github_user(self, username):
        """
        :param username: string
        :return: GithubUser subclass
        """
        user = self.client.get_user(username)
        if user.type == "User":
            return GithubHumanUser(user)
        else:
            return GithubOrganization(user)

    def get_github_object(self, url):
        """
        :param url: string representing a GitHub URL
        :return: GithubObject subclass or None
        """
        regex_result = re.search(self.regex_repo, url)
        if regex_result:
            return self.get_github_repo(regex_result.group(1), regex_result.group(2))
        regex_result = re.search(self.regex_user, url)
        if regex_result:
            return self.get_github_user(regex_result.group(1))
        return None
