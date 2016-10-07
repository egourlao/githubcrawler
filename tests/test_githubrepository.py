from datetime import datetime
from unittest import TestCase

from lib.github.GithubRepository import GithubRepository


class DummyAuthor():
    def __init__(self, n):
        self.name = n


class DummyStatWeek():
    def __init__(self, w, c):
        self.w = w
        self.c = c


class DummyStat():
    def __init__(self, author_name, total, *args):
        self.author = DummyAuthor(author_name)
        self.total = total
        self.weeks = list()
        for stat in args:
            self.weeks.append(stat)


def getDummyRepo(name, *args):
    class DummyRepo():
        full_name = name

        @classmethod
        def get_stats_contributors(self):
            return args
    return DummyRepo()


class TestGithubRepository(TestCase):

    def test_last_commit(self):
        """
        Checking the method get_last_commit returns the last commit with more than 1 commit
        :return:
        """
        stat = DummyStat("fat", 150, DummyStatWeek(datetime(2015, 1, 1), 150), DummyStatWeek(datetime(2017, 1, 1), 1),
                         DummyStatWeek(datetime(2014, 1, 1), 150), DummyStatWeek(datetime(2016, 1, 1), 2000))
        self.assertEqual(datetime(2017, 1, 1), GithubRepository.get_last_commit(stat))
        stat = DummyStat("fat", 150, DummyStatWeek(datetime(2015, 1, 1), 150), DummyStatWeek(datetime(2017, 1, 1), 0),
                         DummyStatWeek(datetime(2014, 1, 1), 150), DummyStatWeek(datetime(2016, 1, 1), 2000))
        self.assertEqual(datetime(2016, 1, 1), GithubRepository.get_last_commit(stat))
        stat = DummyStat("fat", 150, DummyStatWeek(datetime(2015, 1, 1), 0), DummyStatWeek(datetime(2017, 1, 1), 0),
                         DummyStatWeek(datetime(2014, 1, 1), 150), DummyStatWeek(datetime(2016, 1, 1), 0))
        self.assertEqual(datetime(2014, 1, 1), GithubRepository.get_last_commit(stat))

    def test_stats_contributors(self):
        """
        Checking the description contains the correct values for the contributors
        :return:
        """
        DummyRepo = getDummyRepo("jj", DummyStat("fat", 150, DummyStatWeek(datetime(2015, 1, 1), 0),
                                                 DummyStatWeek(datetime(2017, 1, 1), 0),
                                                 DummyStatWeek(datetime(2014, 1, 1), 150)),
                                 DummyStat("izs", 10, DummyStatWeek(datetime(2018, 3, 1), 0),
                                           DummyStatWeek(datetime(2019, 1, 1), 3),
                                           DummyStatWeek(datetime(2014, 1, 1), 150)))
        g = GithubRepository(DummyRepo)
        description = g.print_description()
        self.assertRegex(description, "Username: fat, commits: 150, last commit: Week of the 2014-01-01")
        self.assertRegex(description, "Username: izs, commits: 10, last commit: Week of the 2019-01-01")
