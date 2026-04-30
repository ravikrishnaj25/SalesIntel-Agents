from google.adk.agents import LlmAgent
from ..tools import generate_comparison_chart

comparison_chart_agent = LlmAgent(
    name="ComparisonChartAgent",
    model="gemini-3-flash-preview",
    description="Creates visual comparison infographic using AI image generation",
    instruction="""
You create visual comparison infographics for sales teams using AI image generation.

COMPETITOR PROFILE:
{competitor_profile}

FEATURE ANALYSIS:
{feature_analysis}

SWOT ANALYSIS:
{swot_analysis}

Use the generate_comparison_chart tool to create a visual comparison infographic.

**PREPARE COMPARISON DATA:**

Create a comprehensive comparison summary including:

1. **Overall Verdict** - Who wins overall and why
2. **Feature Scores** - List 8-10 key features with ratings:
   - Feature name
   - Their score (1-10)
   - Our score (1-10)
   - Winner indicator

3. **Key Differentiators** - Top 3 areas where we clearly win
4. **Watch Areas** - Where they have advantage
5. **Verdict Summary** - One-line recommendation

Example comparison_data format:
```
OVERALL: HubSpot leads 7-3 over Salesforce

FEATURE COMPARISON:
- Ease of Use: Them 6/10, Us 9/10 ✓
- Enterprise Features: Them 9/10, Us 7/10 ✗
- Pricing Value: Them 4/10, Us 8/10 ✓
- Integrations: Them 8/10, Us 8/10 =
- Support Quality: Them 6/10, Us 8/10 ✓

KEY WINS: Ease of use, Pricing, Support
THEIR ADVANTAGE: Enterprise features, Brand recognition

VERDICT: Recommend HubSpot for SMB/Mid-market deals
```

Pass this to generate_comparison_chart with:
- competitor_name: The competitor's name
- your_product_name: Your product's name  
- comparison_data: The full comparison summary above

The tool uses Gemini's image generation to create a professional infographic.
""",
    tools=[generate_comparison_chart],
    output_key="chart_result",
)
