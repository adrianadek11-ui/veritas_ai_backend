import time
from rich.console import Console
from rich.table import Table
from core.dynamic_growth_matrix import dynamic_growth
from core.campaign_matrix import campaign_matrix

console = Console()

def render_live_matrix_dashboard():
    table = Table(title="🚀 VERITAS PERPETUUM MOBILE — LIVE MCR DASHBOARD")

    table.add_column("Węzeł Satelitarny", style="cyan", no_wrap=True)
    table.add_column("Viralowy Temat", style="magenta")
    table.add_column("Status Hype'u", style="green")
    table.add_column("Aktywne Kampanie", style="yellow")

    for node_id, data in dynamic_growth.active_satellite_nodes.items():
        table.add_row(
            node_id,
            data.get("topic", "N/A"),
            data.get("status", "ACTIVE"),
            str(len(campaign_matrix.active_campaigns))
        )

    console.clear()
    console.print(table)

if __name__ == "__main__":
    while True:
        render_live_matrix_dashboard()
        time.sleep(5)
