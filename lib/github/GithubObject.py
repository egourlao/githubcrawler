class GithubObject():
    """
    Interface for every GitHub object.
    """
    def print_description(self):
        # Virtual method for outputting a string valuable for printing on a console for description.
        raise NotImplementedError("Cannot get description from a virtual GithubObject.")
