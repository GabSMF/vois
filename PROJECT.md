# Vois — Project Specification

## 1. Project Overview

**Vois** is a multimodal note-generation application designed to help users capture and understand spoken content from classes, meetings, lectures, study sessions, and other real-world situations.

The core workflow is simple:

1. The user starts a recording session.
2. Vois records the session audio.
3. During the recording, the user can take photos.
4. Each photo is associated with the exact timestamp at which it was captured.
5. After the session ends, Vois processes the audio and images.
6. The final output is an AI-generated summary of the session, enriched by both what was said and what was visually captured.

The main idea behind Vois is that spoken explanations often depend on visual context such as whiteboards, slides, handwritten notes, diagrams, formulas, and screenshots. A traditional audio transcript alone may lose that context. Vois solves this by combining audio with timestamped images and using both to create a more complete and useful summary.

---

## 2. Product Vision

Vois aims to become a **multimodal session intelligence system** rather than just a recorder or transcriber.

The product should help users:

* remember what happened in a class or meeting,
* recover the meaning of visual moments tied to speech,
* generate summaries automatically,
* later search through previous sessions,
* navigate to important points in a session timeline.

In short, Vois should transform raw session media into structured, searchable knowledge.

---

## 3. Core Value Proposition

Vois differs from a standard transcription tool because it:

* records **audio**,
* allows **photos during recording**,
* preserves **temporal alignment** between speech and images,
* generates a **multimodal summary** instead of a plain transcript.

Example value:

* A professor explains an equation verbally.
* A student takes a photo of the board.
* Vois knows the photo was taken at that exact moment.
* The final summary can connect the spoken explanation with the equation shown on the board.

---

## 4. Intended Users

Primary users may include:

* university students,
* researchers,
* professionals in meetings,
* people attending lectures, workshops, seminars, or study groups,
* users who need better recall of spoken content with visual context.

---

## 5. Main Functional Requirements

### 5.1 Recording Session

* The system must allow the user to start a session.
* The system must record audio for the duration of the session.
* The system must allow the user to stop the session.
* The system must store metadata for the session, including creation time, duration, status, and ownership.

### 5.2 Timestamped Photos

* During an active recording session, the user must be able to take photos.
* Each photo must be stored with its exact timestamp relative to the session timeline.
* Photos must remain associated with the session they belong to.

### 5.3 Media Storage

* The system must store raw audio files.
* The system must store session photos.
* The system must store derived artifacts such as transcripts, timeline documents, embeddings metadata, and final summaries.

### 5.4 Audio Processing

* After the session ends, the audio must be sent to **Whisper** for transcription.
* The transcription should include timestamps at least at the segment level.
* If feasible, word-level timestamps may also be stored.

### 5.5 Timeline Assembly

* The system must merge transcript segments with photo events.
* The system must create an ordered timeline representation of the session.
* This timeline should act as the canonical structured representation used by downstream AI tasks.

### 5.6 Summary Generation

* The assembled multimodal timeline must be sent to a reasoning/summarization model such as **GPT-5.4**.
* The model should generate a structured summary of the session.
* The summary may contain sections such as title, abstract, key points, concepts, references to important moments, and action items.

### 5.7 Embeddings and Retrieval

* The project will use **Gemini Embeddings 2** for embeddings generation.
* Embeddings should be generated for relevant units such as transcript chunks, timeline blocks, image descriptions, or OCR text if available.
* These embeddings are intended primarily for semantic retrieval and future search features.

---

## 6. Non-Functional Requirements

### 6.1 Scalability

* The architecture should support future growth in number of users and sessions.
* Heavy AI processing must be asynchronous whenever appropriate.

### 6.2 Modularity

* Components such as transcription, embeddings, timeline assembly, storage, and summary generation should remain logically separated.
* The system should allow swapping providers or models later with minimal architectural disruption.

### 6.3 Maintainability

* Code should be written with clear service boundaries.
* Business logic should not be tightly coupled to vendor-specific SDK details.
* The project should maintain clear documentation of architecture, endpoints, and processing flow.

### 6.4 Traceability

* It should be possible to inspect a session’s processing state.
* It should be possible to tell which artifacts were generated for a session.
* Failures should be observable and debuggable.

### 6.5 Cost Awareness

* The project should be designed to evolve from a student prototype or MVP into a more robust product.
* Expensive model calls should be limited to steps where they add significant value.

---

## 7. Proposed High-Level Architecture

Vois should follow a modular pipeline architecture.

### 7.1 Main Components

#### Client Application

Responsible for:

* starting/stopping recording,
* capturing photos during recording,
* sending media and metadata to the backend,
* showing processing status,
* displaying generated summaries.

#### Backend API

Responsible for:

* session creation,
* upload coordination,
* metadata management,
* orchestration of the processing pipeline,
* exposing summary and status endpoints.

#### Storage Layer

Responsible for:

* storing raw audio,
* storing session photos,
* storing generated artifacts,
* storing metadata references.

#### Processing Pipeline

Responsible for:

* transcription with Whisper,
* optional image processing/OCR,
* timeline assembly,
* embedding generation with Gemini Embeddings 2,
* summary generation with GPT-5.4.

#### Retrieval Layer

Responsible for:

* storing embeddings,
* enabling future semantic search,
* enabling navigation to relevant moments across sessions.

---

## 8. Suggested Technical Stack

This section reflects the currently intended stack and may evolve.

### 8.1 AI / Model Choices

* **Whisper** for transcription
* **Gemini Embeddings 2** for embeddings and retrieval support
* **GPT-5.4** (or comparable reasoning model) for final summary generation

### 8.2 Backend

Suggested options:

* FastAPI
* Python-based service layer

### 8.3 Database

Suggested options:

* PostgreSQL for structured metadata

### 8.4 Object Storage

Suggested options:

* Supabase Storage
* MinIO
* S3-compatible storage

### 8.5 Vector Search

Suggested options:

* pgvector
* Qdrant

### 8.6 Async Processing

Suggested options:

* Redis + Celery
* or another background jobs/queue solution if needed

---

## 9. Suggested Data Model

This section is conceptual and not a final schema.

### 9.1 User

Fields may include:

* user_id
* name
* email
* created_at

### 9.2 Session

Fields may include:

* session_id
* user_id
* title
* status
* started_at
* ended_at
* duration
* audio_storage_key
* summary_status

### 9.3 Photo

Fields may include:

* photo_id
* session_id
* storage_key
* taken_at_ms
* uploaded_at

### 9.4 Transcript Segment

Fields may include:

* segment_id
* session_id
* start_ms
* end_ms
* text
* speaker (optional)

### 9.5 Timeline Block

Fields may include:

* block_id
* session_id
* start_ms
* end_ms
* transcript_excerpt
* linked_photo_ids
* derived_context

### 9.6 Summary

Fields may include:

* summary_id
* session_id
* summary_text
* structured_summary_json
* created_at
* model_used

### 9.7 Embedding Record

Fields may include:

* embedding_id
* session_id
* entity_type
* entity_id
* embedding_vector_reference
* source_text

---

## 10. Processing Flow Specification

The intended flow is:

1. User creates a session.
2. User records audio.
3. User takes one or more photos during the recording.
4. System stores the media and timestamps.
5. When the session ends, background processing starts.
6. Whisper generates a transcript with timestamps.
7. The system assembles transcript data and timestamped photo events into a timeline.
8. Gemini Embeddings 2 generates embeddings for retrieval-ready units.
9. GPT-5.4 generates the final summary based on the structured timeline.
10. The summary and derived artifacts are stored and made available to the user.

---

## 11. Example Internal Representation

Below is an example of how a timeline block may conceptually look:

```json
[
  {
    "start_ms": 860000,
    "end_ms": 880000,
    "transcript": "The speaker explains the main concept in this interval.",
    "photos": [
      {
        "photo_id": "img_7",
        "taken_at_ms": 872000,
        "description": "Whiteboard with equations and notes",
        "ocr_text": "optional extracted text"
      }
    ]
  }
]
```

This representation is useful because it preserves chronology and makes downstream processing easier.

---

## 12. Summary Output Expectations

The final summary should ideally be structured rather than just a paragraph.

Possible fields:

* title
* abstract
* main topics
* key insights
* important moments
* image-related references
* action items
* glossary

Example target structure:

```json
{
  "title": "",
  "abstract": "",
  "key_points": [],
  "important_moments": [],
  "action_items": [],
  "glossary": []
}
```

---

## 13. Planned Future Features

The following features are not required for the earliest MVP but are aligned with the product direction:

* OCR on captured photos
* image description generation
* semantic search across sessions
* cross-session knowledge retrieval
* clickable timeline navigation from summary to original media moments
* support for lectures, meetings, and study materials at larger scale
* speaker identification if useful
* collaborative or shared sessions

---

## 14. MVP Scope

A realistic MVP should focus on the smallest end-to-end version of the product.

### MVP Goal

Produce a working pipeline that:

* records one session,
* stores audio and photos,
* preserves photo timestamps,
*/home/gabriel/Downloads/TASKS.md
 transcribes with Whisper,
* assembles a session timeline,
* generates a summary with GPT-5.4.

### MVP Features

* session creation
* audio upload
* photo upload with timestamp
* session finalization
* transcription
* timeline assembly
* summary generation
* summary retrieval

### Out of Scope for First MVP

* advanced multi-user collaboration
* highly polished UI
* full semantic retrieval across many sessions
* extensive OCR/image understanding unless necessary early
* real-time streaming complexity unless explicitly prioritized later

---

## 15. Current Status / Already Done

> This section should remain easy to update over time.

* [x] Product concept for Vois defined
* [x] Core workflow identified: audio recording + timestamped photos + AI summary
* [x] Main AI stack direction chosen: Whisper + Gemini Embeddings 2 + GPT-5.4
* [x] High-level architecture direction defined
* [x] Pipeline approach established around transcript/timeline/summary
* [ ] Backend repository initialized
* [ ] API endpoints implemented
* [ ] Object storage selected and integrated
* [ ] Database schema implemented
* [ ] Audio upload flow implemented
* [ ] Photo timestamp flow implemented
* [ ] Whisper integration implemented
* [ ] Timeline assembler implemented
* [ ] Gemini embeddings integration implemented
* [ ] GPT-5.4 summary integration implemented
* [ ] Frontend/client prototype implemented
* [ ] Search/retrieval layer implemented
* [ ] OCR/image analysis implemented
* [ ] Deployment pipeline implemented

---

## 16. Recommended Development Order

Suggested implementation order:

1. initialize backend project
2. define session and storage models
3. implement session creation endpoint
4. implement audio upload
5. implement photo upload with timestamp
6. implement session finalization endpoint
7. integrate Whisper transcription
8. implement timeline assembler
9. integrate GPT-5.4 summary generation
10. integrate Gemini Embeddings 2
11. implement retrieval/search
12. improve UI and system observability

---

## 17. Agent Update Instructions

This file is expected to be updated over time, possibly by an automated agent.

### 17.1 Primary Goal of Updates

The agent should keep this file as the **single concise source of truth** for the project’s current state, architecture, and implementation progress.

### 17.2 What the Agent Should Update

The agent may update:

* the **Current Status / Already Done** checklist,
* the **Recommended Development Order** if priorities change,
* the **Suggested Technical Stack** if technical decisions are finalized or replaced,
* the **MVP Scope** if the project evolves,
* the **Planned Future Features** section,
* the **architecture description** when implementation becomes more concrete.

### 17.3 What the Agent Should Preserve

The agent should preserve:

* the general explanation of what Vois is,
* the product vision unless explicitly changed,
* the core multimodal concept,
* the distinction between transcription, embeddings, and summarization responsibilities.

### 17.4 Update Rules

When updating this file, the agent should:

* keep the document readable,
* avoid unnecessary rewriting of stable sections,
* only mark something as done when it is actually implemented or clearly completed,
* prefer adding precision rather than adding marketing language,
* keep terminology consistent,
* preserve section numbering where possible.

### 17.5 Progress Reporting Rule

If a component has started but is not complete, the agent should avoid marking it as done and may instead annotate it as:

* in progress,
* partially implemented,
* under evaluation,
* blocked.

### 17.6 Suggested Status Conventions

The agent may use these conventions:

* `[x]` done
* `[ ]` not started
* `[-]` in progress
* `[!]` blocked / needs decision

### 17.7 Architecture Update Rule

If implementation diverges from the current proposed architecture, the agent should update this file so that it reflects the **real architecture**, not an outdated ideal architecture.

### 17.8 Decision Logging

When an important technical choice is finalized, the agent should briefly record it in the relevant section.

Examples:

* object storage finalized as Supabase Storage
* backend framework finalized as FastAPI
* vector storage finalized as pgvector

### 17.9 Scope Discipline

The agent should not expand project scope implicitly. New scope should only be added when there is explicit evidence that the project direction changed.

---

## 18. Open Decisions

The following decisions may still need confirmation:

* exact backend framework
* exact object storage provider
* exact vector database solution
* whether OCR is MVP or post-MVP
* whether image description is MVP or post-MVP
* whether realtime processing is required early
* frontend technology choice
* deployment strategy

---

## 19. One-Sentence Project Definition

**Vois is a multimodal application that records audio, associates user-captured photos with session timestamps, and generates AI summaries from the resulting structured timeline of spoken and visual information.**

