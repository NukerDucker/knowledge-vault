---
title: KMITL B-App — Final Prototype Report, Group 2
tags:
  - university
  - uxui
  - report
status: active
updated: 2026-10-11
subject: uxui
course: "01276545"
feature: 01-university/year-3/uxui/assets/final/2026-10-11/design-system/Status Badge.png
thumbnail: thumbnails/resized/cad9539edc7a7ef71752f5d0eac25ec8_86cf658e.webp
---

# KMITL B-App final prototype report, Group 2 Mookrata

UX/UI Design 01276545 · Chonchanok Nitipornsri 67011106 · Napaul Intharasing 67011178 · Mawin Pengsuk 67011163 · User type Student

Figma file [figma.com/design/bhuuET1PKmzZSGMkVr2de7](https://www.figma.com/design/bhuuET1PKmzZSGMkVr2de7/UX%2FUI%202026%20%E2%80%94%20KMITL-BApp)

At the ECC building of KMITL, booking a room for an activity still depends on LINE chats and paper notices on room doors. A request sent this way can sit unread for days. In Thailand, LINE group chats have become the normal channel for small requests like this one. This is quick for a short question, but it results in requests that are easy to miss and that carry no status at all. KMITL B-App answers this with one place where a student can find a free room, book it in four steps, and follow the request until it is approved. This report covers the work of the whole group in Part A and the flow of each member in Part B.

## Part A. The group project

### 1. Team, flows and screens

The prototype is split by the three sections of the student's task, and each member owns one section from start to end. Every frame carries the owner's name and the user type under it, in Figma and in this report.

| Member | ID | Flow | Frames | Count |
|---|---|---|---|---|
| Chonchanok Nitipornsri | 67011106 | Browse | Home, Search Results, Search Results second state, Filter, Room Detail in four states, Map in two states | 10 |
| Napaul Intharasing | 67011178 | Book | Sign In, Sign Up, Forgot Password, Reset Password, Select Date & Time, Booking Details, Upload Documents, Review Booking, Booking Submitted, five sheets | 16 |
| Mawin Pengsuk | 67011163 | Track | Booking History in four states, Booking Detail in two states, Edit Booking, Profile | 8 |

The flows connect in the order a student uses them. Browse hands over to Book through Book Now on Room Detail and Book This Room on the Map, and Book hands over to Track through View booking details on the confirmation screen. The presentation follows the same order, so each member speaks about the part of the journey that the previous member hands over.

### 2. Background and problem

The research found two users with one failure point. A student submits a booking through LINE and cannot tell whether staff have read it, so by the time it is clear that the activity cannot go ahead, it is too late to rearrange. A professor wants live room availability from the desk, but no shared calendar exists, so he walks the ECC building reading door notices, and double bookings still happen anyway. Both points of view fail at the same place, which is the lack of visibility into room state and booking progress.

The journey map followed the persona New, a 34-year-old Computer Engineering professor, through five stages. His emotion score went from 3 at the start to 2 while finding a room and submitting the request, then fell to 1 out of 5 during the wait and stayed there at the outcome. Despite the effort spent on forms, the deepest problem was the waiting stage, where nobody could see whether a request had been read. The empathy map gave the same picture from the student side, with quotes such as "Messaged staff, got left on read" and "Room shows booked even after cancellation."

### 3. UX process from week 3 to week 11

The project followed the five stages of Design Thinking, Empathize, Define, Ideate, Prototype and Test, which also map onto the Discover, Define, Develop and Deliver phases of the Double Diamond.

| Week | Deliverable | What it contributed |
|---|---|---|
| 3 | Market comparison | Competitor baseline across BU, RMUTL and Calendly |
| 4 | User journey map | The five stages and the emotional low point at the wait |
| 5 | POV and HMW | Two points of view and five HMW questions, narrowed to two |
| 6 | Hooked and Kano | Why live availability and status notification ship first |
| 7 | Crazy 8s and storyboard | First sketches of the booking and tracking screens |
| 8 | User story mapping | Four activities, from log in to tracking the request |
| 9 | Sitemap, card sorting and app comparison | Information structure, tested against three more products |
| 10 | Wireframe and wireflow | The screens joined into one flow in Figma |
| 11 | Hi-fi prototype and usability test | Five participants, fixes and a retest |

Weeks 3 to 5 sit in the Discover and Define phases, weeks 6 to 10 in Develop, and week 11 in Deliver, where the prototype was tested and improved.

### 4. Design rationale

Of the five HMW questions, two were chosen because the others fold into them. The first asks how to make live room availability visible to everyone in one shared place, and the second asks how to notify users automatically at every approval stage so they never have to message staff. Live availability and status notification are Basic features in the Kano model, since the product is broken without them, and they are also the variable reward of the Hooked model, since every return to the app is triggered by a real change in status. Two frameworks reached the same answer independently, which is why these two features were built first.

The build order followed the Kano tiers. Basic features came first with recorded bookings, live availability, status notifications and the approval workflow. Performance features came next with booking history and room detail, and Delight features such as calendar export came last. An AI room suggestion and a loyalty system were cut, because neither traces back to a point of view or an HMW question. The Hooked loop also runs across a single booking lifecycle of one to three days rather than as a daily habit, and notifications fire only on real changes in state, so the app does not manufacture urgency to bring people back.

### 5. Information architecture and flow

The user story map grouped the student's task into four activities, which are logging in, browsing and checking rooms, booking a room, and tracking its status. These four activities became the three flows of the prototype, with the log-in screens grouped into the Book set. Notifications sit at the top level of the app because they carry the second HMW, and Home works as the entry node that the three compared apps did not have.

Each flow keeps its choices small. The booking request is split into four numbered steps, which follows Miller's Law, and the sort sheet and attendee chips offer a short single list, which keeps decisions quick in the way Hick's Law describes. Longer content is shown only when it is needed, such as the collapsible summaries on Review Booking and Booking Detail, and the optional third document behind a plus sign, which is progressive disclosure.

### 6. Design system

The whole file shares one design system, built as two variable collections, a primitive colour set and a semantic set with tokens such as Text/Primary, Text/Secondary and Text/OnPrimary.

| Token | Value | Used for |
|---|---|---|
| Orange/500 | #E8622D | Main buttons, active navigation, selected states |
| Navy/500 | #1B2A5B | Headings, body text and labels |
| Neutral 0, 50, 100, 300, 400, 900 | #FFFFFF, #F5F7FA, #E5E7EB, #9CA3AF, #6B7280, #111827 | Surfaces, secondary text, disabled states |
| Status fills | #047857, #B45309, #C2410C, #4B5563, #DC2626, #6B7280 | Available and Approved, Upcoming and Busy, Partial and Under Review, Cancelled, Rejected, Unavailable and Completed |

Inter is the only typeface, in a scale of 32, 28, 24, 20, 16, 14, 12 and 11 pixels that covers headings, body text, labels and captions. Students spend most of their time in other apps that use neutral sans-serif type, so Inter reads as familiar from the first screen, which is the idea behind Jakob's Law. Cards group the details that belong together, such as room, floor and seats, which uses the Gestalt principles of similarity and common region.

The status badge is one component with ten variants, and each variant pairs a colour with an icon and a word. The badges are the only strongly coloured element on a mostly white card, so a status such as Rejected stands out at a glance, which is the Von Restorff effect.

![[assets/final/2026-10-11/design-system/Status Badge.png]]

The Status Badge component set from the live file, ten variants.

### 7. Accessibility across the file

Every ratio below was calculated from the live hex values in the Figma file with the WCAG 2.2 formula, and none of them is estimated.

| Colour pair | Ratio | WCAG 2.2 |
|---|---|---|
| Navy #1B2A5B body text on white | 13.74:1 | AAA |
| Grey #6B7280 hint and secondary text on white | 4.83:1 | AA |
| White on green #047857, Available and Approved | 5.48:1 | AA |
| White on amber #B45309, Upcoming and Busy | 5.02:1 | AA |
| White on rust #C2410C, Partial and Under Review | 5.18:1 | AA |
| White on red #DC2626, Rejected and error text | 4.83:1 | AA |
| White on grey #4B5563, Cancelled | 7.56:1 | AAA |
| White on slate #6B7280, Unavailable and Completed | 4.83:1 | AA |
| Orange #E8622D booking ID, 24 px Bold on white | 3.38:1 | AA large text |
| Orange button shape on white and on #F5F7FA | 3.38:1 and 3.15:1 | AA UI component |
| White 16 px button label on orange #E8622D | 3.38:1 | Below AA, kept by choice |
| White 12 px stepper numbers and selected chips on orange | 3.38:1 | Below AA, kept by choice |
| Grey #9CA3AF text on white, disabled states only | 2.54:1 | Exempt |

The two orange rows are a judgment call and not a pass. White text on the orange buttons measures 3.38:1, below the 4.5:1 that AA asks for normal text, and a 16 pixel Semi Bold label is not large text, so no large-text exemption is claimed. The orange was kept because a contrast ratio is only an approximation of what people see, and white carries no hue distortion on a saturated fill. This is the argument of The Myths of Color Contrast Accessibility, published on uxmovement in 2019. Despite this, the article rests on a reader poll and one study with no sample sizes, so it supports the choice without proving it, and it never uses text size to excuse its own examples. The stronger evidence came from the test, where none of the five participants raised a problem with button text and Mind praised the bright orange button for staying in the same place on every step.

Fixing a component did not fix every copy of it. The badge colours had been corrected in the component set, but on 11 October, 29 of the 126 badge instances in the file still carried old fills as overrides, and all of them were swept back to their components in the same session. The same day, every button label in the file was set to one size, 16 pixel Semi Bold, where three different sizes had been used before, and the back action on 21 headers moved from the 24 pixel arrow to the whole 68 pixel header bar.

| Flow | Elements with a prototype link | 44 points or more on both sides |
|---|---|---|
| Browse | 78 | 49 |
| Book | 91 | 35 |
| Track | 88 | 42 |

The elements under 44 points are listed in each member's section. The calendar day cells are 24 by 24, which meets the WCAG 2.5.8 minimum but stays under Apple's 44 point guideline, because a seven-column month cannot fit 44 point cells without a redesign. Following Fitts's Law, the main action on each screen is a full-width button low on the screen, the largest target and the easiest one for a thumb to reach.

### 8. Prototype completeness

The prototype has 34 frames, and all of them carry the shared layout grid of four columns with an 8 pixel gutter and a 16 pixel margin. The happy path runs from Sign In to Home, then to Room Detail and Book Now, through the four booking steps to Booking Submitted, and on to the booking detail of the new request. On 11 October, a full sweep of every prototype link found 28 links pointing at deleted variants, and all of them were repaired in the same session, so no link now points at a missing frame. Every one of the 34 frames also has a way to move on or close.

The prototype also covers the states around the happy path, which follows Nielsen's heuristics on visibility of system status, error prevention and recovery from errors. Booking History has an empty state for both Upcoming and Past, Booking Details and Upload Documents each have an empty and a filled state, Sign In shows a wrong-password error on the field, and three sheets confirm or cancel an action before it happens.

### 9. Usability test and iteration

Five participants between 20 and 22 years old were asked to find and book a room in the ECC building, and to search and filter rooms as a second task. The test plan asked each participant to think aloud while working. After a round of fixes, ching ching and cheesy returned for a retest, the attendee step no longer stopped anyone, and both rated the flow 5 out of 5. The findings and changes for each flow are reported in Part B.

The records also have gaps that the report states plainly. Putt's task results were never written down, so only his interview exists, and cheesy gave no score because both of his tasks were blocked on the first pass. Mind's session showed that three rows of the fix tracker, written from a visual comparison, did not match how the prototype actually behaved, and this mismatch is the reason the fixes were checked again in the retest.

### 10. Positioning against existing products

The market comparison in week 3 looked at three products. BU Meeting Room Reservation tracks the status of a request but has no live availability, RMUTL Room Booking shows availability first but makes every participant register and confirm, and Calendly never shows a taken slot but has no approval step for a shared university room. The app comparison in week 9 added Skedda, LibCal and Google Calendar room booking, and all three cover browsing and booking, while none covers the request, approval and notification that follow.

Every product digitizes the request, but none digitizes availability and approval together. KMITL B-App puts live availability on every room card and then layers approval on the booking as a visible status, so the student sees both the free room and the progress of the request in the same app.

### 11. Conclusion and future work

The prototype ships the Basic features that the research asked for, live availability on every room, a four-step request, a visible status from Submitted to Approved, notifications on each change, and a booking history. Some planned features were not built. The automatic release of a cancelled slot, the estimated approval time and the screens for facility staff who approve requests remain future work, and the notifications in the prototype are simulated, not sent as real push messages.

## Part B1. Browse flow, Chonchanok Nitipornsri

### Screens

The Browse flow takes a student from Home to a chosen room, through search, filtering, room detail and the floor map. It contains 10 frames, all captioned Chonchanok / Student.

![[assets/final/2026-10-11/no-grid/Home.png]]
![[assets/final/2026-10-11/no-grid/Search Results.png]]
![[assets/final/2026-10-11/no-grid/Search Results - Empty.png]]
![[assets/final/2026-10-11/no-grid/Filter.png]]
Chonchanok / Student

![[assets/final/2026-10-11/no-grid/Room Detail - Available.png]]
![[assets/final/2026-10-11/no-grid/Room Detail - Review.png]]
![[assets/final/2026-10-11/no-grid/Room Detail - Unavailable.png]]
Chonchanok / Student

![[assets/final/2026-10-11/no-grid/Room Detail - Unavailable Review.png]]
![[assets/final/2026-10-11/no-grid/Map.png]]
![[assets/final/2026-10-11/no-grid/Map - Book disabled.png]]
Chonchanok / Student

### Design decisions

Every room card in Search Results carries a status badge, such as Available or Busy until 15:00, so a student can see which rooms are free before opening any of them. This is the first HMW question in practice, and it is the Kano Basic that the research put first. The filter keeps choices short with capacity, room type and equipment chips, and Room Detail splits its content into Details and Reviews tabs, so the student reads the booking rules and equipment first and opens the reviews only when wanted. When a room is busy, Book Now is greyed out instead of leading to a request that cannot succeed, which is error prevention in Nielsen's fifth heuristic. The Map then shows the selected room on its floor with a suggested route from the lobby, so the student recognizes the room on a plan rather than recalling a room number.

### Usability and accessibility

Of the 78 linked elements in the Browse flow, 49 measure at least 44 points on both sides. The ones below 44 points are the Home avatar and notification bell at 36 by 36, the category tabs and capacity selects at 28 points tall, the filter chips at 23, the Sort by link at 17, the Details and Reviews tabs at 32, the date filter at 41, and several 24 pixel icons. The status badges on the room cards use the AA colours in section 7, and each one pairs its colour with an icon and a word.

### Test findings and before and after

Putt found the building selector on the map unreadable, because it showed bare numbers from 1 to 7, and the floor pills now read 1F to 7F. cheesy saw the same room read as Busy in Search Results and as Unavailable when it was opened, and both screens now use the same wording. He also reported that a red cross badge looked broken, since the busy state used the same red and icon as a rejected booking, and the busy badges now use amber. Nhow found that the Booking Rules section sat flush against the Book Now bar, and the bottom padding of Room Detail was increased so the last rule can scroll clear of it.

![[assets/ut/2026-10-10-prefix/before/10-map.png]]
![[assets/ut/2026-10-10-prefix/after/10-map.png]]

The Map before and after the test round, with the floor pills changed from bare numbers to 1F to 7F.

![[assets/ut/2026-10-10-prefix/before/17-badge-colour-propagation.png]]
![[assets/ut/2026-10-10-prefix/after/17-badge-colour-propagation.png]]

Search Results before and after the badge fix, with the red busy badges replaced by amber.

## Part B2. Book flow, Napaul Intharasing

### Screens

The Book flow takes a student from the Book Now button on a room page to a submitted request with a booking ID and a visible review status. It contains 16 frames, all captioned Napaul / Student, of which four are sign-in screens, seven carry the booking itself, and five are sheets that open over a screen.

![[assets/final/2026-10-11/no-grid/Sign In.png]]
![[assets/final/2026-10-11/no-grid/Sign Up.png]]
![[assets/final/2026-10-11/no-grid/Forgot Password.png]]
![[assets/final/2026-10-11/no-grid/Reset Password.png]]
Napaul / Student

![[assets/final/2026-10-11/no-grid/Select Date & Time.png]]
![[assets/final/2026-10-11/no-grid/Booking Details - Empty.png]]
![[assets/final/2026-10-11/no-grid/Booking Details - Filled.png]]
![[assets/final/2026-10-11/no-grid/Upload Documents - Empty.png]]
Napaul / Student

![[assets/final/2026-10-11/no-grid/Upload Documents - Uploaded.png]]
![[assets/final/2026-10-11/no-grid/Review Booking.png]]
![[assets/final/2026-10-11/no-grid/Booking Submitted.png]]
![[assets/final/2026-10-11/no-grid/Notification.png]]
Napaul / Student

![[assets/final/2026-10-11/no-grid/Sort Sheet.png]]
![[assets/final/2026-10-11/no-grid/Confirm Sheet.png]]
![[assets/final/2026-10-11/no-grid/Cancel Sheet.png]]
![[assets/final/2026-10-11/no-grid/Action Confirm Sheet.png]]
Napaul / Student

### Design decisions

The booking request is split into four numbered steps, Date, Details, Docs and Review, and a stepper at the top of every step shows the student where they are. Furthermore, the bottom navigation bar is also removed inside the flow, so each step offers one main action instead of four tabs that lead away from an unfinished request. On Booking Details, the attendee count is chosen from four preset chips at 10, 20, 30 and 40 people. The row stops at 40 because room ECC-603 seats 40, so a booking over capacity cannot be entered at all. Nielsen's fifth heuristic calls this error prevention, and it is kinder to the student than an error message that appears after the mistake.

Before anything is sent, Review Booking gathers every detail of the request and both documents in one collapsible summary, and the Confirm Sheet asks once more with Go Back as the way out. Booking Submitted answers the problem from research directly, with the heading You're all set, the booking ID in its own card and a tracker from Submitted to Approved. The Notification sheet then carries each change in status, which is the trigger of the Hooked model and brings the student back without anyone sending a LINE message. On the sort sheet, a request for an Apply button was declined, since a single-select list can apply on tap. Everything together, starting from the stepper to the confirmation screen, has led to a flow where the student can see what happened to the request at each point.

### Usability and accessibility

Of the 91 linked elements in the Book flow, 35 measure at least 44 points on both sides. Every button, the sheet actions and the back bar on all six booking steps meet the target, while the 30 calendar day cells are 24 by 24, the attendee chips 28 points tall, the time slots and dropdowns 32, the sort options 22 to 23, and the text links on the sign-in screens about 18. All 18 button labels in the flow are 16 pixel Semi Bold, and the booking ID on the confirmation screen is orange text at 24 pixel Bold, which passes AA as large text at 3.38:1.

### Usability test

| Participant | What broke on the Book flow | What changed |
|---|---|---|
| Putt, 20 | The confirmation screen read as a new or empty page, so he could not tell whether the booking went through | You're all set heading, booking ID card, Back to home as a full button |
| Mind, 22 | The attendee count jumped to 80 for a room that seats 40 and would not come back down | Preset chips at 10, 20, 30 and 40 |
| Nhow, 20 | The sort sheet had no choice between ascending and descending order | Low to high and high to low chips on the sort sheet |
| ching ching, 20 | The two sign-in buttons did not match, and on the retest two chosen time slots showed as one | Buttons matched, and only one slot stays open so the summary stays correct |
| cheesy, 20 | The attendee control blocked his second task, a fixed exceeds capacity warning appeared even for one person, and the sort and notification sheets had no way out | Chips replaced the control, the warning was deleted, both sheets close with a tap, and he finished the whole path on the retest |

The single-slot change on Select Date and Time came after the retest, so no participant has used it yet. As the designer of these screens, I have noticed that the participants found problems a visual check had missed, such as an attendee control that looked correct but did not work.

### Before and after

Each pair below was annotated for the usability test submission, with the issue marked on the earlier build and its fix marked on the build of 11 October.

![[assets/ut/2026-10-11/s6-s10-pairs/1-review-booking__annotated.png]]

Review Booking, from the first draft of 26 September to the current build. The summary became a collapsible card that opens with the activity, and the attachments carry real file names.

![[assets/ut/2026-10-11/s6-s10-pairs/2-upload-documents-empty__annotated.png]]

Upload Documents, from the draft of 1 October to the current build. The Continue button no longer hides under the bottom navigation.

![[assets/ut/2026-10-11/s6-s10-pairs/3-booking-submitted__annotated.png]]

Booking Submitted, from the capture of 2 October to the current build. The screen now says You're all set and shows the booking ID in its own card.

![[assets/ut/2026-10-11/s6-s10-pairs/4-select-date-time__annotated.png]]

Select Date and Time, from the build tested on 8 October to the current build. The progress line starts empty on step one and the stray orange nubs are gone.

![[assets/ut/2026-10-11/s6-s10-pairs/5-booking-details-filled__annotated.png]]

Booking Details, from the build tested on 8 October to the current build. Preset chips replace the two-value control and the fake capacity warning is deleted.

## Part B3. Track flow, Mawin Pengsuk

### Screens

The Track flow lets a student follow every booking after it is sent, from the booking history to the detail of one request, an edit request and the profile. It contains 8 frames, all captioned Mawin / Student.

![[assets/final/2026-10-11/no-grid/Booking History - Upcoming.png]]
![[assets/final/2026-10-11/no-grid/Booking History - Past.png]]
![[assets/final/2026-10-11/no-grid/Booking History - Upcoming Empty.png]]
![[assets/final/2026-10-11/no-grid/Booking History - Past Empty.png]]
Mawin / Student

![[assets/final/2026-10-11/no-grid/Booking Detail - Approved.png]]
![[assets/final/2026-10-11/no-grid/Booking Detail - Completed.png]]
![[assets/final/2026-10-11/no-grid/Edit Booking.png]]
![[assets/final/2026-10-11/no-grid/Profile.png]]
Mawin / Student

### Design decisions

Booking History splits bookings into Upcoming and Past tabs, and every booking card shows the room, the activity, the date and a status badge, so a student can scan the state of every request on one screen. Booking Detail repeats the tracker from the confirmation screen, Submitted, Reviewing and Approved, which keeps the system status visible after the request leaves the Book flow, as Nielsen's first heuristic asks. Edit Booking reuses the fields and attendee chips of the booking form, which follows Nielsen's fourth heuristic on consistency, and it separates Request Edit from Request Cancellation by colour so the destructive choice cannot be mistaken for the safe one. When there are no bookings, the empty state explains this and offers a way to start a booking instead of leaving a blank list. A completed booking also asks the student to rate the room, which is the investment step of the Hooked model, since each rating adds to the reviews that the next student reads on Room Detail.

### Usability and accessibility

Of the 88 linked elements in the Track flow, 42 measure at least 44 points on both sides. The ones below 44 points are the 30 day cells of the date picker at 24 by 24, the time slots at 34 points tall, the attendee chips at 28, the dropdown headers at 20 to 32, the Click here link at 22, and a few 16 to 24 pixel icons. The Track flow carries the widest spread of badge variants in the file, Upcoming, Approved, Pending, Rejected, Completed and Cancelled, and all of them now pass AA, from 4.83:1 for Rejected to 7.56:1 for Cancelled.

### Test findings and before and after

Mind found that Request Edit and Request Cancellation did nothing when she pressed them, and five of her six findings were fixed or addressed after the round. The two buttons for keeping and cancelling a booking had also looked identical, and Keep Booking is now an outlined button while Request Cancellation is a red one. The badge contrast failures landed hardest on the Track flow, since Approved, Pending, Completed and Cancelled all failed AA before the recolour and the instance sweep described in section 7.

![[assets/decision/prototype-evolution/30sep-11-booking-history-upcoming.png]]
![[assets/final/2026-10-11/no-grid/Booking History - Upcoming.png]]

Booking History from the build of 30 September to the current file. Two identical ECC-601 entries became varied real bookings, each with a room photo, floor, seats and a status badge.

![[assets/decision/prototype-evolution/30sep-12-booking-detail.png]]
![[assets/final/2026-10-11/no-grid/Booking Detail - Approved.png]]

Booking Detail from the build of 30 September to the current file. The capacity of 0 is gone, and the screen now shows the review tracker, an Edit booking button and actions to share, add to a calendar and get directions.

## AI Use Log

| # | Tool | Used for, page or section | Level | What we changed and why | Member |
|---|---|---|---|---|---|
| 1 | Claude | Component naming, where to find UI components, icon ideas, Components page | Green | Used as reference only, and the team chose the final names, components and icons | Napaul |
| 2 | DeepSeek through the Figma Desktop Bridge | Audit of the Figma file and the fixes Napaul directed, covering badge overrides, one navy, the hint token, button labels, tap areas, the grid and 28 dead links | Green | Every change was checked by screenshot and logged before and after in the changelog of 11 October | Napaul |
| 3 | ChatGPT | Mock data for room names, booking IDs and activity titles | Green | Changed to real ECC rooms and KMITL naming | Team |
| 4 | Claude | Drafting this report and the slide wording from the team's notes, changelog and test records | Green | Numbers were checked against the live file and the changelog of 11 October, and claims against the test notes | Napaul |

No use above is Yellow level, so no before and after evidence is owed for the log itself.
