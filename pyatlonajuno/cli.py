import click

from . import lib


@click.group()
@click.option("--url")
@click.option("--debug/--no-debug", default=False)
@click.option("--timeout", default=5, type=int,
              help="Seconds to wait for telnet responses")
@click.pass_context
def cli(ctx, url, debug, timeout):
    """ Juno451 CLI.

    This cli is for controling the Atlona Juno 451 HDMI switch.
    """
    ctx.obj = lib.Juno451(url, debug, timeout)


@cli.command()
@click.pass_context
def getpowerstate(ctx):
    "Determine if the Juno is currently powered up"
    print(ctx.obj.getPowerState())


@cli.command()
@click.option("--state", type=click.Choice(["on", "off"]), required=True)
@click.pass_context
def setpowerstate(ctx, state):
    "Turn the Juno on or off"
    print(ctx.obj.setPowerState(state))


@cli.command()
@click.pass_context
def getinputstate(ctx):
    "Get the connection status of the four inputs, True=connected"
    print(ctx.obj.getInputState())


@cli.command()
@click.pass_context
def getsource(ctx):
    "Get the currently active input"
    print(ctx.obj.getSource())


@cli.command()
@click.option("--source",
              type=click.Choice(["1", "2", "3", "4"]),
              required=True)
@click.pass_context
def setsource(ctx, source):
    "Select an input"
    print(ctx.obj.setSource(source))


def main():
    cli()


if __name__ == "__main__":
    cli()
