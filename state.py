from typing import TypedDict, Optional, Dict, Any, Annotated


class GraphState(TypedDict):
    file_path: Annotated[str, lambda x, y: y]

    file_hash: str

    upx_result:   Optional[Dict[str, Any]]
    floss_result: Optional[Dict[str, Any]]

    vt_data: Optional[Dict[str, Any]]

    static_analysis:  Optional[Dict[str, Any]]
    dynamic_analysis: Optional[Dict[str, Any]]
    yara_result:      Optional[Dict[str, Any]]

    aggregated: Optional[Dict[str, Any]]

    insights: Optional[Dict[str, Any]]

    summary_html:          Optional[str]
    structured_report_data: Optional[dict]
    full_report_html:      Optional[str]
