# Vois — TASKS

## 1. Purpose of This File

This file tracks the **execution state** of the Vois project.

While `PROJECT.md` explains what Vois is, why it exists, and how it should work, this file exists to track:

- what needs to be built,
- what is currently being worked on,
- what is blocked,
- what has already been completed,
- what decisions still need to be made.

This file should remain practical, concise, and implementation-oriented.

---

## 2. Status Conventions

Use the following conventions consistently:

- `[ ]` Not started
- `[-]` In progress
- `[x]` Done
- `[!]` Blocked / waiting for decision / external dependency

Priority labels:

- `P0` Critical for MVP
- `P1` Important but not blocking first demo
- `P2` Nice to have / later phase

---

## 3. Current Project Phase

**Current phase:** Early architecture / specification / project setup

**Current objective:** Build the first end-to-end MVP slice:

`session creation -> media upload -> transcription -> timeline assembly -> summary generation`

---

## 4. MVP Definition

The first meaningful MVP is complete when a user can:

1. create a session,
2. upload or record audio,
3. upload one or more photos with timestamps,
4. finish the session,
5. get a generated summary based on the audio and timestamped photos.

The MVP does **not** require:

- polished production UI,
- cross-session semantic search,
- advanced OCR,
- collaboration features,
- real-time streaming,
- production-grade scaling.

---

## 5. Milestones

### Milestone 0 — Project Foundation
- [ ] `P0` Initialize repository structure
- [ ] `P0` Define initial README and local setup instructions
- [ ] `P0` Define environment variable strategy
- [ ] `P0` Choose backend framework definitively
- [ ] `P0` Choose storage provider definitively
- [ ] `P1` Define logging and error reporting approach

### Milestone 1 — Session and Storage Backbone
- [ ] `P0` Create database schema for users, sessions, and photos
- [ ] `P0` Implement session creation endpoint
- [ ] `P0` Implement session retrieval endpoint
- [ ] `P0` Implement audio upload flow
- [ ] `P0` Implement photo upload flow with timestamp metadata
- [ ] `P0` Store media references in database
- [ ] `P1` Validate file types and upload limits

### Milestone 2 — Transcription Pipeline
- [ ] `P0` Implement Whisper service wrapper
- [ ] `P0` Submit audio to transcription pipeline
- [ ] `P0` Store transcript output with timestamps
- [ ] `P0` Define transcript segment format
- [ ] `P1` Handle transcription failures cleanly
- [ ] `P1` Add retry policy for failed transcription jobs

### Milestone 3 — Timeline Assembly
- [ ] `P0` Define timeline block schema
- [ ] `P0` Implement transcript-to-timeline grouping logic
- [ ] `P0` Attach timestamped photos to the correct timeline interval
- [ ] `P0` Store generated timeline document
- [ ] `P1` Add validation tests for timestamp alignment

### Milestone 4 — Summary Generation
- [ ] `P0` Define summary input contract for GPT-5.4
- [ ] `P0` Define target summary output schema
- [ ] `P0` Implement summary generation service
- [ ] `P0` Store structured summary result
- [ ] `P0` Implement summary retrieval endpoint
- [ ] `P1` Add prompt/version tracking for reproducibility

### Milestone 5 — Embeddings and Retrieval Preparation
- [ ] `P1` Define which artifacts will be embedded
- [ ] `P1` Implement Gemini Embeddings 2 service wrapper
- [ ] `P1` Choose vector storage solution definitively
- [ ] `P1` Generate embeddings for timeline/search units
- [ ] `P2` Implement first semantic search endpoint

### Milestone 6 — Async Processing / Background Jobs
- [ ] `P1` Decide whether Redis + Celery will be used in MVP
- [ ] `P1` Implement job queue for long-running processing
- [ ] `P1` Track processing state per session
- [ ] `P1` Implement retry/failure handling for jobs
- [ ] `P2` Separate workers by task type if needed

### Milestone 7 — Frontend / Client Prototype
- [ ] `P0` Create minimal client interface or demo screen
- [ ] `P0` Allow session start/stop from client
- [ ] `P0` Allow photo capture/upload during session
- [ ] `P0` Send timestamp metadata with photos
- [ ] `P0` Show processing state
- [ ] `P0` Show final summary
- [ ] `P2` Improve timeline visualization

### Milestone 8 — OCR / Image Context (Optional Early, Valuable Later)
- [ ] `P2` Decide whether OCR belongs in MVP or post-MVP
- [ ] `P2` Choose OCR solution
- [ ] `P2` Extract OCR text from captured photos
- [ ] `P2` Attach OCR output to timeline blocks
- [ ] `P2` Evaluate image description step for richer context

### Milestone 9 — Deployment and Operations
- [ ] `P1` Define local development workflow
- [ ] `P1` Define deployment target
- [ ] `P1` Configure secrets management
- [ ] `P1` Add healthcheck endpoints
- [ ] `P1` Add basic monitoring/logging
- [ ] `P2` Add CI pipeline

---

## 6. Immediate Next Tasks

These are the next highest-value tasks and should usually stay updated.

1. [ ] `P0` Finalize backend framework choice
2. [ ] `P0` Finalize storage provider choice
3. [ ] `P0` Initialize repository structure
4. [ ] `P0` Implement session creation endpoint
5. [ ] `P0` Implement audio upload endpoint
6. [ ] `P0` Implement photo upload endpoint with timestamp
7. [ ] `P0` Integrate Whisper transcription
8. [ ] `P0` Implement timeline assembler
9. [ ] `P0` Implement GPT-5.4 summary generation

---

## 7. Suggested Repository Structure

This is a suggested structure and may be revised once implementation begins.

```text
/backend
  /app
    main.py
    /routes
      sessions.py
      uploads.py
      summaries.py
    /services
      storage.py
      transcription.py
      timeline.py
      summary.py
      embeddings.py
    /models
    /schemas
    /workers
  requirements.txt or pyproject.toml

/frontend
  (to be defined)
```

---

## 8. API Backlog

### Session Endpoints
- [ ] `P0` `POST /sessions`
- [ ] `P0` `GET /sessions/{id}`
- [ ] `P0` `POST /sessions/{id}/finish`
- [ ] `P1` `GET /sessions/{id}/status`

### Upload Endpoints
- [ ] `P0` `POST /sessions/{id}/audio`
- [ ] `P0` `POST /sessions/{id}/photos`

### Result Endpoints
- [ ] `P0` `GET /sessions/{id}/summary`
- [ ] `P1` `GET /sessions/{id}/timeline`

### Search Endpoints
- [ ] `P2` `POST /search`

---

## 9. Core Service Backlog

### Session Service
- [ ] `P0` Create session
- [ ] `P0` Read session state
- [ ] `P0` Finalize session

### Storage Service
- [ ] `P0` Upload/store audio
- [ ] `P0` Upload/store photos
- [ ] `P0` Store artifact references
- [ ] `P1` Signed URL strategy if needed

### Transcription Service
- [ ] `P0` Whisper request wrapper
- [ ] `P0` Transcript normalization
- [ ] `P1` Error handling and retries

### Timeline Service
- [ ] `P0` Merge transcript and photo events
- [ ] `P0` Serialize timeline document
- [ ] `P1` Validation logic for timestamps

### Summary Service
- [ ] `P0` GPT-5.4 request wrapper
- [ ] `P0` Structured summary parser
- [ ] `P1` Prompt versioning

### Embeddings Service
- [ ] `P1` Gemini Embeddings 2 integration
- [ ] `P1` Embedding storage logic
- [ ] `P2` Retrieval logic

---

## 10. Data Model Backlog

### Required Early Tables / Entities
- [ ] `P0` users
- [ ] `P0` sessions
- [ ] `P0` photos
- [ ] `P0` transcript_segments
- [ ] `P0` summaries

### Later / Optional Entities
- [ ] `P1` timeline_blocks
- [ ] `P1` embedding_records
- [ ] `P2` OCR/image-analysis records
- [ ] `P2` job execution records

---

## 11. Open Technical Decisions

These items require confirmation and should remain visible until decided.

- [!] `P0` Backend framework final choice
- [!] `P0` Object storage provider final choice
- [!] `P1` Vector storage final choice
- [!] `P1` Async jobs included in MVP or added after first synchronous prototype
- [!] `P2` OCR included in MVP or postponed
- [!] `P2` Frontend stack final choice
- [!] `P1` Deployment target

---

## 12. Risks and Watchpoints

### Product Risks
- [ ] Summary quality may be weak if the timeline structure is poor
- [ ] Timestamp alignment may become unreliable if client capture flow is not carefully implemented
- [ ] Photos without useful metadata/context may add noise instead of value

### Technical Risks
- [ ] Large file uploads may complicate the first prototype
- [ ] Processing latency may be high if everything is synchronous
- [ ] Model cost may rise if summary prompts become too large
- [ ] Embeddings may be added too early before the retrieval use case is stable

### Scope Risks
- [ ] Trying to build search, OCR, realtime, and polished UX too early
- [ ] Overengineering with microservices before the MVP works end-to-end

---

## 13. Definition of Done for the First Demo

The first demo is considered successful when all of the following are true:

- [ ] A session can be created
- [ ] Audio can be uploaded and stored
- [ ] A photo can be uploaded with timestamp metadata
- [ ] Whisper can generate a transcript for the session
- [ ] A timeline document can be assembled
- [ ] GPT-5.4 can generate a summary from that timeline
- [ ] The summary can be retrieved and shown to the user

---

## 14. Already Done

- [x] Product concept defined
- [x] Core multimodal workflow defined
- [x] High-level architecture direction defined
- [x] Main AI stack direction chosen: Whisper + Gemini Embeddings 2 + GPT-5.4
- [x] `PROJECT.md` created as project source-of-truth document
- [ ] Repository initialized
- [ ] First backend endpoint implemented
- [ ] First storage integration implemented
- [ ] First end-to-end session processed successfully

---

## 15. Agent Update Instructions

This file is intended to be updated by an agent over time.

### 15.1 Main Rule
Keep this file focused on **execution state**, not high-level product philosophy.

### 15.2 What the Agent Should Update
The agent should update:
- task statuses,
- current phase,
- immediate next tasks,
- milestone progress,
- open technical decisions,
- already done section,
- definition of done progress.

### 15.3 What the Agent Should Not Do
The agent should not:
- rewrite stable project vision unnecessarily,
- mark tasks as done without clear evidence,
- silently expand scope,
- remove blocked items without resolving them,
- replace specific tasks with vague statements.

### 15.4 Update Style Rules
The agent should:
- keep task descriptions concrete,
- keep priorities visible,
- prefer small updates over large rewrites,
- preserve markdown readability,
- preserve section structure where possible.

### 15.5 Progress Rules
- Mark `[x]` only when completed.
- Use `[-]` when work has started but is incomplete.
- Use `[!]` when a decision or blocker prevents progress.
- If a task changes shape, update the task instead of leaving stale wording.

### 15.6 Decision Logging Rule
When a major technical choice is finalized, the agent should update both:
- the relevant backlog/milestone item,
- the open technical decisions section.

Example:
- object storage finalized as Supabase Storage
- backend finalized as FastAPI
- vector storage finalized as pgvector

### 15.7 Scope Discipline
If a new feature appears, the agent should add it only if there is explicit evidence that it is now part of the project.

### 15.8 Keep the File Actionable
This file should always help answer:
- What should be built next?
- What is blocked?
- What is already working?

---

## 16. Short Version

**`PROJECT.md` explains the project. `TASKS.md` tracks how the project gets built.**
