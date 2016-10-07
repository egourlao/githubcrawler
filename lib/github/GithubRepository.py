from lib.github.GithubObject import GithubObject

class GithubRepository(GithubObject):
    def __init__(self, repo):
        """
        :param repo: Object of the github.Repository type.
        :return: Constructed GithubRepository object
        """
        self.repo = repo

    @classmethod
    def get_last_commit(self, stat):
        """
        :param stat: StatsContributor object.
        :return: Date in datetime.datetime type of the last commit's week.
        """
        maximum = stat.weeks[0].w
        committed_date = False
        for week in range(1, len(stat.weeks)):
            if ((maximum < stat.weeks[week].w and stat.weeks[week].c > 0) or \
                        (stat.weeks[week].c > 0 and not committed_date)):
                maximum = stat.weeks[week].w
                committed_date = True
        return maximum

    def print_description(self):
        """
        Runs a GitHub analysis of the wrapped repository and shows committers, and
        their level of commitment.
        :return: String to print.
        """
        description = "Stats for " + self.repo.full_name + " repo:\n\n"
        stats = self.repo.get_stats_contributors()
        if not stats:
            return "No repo stats to show."
        for stat in stats:
            description += "Username: %s, commits: %s, last commit: Week of the %s" % \
                           (stat.author.name if (stat.author and stat.author.name) else \
                                "Cannot show contributor's name",
                            str(stat.total) if stat.total else "Unknown",
                            self.get_last_commit(stat).strftime("%Y-%m-%d")) + "\n"
        return description
