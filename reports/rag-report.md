# RAG Report

## Terminal Testing

| Query | Retrieved Count | Confidence Category | Citations | P@5 | R@5 |
|---|---|---|---|---|---|
| students enrolled in ASD101 |  |  |  |  |  |
| student count |  |  |  |  |  |
| CI report status |  |  |  |  |  |

Fill this table from the output of `python rag_eval.py` and the manual `refresh_corpus` / `retrieve_context` / `answer_question` calls described in the Lab 08 guide.

## UI Testing

- [ ] RAG HTTP server running on port 5003
- [ ] 3 Docker containers running (`docker ps`)
- [ ] `curl http://localhost:5003/health` returns `{"status": "ok", "service": "rag-server"}`
- [ ] `/rag/refresh`, `/rag/retrieve`, `/rag/answer` return `status: success`
- [ ] RAG tab in the browser displays tool responses, citations, and a confidence category
