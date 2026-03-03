# Inventory Control — Requirements & Design (Manual Entry Phase)

**Scope:** This phase supports **manual entry only**. No image upload or AI product identification. All inventory items are added, edited, and deleted by the user.

**Reference:** See [features.md](./features.md) for product vision and future phases (AI ID, expiry intelligence, etc.).

---

## 1. Data Model

| Field         | Type        | Required | Description |
|---------------|-------------|----------|-------------|
| **Category**  | string      | Yes      | Product type (e.g. Lipstick, Foundation, Mascara, Skincare). |
| **Brand**     | string      | Yes      | Brand name (e.g. MAC, Fenty, NARS). |
| **Name**      | string      | Yes      | Product name or shade (e.g. Ruby Woo, Pro Filt’r 230). |
| **Value**     | string      | No       | Free-form value: shade code, size, variant, or notes (e.g. "NC25", "30ml", "Matte"). |
| **Repurchase?** | boolean   | No       | Whether the user would repurchase this item. Default: unset/null until user sets it. |
| **Expired date** | date     | No       | Expiry date (or “use by” / “opened on” if we only store one date in this phase). |

**Identifiers:** Each inventory item is a single row. Uniqueness is **not** enforced on (Category, Brand, Name) — users can own multiple of the same product (e.g. two tubes of the same lipstick).

---

## 2. Backend Requirements

### 2.1 API Surface

- **Create** — `POST /inventory` (or `/inventory/items`)  
  Body: Category, Brand, Name, Value (optional), Repurchase (optional), Expired date (optional).  
  Returns: created item with server-generated id and timestamps.

- **Read (list)** — `GET /inventory`  
  Query params: optional filters (category, brand, repurchase, expired/expiring), sort (e.g. by expired date, brand, category), pagination (limit, offset or cursor).

- **Read (one)** — `GET /inventory/{id}`  
  Returns single item or 404.

- **Update** — `PATCH` or `PUT /inventory/{id}`  
  Body: any subset of fields to update. Returns updated item.

- **Delete** — `DELETE /inventory/{id}`  
  Returns 204 or 200 with confirmation.

### 2.2 Validation Rules

- **Category:** Non-empty string; max length (e.g. 100 chars). Trim leading/trailing whitespace. Reject blank.
- **Brand:** Same as Category.
- **Name:** Same as Category.
- **Value:** Optional; if present, max length (e.g. 200 chars). Trim. Allow empty string → store as null or empty consistently.
- **Repurchase?:** Boolean or null. Accept `true`, `false`, or omit (null).
- **Expired date:** ISO 8601 date only (no time). Accept `YYYY-MM-DD`. Reject invalid dates (e.g. 2025-02-30). Decide whether to allow future-only or also past (for “already expired” tracking).

### 2.3 Behaviour

- **Id:** Server-generated immutable id (UUID or auto-increment). Never user-editable.
- **Timestamps:** `created_at`, `updated_at` (server-set). Optional: `opened_at` in a later phase.
- **Soft delete:** Optional; if used, list endpoints filter out soft-deleted by default and require a flag to show them.

---

## 3. Database Requirements

### 3.1 Schema (conceptual)

- **Table:** e.g. `inventory_items` (or `products` if you prefer).
- **Columns:**  
  `id` (PK), `category`, `brand`, `name`, `value` (nullable), `repurchase` (nullable boolean), `expired_date` (nullable date), `created_at`, `updated_at`, optionally `deleted_at` for soft delete.
- **Indexes:**  
  - Primary key on `id`.  
  - Indexes for list/filter: `category`, `brand`, `expired_date`, `repurchase`.  
  - Optional: composite for “expiring soon” (e.g. `expired_date` where `deleted_at IS NULL`).

### 3.2 Constraints

- NOT NULL on: `id`, `category`, `brand`, `name`, `created_at`, `updated_at`.
- CHECK or application-level: category/brand/name length, expired_date valid date.
- No unique constraint on (category, brand, name) to allow duplicates (same product entered twice).

### 3.3 Migrations

- Versioned migrations for schema changes. Support adding columns (e.g. `opened_at`, `user_id` when multi-user) without breaking existing rows.

---

## 4. Frontend Requirements

### 4.1 Views / Screens

- **Inventory list**  
  Table or card list of all items. Columns: Category, Brand, Name, Value, Repurchase?, Expired date. Row actions: Edit, Delete. Empty state when no items.

- **Add item**  
  Form with: Category, Brand, Name, Value, Repurchase? (checkbox or tri-state: Yes / No / Not set), Expired date (date picker). Submit → create via API, then redirect or refresh list.

- **Edit item**  
  Same fields pre-filled; submit → update via API, then back to list or detail.

- **Optional:** Detail view for one item (e.g. from list click) with Edit/Delete.

### 4.2 List Behaviour

- **Search:** Optional free-text search across Category, Brand, Name, Value.
- **Filters:** By Category, Brand, Repurchase (Yes/No/Any), Expired (e.g. Expired / Expiring within 30 days / No date / Any).
- **Sort:** By Expired date (asc/desc), Brand, Category, Name, Created date.
- **Pagination or infinite scroll** if list is large.

### 4.3 Form Behaviour

- **Category / Brand:** Text inputs; optional autocomplete from existing values to keep naming consistent.
- **Expired date:** Date picker; no time. Clear/reset option.
- **Repurchase?:** Clear tri-state (e.g. “Would repurchase?”: Yes / No / Not set).
- **Validation:** Inline or on submit; match backend rules (required fields, max length, date format). Show clear error messages.
- **Submit:** Disable double-submit; show loading; on success update list or navigate; on error show message and keep form data.

### 4.4 UX Details

- Confirm before delete (e.g. “Remove this item from your inventory?”).
- Success/error toasts or inline messages after create/update/delete.
- Responsive layout so list and forms are usable on mobile (e.g. stacked form, touch-friendly actions).

---

## 5. Edge Cases & Business Rules

### 5.1 Required Fields

- **Empty Category / Brand / Name:** Reject. Show validation error: “Category, Brand, and Name are required.”
- **Whitespace-only:** Trim on backend; if empty after trim, treat as missing and reject.

### 5.2 Value Field

- **Empty Value:** Allowed. Store as null or empty string consistently across backend and frontend.
- **Very long Value:** Truncate or reject at max length; show error.

### 5.3 Repurchase?

- **Not set vs false:** Distinguish “I wouldn’t repurchase” (false) from “I haven’t decided” (null). UI must support three states if product owner wants that.
- **Default on create:** Omit or null; do not default to true/false unless product decision.

### 5.4 Expired Date

- **Invalid date:** Reject (e.g. 2025-02-30, 31 Feb). Validate on backend and optionally in frontend.
- **Past date:** Allow (item already expired). Useful for “expired” filter and reminders.
- **Future date:** Allow (e.g. printed expiry).
- **No date:** Allowed. Item has no expiry recorded; exclude from “expiring soon” logic or show as “No date”.
- **Timezone:** Store date-only (no time). No timezone conversion for “today” in filters (use server or client “today” consistently).

### 5.5 Duplicates

- **Same Category + Brand + Name:** Allowed. Do not auto-merge or block. User may have two identical products (e.g. one open, one backup). Optional: later feature to “group duplicates” or warn “You already have this item.”

### 5.6 Encoding & Characters

- **Unicode:** Support full Unicode in all text fields (brands like NARS, product names with accents, emoji in notes if allowed).
- **DB and API:** UTF-8. Sanitize only for security (e.g. no control characters if needed); do not strip valid Unicode.

### 5.7 Concurrency & Consistency

- **Edit conflict:** If two tabs edit same item, last write wins unless you introduce version/ETag. Document that behaviour; optional later: optimistic locking.
- **Delete then edit:** If user A deletes item and user B (or same user in another tab) edits it, return 404 on update/delete.

### 5.8 List & Performance

- **Empty list:** Show empty state with CTA to add first item. No table headers with zero rows if that looks broken.
- **Large list:** Paginate or virtualize; avoid loading thousands of rows at once.
- **Sort/filter with nulls:** Define sort order for null Expired date (e.g. last or first) and null Repurchase (e.g. group with “Not set”).

### 5.9 Security & Data

- **Input:** Escape/sanitize for XSS in frontend; parameterized queries or ORM on backend. No raw SQL with user input.
- **Auth (future):** Design so every item can later be scoped by `user_id` (or tenant). No auth in manual-entry phase is acceptable; document assumption “single user or no auth for now”.

### 5.10 Localisation (Future)

- **Dates:** Display in user locale (e.g. DD/MM/YYYY vs MM/DD/YYYY) but send/store ISO in API.
- **Numbers/currency:** Not in scope for manual-entry phase; “Value” is free text.

---

## 6. Out of Scope in This Phase

- Image upload and AI product identification.
- PAO (period-after-opening) parsing or auto-calc of expiry from open date.
- Multi-user or authentication.
- Shade matching, recommendations, or “get the look.”
- Barcode or SKU.
- Units or stock quantity (e.g. “2 of this lipstick”); each row is one physical item unless product later decides otherwise.

---

## 7. Summary Checklist

| Area       | Requirements |
|------------|--------------|
| **Data**   | Category, Brand, Name (required); Value, Repurchase?, Expired date (optional). No uniqueness on (Category, Brand, Name). |
| **Backend**| REST CRUD; validation (length, date, required); id and timestamps server-set. |
| **DB**     | Table with PK, indexes for category/brand/expired_date/repurchase; NOT NULL and length/date checks. |
| **Frontend**| List (search, filter, sort, pagination), Add/Edit form (tri-state Repurchase, date picker), delete with confirm. |
| **Edge cases**| Empty/whitespace required fields; invalid/past/future/null dates; duplicates allowed; Unicode; null Repurchase vs false; large list; no auth in phase 1. |

This document is the single reference for the manual-entry inventory phase. When adding image-based or AI features, extend the data model and APIs and keep this as the baseline behaviour.
