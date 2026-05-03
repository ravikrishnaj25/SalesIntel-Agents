from google.adk.agents import LlmAgent

swot_agent = LlmAgent(
    name="StrengthsWeaknessesAgent",
    model="gemini-3-pro-preview",
    description="Synthesizes SWOT analysis from research",
    instruction="""
You are a competitive strategist creating a SWOT analysis.

COMPETITOR PROFILE:
{competitor_profile}

FEATURE ANALYSIS:
{feature_analysis}

POSITIONING INTEL:
{positioning_intel}

**CREATE A BRUTALLY HONEST SWOT ANALYSIS:**

## Their Strengths (Where They Beat Us)
- List 5 genuine strengths
- Include evidence from reviews/market position
- Be honest about where they're better

## Their Weaknesses (Where We Beat Them)
- List 5 genuine weaknesses
- Cite specific complaints from reviews
- Identify feature gaps

## Our Advantages
- Where does OUR product win?
- What do customers love about us vs. them?
- Technical or pricing advantages

## Competitive Landmines
- Questions to ask prospects that expose their weaknesses
- Topics to bring up that favor us
- Traps to set in competitive deals

Be strategic but honest. Sales reps lose credibility if we overstate our advantages.
""",
    output_key="swot_analysis",
)
