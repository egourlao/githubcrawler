import sys

from lib.github.GithubUser import GithubUser

class GithubHumanUser(GithubUser):
    """
    Represents a wrapper for a human GitHub user.
    """
    def print_repos_languages(self):
        """
        :return: String that represents a console description of the repositories the user has created and contributed
        to, and the languages he's used in these projecs.
        """
        # Repositories
        languages = dict()
        description = "################\n\nRepositories\n"
        repos = self.user.get_repos()
        for repo in repos:
            description += repo.full_name + (" (Fork of " + repo.parent.full_name + ")" if repo.parent else "") + "\n"
            if repo.language in languages:
                languages[repo.language] = languages[repo.language] + 1
            else:
                languages[repo.language] = 1

        # Languages
        description += "\n################\n\nLanguages from the least to the most used:\n\n"
        if sys.version_info >= (3, 0):
            lang_list = [{'name': lang, 'nb': nb} for lang, nb in languages.items()]
        else:
            lang_list = [{'name': lang, 'nb': nb} for lang, nb in languages.iteritems()]
        for lang in sorted(lang_list, key=lambda lang: lang['nb']):
            description += lang['name'] + ": " + str(lang['nb']) + "\n"

        return description

    def print_description(self):
        # Prints relevant information about the user.
        return self.print_general_information() + self.print_repos_languages()
