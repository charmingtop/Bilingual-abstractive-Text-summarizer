"""
Sample texts for testing the summarizer.
"""

SAMPLE_TEXTS = {
    "news_article": """
    Global temperatures have reached record highs for the third consecutive year, 
    according to a report released by the International Climate Research Institute. 
    The study indicates that average global temperatures have increased by 1.2°C 
    compared to pre-industrial levels. Scientists warn that immediate action is 
    required to prevent catastrophic climate change impacts. The report highlights 
    the urgent need for countries to accelerate their transition to renewable energy 
    sources and implement more stringent carbon emission regulations.
    """,
    
    "scientific_abstract": """
    This research paper presents a novel approach to quantum machine learning 
    that significantly improves computational efficiency for large-scale optimization 
    problems. Our method combines variational quantum algorithms with classical 
    neural networks, achieving a 45% reduction in computation time compared to 
    existing techniques. Experimental results demonstrate the effectiveness of 
    our approach on benchmark datasets, with implications for drug discovery, 
    materials science, and financial modeling. The proposed framework opens new 
    avenues for practical quantum computing applications.
    """,
    
    "business_report": """
    Quarterly financial results exceeded market expectations, with revenue growth 
    of 18% year-over-year. The technology division performed exceptionally well, 
    contributing 65% of total revenue. However, increased research and development 
    expenses impacted operating margins, which decreased by 2 percentage points. 
    The company announced a strategic partnership with a leading AI research firm 
    and plans to expand its product offerings in the Asian market. Management 
    remains optimistic about future growth prospects despite macroeconomic challenges.
    """
}

def get_sample_text(text_type: str = "news_article") -> str:
    """Get sample text by type."""
    return SAMPLE_TEXTS.get(text_type, SAMPLE_TEXTS["news_article"])