import typer
from . import creator

cli = typer.Typer()

@cli.command()
def module(name: str):
    creator.create_module(name, "src/")
    typer.echo(f"Module {name} created")

@cli.command()
def init():
    creator.init_project()
    typer.echo("Project initialized")