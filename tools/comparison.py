from google.adk.tools import ToolContext
from google.genai import types, Client
from .base import get_logger, get_timestamp, save_to_outputs

logger = get_logger()

COMPARISON_PROMPT_TEMPLATE = """Create a professional competitive comparison infographic.

**COMPARISON: {your_product_name} vs {competitor_name}**

Style: Clean, modern, sales-ready infographic
Colors: 
- Green (#22c55e) for {your_product_name} (your product)
- Red (#ef4444) for {competitor_name} (competitor)
- Dark blue (#1e3a5f) for headers and text
- White background

**DATA TO VISUALIZE:**
{comparison_data}

**INFOGRAPHIC LAYOUT:**

1. **Header** - "{your_product_name} vs {competitor_name}" prominently at top
2. **Score Overview** - Large visual showing overall winner
3. **Feature Comparison** - Side-by-side bars or ratings for each feature
4. **Key Differentiators** - Icons highlighting where {your_product_name} wins
5. **Bottom Line** - Clear verdict/recommendation badge

**DESIGN REQUIREMENTS:**
- Professional, enterprise-ready aesthetic
- Easy to read at a glance
- Color-coded clearly (green = us, red = them)
- Include checkmarks for wins, X marks for losses
- Make it look like a Gartner or Forrester comparison graphic
- Data-rich but not cluttered

Generate a visually compelling infographic that sales reps can share with prospects."""

async def generate_comparison_chart(
    competitor_name: str,
    your_product_name: str,
    comparison_data: str,
    tool_context: ToolContext
) -> dict:
    """Generate a visual comparison infographic using Gemini image generation."""
    prompt = COMPARISON_PROMPT_TEMPLATE.format(
        your_product_name=your_product_name,
        competitor_name=competitor_name,
        comparison_data=comparison_data
    )

    try:
        client = Client()
        response = await client.aio.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )

        # Look for image in response
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type
                
                # Save as ADK artifact
                timestamp = get_timestamp()
                ext = "png" if "png" in mime_type else "jpg"
                artifact_name = f"comparison_infographic_{timestamp}.{ext}"
                
                image_artifact = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                version = await tool_context.save_artifact(filename=artifact_name, artifact=image_artifact)
                logger.info(f"Saved comparison infographic: {artifact_name} (version {version})")
                
                # Also save to outputs folder
                save_to_outputs(artifact_name, image_bytes, is_text=False)
                
                return {
                    "status": "success",
                    "message": f"Comparison infographic saved as '{artifact_name}' - view in Artifacts tab",
                    "artifact": artifact_name,
                    "version": version,
                    "comparison": f"{your_product_name} vs {competitor_name}"
                }

        return {
            "status": "partial",
            "message": "Image generation not available, text description provided",
            "description": response.text if response.text else "No content generated"
        }

    except Exception as e:
        logger.error(f"Error generating comparison infographic: {e}")
        return {"status": "error", "message": str(e)}
