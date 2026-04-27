"""Custom tools for the Battle Card Pipeline.

Provides HTML battle card generation and comparison chart creation.
Modularized entry point.
"""

from tools import generate_battle_card_html, generate_comparison_chart

# Re-exporting for ADK discovery if needed
__all__ = [
    "generate_battle_card_html",
    "generate_comparison_chart"
]
