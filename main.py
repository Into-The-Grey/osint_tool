#!/usr/bin/env python3
import click
from controller import Controller
from config import load_config
from rich.console import Console
import time
import os
import sqlite3

console = Console()

# Global flag to control database check (True by default)
RUN_DB_CHECK = True
DEFAULT_DB_PATH = "osint_results.db"


def setup_database(default_db_path):
    """
    Prompts the user for a database file path (defaulting to default_db_path)
    and creates a local SQLite database with a sample table for scan results.
    """
    db_path = click.prompt(
        "Enter path for the local SQLite database", default=default_db_path
    )
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Create a sample table for scan results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                result TEXT,
                scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        conn.close()
        console.print(f"[bold green]Database initialized at {db_path}.[/bold green]")
        return db_path
    except Exception as e:
        console.print(f"[bold red]Error initializing database: {e}[/bold red]")
        return None


def check_database():
    """
    Checks if the default database file exists. If not, prompts the user with:
    Y = run setup now, N = skip for this run, D = disable database check for this session.
    """
    global RUN_DB_CHECK
    if RUN_DB_CHECK and not os.path.exists(DEFAULT_DB_PATH):
        answer = (
            click.prompt(
                f"No local storage database found at '{DEFAULT_DB_PATH}'. Do you want to set up the database now? (Y=Run now, N=Skip this time, D=Disable DB check)",
                type=str,
                default="N",
            )
            .strip()
            .upper()
        )
        if answer == "Y":
            setup_database(DEFAULT_DB_PATH)
        elif answer == "N":
            console.print("[yellow]Skipping database setup for this run.[/yellow]")
        elif answer == "D":
            RUN_DB_CHECK = False
            console.print("[yellow]Database check disabled for this session.[/yellow]")
        else:
            console.print(
                "[red]Unrecognized input. Skipping database setup for this run.[/red]"
            )


@click.command()
@click.option(
    "-t",
    "--target",
    multiple=True,
    required=True,
    help="""Input target(s).

  Email:      john.doe@example.com
  
  Username:   jdoe123
  
  Domain:     example.com
  
  IP:         1.2.3.4
  
  Phone:      +1234567890
  
  Address:    '123 Main St, City, Country'
  
  Name:       'John Doe'""",
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

    For more information, visit our GitHub repository:
    https://github.com/Into-The-Grey/osint_tool

    Please use this tool responsibly and ethically, ensuring you have permission to perform
    any scans on the provided targets. Failure to do so may result in legal consequences.
    This tool is intended for educational and research purposes only.
    
    YOU ARE RESPONSIBLE FOR YOUR ACTIONS. YOU HAVE BEEN WARNED.
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

    # Check for local storage database before scanning
    check_database()

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


if __name__ == "__main__":
    main()
