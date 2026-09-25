# Design QA

final result: passed

## Evidence

- Design source: Figma file `GV8CeHa4sr9Z3r4D63pf6n`, node `5:14075`.
- Reference frames: `2086:1748` (1440 × 9934) and `2087:3158` (1440 × 9034).
- Reference renders: `.shots/figma-2086-1748.jpg` and `.shots/figma-2087-3158.jpg`.
- Implementations: `http://127.0.0.1:8088/index-1.html` and `http://127.0.0.1:8088/index-2.html`.
- Comparison renders: `.shots/qa-compare-v1.html` and `.shots/qa-compare-v2.html`.

## Comparison history

1. Initial comparison found a 40 px narrow desktop content area, a missing second student section in variant 1, incorrect compact-section heights in variant 2, a taller footer, and an incorrect media feature image/layout.
2. The container, section spacing, employer mosaic, student variants, footer rhythm, media assets, and wide media grid were brought in line with the Figma geometry.
3. Final desktop measurements match the Figma frame dimensions:
   - variant 1: viewport/content width 1440 px; rendered height 9934 px (fractional browser layout variance below 0.5 px);
   - variant 2: viewport/content width 1440 px; rendered height 9034 px exactly.
4. Final visual comparison confirmed matching section order, card grids, media hierarchy, team/CTA/footer alignment, and corrected image crops.
5. Follow-up correction for the photographic student cards aligned their navy backgrounds, white controls, exact copy, and image starts at 223/222/220 px with the Figma frames.
6. Modal regression check confirmed stable content geometry during scroll locking, animated open/close states, Escape handling, focus restoration, and no residual body padding after repeated cycles.
7. Production carousel follow-up aligned the 1440 × 760 frame geometry, restored five equal-width desktop tabs, and raised tab labels by 8 px so their bottom clearance matches the 16 px rounded section divider in Figma.
8. Direction modal arrows now cycle a three-image gallery for the selected direction; the heading and descriptive copy remain stable, both directions wrap correctly, and the controls expose photo-specific accessible labels.
9. The student-area subnavigation is now generated consistently on practices, internships, education, career-track, and events pages; each route retains all five links and marks exactly one active item with both `is-active` and `aria-current="page"`.
10. Breadcrumbs on education, career-track, and events now include the same intermediate “Школьникам и студентам” level as practices and internships; a route test covers the full three-level hierarchy on all five pages.
11. Student section transitions now keep the navigation at a stable position: the five pages share one hero spacing and reserve three subtitle lines. Browser clicks through all five routes kept the same navigation coordinates at desktop width; at 390 and 320 px, the mobile navigation height and position were consistent and the document had no horizontal overflow.

## Functional and responsive checks

- Production carousel advances and updates the selected tab.
- Direction card opens its modal; the close control dismisses it.
- No broken images were found.
- A clean page load produced no console errors.
- Mobile smoke test at 390 × 844 produced no horizontal page overflow (`scrollWidth === clientWidth`).

## Result

Passed. No blocking design, interaction, resource, or responsive issues remain in the reviewed landing-page variants.
