import typer
import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from vault_manager import VaultManager

app = typer.Typer(help="SyntaxVault: A CLI for your favorite code snippets.")
console = Console()
manager = VaultManager()

@app.command()
def add(name: str):
    """Add a new snippet to the vault."""
    if manager.get_snippet(name):
        console.print(f"[bold red]Error:[/bold red] Snippet '{name}' already exists.")
        raise typer.Exit()

    console.print("[bold cyan]Enter/Paste your code (Press Ctrl-D or Ctrl-Z on Windows to save):[/bold cyan]")
    
    # Collect multiline input
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        code = "\n".join(lines)

    if not code.strip():
        console.print("[bold red]Error:[/bold red] Code cannot be empty.")
        raise typer.Exit()

    language = typer.prompt("Language (e.g., python, bash, sql)", default="text")
    description = typer.prompt("Description")

    manager.add_snippet(name, code, language, description)
    console.print(f"\n[bold green]Success![/bold green] Snippet '{name}' added.")

@app.command()
def list():
    """List all saved snippets."""
    vault = manager.load_vault()
    
    if not vault:
        console.print("[yellow]The vault is empty. Use 'sv add' to get started.[/yellow]")
        return

    table = Table(title="SyntaxVault Snippets", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Language", style="green")
    table.add_column("Description", style="white")

    for name, data in vault.items():
        table.add_row(name, data["language"], data["description"])

    console.print(table)

@app.command()
def get(name: str):
    """Retrieve a snippet and copy it to the clipboard."""
    snippet = manager.get_snippet(name)
    
    if not snippet:
        console.print(f"[bold red]Error:[/bold red] Snippet '{name}' not found.")
        return

    # Display highlighted code
    syntax = Syntax(snippet["code"], snippet["language"], theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"Snippet: {name}", subtitle=snippet["description"]))

    # Clipboard logic
    pyperclip.copy(snippet["code"])
    console.print("\n[bold green]✓ Code copied to clipboard![/bold green]")

@app.command()
def delete(name: str):
    """Delete a snippet from the vault."""
    if not manager.get_snippet(name):
        console.print(f"[bold red]Error:[/bold red] Snippet '{name}' not found.")
        return

    confirm = typer.confirm(f"Are you sure you want to delete '{name}'?")
    if confirm:
        manager.delete_snippet(name)
        console.print(f"[bold green]Success:[/bold green] Snippet '{name}' deleted.")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")

@app.command()
def search(query: str):
    """Filter snippets by name or description."""
    results = manager.search_snippets(query)
    
    if not results:
        console.print(f"[yellow]No snippets found matching '{query}'.[/yellow]")
        return

    table = Table(title=f"Search Results: {query}", show_header=True, header_style="bold blue")
    table.add_column("Name", style="cyan")
    table.add_column("Language", style="green")
    table.add_column("Description", style="white")

    for name, data in results.items():
        table.add_row(name, data["language"], data["description"])

    console.print(table)

@app.command()
def edit(name: str):
    """Edit an existing snippet's details."""
    snippet = manager.get_snippet(name)
    
    if not snippet:
        console.print(f"[bold red]Error:[/bold red] Snippet '{name}' not found.")
        raise typer.Exit()

    console.print(f"[bold yellow]Editing snippet: {name}[/bold yellow]")
    console.print("Leave blank and press Enter to keep the current value.")

    # Edit Description
    new_desc = typer.prompt("New Description", default=snippet["description"])
    
    # Edit Language
    new_lang = typer.prompt("New Language", default=snippet["language"])
    
    # Edit Code
    change_code = typer.confirm("Do you want to update the code content?", default=False)
    new_code = None
    
    if change_code:
        console.print("[bold cyan]Enter/Paste your NEW code (Press Ctrl-D to save):[/bold cyan]")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            new_code = "\n".join(lines)
            if not new_code.strip():
                console.print("[yellow]Code was empty. Keeping original code.[/yellow]")
                new_code = None

    # Apply updates
    manager.update_snippet(name, code=new_code, language=new_lang, description=new_desc)
    console.print(f"[bold green]Success![/bold green] Snippet '{name}' has been updated.")

@app.command()
def template(lang: str = "cpp"):
    """Quickly copy a coding template for a specific language (default: cpp)."""
    template_name = f"template-{lang.lower()}"
    snippet = manager.get_snippet(template_name)
    
    if not snippet:
        console.print(f"[bold red]Error:[/bold red] No template found for '{lang}'.")
        console.print(f"[yellow]Hint: Run 'sv add {template_name}' to create one first.[/yellow]")
        return

    pyperclip.copy(snippet["code"])
    console.print(f"[bold green]✓ {lang.upper()} template copied to clipboard![/bold green]")
    console.print(f"[dim]Description: {snippet['description']}[/dim]")


if __name__ == "__main__":
    app()