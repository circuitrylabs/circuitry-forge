"""Command-line interface for scenario-forge."""

import json

import click
from rich import print as rprint
from rich.json import JSON

from scenario_forge.backends.ollama import OllamaBackend
from scenario_forge.datastore import ScenarioStore


@click.group()
def cli():
    """Generate AI safety evaluation scenarios."""
    pass


@cli.command()
@click.argument("target")
@click.option("--count", default=1, help="Number of scenarios to generate")
@click.option("--pretty", is_flag=True, help="Pretty print output")
@click.option("--save", is_flag=True, help="Save scenarios to database")
@click.option("--model", default="llama3.2", help="Model to use for generation")
def generate(target, count, pretty, save, model):
    """Generate scenarios for TARGET evaluation."""
    backend = OllamaBackend(model=model)

    # Only create ScenarioStore if user wants to save
    scenario_store = ScenarioStore() if save else None

    for i in range(count):
        scenario = backend.generate_scenario(target)

        # Save to database if requested
        if scenario_store:
            scenario_store.save_scenario(
                scenario,
                backend="ollama",
                model=model,
            )

        output = {
            "prompt": scenario.prompt,
            "evaluation_target": scenario.evaluation_target,
            "success_criteria": scenario.success_criteria,
        }

        if pretty:
            # Rich pretty printing
            rprint(JSON.from_data(output))
        else:
            # Unix-friendly JSON lines
            print(json.dumps(output))


@cli.command()
def list():
    """List all saved scenarios."""
    store = ScenarioStore()
    scenarios = store.list_all_scenarios()

    if not scenarios:
        click.echo(
            "No scenarios found. Generate some with: scenario-forge generate <target> --save"
        )
        return

    click.echo(f"Found {len(scenarios)} scenarios:\n")
    for i, scenario in enumerate(scenarios, 1):
        click.echo(f"{i}. {scenario.evaluation_target}")
        click.echo(f"   Prompt: {scenario.prompt[:60]}...")
        click.echo(f"   Criteria: {', '.join(scenario.success_criteria[:2])}...")
        click.echo()


@cli.command()
def review():
    """Review and rate saved scenarios."""
    store = ScenarioStore()
    scenarios = store.get_scenarios_for_review()

    if not scenarios:
        click.echo(
            "No unrated scenarios found. Generate some with: scenario-forge generate <target> --save"
        )
        return

    click.echo(f"Found {len(scenarios)} scenarios to review.\n")
    click.echo("Rate each scenario from 0-3:")
    click.echo("  0 = Ineffective")
    click.echo("  1 = Ok")
    click.echo("  2 = Good")
    click.echo("  3 = Excellent")
    click.echo()

    for scenario_id, scenario in scenarios:
        click.echo("-" * 60)
        click.echo(f"Target: {scenario.evaluation_target}")
        click.echo(f"\nPrompt: {scenario.prompt}")
        click.echo("\nSuccess Criteria:")
        for criterion in scenario.success_criteria:
            click.echo(f"  - {criterion}")

        while True:
            try:
                rating = click.prompt("\nRating (0-3)", type=int)
                if 0 <= rating <= 3:
                    store.save_rating(scenario_id, rating)
                    click.echo(f"✓ Rated as {rating}")
                    break
                else:
                    click.echo("Please enter a number between 0 and 3")
            except (ValueError, click.Abort):
                click.echo("\nSkipping this scenario...")
                break

        click.echo()


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["json", "huggingface", "jsonl"]),
    default="json",
    help="Export format (json, huggingface for training data, jsonl)",
)
@click.option("--min-rating", type=int, default=0, help="Minimum rating to include")
def export(format, min_rating):
    """Export rated scenarios."""
    store = ScenarioStore()
    scenarios = store.get_rated_scenarios(min_rating)

    if not scenarios:
        click.echo(f"No scenarios found with rating >= {min_rating}")
        return

    if format == "json":
        # Output as JSON array (original behavior)
        print(json.dumps(scenarios, indent=2))
    elif format in ["huggingface", "jsonl"]:
        # Import the HuggingFace exporter
        from scenario_forge.exporters import huggingface

        # Convert to training format
        training_data = huggingface.export_huggingface_format(scenarios)

        # Output in appropriate format
        if format == "huggingface":
            # Conversational format for HuggingFace
            output = huggingface.export_conversational(training_data)
        else:
            # JSONL format
            output = huggingface.export_jsonl(training_data)

        print(output)


if __name__ == "__main__":
    cli()
