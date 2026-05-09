from tracker.models.orchestration_result import OrchestrationResult


def build_batch_report(results: list[OrchestrationResult]) -> dict:
    updated = [result for result in results if result.status == "updated"]
    unchanged = [result for result in results if result.status == "unchanged"]
    failed = [result for result in results if result.status == "failed"]

    return {
        "total": len(results),
        "updated_count": len(updated),
        "unchanged_count": len(unchanged),
        "failed_count": len(failed),
        "updated_titles": [result.title for result in updated],
        "failed_items": [
            {
                "title": result.title,
                "site": result.site,
                "message": result.message,
            }
            for result in failed
        ],
    }