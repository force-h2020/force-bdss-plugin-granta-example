import sys
import click
from subprocess import check_call

DEFAULT_PYTHON_VERSION = "2.7"
PYTHON_VERSIONS = ["2.7", "3.5"]

ADDITIONAL_CORE_DEPS = [
]

ADDITIONAL_PLATFORM_CORE_DEPS = {
    'rh6-x86_64': [
        'lxml==3.7.3-2'
    ],
    'osx-x86_64': [
        'lxml==3.7.3-1'
    ]
}

ADDITIONAL_PIP_DEPS_27 = [
]


@click.group()
def cli():
    pass


python_version_option = click.option(
    '--python-version',
    default=DEFAULT_PYTHON_VERSION,
    type=click.Choice(PYTHON_VERSIONS),
    show_default=True,
    help="Python version for the environment")


@cli.command(name="install", help="Creates the execution environment")
@python_version_option
def install(python_version):
    env_name = get_env_name(python_version)
    check_call(["edm", "install", "-e", env_name, "--yes"]
               + ADDITIONAL_CORE_DEPS
               + ADDITIONAL_PLATFORM_CORE_DEPS[current_platform()])

    if python_version == "2.7" and len(ADDITIONAL_PIP_DEPS_27):
        check_call([
            "edm", "run", "-e", env_name, "--",
            "pip", "install"] + ADDITIONAL_PIP_DEPS_27)

    check_call([
        "edm", "run", "-e", env_name, "--",
        "pip", "install", "-e", "."])


@cli.command(help="Run the tests")
@python_version_option
def test(python_version):
    env_name = get_env_name(python_version)

    check_call([
        "edm", "run", "-e", env_name, "--", "python", "-m", "unittest",
        "discover"
    ])


@cli.command(help="Run flake")
@python_version_option
def flake8(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "flake8", "."])


@cli.command(help="Runs the coverage")
@python_version_option
def coverage(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--",
                "coverage", "run", "-m", "unittest", "discover"])


@cli.command(help="Builds the documentation")
@python_version_option
def docs(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "make", "html"], cwd="doc")


def get_env_name(python_version):
    return "force-py{}".format(remove_dot(python_version))


def remove_dot(python_version):
    return "".join(python_version.split('.'))


def current_platform():
    platform = sys.platform
    if platform.startswith("linux"):
        return "rh6-x86_64"
    elif platform == "darwin":
        return "osx-x86_64"
    else:
        raise RuntimeError("platform {!r} not supported".format(platform))


if __name__ == "__main__":
    cli()
