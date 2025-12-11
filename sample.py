from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

data = {
    "name": "John Jones",
    "age": 30,
    "address": {"street": "123 Main St", "city": "Gotham", "state": "NY"},
    "hobbies": ["reading", "hiking", "coding", "crimefighting"]
}

console = Console()
pretty_data = Pretty(data)
panel = Panel(pretty_data, title="User Data", border_style="blue")
console.print(panel)