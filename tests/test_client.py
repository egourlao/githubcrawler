import io

from unittest import mock, TestCase

from github import BadCredentialsException, RateLimitExceededException

from lib.cli.Client import Client
from lib.github.NotConnectedException import NotConnectedException


class DummyObject():
    def print_description(self):
        return "hello world"


class DummyFactory():
    def get_github_object(self, url):
        if url:
            return DummyObject()
        else:
            return False

def RaisingExceptionFactory(ex):
    class DummyRaisingExceptionFactory():
        def get_github_object(self, url):
            raise ex
    return DummyRaisingExceptionFactory


class TestClient(TestCase):

    def test_connection(self):
        """
        Testing the client takes connected when credentials given, and not when no credentials given
        :return:
        """
        conn = Client("jj", "pw")
        self.assertTrue(conn.connected)
        noconn = Client()
        self.assertFalse(noconn.connected)

    @mock.patch('lib.cli.Client.GithubObjectFactory')
    def test_printing_description(self, mock_factory):
        """
        Checking the description of the object given by the factory is printed
        :param mock_factory: Mock representing the GithubObjectFactory
        :return:
        """
        factory = mock_factory.return_value
        factory.get_github_object.return_value = DummyObject()
        out = io.StringIO()
        conn = Client(out=out)
        conn.main("test")
        self.assertEqual(out.getvalue().strip(), "hello world")

    @mock.patch('lib.cli.Client.GithubObjectFactory')
    def test_printing_error(self, mock_factory):
        """
        Checking the right error messages are printed if there is an error
        :param mock_factory: Mock representing the GithubObjectFactory
        :return:
        """
        for (exception, given_error) in [(NotConnectedException(), "You need to provide GitHub credentials to see" + \
                " repository activity - [-h] for help."),
                                   (BadCredentialsException(403, "random_data"), "Bad user credentials, please try" + \
                                           " again."),
                                   (RateLimitExceededException(403, "random_data"), "The rate limit has been exceed" + \
                                           "ed, please log in or wait some time to use the app again."),
                                   (Exception(), "Something happened, please try again.")]:
            factory = mock_factory.return_value
            factory.get_github_object.side_effect = exception
            out = io.StringIO()
            conn = Client(out=out)
            conn.main("test")
            self.assertEqual(out.getvalue().strip(), given_error)
