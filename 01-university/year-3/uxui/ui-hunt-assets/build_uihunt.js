const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  Header, AlignmentType, BorderStyle,
  TabStopType, TabStopPosition
} = require('docx');
const fs = require('fs');
const path = require('path');

const ASSETS = __dirname;
const OUT = path.join(require('os').homedir(), 'Documents', 'University', 'Year-3', 'UXUI', '67011178_UIHunt.docx');

const PAGE = { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } };
const NAVY = '1F3864';
const BLUE = '2E75B6';

function img(filename, altTitle, w, h) {
  const data = fs.readFileSync(path.join(ASSETS, filename));
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 80 },
    children: [new ImageRun({
      type: 'png', data,
      transformation: { width: w, height: h },
      altText: { title: altTitle, description: altTitle, name: altTitle }
    })]
  });
}

const ss = (f, alt) => img(f, alt, 480, 255);

function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 240 },
    children: [new TextRun({ text, italics: true, size: 20, font: 'Times New Roman' })]
  });
}

function sectionHead(text) {
  return new Paragraph({
    spacing: { before: 400, after: 120 },
    children: [new TextRun({ text, bold: true, size: 28, color: BLUE, font: 'Times New Roman' })]
  });
}

function dim(label, text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 200, after: 80, line: 360, lineRule: 'auto' },
    children: [
      new TextRun({ text: label + ': ', bold: true, size: 24, font: 'Times New Roman' }),
      new TextRun({ text, size: 24, font: 'Times New Roman' })
    ]
  });
}

function body(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: 160, line: 360, lineRule: 'auto' },
    indent: { firstLine: 720 },
    children: [new TextRun({ text, size: 24, font: 'Times New Roman' })]
  });
}

function urlLine(text) {
  return new Paragraph({
    spacing: { before: 0, after: 120 },
    children: [new TextRun({ text, size: 20, color: '767676', italics: true, font: 'Times New Roman' })]
  });
}

function gap() {
  return new Paragraph({ spacing: { before: 0, after: 80 }, children: [new TextRun('')] });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Times New Roman', size: 24 } } }
  },
  sections: [{
    properties: { page: PAGE },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA', space: 1 } },
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            new TextRun({ text: 'UI Hunt', bold: true, size: 20, font: 'Times New Roman' }),
            new TextRun({ text: '\t', size: 20 }),
            new TextRun({ text: 'Napaul Intharasing (67011178)', size: 20, font: 'Times New Roman' }),
          ]
        })]
      })
    },
    children: [

      // ── TITLE ────────────────────────────────────────────────────────────────
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 480, after: 120 },
        children: [new TextRun({ text: 'UI Hunt: Unusual Screens', bold: true, size: 52, color: NAVY, font: 'Times New Roman' })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 480 },
        children: [new TextRun({ text: 'Napaul Intharasing (67011178)', size: 24, font: 'Times New Roman' })]
      }),

      body('This report collects four web interfaces that produce confusion and mistrust in real users. Two examples come from Thai government websites that most Thai people are required to use at some point in their lives, and two come from international platforms with hundreds of millions of active users. Each interface is evaluated across the four dimensions the course establishes, which are Layout, Navigation, Colour and Buttons, and the UI Why. The goal is not only to identify problems and failures, but also to understand the decisions that led designers to build the interface this way, because that reasoning is what the improvement proposal must address.'),

      gap(),

      // ── SITE 1 ───────────────────────────────────────────────────────────────
      sectionHead('1.  กรมสรรพากร — The Revenue Department (rd.go.th)'),
      urlLine('https://www.rd.go.th    ·    Thai Government Website'),

      ss('ss_rd_main_vp_ann.png', 'rd.go.th homepage above the fold'),
      caption('Figure 1a  "rd.go.th — homepage: above-the-fold view"'),
      ss('ss_rd_scroll_ann.png', 'rd.go.th homepage scrolled'),
      caption('Figure 1b  "rd.go.th — homepage scrolled: icon grid continues without visual change"'),

      dim('Layout', 'The homepage opens with a rotating banner and then immediately presents a grid of more than thirty service icons, all rendered at the same size and with the same visual weight. There is no grouping of elements that communicates which tasks are important and which are rarely accessed. Logical grouping, the principle that related elements should be clustered and visually distinguished from unrelated ones, is absent from the entire page. The eye has no starting point, because the design treats every item as equally important to every user who visits the site.'),

      dim('Navigation', 'The top navigation bar expands into multiple dropdowns, each holding between ten and fifteen items arranged in alphabetical order rather than by frequency of use. A user who needs to file a personal income tax return must first understand the department\'s internal category structure before finding the correct page. There is no search bar on the homepage. Active guidance, which the course describes as giving users constructive direction when they appear confused or lost, does not exist here. Suggestions, alternative paths, and zero-result messages are all absent from the interface.'),

      dim('Colour and Buttons', 'Every service icon on the page shares the same blue-and-white colour scheme, with no distinction between tasks that most users need and tasks that are accessed only by specialists. There is no high-contrast call-to-action that draws the eye toward the single most common job on the site, which is submitting an annual tax return. Colour serves a decorative purpose here rather than a behavioural one, which means it fails to communicate priority or guide action.'),

      dim('The UI Why', 'Government portals in Thailand often build their information architecture from an organisational chart rather than from research into how users think about their tasks. This produces a design that serves the department\'s internal classification logic rather than the user\'s mental model. Everything together, starting from the banner, the icon grid, and the dropdown menus, has led to a page where everything is visible but nothing is findable quickly. The improvement is to surface three to five primary tasks as large, plain-language buttons above the fold, and move all other services behind a search field. This follows the Availability First principle, showing the user what they can do before asking them to navigate through a structure they did not help design.'),

      gap(),

      // ── SITE 2 ───────────────────────────────────────────────────────────────
      sectionHead('2.  สำนักงานประกันสังคม — Social Security Office (sso.go.th)'),
      urlLine('https://www.sso.go.th    ·    Thai Government Website'),

      ss('ss_sso_main_vp_ann.png', 'sso.go.th homepage above the fold'),
      caption('Figure 2a  "sso.go.th — homepage: three visual systems active in one viewport"'),
      ss('ss_sso_scroll_ann.png', 'sso.go.th homepage scrolled'),
      caption('Figure 2b  "sso.go.th — scrolled: news feed and further icon clusters below fold"'),

      dim('Layout', 'The homepage runs three independent visual systems inside the same viewport. A rotating hero banner fills the top portion of the screen, a row of icon shortcuts sits below it, and a news feed column runs along the right side. None of the three systems shares a card style, a font size, or a spacing rhythm with the others. This absence of logical grouping means that a user scanning the page cannot tell which elements are interactive, which are informational, and which are decorative. The natural reading path from the top left is interrupted at every row by a change in visual pattern.'),

      dim('Navigation', 'The primary navigation bar holds six top-level categories, each expanding into a dropdown with eight to fifteen items. The same service, สิทธิประโยชน์ or social insurance benefits, appears under at least two different parent categories with slightly different label names. A user who follows the wrong branch must go back and try the other path. Similarly, the icon shortcuts on the main page carry no persistent text labels, which means the user must recall what each icon means rather than recognising it from a description. The course identifies this pattern as a gap in the Skedda case study, where icon-only navigation forces users to hover in order to learn.'),

      dim('Colour and Buttons', 'Primary action buttons and informational links share the same blue colour throughout the page. There is no visual distinction between a button that submits a real insurance claim online and a link that opens a PDF document of regulations. In areas where status information is shown using colour coding, the state cannot be read by a user with colour vision deficiency, because colour is the only signal and no text label accompanies it. The course notes this as a direct design failure, stating that colour-only coding excludes users and that text must always be paired with hue to communicate state.'),

      dim('The UI Why', 'The most likely reason for the three-column layout is political rather than user-centred. Each column represents the content priority of a different internal department. The news feed exists because the communications team requires visibility on the homepage. The icon grid exists because the IT division manages the service shortcuts. The banner exists for executive and ministry announcements. The user\'s actual task, which is checking whether they are covered for a hospital visit or submitting a monthly contribution update, cuts across all three columns but lives clearly in none of them. The improvement is to replace the three competing systems with a single search bar as the primary input, and to display the five most common user tasks as large text cards beneath it.'),

      gap(),

      // ── SITE 3 ───────────────────────────────────────────────────────────────
      sectionHead('3.  Amazon.com — Search Results'),
      urlLine('https://www.amazon.com/s?k=laptop    ·    International E-commerce Platform'),

      ss('ss_amazon_search_ann.png', 'Amazon.com laptop search results'),
      caption('Figure 3a  "Amazon.com — search results: sponsored and organic cards visually identical"'),
      ss('ss_amazon_product_ann.png', 'Amazon.com product detail page'),
      caption('Figure 3b  "Amazon.com — product detail: competing information blocks at equal visual weight"'),

      dim('Layout', 'The search results page places four sponsored advertisement cards at the very top of every search, before a single organic result appears. Each sponsored card uses the same border, typography, image ratio, and card size as an organic result. The only differentiator is a small grey label reading Sponsored, printed at approximately ten points. A user scanning down the page from the top left, which is the natural reading path, will read four paid advertisements before encountering any unbiased result, without realising this has happened. On the product detail page in Figure 3b, competing information blocks including the price, the Prime badge, an Amazon\'s Choice label, a stock warning, and a cross-sell carousel all occupy the same visual band at the same weight, so the user cannot quickly locate the information that matters most to their decision.'),

      dim('Navigation', 'The filter sidebar on the search results page contains more than twenty filter categories, many of them collapsed by default, with no indication of which filter would most reduce the result set for a given search term. When a filter combination produces zero results, the page returns an empty state with no suggestion about which setting to relax or which alternative to try. Furthermore, the breadcrumb trail at the top of the page does not reflect the current filter state, so a user cannot retrace the steps they took to narrow the search and go back to a previous narrower view.'),

      dim('Colour and Buttons', 'The Add to Cart button uses an orange-yellow colour that meets contrast standards. Directly below it sits a Buy Now button styled at the same size and visual weight. Two equally prominent primary actions on a single screen mean the user must read each label before deciding, because visual weight alone does not guide the choice. This removes the main function that colour and size are meant to serve, which is to show the user what the next step is without requiring them to slow down and read everything.'),

      dim('The UI Why', 'Sponsored placement generates significant advertising revenue for Amazon, and making these cards visually distinct from organic results would reduce their click-through rates and therefore reduce their value to advertisers. This is the trade-off the design accepts: higher revenue in exchange for a results page where users cannot easily tell what is paid and what is genuine. By Using the Airbnb case study in this course, a useful counter-example appears. Airbnb lists prices include all fees as a UX strength precisely because removing the cost surprise at checkout builds the trust that keeps users coming back. The parallel improvement for Amazon is to give sponsored cards a distinct coloured left border, communicating paid placement clearly without removing the advertisements from the page entirely.'),

      gap(),

      // ── SITE 4 ───────────────────────────────────────────────────────────────
      sectionHead('4.  Booking.com — Hotel Search Results'),
      urlLine('https://www.booking.com    ·    International Travel Booking Platform'),

      ss('ss_booking_results_ann.png', 'Booking.com Bangkok hotel search results'),
      caption('Figure 4a  "Booking.com — search results: urgency badges positioned above the price"'),
      ss('ss_booking_hotel_ann.png', 'Booking.com hotel detail page'),
      caption('Figure 4b  "Booking.com — hotel detail: room rows each carry their own urgency label"'),

      dim('Layout', 'Each hotel result card carries seven to nine separate pieces of information: a thumbnail, the hotel name, a star rating, a guest review score, a location tag, amenity icons, a nightly price that excludes taxes, and one or two urgency badges. The urgency badges, which include messages such as Only 2 rooms left and Booked 12 times today, are printed in red or orange and placed directly above the price. This arrangement draws the eye to manufactured pressure and anxiety before it reaches the pricing information. On the hotel detail page in Figure 4b, every room type row carries its own urgency label in red text, so a user scrolling through room options encounters the same warning messages repeated down the entire page.'),

      dim('Navigation', 'The default sort order on the search results page is labelled Our top picks, which is a proprietary ranking algorithm rather than a neutral criterion such as price or guest rating. A user who does not manually change this setting is comparing hotels on a basis they did not choose and cannot inspect or understand. The course notes that Airbnb\'s linked map view allows users to trade price against location as they browse through results. Booking.com provides a map toggle but places it behind a secondary control, so the default experience is the list view where urgency badges can be applied to every row and seen repeatedly.'),

      dim('Colour and Buttons', 'Red and orange are used consistently for urgency and scarcity labels across both the search results and hotel detail pages. This is a recognisable colour convention and users understand it as a warning. The problem is that these labels are not verified against real inventory. A room listed as Only 1 left at this price may have dozens of identical rooms available at a marginally higher price, which the page never discloses. Furthermore, there are also pricing misunderstandings and conflicts that arise because the nightly rate shown on the results card excludes taxes and service fees, which can add fifteen to thirty percent to the final total that only appears at the payment step.'),

      dim('The UI Why', 'The urgency patterns on Booking.com are a deliberate application of loss aversion, where users are more motivated by the fear of losing something than by the satisfaction of finding a good deal. In Kano terms, transparent pricing is a Must-Be feature. Its presence does not increase user satisfaction above baseline, but its absence causes active dissatisfaction and abandoned bookings, because the user feels deceived when the final price differs from the one they expected. The improvement is to display the total price including all taxes and fees on the results card from the beginning, and to replace unverifiable urgency labels with factual and neutral availability counts. This matches the approach the course attributes to Airbnb as a UX strength and removes the deceptive pattern without eliminating genuine scarcity information from the interface.'),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log('Done:', OUT);
}).catch(err => { console.error(err); process.exit(1); });
