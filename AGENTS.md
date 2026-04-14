# AGENTS.md

## 1. Purpose

This file provides working instructions for coding agents operating on the **Vois** repository.

Vois is a multimodal application that:
- records audio,
- allows users to take photos during a session,
- stores the timestamp of each photo,
- processes the captured session,
- generates an AI summary grounded in spoken and visual context.

This document is meant to help agents make useful, low-risk, scope-aware changes to the project.

---

## 2. Primary Source of Truth

Agents should treat the following files as the main reference documents:

- `PROJECT.md` → product definition, architecture, requirements, MVP scope
- `TASKS.md` → backlog, milestones, current progress, priorities
- `AGENTS.md` → implementation behavior and agent operating rules

If these files disagree:
1. Prefer the **real implemented code** over outdated documentation.
2. Update the documentation to reflect reality.
3. Do not silently expand the project scope.

---

## 3. Product Summary

**Vois** is a multimodal session intelligence application.

The intended core flow is:
1. User starts a session.
2. User records audio.
3. User takes photos during the recording.
4. Each photo is linked to a session timestamp.
5. After the session ends, the system processes the session.
6. Whisper generates a timestamped transcript.
7. The system assembles a structured timeline.
8. Gemini Embeddings 2 generates retrieval embeddings.
9. A reasoning model such as GPT-5.4 generates the final summary.

The core idea is to transform raw audio and timestamped images into structured, searchable knowledge.

---

## 4. Current Intended Stack

Unless explicitly changed in code or project docs, assume the following intended stack:

### AI / ML
- **Whisper** for transcription
- **Gemini Embeddings 2** for embeddings / retrieval
- **GPT-5.4** or similar reasoning model for final summary generation

### Backend
- Python
- FastAPI preferred unless another framework has already been adopted

### Data / Infra
- PostgreSQL for metadata
- Object storage for audio, photos, transcripts, timeline artifacts, summaries
- `pgvector` or equivalent vector storage if retrieval is implemented
- Background jobs / queue if processing becomes asynchronous

### General Architecture Style
- Prefer a **modular monolith** first
- Avoid unnecessary microservices in early stages
- Separate logical responsibilities into services/modules

---

## 5. Architectural Principles

Agents should preserve these architectural principles unless there is a strong reason to change them.

### 5.1 Structured Intermediate Representations
Do not design the system as:
- raw media → giant single prompt → final result

Prefer:
- raw media → transcript / image-derived context → timeline → summary / retrieval

The timeline or equivalent structured session representation should remain a central artifact.

### 5.2 Separation of Responsibilities
Keep these concerns logically distinct:
- session management
- storage
- transcription
- image handling
- timeline assembly
- embeddings generation
- summary generation
- retrieval/search

### 5.3 Replaceable Providers
Business logic should not be tightly coupled to one vendor SDK when avoidable.
Use thin wrappers or service abstractions where practical.

### 5.4 Asynchronous-Friendly Design
Heavy operations such as transcription, embeddings, OCR, or summary generation should be designed in a way that can later move to background processing if needed.

### 5.5 Metadata and Artifacts
Large media and generated artifacts should not be stored directly in relational rows when avoidable.
Use the database for structured metadata and object storage for large files/artifacts.

---

## 6. MVP Priority

Agents should optimize for the **smallest working end-to-end slice**.

The MVP is not “all possible intelligence features.”
The MVP is a functioning pipeline that can:
- create a session,
- store audio,
- store photos with timestamps,
- transcribe audio,
- assemble a timeline,
- generate a final summary,
- return the result.

### Highest-priority implementation order
1. session creation and persistence
2. audio upload/storage
3. photo upload with timestamps
4. session finalization flow
5. Whisper integration
6. timeline assembly
7. summary generation
8. embeddings / retrieval
9. OCR / richer vision processing
10. advanced search / cross-session features

Agents should avoid spending large effort on lower-priority features before the main path works.

---

## 7. Expected Core Domain Concepts

Agents should generally model the system around these entities.
Names may vary, but the concepts should remain clear.

### User
Represents an account / owner of sessions.

### Session
Represents one recording event.
Typical fields may include:
- `id`
- `user_id`
- `title`
- `status`
- `started_at`
- `ended_at`
- `duration_ms`
- `audio_storage_key`

### Photo Event
Represents an image captured during a session.
Typical fields may include:
- `id`
- `session_id`
- `storage_key`
- `taken_at_ms`
- `uploaded_at`

### Transcript Segment
Represents a time-aligned text segment.
Typical fields may include:
- `id`
- `session_id`
- `start_ms`
- `end_ms`
- `text`

### Timeline Block
Represents an assembled multimodal interval.
Typical fields may include:
- `id`
- `session_id`
- `start_ms`
- `end_ms`
- `transcript_excerpt`
- `linked_photo_ids`
- `derived_context`

### Summary
Represents the final generated output for a session.

### Embedding Record
Represents indexed retrieval units.

---

## 8. Recommended Repository Structure

If the repository is still early-stage, agents may use a structure close to:

```text
/backend
  /app
    main.py
    /api
    /models
    /schemas
    /services
    /repositories
    /workers
    /core
    /tests
/frontend
/docs
PROJECT.md
TASKS.md
AGENTS.md
```

If the repo already uses a different structure, do not reorganize it aggressively without a clear reason.
Prefer incremental consistency over large refactors.

---

## 9. Backend Implementation Guidance

### 9.1 API Style
Prefer explicit, predictable REST-style endpoints for the MVP.

Likely useful endpoints:
- `POST /sessions`
- `GET /sessions/{session_id}`
- `POST /sessions/{session_id}/audio`
- `POST /sessions/{session_id}/photos`
- `POST /sessions/{session_id}/finish`
- `GET /sessions/{session_id}/status`
- `GET /sessions/{session_id}/timeline`
- `GET /sessions/{session_id}/summary`

### 9.2 Service Boundaries
Use service classes/modules where helpful, such as:
- `SessionService`
- `StorageService`
- `TranscriptionService`
- `TimelineService` or `TimelineAssembler`
- `SummaryService`
- `EmbeddingService`

### 9.3 Schemas and Validation
Validate request and response payloads clearly.
Do not leave public API payloads loosely specified if typed schemas are available.

### 9.4 Errors
Return meaningful errors.
Avoid silent failures.
Store or expose processing status when background work is involved.

---

## 10. Storage Guidance

### 10.1 Object Storage
Use object storage or an equivalent abstraction for:
- raw audio files
- session photos
- transcript files
- timeline artifacts
- summary artifacts

### 10.2 Metadata Database
Use the relational database for:
- users
- sessions
- timestamps
- processing states
- model metadata
- references to stored artifacts

### 10.3 Avoid
Avoid putting large binary payloads directly into relational tables unless there is a strong reason.

---

## 11. AI Integration Guidance

### 11.1 Whisper
Use Whisper for transcription.
Store transcript output in a way that preserves timestamps.
Prefer segment timestamps at minimum.

### 11.2 Gemini Embeddings 2
Use Gemini Embeddings 2 for retrieval-oriented representations.
Do not treat embeddings generation as a replacement for structured timeline creation.

### 11.3 GPT-5.4
Use GPT-5.4 or the chosen reasoning model for final summary generation.
Prefer grounded prompts built from the assembled timeline rather than raw unstructured inputs whenever possible.

### 11.4 Prompting Principle
Prompts should be deterministic and inspectable enough to debug.
Avoid turning the pipeline into opaque prompt glue.

---

## 12. Timeline Assembly Guidance

The timeline is a central concept.
Agents should preserve or improve its role.

A timeline block should typically combine:
- transcript text for a time interval,
- photo events whose timestamps fall within or near that interval,
- optionally OCR text,
- optionally image descriptions,
- other derived contextual notes.

The goal is to create a chronological representation that can drive:
- final summary generation,
- future retrieval/search,
- timeline navigation.

---

## 13. Background Jobs Guidance

If background processing exists or is introduced, agents should keep jobs focused and composable.

Examples of good background tasks:
- transcribe session
- process photo set
- assemble timeline
- generate embeddings
- generate summary

Good practices:
- store job status
- allow retries where safe
- make tasks idempotent where practical
- avoid giant all-in-one jobs if smaller steps are cleaner

Do not introduce queue complexity too early if the project is still proving the main flow.

---

## 14. Coding Guidelines

### 14.1 General
- Prefer simple, readable code.
- Prefer explicit names over clever abstractions.
- Avoid premature optimization.
- Keep functions small enough to understand.

### 14.2 Type Safety
- Use type hints where the language/framework supports them.
- Keep schemas and internal data structures reasonably explicit.

### 14.3 Configuration
- Put secrets and credentials in environment variables.
- Do not hardcode provider keys.
- Document required environment variables when adding them.

### 14.4 Logging
- Log important transitions in processing pipelines.
- Avoid logging sensitive raw user content unless necessary for debugging and appropriately controlled.

### 14.5 Tests
When adding or modifying logic, add tests where practical.
Prioritize tests for:
- session lifecycle
- timestamp handling
- timeline assembly logic
- storage integration boundaries
- API contract behavior

---

## 15. Documentation Update Rules

Agents are expected to keep documentation aligned with real progress.

### Update `PROJECT.md` when:
- product scope changes,
- architecture decisions become concrete,
- technical choices are finalized,
- MVP definition changes.

### Update `TASKS.md` when:
- tasks start,
- tasks finish,
- priorities change,
- blockers appear,
- new implementation milestones are identified.

### Update `AGENTS.md` when:
- development workflow changes,
- stack assumptions change,
- agent instructions become outdated.

Agents should avoid rewriting documentation cosmetically without useful changes.

---

## 16. Status Conventions

If status markers are used in docs, prefer:
- `[x]` done
- `[ ]` not started
- `[-]` in progress
- `[!]` blocked / needs decision

Do not mark something as done if it is only partially implemented.

---

## 17. Safe Change Policy

Agents should prefer changes that are:
- incremental,
- reversible,
- testable,
- documented.

Avoid:
- broad repo-wide rewrites without a clear need,
- introducing major frameworks casually,
- hidden architectural shifts without doc updates,
- scope creep disguised as refactoring.

---

## 18. Decision-Making Rules

When a decision is unclear, agents should generally prefer:
1. the simpler implementation,
2. the version that preserves the core architecture,
3. the version that keeps the MVP moving,
4. the version easiest to debug and document.

When major ambiguity remains, update docs with the open decision rather than pretending it is resolved.

---

## 19. Anti-Goals

Agents should not optimize for these too early:
- perfect enterprise-scale architecture,
- advanced distributed systems design,
- excessive provider abstraction before first integration,
- polished design systems before core pipeline works,
- speculative features not in scope.

Vois should first become a working product, then a sophisticated one.

---

## 20. Definition of Useful Progress

A change is useful if it clearly advances one of the following:
- session lifecycle implementation,
- storage integration,
- timestamped photo handling,
- transcription pipeline,
- timeline assembly,
- summary generation,
- retrieval/search support,
- developer clarity/documentation.

If a change does not clearly support one of these, agents should question whether it belongs in the current phase.

---

## 21. Example Near-Term Priorities

Unless `TASKS.md` says otherwise, useful near-term priorities include:
- create backend skeleton
- define session and photo models
- implement session creation
- implement audio upload flow
- implement photo upload with timestamps
- integrate Whisper transcription
- implement timeline assembler
- implement summary generation

---

## 22. One-Sentence Working Definition

**Vois is a multimodal application that records audio, links timestamped images to session moments, and generates AI summaries from the resulting structured timeline of spoken and visual information.**
