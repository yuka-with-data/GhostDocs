# 👻 Lost Knowledge

The project currently suffers from significant documentation drift, creating uncertainty around the modern, correct way to set up and run the application. While the core purpose—processing archived records and generating summary reports—is clear, the necessary prerequisites, expected input formats, and operational steps appear outdated or insufficiently documented.

Specific knowledge gaps relate to:

*   **Current Workflow Definition:** The `README.md` warns that the setup instructions may not reflect recent changes, but it does not provide a definitive, up-to-date workflow.
*   **Configuration Dependencies:** It is unclear whether the current version relies on legacy configuration files or if modern initialization practices have replaced them.
*   **Input/Output Standards:** The required format for input archive files and the expected process for report generation are documented as being subject to change, leaving maintainers without definitive current standards.

# 🕯️ Ghost Sightings

The following evidence suggests critical knowledge gaps that require immediate clarification:

*   **Outdated Setup Instructions:** The file `docs/old-setup.md` is explicitly titled "Previous Setup Instructions," confirming that the documented procedures are historical, not current.
*   **Unconfirmed Dependencies (TODO):** In `docs/old-setup.md`, there is a marker stating: `- TODO: Confirm whether the current version still requires the legacy configuration file.` This indicates a key architectural decision regarding configuration files has not been verified against the current implementation.
*   **Outdated Processing Knowledge (FIXME):** Similarly, `docs/old-setup.md` contains: `- FIXME: Update the instructions for the latest archive format.` This suggests that the operational guide for the primary input data (archived records) is incorrect or incomplete.
*   **Warning of Stale Documentation:** The `README.md` explicitly warns maintainers: "The archive processing workflow was updated last year, but the setup instructions may not reflect every change." This acknowledges a gap but does not resolve it.

# 🎃 Resurrection Plan

To restore clarity and improve maintainability, I recommend the following actions, prioritized by the potential impact on new contributors and daily maintenance.

### 🛠️ Priority 1: Establish the Current Standard Workflow

*   **Action:** Replace or heavily update `docs/old-setup.md` with a new, authoritative document (e.g., `docs/setup.md`).
*   **Goal:** Remove all `TODO` and `FIXME` markers related to current process knowledge.
*   **Focus Areas:** Document the current, preferred method for dependency installation, and provide clear, step-by-step instructions for the absolute latest archive format.

### 🔍 Priority 2: Clarify Technical Assumptions

*   **Action:** Confirm the existence and usage status of any legacy configuration files.
*   **Goal:** Determine if the system was migrated away from legacy config files. If it is still required, document *how* and *why*. If it is obsolete, confirm the removal of the requirement.

### 📚 Priority 3: Update Core Documentation Files

*   **Action:** Update `README.md` to point to the new, authoritative setup document (created in Priority 1).
*   **Goal:** Ensure that the first place a maintainer looks for setup information immediately points to the most accurate source, thereby removing the historical ambiguity.
