# Vois

Vois is a multimodal application that records audio, associates user-captured photos with session timestamps, and generates AI-powered summaries from the resulting timeline of spoken and visual information.

## What Vois does

Vois is designed for classes, meetings, lectures, and study sessions.

A user can:

- start a recording session,
- record audio,
- take photos during the recording,
- preserve the exact timestamp of each captured image,
- generate a final AI summary that uses both speech and visual context.

The key idea is that spoken explanations often depend on things like whiteboards, slides, handwritten notes, formulas, or diagrams. Vois keeps that visual context connected to the audio timeline instead of treating it as separate information.

## Core workflow

1. The user starts a session.
2. Vois records audio.
3. The user captures photos during the session.
4. Each photo is linked to the timestamp at which it was taken.
5. After the session ends, the system processes the media.
6. A structured summary is generated from the combined timeline.

## Current technical direction

Vois is currently being designed around the following core components:

- **Whisper** for audio transcription
- **Gemini Embeddings 2** for embeddings and retrieval support
- **GPT-5.4** or a comparable reasoning model for final summary generation

The architecture follows a modular multimodal pipeline:

- media capture
- storage
- transcription
- timeline assembly
- embeddings generation
- summary generation

## Project goals

Vois aims to become more than a transcription tool. The long-term goal is to turn raw session media into structured, searchable knowledge.

This includes support for:

- multimodal summaries,
- future semantic search,
- timeline navigation,
- better recall of classes and meetings.

## MVP focus

The first working version is focused on the smallest end-to-end flow:

- audio recording
- timestamped photo capture
- session storage
- transcription
- timeline assembly
- final summary generation

## Planned stack

The exact implementation may evolve, but the current direction is:

- **Frontend:** mobile or web client
- **Backend:** Python service layer
- **Database:** PostgreSQL
- **Object storage:** S3-compatible or equivalent storage
- **Embeddings/search:** Gemini Embeddings 2 + vector storage
- **Summarization:** GPT-5.4

## Status

The project is currently in architecture and specification stage.

Already defined:

- product concept
- core workflow
- main AI stack direction
- high-level system architecture
- internal project documentation

## Internal docs

This repository may include the following internal documents:

- `PROJECT.md` — complete project specification
- `TASKS.md` — execution backlog and milestone tracking
- `AGENTS.md` — instructions for coding agents working in the repository

## Vision in one sentence

**Vois turns audio recordings and timestamped photos into structured AI-generated summaries of real-world sessions.**
