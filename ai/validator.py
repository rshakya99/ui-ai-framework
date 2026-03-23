def validator_agent(state):
    results = state.get("execution_results", [])

    if not results:
        raise Exception("No execution results!")

    final_status = "PASSED"

    for r in results:
        if str(r["expected"]).lower() != str(r["actual"]).lower():
            r["status"] = "FAILED"
            final_status = "FAILED"
        else:
            r["status"] = "PASSED"

    return {
        "execution_results": results,
        "final_result": final_status
    }