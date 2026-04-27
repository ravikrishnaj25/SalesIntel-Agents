from datetime import datetime
from google.adk.tools import ToolContext
from google.genai import types, Client
from .base import get_logger, clean_markdown_response, get_timestamp, save_to_outputs

logger = get_logger()

BATTLE_CARD_PROMPT_TEMPLATE = """Generate a professional sales battle card in HTML format.

**DATE: {current_date}**

This is a competitive battle card for sales reps to use during deals.

Style it for SALES TEAMS with:
- Clean, scannable design (reps glance at this during calls)
- Color coding: GREEN for our advantages, RED for competitor strengths
- Collapsible sections for detailed content
- Quick-reference format at the top
- Dark blue (#1e3a5f) and orange (#f97316) color scheme
- Print-friendly layout

COMPETITIVE INTELLIGENCE DATA:
{battle_card_data}

**REQUIRED SECTIONS:**

1. **Header** - Competitor name, logo placeholder, last updated date
2. **Quick Stats** - 5-6 one-liner facts about the competitor
3. **At a Glance** - 3 columns: They Win | We Win | Toss-up
4. **Feature Comparison** - Table with checkmarks/X marks
5. **Positioning** - How to position against them (2-3 sentences)
6. **Their Strengths** - Honest list with red indicators
7. **Their Weaknesses** - List with green indicators (our opportunities)
8. **Objection Handling** - Top 5 objections with quick responses
9. **Killer Questions** - Questions to ask prospects
10. **Landmines** - Traps to set in competitive deals

Make it visually impressive but FAST TO SCAN. Sales reps have seconds, not minutes.

Generate complete, valid HTML with embedded CSS and JavaScript for collapsible sections."""

async def generate_battle_card_html(
    battle_card_data: str,
    tool_context: ToolContext
) -> dict:
    """Generate a professional HTML battle card for sales teams."""
    current_date = datetime.now().strftime("%B %d, %Y")
    prompt = BATTLE_CARD_PROMPT_TEMPLATE.format(
        current_date=current_date,
        battle_card_data=battle_card_data
    )

    try:
        client = Client()
        response = await client.aio.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )

        html_content = response.text
        html_content = clean_markdown_response(html_content, "html")

        # Save as ADK artifact
        timestamp = get_timestamp()
        artifact_name = f"battle_card_{timestamp}.html"
        html_artifact = types.Part.from_bytes(
            data=html_content.encode('utf-8'),
            mime_type="text/html"
        )
        
        version = await tool_context.save_artifact(filename=artifact_name, artifact=html_artifact)
        logger.info(f"Saved battle card artifact: {artifact_name} (version {version})")

        # Also save to outputs folder
        save_to_outputs(artifact_name, html_content.encode('utf-8'))
        
        return {
            "status": "success",
            "message": f"Battle card saved as '{artifact_name}' - view in Artifacts tab",
            "artifact": artifact_name,
            "version": version
        }

    except Exception as e:
        logger.error(f"Error generating battle card: {e}")
        return {"status": "error", "message": str(e)}
