#!/usr/bin/env python3
import click
from controller import Controller
from config import load_config
from rich.console import Console
import time

console = Console()


@click.command()
@click.option(
    "-t",
    "--target",
    multiple=True,
    required=True,
    help="Input target(s). Examples: email:john.doe@example.com, username:jdoe, domain:example.com, ip:1.2.3.4, phone:+1234567890, address:'123 Main St, City, Country', realname:'John Doe'",
)
@click.option("--darkweb", is_flag=True, help="Enable dark web scanning via Tor")
@click.option("--permutations", is_flag=True, help="Enable username permutation search")
@click.option("--output", default="results.json", help="Output file (JSON format)")
@click.option("--host", default=None, help="Host for web UI (optional)")
@click.option("--port", default=5000, help="Port for web UI (optional)")
def main(target, darkweb, permutations, output, host, port):
    """
    OSINT Tool - A Modular OSINT Intelligence Gathering Platform

    This tool accepts one or more targets and scans them using a modular set of passive
    and active intelligence modules. The scan dynamically expands based on discovered
    information, correlating results into a unified knowledge graph.
    """
    # Display a welcome banner using Rich
    console.print(
        "[bold green]====================================[/bold green]",
        justify="center",
    )
    console.print(
        "[bold green]         OSINT Tool v1.0          [/bold green]", justify="center"
    )
    console.print(
        "[bold green] Modular OSINT Intelligence Gathering [/bold green]",
        justify="center",
    )
    console.print(
        "[bold green]====================================[/bold green]\n",
        justify="center",
    )

    # Create a simple configuration object from the CLI options
    class Args:
        def __init__(self, darkweb, permutations, output):
            self.darkweb = darkweb
            self.permutations = permutations
            self.output = output

    args_obj = Args(darkweb, permutations, output)

    # Load configuration
    config = load_config(args_obj)

    # Print summary of provided targets
    console.print(
        "[bold blue]Starting scan with targets:[/bold blue] " + ", ".join(target)
    )
    console.print("Processing... please wait...\n", style="italic")

    # Instantiate and run the Controller
    controller = Controller(config)
    start_time = time.time()
    result_graph = controller.run(list(target))
    elapsed = time.time() - start_time

    console.print(
        f"\n[bold green]Scan complete![/bold green] Elapsed time: {elapsed:.2f} seconds",
        justify="center",
    )
    # Optionally, you could print out a summary or prompt to view results/download them.


if __name__ == "__main__":
    main()
