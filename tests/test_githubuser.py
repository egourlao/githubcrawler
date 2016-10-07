from unittest import TestCase

from lib.github.GithubHumanUser import GithubHumanUser
from lib.github.GithubOrganization import GithubOrganization
from lib.github.GithubUser import GithubUser


class DummyRepo():
    def __init__(self, n, l, p_f=None):
        self.full_name = n
        self.language = l
        if p_f:
            self.parent = DummyRepo(p_f, l)
        else:
            self.parent = None


class DummyUser():
    def __init__(self, *args):
        self.repos = args

    def get_repos(self):
        return self.repos

class DummyFullUser():
    name = "fat"
    bio = "testbio"
    email = "johnny@appleseed.com"
    location = "Paris, FR"
    company = "Sqreen"
    blog = None

    def get_repos(self):
        return []


class TestGithubUser(TestCase):

    def test_user_descriptions(self):
        """
        Checking the descriptions contain the repositories, and indication of forks, and languages
        :return:
        """
        g = GithubHumanUser(DummyUser(DummyRepo("dotpy3/kanban", "PHP"),
                                      DummyRepo("dotpy3/ajb", "Python"),
                                      DummyRepo("dotpy3/ajc", "HTML", "fat/ajc"),
                                      DummyRepo("dotpy3/bootstrap", "HTML", "twitter/bootstrap")))
        description = g.print_repos_languages()
        self.assertRegex(description, "dotpy3/kanban")
        self.assertRegex(description, "dotpy3/ajb")
        self.assertRegex(description, "dotpy3/ajc \(Fork of fat/ajc\)")
        self.assertRegex(description, "dotpy3/bootstrap \(Fork of twitter/bootstrap\)")
        self.assertRegex(description, "PHP: 1")
        self.assertRegex(description, "HTML: 2")
        self.assertRegex(description, "Python: 1")

    def test_user_standard_description(self):
        """
        Checking the standard descriptions contain the correct values
        :return:
        """
        g = GithubUser(DummyFullUser())
        g2 = GithubHumanUser(DummyFullUser())
        g3 = GithubOrganization(DummyFullUser())
        description1 = g.print_general_information()
        description2 = g2.print_general_information()
        description3 = g2.print_description()
        description4 = g3.print_description()
        description5 = g3.print_general_information()
        for i in ["Name:(\s*)fat", "Bio:(\s*)testbio", "Email address:(\s*)johnny@appleseed.com", "Company:(\s*)Sqreen",
                  "Location:(\s*)Paris, FR", "Blog:(\s*)None"]:
            for j in [description1, description2, description3, description4, description5]:
                self.assertRegex(j, i)
