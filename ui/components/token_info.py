from textual.widgets import Static


class TokenInfo(Static):
    def update_display(self, metadata: dict[str, int]) -> None:
        self.update(
            "[b]Usage[/b]\n"
            "[dim]────────[/dim]\n"
            f"[dim]Input[/dim]  [b]{metadata['prompt_token_count']}[/b]\n"
            f"[dim]Output[/dim] [b]{metadata['candidates_token_count']}[/b]"
        )
