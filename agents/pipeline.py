from google.adk.agents import SequentialAgent
from .competitor_research import competitor_research_agent
from .product_feature import product_feature_agent
from .positioning_analyzer import positioning_analyzer_agent
from .swot import swot_agent
from .objection_handler import objection_handler_agent
from .battle_card_generator import battle_card_generator_agent
from .comparison_chart import comparison_chart_agent

battle_card_pipeline = SequentialAgent(
    name="BattleCardPipeline",
    description="Complete battle card pipeline: Research → Features → Positioning → SWOT → Objections → Battle Card → Chart",
    sub_agents=[
        competitor_research_agent,
        product_feature_agent,
        positioning_analyzer_agent,
        swot_agent,
        objection_handler_agent,
        battle_card_generator_agent,
        comparison_chart_agent,
    ],
)
