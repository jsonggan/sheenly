# Makeup Inventory App — Product & Features Document

## Product Vision

A home makeup inventory app where users can **upload an image of their makeup**, and AI identifies products on the table and records them to a database. Users can later add **expiry dates**, get **recommendations** based on their inventory, and receive **color-tone suggestions** from **face analysis**.

---

## Is This a Good Idea?

**Yes, with caveats.**

- **Real problem:** Most people don’t know what they own, products expire unnoticed, and repurchasing is chaotic.
- **Differentiator:** AI (image recognition + face analysis) makes it feel modern and useful, not just another list app.
- **Risk:** The recommendation engine must be strong from day one. Wrong undertone or bad product suggestions will destroy trust.

---

## Competitor Analysis

| Competitor | Focus | Gap vs. Us |
|------------|--------|------------|
| **YSL Beauty Scanner / L'Oréal Modiface** | Brand-specific AR try-on | Not inventory; brand-owned → conflict of interest in recommendations. |
| **Glambot** | Reselling used makeup | No inventory or recommendation layer. |
| **Think Dirty / CosDNA** | Ingredient safety scanning | No inventory, no AI recommendations. |
| **BeautyStack / Curel** | Community-driven logging | Basic logging only; no image recognition. |
| **Pincel / Makeup by Mario** | Tutorials | Not inventory. |

**Conclusion:** No dominant “makeup operating system” that combines **inventory + expiry tracking + AI recommendations + skin/face analysis**. That’s the opening.

---

## Core Features (MVP)

1. **Image upload → AI product identification**  
   User uploads a photo of makeup on a table; AI detects and lists products → save to DB.

2. **Expiry tracking**  
   User can record and edit expiry/open dates per product; reminders when items are close to expiring.

3. **Inventory list**  
   Searchable, filterable list of all identified products (with optional manual add/edit).

---

## Expanded Features (Post-MVP)

### Must-Haves

- **Expiry intelligence**  
  Use the **PAO symbol** (open-jar icon with “6M”, “12M”, etc.) and read it from the uploaded image. Many users don’t know this exists.

- **Duplicate detection**  
  “You own 4 similar nude lipsticks — here are the differences.” Useful and shareable.

- **Low-stock alerts**  
  Estimate usage from repurchase history; nudge before a product runs out.

- **Shade matching across brands**  
  “Your MAC NC25 matches Fenty 230N and NARS Syracuse.” Strong retention driver.

- **Ingredient conflict checker**  
  Flag combinations that shouldn’t be layered (e.g. retinol + vitamin C). Safety/skincare angle.

- **Skin tone profile**  
  From face scan, build a persistent profile so every recommendation is filtered by undertone/skin type.

- **“Get the look” reverse feature**  
  User uploads an Instagram (or any) photo of a look; app suggests which products in their inventory can replicate it and what’s missing.

### Nice-to-Haves

- **Wishlists with price-drop tracking**  
  Integrate Sephora/Ulta/Amazon (APIs or scraping) for price alerts.

- **Routine builder**  
  Morning vs. evening routines, ordered by application order.

---

## AI & Recommendation Layer

- **Image recognition:** Identify products (brand, type, shade where visible) from table/desk photos.
- **Face analysis:** Infer skin tone/undertone for color recommendations (foundation, lip, blush, etc.).
- **Similar products:** Recommend alternatives based on what’s already in the inventory (same category, similar shade/use case).
- **Trust:** Recommendations must be accurate and unbiased; brand-agnostic positioning is the moat.

---

## Scaling & Monetization

- **Affiliate:** Sephora, Ulta, Amazon affiliate programs on recommended products.
- **Subscription:** Premium features (shade matching, skin analysis, routine AI, advanced alerts).
- **B2B data:** Anonymized trends (what people own vs. buy) as a future data product for brands.

**Risk:** Sephora/Ulta could build this in-house (they have purchase history). **Moat:** Brand agnosticism — users trust the app because it’s not pushing one brand.

---

## Recommended Build Order

1. **MVP:** Image upload → AI product ID → save to DB + **expiry tracking** and basic inventory list. No face analysis yet.
2. **Second:** Expiry intelligence (PAO reading), duplicate detection, low-stock alerts.
3. **Third:** Face analysis + skin tone profile + shade matching and “get the look.”
4. **Fourth:** Routine builder, wishlists, price tracking, ingredient checker.

**Rationale:** Face analysis is harder and needs more user trust. Earn trust with simple, reliable utility first; then add AI skin and color features. The recommendation engine is where the product wins or loses long-term — invest in it early in design and data.

---

## Platform

- **TBD:** Mobile app, web app, or both. Decision should align with where target users (e.g. girlfriend → later beauty enthusiasts) actually manage their routines and take photos (phone-first suggests mobile or responsive web + mobile).

---

## Summary

- **Idea:** Strong; real problem, clear gap in the market.
- **MVP:** Image-based inventory + expiry tracking + DB.
- **Differentiation:** Brand-agnostic inventory + expiry + AI (ID, then face + recommendations).
- **Monetization:** Affiliate, premium subscription, optional B2B data.
- **Success factor:** Recommendation quality and user trust; keep recommendations accurate and unbiased.
