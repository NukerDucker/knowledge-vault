---
title: KMITL B-App — Usability Test & UI Improvement (submission draft)
tags:
  - university
  - individual
status: submitted
subject: uxui
course: 01276545
due: 2026-10-12
updated: 2026-10-11
feature: 01-university/year-3/uxui/assets/ut/2026-10-11/with-grid/Select Date & Time.png
thumbnail: thumbnails/resized/6dde2421ce5768bd5b3973415a235241_86cf658e.webp
---

# KMITL B-App Usability Test and UI Improvement

**Napaul Intharasing** · 67011178 · UX&UI CEI 1/2026 · Group 2 Mookrata
Scope: screens 6 to 10, the booking flow, from Select Date and Time through to Booking Submitted

---

## 1. Test participants

The test ran across two rounds with five people, and the roles followed the workshop brief, where one moderator runs the session and one note-taker records what happens while the participant works. Mind, ching ching and cheesy joined from outside the class, and Nhow is enrolled in the same course but sits in another group. Ages ranged from 20 to 22, and every session used the think-aloud method so participants described what they were looking for while they moved through the flow. Two of the five ran against the build of 8 October, and cheesy repeated the whole path twice with identical results on both passes.

| Participant | Age | Prior experience | Task score |
|---|---|---|---|
| Putt | 20 | Never used a booking app, closest experience is hotel booking | 4 / 5 |
| Mind | 22 | Yes, KMITL UAPP, books rooms and venues routinely | 3 / 5 |
| Nhow | 20 | None | 4 / 5 |
| ching ching | 20 | None stated | 2 / 5 before the fixes, 5 / 5 on the retest |
| cheesy | 20 | None stated | not scored before the fixes, both tasks blocked, 5 / 5 on the retest |

Putt's task fields were left empty during his run, so the evidence for that session is the post-test interview together with what he was observed to do. ching ching stopped before attempting the tasks and still scored the build 2 out of 5, which makes hers the lowest rating of the five and the one the defects decided; that score therefore belongs to the build she ran, before the fix pass. cheesy attempted both tasks and was ready to score them, and neither could be completed, so no rating was recorded for a run that the defects had already decided. On 10 October, the tasks were changed from 60 to 40 people, since a chosen number cannot follow the user to later screens without a paid Figma plan. Both of them retested the updated build against the revised tasks and rated it 5 out of 5, and cheesy completed every task on that run.

---

## 2. Feedback summary, per participant

### Putt, 20

Putt had never used a booking application before, and his closest experience comes from hotel websites. His run produced only the post-test interview, because the task fields were left empty during the session, and the confirmation screen gave him the most trouble of anything he saw. It did not announce itself, so he read it as a new page or an empty one and could not tell whether the booking had actually gone through. He also found the building selector on the map unreadable, since it showed bare numbers from 1 to 7 with no labels attached to them. Both problems were corrected after the round. The confirmation screen now opens with "You're all set!" over confetti and offers Back to home as a proper button, and the floor pills read 1F through 7F.

### Mind, 22

Mind books rooms and venues regularly through the KMITL UAPP, which gave her the strongest basis for comparison of anyone in the round. Her session produced six findings. The fields on the booking form look editable but cannot be typed into, which is a limit of the Figma prototype rather than a design defect, and the attendee control jumped to 80 on a room that seats 40 and then refused to move back down. The Request Edit and Request Cancellation actions did nothing when she pressed them, and the back arrow sometimes needed several taps before it responded. She also suggested that controls which do not work should be greyed out, so that they read as inactive instead of broken. Five of the six were fixed or addressed, and her suggestion was adopted through the disabled variant of the button component.

### Nhow, 20

Nhow scored the build 4 out of 5, reported no friction at all and completed the flow without hesitation, which is worth reading with some care, because the same build produced hard failures for two other participants. His two structural findings both held up under checking. The sticky Book Now bar sat flush against the Booking Rules section with no clearance at all, and it was already clipped by a single pixel on the unavailable variant of the room page. The sort sheet also offered no choice between ascending and descending order. He asked for an Apply button on the sort sheet as well, and that request was declined with reasoning, since a single-select list applies on tap and the multi-step confirmation belongs to filtering instead.

### ching ching, 20

ching ching stopped before the tasks and questioned the fidelity of the prototype instead, because she could not enter text in any field and could not tell whether the prototype was meant to be interactive at all. She scored what she saw 2 out of 5, the lowest rating in the round, and that number follows from the blocking defects rather than from taste. That ambiguity is the finding which outranks everything else she said. Her typing and summary observations resolve to prototype limits that Figma imposes, so they are recorded as a tool constraint rather than a design fault. The asymmetry she surfaced between the two sign-in buttons was real, and it was fixed afterwards. On the retest, ching ching rated this part 5 out of 5 and found one new problem, where choosing two time slots showed only the later one in the summary. This was handled after the retest, and section 5 explains what the prototype can and cannot do about it.

### cheesy, 20

cheesy ran the full booking path twice and reproduced his results on both passes, so his findings are stable rather than incidental. He attempted both tasks and intended to score them, and both were blocked before he could finish. The first task asked for a booking of 60 people, and room ECC-608 reads as busy in the search results but as unavailable when the room is opened, so one real state carries two different words and the task could not proceed. The second task ran on ECC-603, where the attendee control snapped between 1 and 80 with nothing in between and would not move back down once it had jumped. From that point even a booking for one person reported that it exceeded the room capacity, and refreshing the page did not clear it. He reported that a red cross badge reads as broken, since the busy state used the same red and the same icon as rejected, and his own suggestion was a do not disturb sign or an amber clock instead. The sort sheet and the notification sheet both left him with no way out, because the search background behind the sheet had disappeared. This pass produced change log entries 23 through 28 and shaped three of the five improvements explained in section 5. On the retest after the fix pass, which used the revised 40-person tasks, cheesy finished the whole path without getting stuck and described everything as intuitive. The one item still raised was that the map of ECC-603 does not allow booking the room, and the map sits outside the screens covered by this submission.

---

## 3. All UI screens with the grid visible

Seven screens are captured here with the layout grid switched on. The grid uses four columns with an 8 pixel gutter and a 16 pixel margin, and the pattern is drawn in the project orange at ten percent opacity, which keeps it visible without competing with the interface underneath. Screen 7 and screen 8 each carry two states, empty and filled for the booking details and empty and uploaded for the documents, which is why seven captures cover five screens. The same screens without the grid are supplied as a separate file.

![[assets/ut/2026-10-11/with-grid/Select Date & Time.png]]
S6, Select Date and Time

![[assets/ut/2026-10-11/with-grid/Booking Details - Empty.png]]
S7, Booking Details, empty state

![[assets/ut/2026-10-11/with-grid/Booking Details - Filled.png]]
S7, Booking Details, filled state

![[assets/ut/2026-10-11/with-grid/Upload Documents - Empty.png]]
S8, Upload Documents, empty state

![[assets/ut/2026-10-11/with-grid/Upload Documents - Uploaded.png]]
S8, Upload Documents, uploaded state

![[assets/ut/2026-10-11/with-grid/Review Booking.png]]
S9, Review Booking

![[assets/ut/2026-10-11/with-grid/Booking Submitted.png]]
S10, Booking Submitted

---

## 4. Before and after, one pair per screen

Each pair shows the screen before the changes on the left and the current Figma build on the right, with numbered callouts that match each issue to its fix. The pairs run in date order, from the earliest draft to the build the second round tested, and each of the five screens from 6 to 10 appears once. Booking Details appears in its filled state and Upload Documents in its empty state, which show the changes on each screen most clearly. Review Booking and Upload Documents go back to the drafts of 26 September and 1 October, because their biggest visual changes happened before the testing began. The confirmation screen uses a capture from 2 October, the closest one saved before Putt's session on 5 October. Select Date and Time and Booking Details are compared against that tested build of 8 October. Some entries in the change log leave no pixel difference at all, because they correct prototype wiring, and those are described in writing at the end of section 5.

![[assets/ut/2026-10-11/s6-s10-pairs/1-review-booking__annotated.png]]

![[assets/ut/2026-10-11/s6-s10-pairs/2-upload-documents-empty__annotated.png]]

![[assets/ut/2026-10-11/s6-s10-pairs/3-booking-submitted__annotated.png]]

![[assets/ut/2026-10-11/s6-s10-pairs/4-select-date-time__annotated.png]]

![[assets/ut/2026-10-11/s6-s10-pairs/5-booking-details-filled__annotated.png]]

---

## 5. Written explanation of each improvement

### 1. Summary layout on Review Booking

This pair goes back to the first draft of 26 September, because the review screen changed more in its layout than through any single fix. In that draft every summary row carried the same flat orange block, and the room was listed before the activity it was booked for. Both attachments read "Attachment title", so a user could not tell the proposal from the participant list. The current screen groups these details in a collapsible summary card with smaller tinted icons. It opens with the activity name, and the attachments carry their real file names. The stepper also gained numbered labels, and the bottom navigation was removed, since a four-step booking should not offer an exit halfway through. A smaller data fix sits inside the same card, because the build of 8 October still named room ECC-601 and 20 people, and both rows now match the booking. Change log entries 1, 8, 9 and 12.

### 2. The hidden button on Upload Documents

This pair uses the draft of 1 October, because the clearest problem on this screen was one that never reached a participant. The Continue to review button sat under the bottom navigation, so only a sliver of it showed and the user had no visible way forward. The navigation is gone from the whole booking flow, and the button now sits in full view above the home indicator. The optional third document now folds behind a plus sign, which keeps attention on the two required uploads. The room card lost its Floor 0 label and its row of three outlined chips, and now shows the real floor with one status badge and a seat count. The progress line on this step also stopped running ahead of the current step, which is the same fault cheesy pointed out on the details screen. Change log entries 6, 12 and 44.

### 3. Confirmation on Booking Submitted

Putt tested the flow on 5 October and could not tell whether the booking had gone through, because the confirmation screen read to him like a new page or an empty one. The heading now reads "You're all set!" above a burst of confetti, and the booking ID sits in a full-width card directly under the progress tracker. Back to home also moved from a small underlined link to an outlined button, so both ways out of the screen read as actions the user can take. The earlier capture is from 2 October, which is the closest one saved before his session. Change log entry 11.

### 4. Time slots and the progress line on Select Date and Time

This screen carried two separate problems. The progress line drew its first segment in orange while the user was still on step one, the same fault cheesy described as a line running ahead of the current step. Every empty segment also carried a one pixel orange nub. Step one now shows no filled segment and the nubs are gone. During the retest, ching ching picked two time slots and the summary showed only one of them, because the summary cannot follow the choice without a paid Figma feature. The grid now allows a single slot, and only 13:00 to 14:00, the slot the summary shows, stays open, which keeps the flow coherent although it does not remove the limit itself. That change landed after the retest, so no participant has used it yet. Furthermore, the Available badge also moved to a darker green so that its white text passes the contrast check. Change log entries 44 and 46.

### 5. Attendee count, preset chips on Booking Details

This change mattered most, because three of the five participants ran into the same control, and for cheesy it stopped the second task outright. Mind saw the count jump to 80 on a room that seats 40, which is the same fault ching ching described as moving only between 1 and 80. The old control carried only two variants, so exactly two values existed and nothing in between could be reached. A booking for 60 people was therefore impossible to enter, and because the default landed on the high variant, the capacity validation fired on input that was perfectly valid, which is how cheesy received an exceeds capacity warning at one attendee. Preset chips at 10, 20, 30 and 40 now replace it, built as one component where tapping a chip selects it and clears the others. The row stops at 40 because ECC-603 seats 40, so an over-capacity count is unreachable rather than rejected after the fact. The filled screen opens with 40 selected, since that is the count the task asks for. The screen also carried a hardcoded warning label that asserted the error regardless of input, and it was deleted from all five copies. On the retest, the attendee step no longer stopped anyone, and both retested participants rated the flow 5 out of 5. Although that score belongs to the whole fix pass, the retest also put the new chips in front of cheesy, the participant whose second task the old control had blocked. The same pair also shows the Purpose field holding a real value where grey placeholder text used to sit, while the progress line and step labels match the rest of the flow. Change log entries 23, 36 and 37.

### Lower-priority changes, described in writing

The changes below are logged in writing and in order of priority, because they either alter how the prototype behaves or sit on the second state of a screen already paired above.

| Screen | Raised by | What changed |
|---|---|---|
| Booking Details, empty state | Mind, ching ching | The Purpose dropdown showed the leftover words "Selected value" and the Additional note field asked for an activity name, and both hints now describe their own field. Typing is impossible in a Figma prototype, so tapping a field now fills it with sample text |
| Confirm sheet, opened from S9 | cheesy | The sheet had no way to dismiss it, so stepping back from the confirm step did nothing. It now opens over the review screen again and can be closed |
| Stepper, S6 to S9 | Teammate report | Tapping a later step lit its bubble without doing anything, and the stepper now only reports progress and cannot be tapped |
| Review Booking, S9 | Teammate report | Tapping a file row collapsed the whole booking summary, and now only the summary header opens and closes it |

---

## 6. Prototype link and submission map

The prototype is in the file **UX/UI 2026 — KMITL-BApp**, and the screens sit at nodes 4673:10421 through 4673:10427 inside the section Napaul / User / Booking Flow.
https://www.figma.com/design/bhuuET1PKmzZSGMkVr2de7/UX%2FUI%202026%20%E2%80%94%20KMITL-BApp

As someone who has spent this term building a booking flow for KMITL, I have noticed how much of the work sits in details that nobody mentions when the flow runs smoothly. This realization led me to reflect on the screens that the testers never questioned, because those are the ones where the decisions were already correct and the rest had to be found by watching people hesitate. Through testing for this report, I discovered that almost none of the failures were about visual design. Most of them traced back to a state that carried the wrong word, or to a control that promised something the prototype could not deliver.

| Requirement                                                         | Where it is                           |
| ------------------------------------------------------------------- | ------------------------------------- |
| Brief profile of five participants, pseudonyms                      | Section 1                             |
| Feedback summary for each participant                               | Section 2                             |
| All UI screens with grid and pattern shown                          | Section 3                             |
| Every page captured with the grid setting visible                   | Section 3                             |
| Separate PDF, each page alone, no grid                              | KMITL-BApp_Napaul_screens_no-grid.pdf |
| Before and after comparison, at least five improvements highlighted | Section 4, five pairs, one per screen               |
| Brief written explanation of each improvement                       | Section 5                             |
| Updated Figma link, view mode                                       | Section 6                             |

---

*Working note → [[uxui-usability-test]] · Hub → [[uxui-facility-booking-project]] · Status → [[uxui-project-state]]*
