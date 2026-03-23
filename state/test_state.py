from typing import TypedDict, List, Dict

class AppState(TypedDict, total=False):
    scenario: str
    driver: object
    test_cases: List[Dict]
    execution_results: List[Dict]
    final_result: str