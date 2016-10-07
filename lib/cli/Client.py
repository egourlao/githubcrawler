import sys

from github import Github, BadCredentialsException, RateLimitExceededException

from lib.github.GithubObjectFactory import GithubObjectFactory
from lib.github.NotConnectedException import NotConnectedException

class Client():
    """
    Represents the interface between the business models and the CLI.
    """
    def __init__(self, username=None, password=None, out=sys.stdout):
        """
        :param username: string
        :param password: string
        :param out: sys.stdout or io.StringIO object.
        """
        self.out = out
        if username and password:
            self.g = Github(username, password)
            self.connected = True
        else:
            self.g = Github()
            self.connected = False

    def main(self, url):
        """
        Processes the URL to print a description out if it is a GitHub user or repo URL.
        :param url: string
        :return: None
        """
        factory = GithubObjectFactory(self.g, self.connected)
        try:
            github_object = factory.get_github_object(url)
            if github_object:
                self.out.write(github_object.print_description())
            else:
                self.out.write("No GitHub object was found for this URL.")
        except NotConnectedException:
            self.out.write("You need to provide GitHub credentials to see repository activity - [-h] for help.")
        except BadCredentialsException:
            self.out.write("Bad user credentials, please try again.")
        except RateLimitExceededException:
            self.out.write("The rate limit has been exceeded, please log in or wait some time to use the app again.")
        except Exception:
            self.out.write("Something happened, please try again.")
