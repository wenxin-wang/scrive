# A wrapper library for git

from subprocess import call

class Repository:
    @staticmethod
    def get_toplevel():
        """Get the toplevel of a project"""
        call(["git", "rev-parse", "--show-toplevel"])
