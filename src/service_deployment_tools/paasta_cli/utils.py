import fnmatch
import glob
import os


def load_method(module_name, method_name):
    """
    Return a function given a module and method name
    :param module_name: a string
    :param method_name: a string
    :return: a function
    """
    module = __import__(module_name, fromlist=[method_name])
    method = getattr(module, method_name)
    return method


def file_names_in_dir(directory):
    """
    Read and return the files names in the directory
    :return: a list of strings such as ['list','check'] that correspond to the
    files in the directory without their extensions
    """
    dir_path = os.path.dirname(os.path.abspath(directory.__file__))
    path = os.path.join(dir_path, '*.py')

    for file_name in glob.glob(path):
        basename = os.path.basename(file_name)
        root, _ = os.path.splitext(basename)
        if root == '__init__':
            continue
        yield root


def is_file_in_dir(file_name, path):
    """
    Recursively search path for file_name
    :param file_name: a string of a file name to find
    :param path: a string path
    :param file_ext: a string of a file extension
    :return: a boolean
    """
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, file_name):
                return os.path.join(root, filename)
    return False


def check_mark():
    """
    Return output the can print a checkmark
    """
    return PaastaColors.green(u'\u2713'.encode('utf-8'))


def x_mark():
    """
    Return output the can print an x mark
    """
    return PaastaColors.red(u'\u2717'.encode('utf-8'))


def arrow():
    """
    Return output that can print an arrow going down then right
    """
    return PaastaColors.green(u'\u21B3'.encode('utf-8'))


def success(msg):
    return "%s %s" % (check_mark(), msg)


def sub_success(msg):
    return "%s %s" % (arrow(), msg)


def failure(msg, link):
    return "%s %s %s" % (x_mark(), msg, PaastaColors.blue(link))


class PaastaColors:
    """
    Collection of static variables and methods to assist in coloring text
    """
    # ANSI colour codes
    DEFAULT = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'

    @staticmethod
    def blue(text):
        return PaastaColors.color_text(PaastaColors.BLUE, text)

    @staticmethod
    def green(text):
        return PaastaColors.color_text(PaastaColors.GREEN, text)

    @staticmethod
    def red(text):
        return PaastaColors.color_text(PaastaColors.RED, text)

    @staticmethod
    def color_text(color, text):
        return color + text + PaastaColors.DEFAULT


class PaastaCheckMessages:
    """
    Collection of message printed out by 'paasta check'.  Helpful as it avoids
    cumbersome maintenance of the unit tests.
    """

    DEPLOY_YAML_FOUND = success("deploy.yaml exists for a Jenkins pipeline")

    DEPLOY_YAML_MISSING = failure(
        "No deploy.yaml exists, so your service cannot be deployed.\n  "
        "Push a deploy.yaml and run `paasta build-deploy-pipline`.\n  "
        "More info:", "http://y/yelpsoa-configs")

    DOCKERFILE_FOUND = success("Found Dockerfile")

    DOCKERFILE_MISSING = failure(
        "Dockerfile not found. Create a Dockerfile and try again.\n  "
        "More info:", "http://y/paasta-runbook-dockerfile")

    DOCKERFILE_VALID = success(
        "Your Dockerfile pulls from the standard Yelp images.")

    DOCKERFILE_INVALID = failure(
        "Your Dockerfile does not use the standard Yelp images.\n  "
        "This is bad because your `docker pulls` will be slow and you won't be "
        "using the local mirrors.\n  "
        "More info:", "http://y/paasta-runbook-dockerfile")

    MARATHON_YAML_FOUND = success("Found marathon.yaml file")

    MARATHON_YAML_MISSING = failure(
        "No marathon.yaml exists, so your service cannot be deployed.\n  "
        "Push a deploy.yaml and run `paasta build-deploy-pipline`.\n  "
        "More info:", "http://y/yelpsoa-configs")

    SENSU_MONITORING_FOUND = success(
        "monitoring.yaml found for Sensu monitoring")

    SENSU_MONITORING_MISSING = failure(
        "Your service is not using Sensu (monitoring.yaml).\n  "
        "Please setup a monitoring.yaml so we know where to send alerts.\n  "
        "More info:", "http://y/monitoring-yaml")

    SENSU_TEAM_MISSING = failure(
        "Cannot get team name. Ensure 'team' field is set in monitoring.yaml.\n"
        "  More info:", "http://y/monitoring-yaml")

    SERVICE_NAME_NOT_FOUND = "Could not figure out the service name.\n" \
                             "Please run this from the root of a copy " \
                             "(git clone) of your service."

    SMARTSTACK_YAML_FOUND = success("Found smartstack.yaml file")

    SMARTSTACK_YAML_MISSING = failure(
        "Your service is not setup on smartstack yet and will not be "
        "automatically load balanced.\n  "
        "More info:", "http://y/smartstack-cep323")

    SMARTSTACK_PORT_MISSING = failure(
        "Could not determine port. "
        "Ensure 'proxy_port' is set in smartstack.yaml.\n  "
        "More info:", "http://y/smartstack-cep323")

    @staticmethod
    def sensu_team_found(team_name):
        return success(
            "Your service uses Sensu and team %s will get alerts." % team_name)

    @staticmethod
    def smartstack_port_found(instance, port):
        return sub_success(
            "Instance %s of your service is using smartstack port %d "
            "and will be automatically load balanced" % (instance, port))
