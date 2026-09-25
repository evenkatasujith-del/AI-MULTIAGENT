import wikipedia


def get_evidence(claim):

    try:
        search_results = wikipedia.search(claim, results=3)

        if not search_results:
            return {
                "status": "NO_EVIDENCE",
                "sources": []
            }

        sources = []

        for result in search_results[:3]:

            try:
                page = wikipedia.page(
                    result,
                    auto_suggest=False
                )

                sources.append({
                    "title": page.title,
                    "url": page.url,
                    "evidence": page.summary[:500]
                })

            except Exception:
                continue

        if not sources:
            return {
                "status": "NO_EVIDENCE",
                "sources": []
            }

        return {
            "status": "EVIDENCE_FOUND",
            "sources": sources
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "sources": [],
            "error": str(e)
        }