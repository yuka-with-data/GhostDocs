### 👻 Lost Knowledge

The primary knowledge deficit is the absence of a single, canonical source of truth for the project's current operational workflow. While the general purpose of the system (processing archived records and generating reports) is known, critical, step-by-step technical knowledge required for setup, configuration, and core data handling processes is either missing or explicitly marked as outdated.

Specifically, the maintainer lacks definitive answers to:

1.  **Current Configuration Requirements:** It is unclear whether the modern version of the project still relies on a "legacy configuration file." This represents an unknown architectural dependency that could prevent successful setup.
2.  **Canonical Setup Workflow:** There is no unified, current setup guide. The existence of historical instructions (e.g., in `docs/old-setup.md`) indicates significant process changes, but the modern, definitive workflow is not documented, making onboarding and maintenance risky.
3.  **Input Data Standards:** The required format, source, and processing steps for the primary input data (archived records) are undocumented for the current version.

### 🕯️ Ghost Sightings

Multiple files across the repository consistently point to the same critical gaps, suggesting the project has undergone significant undocumented technical evolution.

*   **File: `docs/old-setup.md`**
    *   **Evidence:** This file is titled "Previous Setup Instructions," confirming its historical status.
    *   **Significance:** This establishes that the document cannot be trusted for current operations, requiring a clear deprecation strategy.
    *   **Evidence:** The `TODO: Confirm whether the current version still requires the legacy configuration file.` (Found in multiple reports, including `test-1.md`, `test-2.md`, `test-3.md`, `test-4.md`, and `test-5.md`).
    *   **Significance:** This is a critical, unresolved technical dependency question that must be answered by a developer. The project cannot be considered maintainable until this status is confirmed.
    *   **Evidence:** The `FIXME: Update the instructions for the latest archive format.` (Found in multiple reports).
    *   **Significance:** This marks a failure point in the operational documentation. Without the current, correct archive format instructions, the core functionality cannot be reliably implemented or understood.

*   **File: `README.md`**
    *   **Evidence:** The note stating: "The archive processing workflow was updated last year, but the setup instructions may not reflect every change." (Found in `test-1.md`, `test-2.md`, `test-3.md`, and `test-4.md`).
    *   **Significance:** This general warning flag is highly significant. It confirms documentation drift—a known failure state—and mandates that the entire setup guide suite needs review.

*   **Structured Findings (Multiple Tests):** The repeated references to the need to resolve the `TODO` and `FIXME` markers across various test reports confirm that these are systemic knowledge gaps, not isolated issues.

### 🎃 Resurrection Plan

The following plan prioritizes addressing the underlying technical knowledge (resolving the dependencies) before updating the documentation, ensuring that the new documentation is based on current reality.

#### 🛠️ Phase 1: Resolve Core Dependencies (Highest Priority)

The immediate goal is to resolve the technical ambiguities marked by `TODO`/`FIXME` through direct developer investigation, as all documentation hinges on these answers.

1.  **Determine Configuration Status:** A developer must confirm definitively if the project requires the legacy configuration file. The result must update the `docs/old-setup.md` section or the new guide to reflect the current reality (i.e., mandatory, optional, or obsolete).
2.  **Establish Current Data Standards:** A developer must identify the current, supported archive format and document the exact, canonical method for processing this input data.

#### 📜 Phase 2: Establish the Single Source of Truth (High Priority)

Once the technical dependencies are resolved (Phase 1), the documentation must be restructured.

1.  **Create a Definitive Setup Guide:** Create a new, authoritative document (e.g., `docs/SETUP.md`) that contains the *current* setup and operational workflow. This guide must resolve all outstanding `TODO` and `FIXME` markers.
2.  **Deprecate Historical Content:** Update `README.md` to point exclusively to the new `docs/SETUP.md`. Modify `docs/old-setup.md` to explicitly function as an archive document, stating *when* it was relevant and *why* it is no longer the official guide.

#### 🧹 Phase 3: Review and Generalize (Medium Priority)

1.  **Architecture Decisions:** Implement a `DECISION_LOG.md` or similar file to capture major architectural shifts (e.g., the transition from the legacy config file to the modern method). This prevents future knowledge gaps by formalizing *why* changes were made.
2.  **Clean Up Reports:** Address the general "workflow was updated" warning in `README.md` by replacing vague statements with specific version numbers and documented functional scope.
