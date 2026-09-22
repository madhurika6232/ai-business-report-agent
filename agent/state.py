from typing import TypedDict, List, Optional, Annotated
import operator

class ReportState(TypedDict):
    # Input
    csv_path: str                          # path to uploaded CSV
    df_summary: str                        # text summary of the dataframe
    
    # Agent decisions
    analyses_to_run: List[str]             # agent decides which analyses to run
    
    # Analysis results
    trend_results: Optional[dict]          # output from trend analysis
    outlier_results: Optional[dict]        # output from outlier detection
    forecast_results: Optional[dict]       # output from forecasting
    chart_paths: Annotated[List[str], operator.add]  # paths to generated charts
    
    # Final output
    narrative: Optional[str]              # plain-English summary written by AI
    report_path: Optional[str]            # path to final PDF
    
    # Control
    error: Optional[str]                  # any error messages