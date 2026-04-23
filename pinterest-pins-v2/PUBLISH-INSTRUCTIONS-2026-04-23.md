# Pinterest Publishing Instructions — 2026-04-23

Chrome extension was not connected during the scheduled pin run, so these 3 pins need to be published manually (or by a future run with Chrome connected).

**Account:** pinterest.com/wolvestack (wolvestack@pm.me)
**Board:** Peptide Research Guides

---

## Pin 1 — Cagrisema

- **Image:** `pinterest-pins-v2/pin-cagrisema-guide.png`
- **Title:** Cagrisema Guide: GLP-1/Amylin Combination for Weight Loss
- **Description:** Research guide to cagrisema — the investigational GLP-1/amylin receptor co-agonist from Novo Nordisk. Covers Phase 3 weight-loss data, dosing protocol, and comparison to semaglutide and tirzepatide. #peptides #research #biohacking #health #cagrisema #GLP1 #amylin #weightloss #NovoNordisk #obesity
- **Link:** https://wolvestack.com/cagrisema-guide
- **Board:** Peptide Research Guides

---

## Pin 2 — Cerebrolysin

- **Image:** `pinterest-pins-v2/pin-cerebrolysin-guide.png`
- **Title:** Cerebrolysin: What the Research Actually Shows
- **Description:** Evidence-based guide to cerebrolysin — the porcine-derived neurotrophic peptide mixture. Covers stroke and Alzheimer's clinical data, dosing protocols, cognitive enhancement mechanisms, and safety profile. #peptides #research #biohacking #nootropics #cerebrolysin #cognitive #brainhealth #neuroprotection #alzheimers #stroke
- **Link:** https://wolvestack.com/cerebrolysin-guide
- **Board:** Peptide Research Guides

---

## Pin 3 — HGH Fragment 176-191

- **Image:** `pinterest-pins-v2/pin-fragment-176-191-guide.png`
- **Title:** HGH Fragment 176-191 Guide: The Fat Loss Peptide Explained
- **Description:** Complete guide to HGH Fragment 176-191 — the modified GH peptide that targets lipolysis without the systemic growth hormone side effects. Covers mechanism, clinical evidence, dosing, and stacking protocols. #peptides #research #biohacking #health #HGHfragment #fatloss #lipolysis #weightloss #GH #bodycomposition
- **Link:** https://wolvestack.com/fragment-176-191-guide
- **Board:** Peptide Research Guides

---

## Manual Publishing Workflow (reference)

1. Go to https://www.pinterest.com/pin-builder/?tab=save_from_url
2. For each pin above:
   - Upload the image from `pinterest-pins-v2/`
   - Paste the Title
   - Paste the destination Link (article URL)
   - Paste the Description LAST (Pinterest loses the description if focus moves)
   - Select board: **Peptide Research Guides**
   - Click Publish
3. After each pin is published, update `pinterest-pins-log.json`:
   - Set `status` to `published_v2`
   - Set `pin_v2_date` to today's date
