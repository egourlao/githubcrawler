from lib.github.GithubObject import GithubObject

class GithubUser(GithubObject):
    def __init__(self, user):
        """
        :param user: Object of the github.NamedUser type.
        :return: Constructed GithubUser object
        """
        self.user = user

    def print_general_information(self):
        """
        :return: Prints general information about the user
        """
        user = self.user
        return "################\n\nName:" + "\t\t" + (user.name or user.login or "None") + "\nEmail address:\t" + \
               (user.email or "None") + "\n\n" + "Bio:\t\t" + (user.bio or "None") + "\nLocation:\t" + \
               (user.location or "None") + "\nCompany:\t" + (user.company or "None") + \
               "\nBlog:\t\t" + (user.blog or "None") + "\n"
