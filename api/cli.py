from __future__ import annotations

import click

from api.application.evals.rubric_eval import run_promotion_evals


@click.group()
def cli() -> None:
    """Language tutor maintenance commands."""


@cli.command("evals")
def evals_command() -> None:
    results = run_promotion_evals()
    for name, passed in results.items():
        click.echo(f"{name}: {'PASS' if passed else 'FAIL'}")
    if not all(results.values()):
        raise click.ClickException("One or more evals failed")


if __name__ == "__main__":
    cli()
