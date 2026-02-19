import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
import shutil
from generator import CodeGenerator
from snippets import SnippetManager

app = typer.Typer(help="Fast project scaffolding and code generation CLI")
console = Console()
generator = CodeGenerator()
snippet_manager = SnippetManager()

@app.command()
def init(
    template: str = typer.Argument(..., help="Template name: fastapi, flask, react, vue"),
    name: str = typer.Option("my-project", help="Project name")
):
    """Initialize a new project from template"""
    try:
        generator.create_project(template, name)
        console.print(f"[green]✓[/green] Project '{name}' created successfully!")
        console.print(f"[dim]cd {name} && pip install -r requirements.txt[/dim]")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {str(e)}")
        raise typer.Exit(1)

@app.command()
def snippet(
    action: str = typer.Argument(..., help="Action: add, list, use"),
    name: str = typer.Option(None, help="Snippet name"),
    file: str = typer.Option(None, help="File path for snippet content")
):
    """Manage code snippets"""
    if action == "add":
        if not name or not file:
            console.print("[red]✗[/red] Both --name and --file required for add")
            raise typer.Exit(1)
        snippet_manager.add_snippet(name, file)
        console.print(f"[green]✓[/green] Snippet '{name}' added")
    
    elif action == "list":
        snippets = snippet_manager.list_snippets()
        if not snippets:
            console.print("[yellow]No snippets found[/yellow]")
            return
        
        table = Table(title="Available Snippets")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        for s in snippets:
            table.add_row(s["name"], s.get("description", ""))
        console.print(table)
    
    elif action == "use":
        if not name:
            console.print("[red]✗[/red] --name required for use")
            raise typer.Exit(1)
        content = snippet_manager.get_snippet(name)
        console.print(content)
    
    else:
        console.print(f"[red]✗[/red] Unknown action: {action}")
        raise typer.Exit(1)

@app.command()
def generate(
    type: str = typer.Argument(..., help="Type: crud, api, model, component"),
    name: str = typer.Option(..., help="Name of the generated code"),
    output: str = typer.Option(".", help="Output directory")
):
    """Generate code based on rules"""
    try:
        result = generator.generate_code(type, name, output)
        console.print(f"[green]✓[/green] Generated {type} '{name}' at {result}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
