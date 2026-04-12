const fs = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat,
        HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak, ExternalHyperlink, TableOfContents } = fs;

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function headerCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: "1a3a4a", type: ShadingType.CLEAR },
    margins: cellMargins,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: "FFFFFF", font: "Arial", size: 20 })] })]
  });
}

function cell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    margins: cellMargins,
    children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20 })] })]
  });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1a3a4a" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2e75b6" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "333333" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets2",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets3",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets4",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets5",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets6",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets7",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbersPhase",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [
    // TITLE PAGE
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ spacing: { before: 3000 }, children: [] }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "WOLVESTACK", size: 56, bold: true, font: "Arial", color: "1a3a4a" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [new TextRun({ text: "Peptide Tracking App", size: 44, font: "Arial", color: "2e75b6" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "Business Plan & Market Analysis", size: 28, font: "Arial", color: "666666" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "April 2026", size: 24, font: "Arial", color: "666666" })]
        }),
        new Paragraph({ spacing: { before: 2000 }, children: [] }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 6, color: "2e75b6", space: 1 } },
          spacing: { before: 200 },
          children: [new TextRun({ text: "CONFIDENTIAL", size: 20, font: "Arial", color: "999999", italics: true })]
        }),
      ]
    },
    // TABLE OF CONTENTS
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      headers: {
        default: new Header({ children: [new Paragraph({ children: [new TextRun({ text: "Wolvestack App Business Plan", font: "Arial", size: 18, color: "999999" })] })] })
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Page ", font: "Arial", size: 18, color: "999999" }), new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "999999" })]
        })] })
      },
      children: [
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
        new Paragraph({ children: [new PageBreak()] }),

        // SECTION 1: EXECUTIVE SUMMARY
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Executive Summary")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("The peptide tracking app market is experiencing explosive growth. A competitor app reached $10k MRR within 4 days of launch and became the #3 fastest growing new app globally (April 2026). The broader peptide therapeutics market is projected to grow from $54.57 billion in 2026 to $81.5 billion by 2034."),
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("Wolvestack is uniquely positioned to capitalize on this opportunity. With 51 published research articles across 13 languages, an established Pinterest presence, existing affiliate relationships with peptide vendors, and deep domain expertise, Wolvestack already owns the content layer that every competitor app lacks. The strategy is to launch a companion app (or rebrand as a platform) that converts existing organic traffic into recurring subscription revenue while leveraging content as the moat no pure-tool competitor can replicate."),
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun({ text: "Target: $10k MRR within 90 days of launch.", bold: true }),
        ]}),

        // SECTION 2: MARKET ANALYSIS
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Market Analysis")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Market Size & Growth")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("The peptide market sits at the intersection of three massive trends: biohacking going mainstream, GLP-1 weight loss drugs exploding in popularity, and health apps reaching $3.5B in revenue (up 23.5% YoY). Peptides went from underground biohacker forums to Marketplace (NPR) coverage in January 2026. The user base is expanding from hardcore biohackers to mainstream health consumers, particularly driven by semaglutide and tirzepatide adoption."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Competitive Landscape")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("At least 10 peptide tracking apps now exist in the App Store. The market went from zero to crowded in roughly 6 months. Key competitors:"),
        ]}),

        // Competitor table
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [1800, 2200, 2200, 1560, 1600],
          rows: [
            new TableRow({ children: [
              headerCell("App", 1800), headerCell("Key Features", 2200), headerCell("Pricing", 2200), headerCell("Rating", 1560), headerCell("Differentiator", 1600)
            ]}),
            new TableRow({ children: [
              cell("PeptIQ", 1800), cell("AI protocols (GPT-4), vial scanner, Apple Health sync, 85+ peptides", 2200), cell("Free (3 peptides) / $19.99/mo or $99.99/yr", 2200), cell("New, growing fast", 1560), cell("AI-powered protocol builder", 1600)
            ]}),
            new TableRow({ children: [
              cell("SHOTLOG", 1800), cell("Dose tracking, reconstitution calc, weight/photo tracking, half-life decay", 2200), cell("Free + Premium (30-day demo)", 2200), cell("2.8/5 (10 ratings)", 1560), cell("Half-life visualization", 1600)
            ]}),
            new TableRow({ children: [
              cell("PeptideKit", 1800), cell("Protocol management, progress tracking (weight, muscle, aging, healing)", 2200), cell("Freemium subscription", 2200), cell("Early stage", 1560), cell("Goal-based tracking", 1600)
            ]}),
            new TableRow({ children: [
              cell("PepTracker", 1800), cell("Dose logging, reminders, weight loss tracking", 2200), cell("Freemium", 2200), cell("Positive reviews", 1560), cell("GLP-1 focused", 1600)
            ]}),
            new TableRow({ children: [
              cell("Pep", 1800), cell("Peptide + TRT + HRT + GLP-1 tracking", 2200), cell("Subscription", 2200), cell("New", 1560), cell("Broad hormone scope", 1600)
            ]}),
            new TableRow({ children: [
              cell("CycleViz", 1800), cell("Fast compound logging, injection site, notes", 2200), cell("Subscription", 2200), cell("New", 1560), cell("Speed of logging", 1600)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Competitor Weaknesses")] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
          new TextRun({ text: "No content moat: ", bold: true }), new TextRun("Every competitor is a pure tool. They have no original research, no educational content, no SEO presence. Users discover them through App Store search, not organic traffic.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
          new TextRun({ text: "No community: ", bold: true }), new TextRun("Most are solo-dev projects with no forums, no user-generated protocols, no social features.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
          new TextRun({ text: "Generic AI: ", bold: true }), new TextRun("PeptIQ uses GPT-4 with generic prompting. None are fine-tuned on actual peptide research data.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
          new TextRun({ text: "No vendor relationships: ", bold: true }), new TextRun("None have affiliate integrations with peptide suppliers, missing the highest-margin revenue stream.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
          new TextRun({ text: "No multilingual support: ", bold: true }), new TextRun("All English-only. The international peptide market is completely unserved by apps.")
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        // SECTION 3: WOLVESTACK COMPETITIVE ADVANTAGES
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Wolvestack Competitive Advantages")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("Wolvestack has several structural advantages that no pure-app competitor can easily replicate:"),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Existing Content & SEO Moat")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("51 research articles covering every major peptide, published in 13 languages (663 total pages). This content already ranks in search and drives organic traffic. Competitors would need months of content creation to match this, and Wolvestack adds new articles daily via automated pipeline."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Built-in Distribution")] }),
        new Paragraph({ numbering: { reference: "bullets2", level: 0 }, children: [
          new TextRun({ text: "SEO traffic: ", bold: true }), new TextRun("Organic visitors already landing on Wolvestack articles are the exact target user for a peptide app. Every article becomes a funnel to the app.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets2", level: 0 }, children: [
          new TextRun({ text: "Pinterest: ", bold: true }), new TextRun("51 pins on the Peptide Research Guides board, driving additional discovery traffic.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets2", level: 0 }, children: [
          new TextRun({ text: "Multilingual reach: ", bold: true }), new TextRun("Content in 13 languages means app can launch internationally from day one with built-in user acquisition in each market.")
        ]}),
        new Paragraph({ spacing: { after: 120 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Affiliate Revenue Layer")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("Existing affiliate relationships with Ascension, Particle (10%), Limitless, and Integrative Peptides. Peptide vendor affiliate commissions are lucrative: Apollo offers 20% with $150+ AOV and lifetime rebills. An in-app vendor marketplace with affiliate tracking could generate more revenue than subscriptions alone. Average peptide user spends $500+/month on peptides."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("App Store Optimization Experience")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("Your existing ASO experience is a major advantage in a category that just exploded. Most competing devs are building apps, not optimizing listings. Key ASO opportunities: custom product pages (up to 70 CPPs per app now), long-tail keyword targeting for specific peptides (\"BPC-157 tracker\", \"semaglutide dose calculator\"), and multilingual metadata that most competitors ignore entirely."),
        ]}),

        // SECTION 4: PRODUCT STRATEGY
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Product Strategy")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("App vs Sister App Decision")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun({ text: "Recommendation: Sister app under the Wolvestack brand.", bold: true }),
          new TextRun(" Keep the website as the content/SEO engine and launch a dedicated app. The website drives traffic and credibility; the app captures and monetizes that traffic. They reinforce each other. The app name should include \"Wolvestack\" for brand continuity but also target keywords (e.g., \"Wolvestack: Peptide Tracker\")."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Core Features (MVP)")] }),
        new Paragraph({ spacing: { after: 60 }, children: [
          new TextRun({ text: "Launch with these features to be competitive:", italics: true }),
        ]}),
        new Paragraph({ numbering: { reference: "bullets3", level: 0 }, children: [
          new TextRun({ text: "Peptide Library: ", bold: true }), new TextRun("Full database of 85+ peptides with Wolvestack research content integrated (not just names and dosages, but actual research summaries from your articles). This is the key differentiator.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets3", level: 0 }, children: [
          new TextRun({ text: "Dose Tracker & Reminders: ", bold: true }), new TextRun("Log injections with time, dosage, injection site. Push notification reminders. Site rotation tracking with body map.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets3", level: 0 }, children: [
          new TextRun({ text: "Reconstitution Calculator: ", bold: true }), new TextRun("Table stakes feature. Calculate BAC water volume, syringe units from vial size and desired dose.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets3", level: 0 }, children: [
          new TextRun({ text: "Protocol Templates: ", bold: true }), new TextRun("Pre-built protocols for common stacks (BPC-157 + TB-500, CJC-1295 + Ipamorelin, etc.) pulled from Wolvestack guide content.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets3", level: 0 }, children: [
          new TextRun({ text: "Progress Tracking: ", bold: true }), new TextRun("Weight, body measurements, progress photos, mood, side effects. Apple Health integration.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets3", level: 0 }, children: [
          new TextRun({ text: "Inventory Management: ", bold: true }), new TextRun("Track vial supply, expiration dates, reorder alerts that link to affiliate vendors.")
        ]}),
        new Paragraph({ spacing: { after: 120 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Premium Features (Subscription)")] }),
        new Paragraph({ numbering: { reference: "bullets4", level: 0 }, children: [
          new TextRun({ text: "AI Protocol Assistant: ", bold: true }), new TextRun("Claude or GPT-powered, but trained on Wolvestack's 51 research articles. Users describe goals, get personalized protocol suggestions with citations to your research.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets4", level: 0 }, children: [
          new TextRun({ text: "Half-Life Decay Visualization: ", bold: true }), new TextRun("Animated charts showing active peptide levels over time based on logged doses.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets4", level: 0 }, children: [
          new TextRun({ text: "Advanced Analytics: ", bold: true }), new TextRun("Correlation analysis between peptide protocols and tracked health metrics.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets4", level: 0 }, children: [
          new TextRun({ text: "Vendor Marketplace: ", bold: true }), new TextRun("In-app peptide vendor comparison with pricing, purity data, and one-tap ordering through affiliate links.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets4", level: 0 }, children: [
          new TextRun({ text: "Multilingual Support: ", bold: true }), new TextRun("Leverage existing 13-language content for international users. No competitor offers this.")
        ]}),
        new Paragraph({ numbering: { reference: "bullets4", level: 0 }, children: [
          new TextRun({ text: "Cloud Sync & Export: ", bold: true }), new TextRun("Cross-device sync, data export for sharing with healthcare providers.")
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        // SECTION 5: BUSINESS MODEL & PRICING
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Business Model & Pricing")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Revenue Streams")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("Three complementary revenue streams, designed so each reinforces the others:"),
        ]}),

        // Revenue streams table
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [2200, 2800, 2200, 2160],
          rows: [
            new TableRow({ children: [
              headerCell("Stream", 2200), headerCell("Mechanism", 2800), headerCell("Expected Revenue", 2200), headerCell("Margin", 2160)
            ]}),
            new TableRow({ children: [
              cell("App Subscription", 2200), cell("Monthly/annual premium tier via App Store + web", 2800), cell("$5-15k/mo at scale", 2200), cell("~70% (after Apple cut)", 2160)
            ]}),
            new TableRow({ children: [
              cell("Affiliate Commissions", 2200), cell("In-app vendor links, reorder alerts, marketplace", 2800), cell("$3-10k/mo at scale", 2200), cell("~95% (pure margin)", 2160)
            ]}),
            new TableRow({ children: [
              cell("Sponsored Vendor Listings", 2200), cell("Premium placement in vendor marketplace", 2800), cell("$1-3k/mo at scale", 2200), cell("~100%", 2160)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Pricing Strategy")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("Price at $14.99/month or $79.99/year (45% discount for annual). This undercuts PeptIQ ($19.99/mo) while still being premium. The target user spends $500+/month on peptides; $15/mo for tracking and optimization is trivially justified. Offer a 7-day free trial with full access to drive conversion."),
        ]}),

        // Pricing tier table
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [2000, 3680, 3680],
          rows: [
            new TableRow({ children: [
              headerCell("Tier", 2000), headerCell("Features", 3680), headerCell("Price", 3680)
            ]}),
            new TableRow({ children: [
              cell("Free", 2000), cell("3 peptides, basic tracker, reconstitution calculator, library access (limited), ads for vendor marketplace", 3680), cell("$0", 3680)
            ]}),
            new TableRow({ children: [
              cell("Premium", 2000), cell("Unlimited peptides, AI assistant, advanced analytics, half-life charts, cloud sync, no ads, full library, protocol templates, inventory management", 3680), cell("$14.99/mo or $79.99/yr", 3680)
            ]}),
            new TableRow({ children: [
              cell("Lifetime", 2000), cell("All Premium features forever. Early adopter offer only.", 3680), cell("$149.99 (launch promo)", 3680)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Revenue Projections")] }),
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [2340, 2340, 2340, 2340],
          rows: [
            new TableRow({ children: [
              headerCell("Milestone", 2340), headerCell("Timeline", 2340), headerCell("Subscribers", 2340), headerCell("MRR (App Only)", 2340)
            ]}),
            new TableRow({ children: [
              cell("Launch", 2340), cell("Month 1", 2340), cell("100-200", 2340), cell("$1,500 - $3,000", 2340)
            ]}),
            new TableRow({ children: [
              cell("Growth", 2340), cell("Month 3", 2340), cell("500-700", 2340), cell("$7,500 - $10,500", 2340)
            ]}),
            new TableRow({ children: [
              cell("Scale", 2340), cell("Month 6", 2340), cell("1,500-2,000", 2340), cell("$22,500 - $30,000", 2340)
            ]}),
            new TableRow({ children: [
              cell("Maturity", 2340), cell("Month 12", 2340), cell("3,000-5,000", 2340), cell("$45,000 - $75,000", 2340)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 80 }, children: [
          new TextRun({ text: "Note: Affiliate revenue adds an estimated 30-50% on top of subscription MRR.", italics: true, size: 20, color: "666666" }),
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        // SECTION 6: APP STORE STRATEGY
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("App Store Optimization Strategy")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Keyword Strategy")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("The peptide tracker category is new enough that keyword competition is relatively low, but growing fast. Target a mix of broad and long-tail keywords:"),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Primary Keywords")] }),
        new Paragraph({ numbering: { reference: "bullets5", level: 0 }, children: [new TextRun("peptide tracker, peptide calculator, peptide app, peptide dose tracker")] }),
        new Paragraph({ numbering: { reference: "bullets5", level: 0 }, children: [new TextRun("semaglutide tracker, tirzepatide tracker, GLP-1 tracker")] }),
        new Paragraph({ numbering: { reference: "bullets5", level: 0 }, children: [new TextRun("BPC-157 dosage, TB-500 protocol, peptide reconstitution")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Long-Tail Keywords (Less Competition)")] }),
        new Paragraph({ numbering: { reference: "bullets6", level: 0 }, children: [new TextRun("peptide injection site rotation, peptide half-life calculator")] }),
        new Paragraph({ numbering: { reference: "bullets6", level: 0 }, children: [new TextRun("peptide stacking guide, peptide reconstitution calculator")] }),
        new Paragraph({ numbering: { reference: "bullets6", level: 0 }, children: [new TextRun("biohacking tracker, peptide research guide, peptide protocol builder")] }),
        new Paragraph({ spacing: { after: 120 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Custom Product Pages (CPPs)")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("With up to 70 CPPs now available, create targeted landing pages for different user intents. For example: a GLP-1/weight loss focused CPP for \"semaglutide tracker\" searches, a healing/recovery CPP for \"BPC-157 dosage\" searches, and a bodybuilding CPP for \"peptide stack\" searches. Each CPP shows screenshots and copy tailored to that specific use case."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Cross-Promotion Flywheel")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("This is the biggest advantage over competitors: every Wolvestack article becomes an app funnel. Add smart app banners to the website, deep links from articles to relevant app content (e.g., \"BPC-157 Guide\" article links to the BPC-157 protocol template in the app), and in-app links back to full research articles on the website. Pinterest pins can also include app download CTAs. This creates a flywheel: content drives app installs, app users consume more content, more content ranks higher, drives more installs."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Ratings & Reviews Strategy")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("Prompt for reviews after positive moments (successful protocol completion, milestone tracked). Target 4.7+ average with 100+ reviews within first 60 days. Respond to every review publicly. Most competitors have very few ratings (SHOTLOG has only 10), so building a review base quickly will dominate the category."),
        ]}),

        // SECTION 7: TECHNICAL APPROACH
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Technical Approach")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Build vs No-Code")] }),
        new Paragraph({ spacing: { after: 120 }, children: [
          new TextRun("Two viable paths depending on budget and timeline:"),
        ]}),

        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [1800, 3780, 3780],
          rows: [
            new TableRow({ children: [
              headerCell("Approach", 1800), headerCell("Pros", 3780), headerCell("Cons", 3780)
            ]}),
            new TableRow({ children: [
              cell("React Native / Flutter", 1800), cell("Full control, custom UI, better performance, own your codebase, App Store + Google Play from one codebase", 3780), cell("2-4 months dev time, $5-15k if outsourced, ongoing maintenance", 3780)
            ]}),
            new TableRow({ children: [
              cell("No-Code (FlutterFlow, Adalo)", 1800), cell("Launch in 2-4 weeks, lower upfront cost, iterate faster, some offer 50/50 revenue split with technical partner", 3780), cell("Limited customization, vendor lock-in, harder to differentiate UI, platform fees", 3780)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 120 }, children: [] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun({ text: "Recommendation: ", bold: true }),
          new TextRun("Start with React Native for a native feel on both platforms. Use Expo for faster development. The investment pays off with full ownership and the ability to build genuinely differentiated features (AI integration, vendor marketplace, deep linking with website). If budget is tight, a no-code MVP to validate demand first is also viable."),
        ]}),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("AI Integration")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("The AI protocol assistant is the premium feature that justifies subscription pricing. Fine-tune or RAG-augment a model with all 51 Wolvestack research articles as source material. Unlike PeptIQ (which uses generic GPT-4), Wolvestack's AI would cite specific research from its own articles, creating a self-reinforcing content ecosystem. Cost: approximately $0.01-0.05 per query using Claude Haiku or GPT-4o-mini, well within margin at $14.99/mo subscription."),
        ]}),

        // SECTION 8: GO-TO-MARKET
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Go-to-Market Plan")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Phase 1: Pre-Launch (Weeks 1-4)")] }),
        new Paragraph({ numbering: { reference: "numbersPhase", level: 0 }, children: [
          new TextRun("Add email capture / waitlist to all Wolvestack articles (\"Get early access to the Wolvestack peptide tracking app\")")
        ]}),
        new Paragraph({ numbering: { reference: "numbersPhase", level: 0 }, children: [
          new TextRun("Create landing page at wolvestack.com/app with feature preview and email signup")
        ]}),
        new Paragraph({ numbering: { reference: "numbersPhase", level: 0 }, children: [
          new TextRun("Add Pinterest pins specifically about the upcoming app")
        ]}),
        new Paragraph({ numbering: { reference: "numbersPhase", level: 0 }, children: [
          new TextRun("Build MVP with core features (tracker, calculator, library, reminders)")
        ]}),
        new Paragraph({ spacing: { after: 120 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Phase 2: Launch (Weeks 5-8)")] }),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Submit to App Store with optimized metadata, screenshots, and CPPs")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Email waitlist with launch announcement and 30-day free premium trial")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Add smart app banners and deep links to all 663 article pages")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Lifetime deal at $149.99 for first 100 users (creates urgency, generates reviews, front-loads revenue)")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Post on peptide Reddit communities, biohacking forums, and relevant X/Twitter accounts")
        ]}),
        new Paragraph({ spacing: { after: 120 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Phase 3: Growth (Months 3-6)")] }),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Launch vendor marketplace with affiliate integration")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Add AI protocol assistant as premium feature")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Expand to international markets leveraging existing 13-language content")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Introduce sponsored vendor listings")
        ]}),
        new Paragraph({ numbering: { reference: "bullets7", level: 0 }, children: [
          new TextRun("Explore Apple Search Ads for high-intent keywords")
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        // SECTION 9: RISKS & MITIGATION
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Risks & Mitigation")] }),
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [2800, 2400, 4160],
          rows: [
            new TableRow({ children: [
              headerCell("Risk", 2800), headerCell("Severity", 2400), headerCell("Mitigation", 4160)
            ]}),
            new TableRow({ children: [
              cell("App Store rejection (health claims)", 2800), cell("Medium", 2400), cell("Frame as research/educational tracker, not medical device. Avoid treatment claims. Include disclaimers.", 4160)
            ]}),
            new TableRow({ children: [
              cell("Market saturation", 2800), cell("Medium", 2400), cell("Content moat and affiliate revenue mean Wolvestack can succeed even in a crowded tracker market. Differentiation through content, not just features.", 4160)
            ]}),
            new TableRow({ children: [
              cell("Regulatory changes (peptide scheduling)", 2800), cell("Low-Medium", 2400), cell("Diversify to broader biohacking/supplement tracking. App architecture should support any compound, not just peptides.", 4160)
            ]}),
            new TableRow({ children: [
              cell("Apple 30% commission on subscriptions", 2800), cell("Low", 2400), cell("Offer web-based subscription as alternative. Affiliate revenue bypasses Apple entirely.", 4160)
            ]}),
            new TableRow({ children: [
              cell("AI costs at scale", 2800), cell("Low", 2400), cell("Use Claude Haiku or GPT-4o-mini ($0.01-0.05/query). Rate limit free tier. Revenue per user far exceeds AI cost.", 4160)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        // SECTION 10: FINANCIAL SUMMARY
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Financial Summary")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Startup Costs")] }),
        new Table({
          width: { size: 9360, type: WidthType.DXA },
          columnWidths: [4680, 4680],
          rows: [
            new TableRow({ children: [
              headerCell("Item", 4680), headerCell("Estimated Cost", 4680)
            ]}),
            new TableRow({ children: [
              cell("App development (React Native, outsourced)", 4680), cell("$5,000 - $15,000", 4680)
            ]}),
            new TableRow({ children: [
              cell("Apple Developer Account", 4680), cell("$99/year", 4680)
            ]}),
            new TableRow({ children: [
              cell("Google Play Developer Account", 4680), cell("$25 one-time", 4680)
            ]}),
            new TableRow({ children: [
              cell("Backend hosting (Firebase/Supabase)", 4680), cell("$0-50/mo initially", 4680)
            ]}),
            new TableRow({ children: [
              cell("AI API costs (first 3 months)", 4680), cell("$100-500", 4680)
            ]}),
            new TableRow({ children: [
              cell("Design assets / App Store screenshots", 4680), cell("$500-1,000", 4680)
            ]}),
            new TableRow({ children: [
              cell("Apple Search Ads (launch budget)", 4680), cell("$500-2,000", 4680)
            ]}),
            new TableRow({ children: [
              cell("Total estimated startup", 4680), cell("$6,000 - $19,000", 4680)
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 160 }, children: [] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Break-Even Analysis")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("At $14.99/mo with Apple's 30% cut, net revenue per subscriber is approximately $10.50/mo. At $15k startup cost, break-even requires approximately 1,430 subscriber-months, or roughly 240 subscribers sustained for 6 months. Given existing Wolvestack traffic and the affiliate revenue layer (which has near-zero marginal cost), break-even within 3-4 months post-launch is realistic."),
        ]}),

        // SECTION 11: CONCLUSION
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Conclusion & Recommendation")] }),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("The peptide app market is in a land-grab phase. Multiple apps have launched in the past 6 months, at least one has hit $10k MRR within days, and the underlying market (peptide therapeutics, GLP-1 drugs, biohacking) is growing rapidly. Wolvestack has structural advantages that pure-tool competitors cannot replicate: content moat, SEO distribution, multilingual reach, affiliate relationships, and ASO experience."),
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun("The recommendation is to move quickly. Launch an MVP within 8 weeks, use existing content as distribution, and layer in premium features (AI, vendor marketplace) in months 2-4. The combination of subscription revenue and affiliate commissions creates a diversified revenue model with strong margins. The window for establishing dominance in this category is open but closing."),
        ]}),
        new Paragraph({ spacing: { after: 160 }, children: [
          new TextRun({ text: "Next steps: Validate demand by adding a waitlist to wolvestack.com, begin MVP development, and prepare App Store assets.", bold: true }),
        ]}),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buffer => {
  require('fs').writeFileSync("/sessions/confident-friendly-thompson/mnt/cowork/peptide-daily-content/wolvestack-app-business-plan.docx", buffer);
  console.log("Document created successfully");
});
