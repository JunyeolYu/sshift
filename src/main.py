# SSHIFT - SSH server management tool
#    _____   __  __   __  __
#   / ___/  / / / /  / / / /
#  / /     / /_/ /  / /_/ /
# /_/      \__, /   \__,_/
#         /____/
# Copyright (c) 2025 Junyeol Yu <ryuwhale95@gmail.com>
## Permission is granted to use, modify, and distribute this file freely.

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, ListView, ListItem, Label
from textual.reactive import reactive
from textual.binding import Binding

SERVERS = [
    {"name": "test1", "host": "192.168.0.1", "username": "test", "port": "22"},
    {"name": "test2", "host": "192.168.0.2", "username": "test", "port": "22"},
]

class SSHIFT(App):
    CSS = """
    Screen {
        layout: vertical;
        height: 50;
    }
    
    #server-list {
        height: 10;
        max-width: 80; 
        border: heavy white;
        padding: 0;
        background: #000000;
    }

    #botton-panel {
        height: 30;
        max-width: 80;
        layout: horizontal;
    }

    .details {
        border: heavy red;
        max-width: 70%;
        width: 1fr;
    }
    
    .keybindings {
        border: heavy blue;
        max-width: 30%;
        width: 1fr;
    }
    """

    selected_index = reactive(0)
    
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield ListView(
            *[ListItem(Label(f"{i+1}: {s['name']} ({s['username']}@{s['host']} w/ {s['port']})")) for i, s in enumerate(SERVERS)],
            id="server-list"
        )
        yield Horizontal(
            Static(id="connection-panel", classes="details"),
            Static("Keybindings\n\n↑↓: Select\n⏎ : Connect\nq : Exit", classes="keybindings"),
            id="botton-panel"
        )

    def on_mount(self):
        self.update_connection_panel(0)

    def on_list_view_selected(self, event: ListView.Selected):
        self.selected_index = event.index
        self.update_connection_panel(event.index)

    def update_connection_panel(self, index: int):
        s = SERVERS[index]
        content = (
            "Details\n\n"
            f"IP Addr.  : {s['host']}\n"
            f"Username  : {s['username']}\n"
            f"Port No.  : {s['port']}"
        )
        self.query_one("#connection-panel", Static).update(content)

if __name__ == "__main__":
    SSHIFT().run(inline=True)