from unittest import TestCase

from lib.github.GithubHumanUser import GithubHumanUser
from lib.github.GithubObjectFactory import GithubObjectFactory
from lib.github.GithubOrganization import GithubOrganization
from lib.github.GithubRepository import GithubRepository
from lib.github.NotConnectedException import NotConnectedException


class DummyRepo():
    pass


class DummyUser():
    def __init__(self, type):
        self.type = type

    def get_repo(self, n):
        return DummyRepo()


class DummyClient():
    def get_user(self, t):
        return DummyUser(t)


class DummyHumanUserClient():
    def get_user(self, n):
        return DummyUser('User')


class DummyOrganizationClient():
    def get_user(self, n):
        return DummyUser('Organization')


class TestGithubObjectFactory(TestCase):

    def test_not_connected(self):
        """
        Checking the factory throws the right exception if a repo is called while not connected
        :return:
        """
        g = GithubObjectFactory("dummy", False)
        with self.assertRaises(NotConnectedException):
            g.get_github_object("https://github.com/dotpy3/akanban")

    def test_renders_repo(self):
        """
        Checking calling repo URLs returns GithubRepository objects
        :return:
        """
        valid_repo_urls = ["http://github.com/dotpy3/kanban",
                           "https://github.com/twitter/bootstrap/",
                           "https://www.github.com/sqreen/node_client33/"]
        g = GithubObjectFactory(DummyClient(), True)
        for url in valid_repo_urls:
            self.assertEqual(type(g.get_github_object(url)), GithubRepository)

    def test_renders_human(self):
        """
        Checking calling user URLs returns GithubHumanUser objects
        :return:
        """
        valid_repo_urls = ["http://github.com/dotpy3/",
                           "https://github.com/twitter",
                           "https://www.github.com/sqreen/"]
        g = GithubObjectFactory(DummyHumanUserClient(), True)
        for url in valid_repo_urls:
            self.assertEqual(type(g.get_github_object(url)), GithubHumanUser)

    def test_renders_org(self):
        """
        Checking calling org URLs returns GithubOrganization objects
        :return:
        """
        valid_repo_urls = ["http://github.com/dotpy3/",
                           "https://github.com/twitter/",
                           "https://www.github.com/sqreen/"]
        g = GithubObjectFactory(DummyOrganizationClient(), True)
        for url in valid_repo_urls:
            self.assertEqual(type(g.get_github_object(url)), GithubOrganization)
