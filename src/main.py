# SSHIFT - SSH server management tool
#    _____   __  __   __  __
#   / ___/  / / / /  / / / /
#  / /     / /_/ /  / /_/ /
# /_/      \__, /   \__,_/
#         /____/
# Copyright (c) 2025 Junyeol Yu <ryuwhale95@gmail.com>
## Permission is granted to use, modify, and distribute this file freely.

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import Static, ListView, ListItem, Label
from textual.reactive import reactive
from textual.binding import Binding
import configparser
from pathlib import Path

def load_config():
    config_path = Path.home() / ".sshift-config"
    if not config_path.exists():
        config_path.write_text(
            "# SSHift config\n"
            "# Example:\n"
            "# [my-server]\n"
            "# HostName = dev\n"
            "# Host = 192.168.0.10\n"
            "# User = ubuntu\n"
            "# Port = 22\n"
        )
        return []

    try:
        config = configparser.ConfigParser()
        config.read(config_path)

        servers = []
        for section in config.sections():
            servers.append({
                "name": config[section].get("HostName", section),
                "host": config[section]["Host"],
                "username": config[section]["User"],
                "port": config[section].get("Port", "22")
            })
        return servers
    except Exception as e:
        print(f"⚠ Failed to parse config: {e}")
        return []

class SSHIFT(App):
    CSS = """
    Screen {
        overflow: auto;
        background: #000000;
        height: 15;
    }
    
    #server-list {
        height: 8;
        min-width: 20;
        max-width: 80; 
        border: heavy white;
        padding: 0;
        background: #000000;
    }

    #botton-panel {
        height: 7;
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
        Binding(key="j", action="cursor_down", description="Down"),
        Binding(key="k", action="cursor_up", description="Up"),
    ]
    def __init__(self):
        super().__init__()
        self.config = load_config()

    def compose(self) -> ComposeResult:
        list_content = (
            [ListItem(Label(f"{i+1}: {s['name']} ({s['username']}@{s['host']})")) for i, s in enumerate(self.config)]
            if self.config else
            [ListItem(Label("⚠ No servers configured in ~/.sshift-config"))]
        )

        yield Container(
            ListView(*list_content, id="server-list"),
            Horizontal(
                Static("<Details>", id="connection-panel", classes="details"),
                Static("<Keybindings>\n\n↑↓: Select\n⏎ : Connect\nq : Exit", classes="keybindings"),
                id="botton-panel"
            ),
            id="outer"
        )

    def on_mount(self):
        if self.config:
            self.update_connection_panel(0)

    def on_list_view_selected(self, event: ListView.Selected):
        self.selected_index = event.item_index
        self.update_connection_panel(event.item_index)

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        list_view = self.query_one("#server-list", ListView)
        self.selected_index = list_view.index
        self.update_connection_panel(list_view.index)
    
    def update_connection_panel(self, index: int):
        s = self.config[index]
        content = (
            "<Details>\n\n"
            f"IP Addr.  : {s['host']}\n"
            f"Username  : {s['username']}\n"
            f"Port No.  : {s['port']}"
        )
        self.query_one("#connection-panel", Static).update(content)

if __name__ == "__main__":
    SSHIFT().run(inline=True)