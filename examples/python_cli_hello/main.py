"""Python Cli Hello

Example generated CLI that greets users.
Generated using AGF template 'python_cli_basic'.
"""
import click


def greet(name: str) -> str:
    return f"Hello, {name}!"


@click.command()
@click.option("--name", default="world", help="Name to greet")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def main(name: str, verbose: bool) -> None:
    """Entry point for Python Cli Hello."""
    message = greet(name)
    if verbose:
        click.echo(f"[python_cli_hello] {message}")
    else:
        click.echo(message)


if __name__ == "__main__":
    main()
