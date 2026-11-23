/**
 * GhostDocs Demo Website
 * Handles lightweight mobile navigation interactions.
 */

// Mobile navigation toggle
const menuToggle = document.querySelector(".menu-toggle");
const mainNav = document.querySelector(".main-nav");

menuToggle.addEventListener("click", () => {
    const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";

    // Toggle navigation visibility.
    mainNav.classList.toggle("active");

    // Update accessibility attributes.
    menuToggle.setAttribute("aria-expanded", String(!isExpanded));
    menuToggle.setAttribute(
        "aria-label",
        isExpanded ? "Open navigation menu" : "Close navigation menu"
    );
});
