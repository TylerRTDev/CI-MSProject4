# Real Legacy Media — TESTING.md

This document details the testing approach, execution, coverage, and outcomes for **Real Legacy Media**, a full‑stack Django e‑commerce project.

### Table of Contents

* [Testing Strategy Overview](#testing-strategy-overview)
* [Testing User Stories](#testing-user-stories)
* [Responsive Testing](#responsive-testing)
* [Accessibility](#accessibility)
* [Code Validation](#code-validation)
* [Manual Testing Matrix](#manual-testing-matrix)
* [Automated Tests](#automated-tests)
* [Coverage Summary](#coverage-summary)
* [Bug Tracking & Resolutions](#bug-tracking--resolutions)
* [Deployment & Environment Testing](#deployment--environment-testing)
* [Conclusion](#conclusion)

## Testing Strategy Overview

* **Automated tests** using Django's `TestCase` and the Django test runner, grouped by app (`accounts`, `cart`, `checkout`, `core`, `orders`, `products`).
* **Coverage** measured with `coverage.py` (branch coverage optional).
* **Manual exploratory testing** across core purchase flows (browse → add to cart → checkout → Stripe redirect → webhook confirmation → order history).
* **Regression testing** after refactors (e.g., renaming `order_number` to `order_session` in checkout and updating references).
* **Tools**: Chrome DevTools (mobile emulation), W3C validators, flake8, and Stripe test dashboard for webhook validation.

## Testing User Stories

### Visitors / Shoppers

| Story                                       | Test Description                                                              | Verification                                                                            |
| ------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Browse products & filter by category/format | Navigate products list, apply filters, paginate; filters persist across pages | ✅ Manually verified; filter state preserved via querystring and respected by pagination |
| Search for items                            | Use navbar search to find titles/artists                                      | ✅ Manually verified results relevance                                                   |
| View product details                        | Open product page; images, price, stock, and add-to-cart visible              | ✅ Verified                                                                              |
| Add to cart                                 | Pick size/qty, add to cart                                                    | ✅ Success message + cart badge count updates                                            |
| Update cart quantities                      | Increase/decrease quantities; remove items                                    | ✅ Totals recalculated; zero qty removes item                                            |
| Checkout as guest                           | Provide email when prompted and proceed                                       | ✅ Redirect to checkout form then to Stripe                                              |
| Pay via Stripe (test mode)                  | Create Checkout Session and complete test payment                             | ✅ Redirect to Stripe; success then webhook received                                     |
| Receive order confirmation                  | After payment, order email sent and order visible in history                  | ✅ Confirmed in console email backend and UI                                             |

### Registered Users

| Story                        | Test Description                                             | Verification                                                      |
| ---------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------- |
| Register & login             | Create account, login/logout                                 | ✅ Views render and redirects correct                              |
| View order history & details | Access `/accounts/order-history/` and individual order pages | ✅ Requires auth; pages load with correct data                     |
| Manage account details       | Update profile fields and (optionally) change password       | ✅ Profile form persists; password change needs valid old password |

## Responsive Testing

Tested at breakpoints **360, 390, 768, 1024, 1440+** with Chrome DevTools and physical devices (iPhone/Android), validating flex/grid layout, sticky header, product grids, cart table, and checkout forms.

| Device         | Browser | Layout | Key Notes                                       |
| -------------- | ------- | ------ | ----------------------------------------------- |
| iPhone 13      | Safari  | ✅      | Navbar collapses; cards stack; CTA spacing OK   |
| Pixel 7        | Chrome  | ✅      | Filters collapse; pagination is finger‑friendly |
| iPad Air       | Safari  | ✅      | Two‑column layout; checkout forms comfortable   |
| MacBook Pro    | Chrome  | ✅      | 3–4 column grids; hover states; sticky header   |
| Windows Laptop | Edge    | ✅      | Consistent spacing and typography               |

*No overflow, layout shifts, or zoom traps observed.*

## Accessibility

* Semantic headings & landmarks in templates.
* Form labels associated to inputs; error messages displayed near fields.
* Sufficient color contrast checked in DevTools.
* Keyboard: interactive elements focusable; toasts dismissible; modals close with Escape.

## Code Validation

* **HTML**: W3C Markup Validator — no blocking errors.
* **CSS**: W3C Jigsaw — passed (minor vendor prefix warnings ignored).
* **Python**: `flake8` — no critical issues; line length kept ≤ 88 where practical.
* **Django**: `python manage.py check` — OK.

## Manual Testing Matrix

| Feature             | Steps                                     | Expected                                   | Result                            |
| ------------------- | ----------------------------------------- | ------------------------------------------ | --------------------------------- |
| Search              | Enter term in navbar search; submit       | Results list shows matching items          | ✅ Passed                          |
| Filter + Pagination | Apply filter, navigate to next/prev pages | Filter persists; page shows filtered items | ✅ Passed (fixed using `page_obj`) |
| Product Detail      | Open detail; add to cart                  | Success message; cart count increases      | ✅ Passed                          |
| Cart Update         | Increase/decrease qty; remove item        | Totals update; item removed at 0           | ✅ Passed                          |
| Empty Cart Edge     | Remove last item                          | Cart page shows empty state                | ✅ Passed                          |
| Guest Checkout      | Visit checkout unauthenticated            | Prompt for email then checkout form        | ✅ Passed                          |
| Stripe Redirect     | Click “Proceed to Payment”                | 302 redirect to Stripe                     | ✅ Passed                          |
| Webhook Receipt     | Complete test payment                     | Webhook processes session; order created   | ✅ Passed                          |
| Order Email         | Place order in test mode                  | Console email printed with correct details | ✅ Passed                          |
| Order History       | Visit order history & detail              | Lists past orders; detail displays items   | ✅ Passed                          |
| Account Update      | Change profile info                       | Updated fields saved and shown             | ✅ Passed                          |
| Change Password     | Submit old + new password                 | Redirect with success; can login with new  | ✅ Passed                          |

## Automated Tests

All automated tests live under each app’s `tests/` package. Below is a grouped summary by app.

#### `accounts`

| Test Name                                               | Purpose                                          | Area   | Result   |
| ------------------------------------------------------- | ------------------------------------------------ | ------ | -------- |
| `test_profile_created_when_user_created`                | Profile created when user created                | Models | ✅ Passed |
| `test_register_url_resolves`                            | Register url resolves                            | URLs   | ✅ Passed |
| `test_profile_url_resolves`                             | Profile url resolves                             | URLs   | ✅ Passed |
| `test_login_view_get`                                   | Login view get                                   | Views  | ✅ Passed |
| `test_login_view_post_valid`                            | Login view post valid                            | Views  | ✅ Passed |
| `test_login_view_post_invalid`                          | Login view post invalid                          | Views  | ✅ Passed |
| `test_order_history_view_requires_login`                | Order history view requires login                | Views  | ✅ Passed |
| `test_order_history_view_logged_in`                     | Order history view logged in                     | Views  | ✅ Passed |
| `test_register_view_status_code`                        | Register view status code                        | Views  | ✅ Passed |
| `test_profile_view_requires_login`                      | Profile view requires login                      | Views  | ✅ Passed |
| `test_logged_in_user_can_access_profile`                | Logged in user can access profile                | Views  | ✅ Passed |
| `test_change_password_view_requires_login`              | Change password view requires login              | Views  | ✅ Passed |
| `test_account_detail_view_post_change_password_valid`   | Account detail view post change password valid   | Views  | ✅ Passed |
| `test_account_detail_view_post_change_password_invalid` | Account detail view post change password invalid | Views  | ✅ Passed |
| `test_logout_view_redirects`                            | Logout view redirects                            | Views  | ✅ Passed |
| `test_update_email_view_redirects`                      | Update email view redirects                      | Views  | ✅ Passed |
| `test_account_detail_view_requires_login`               | Account detail view requires login               | Views  | ✅ Passed |
| `test_account_detail_view_logged_in`                    | Account detail view logged in                    | Views  | ✅ Passed |
| `test_account_detail_view_get`                          | Account detail view get                          | Views  | ✅ Passed |
| `test_account_detail_view_post_update_profile_valid`    | Account detail view post update profile valid    | Views  | ✅ Passed |

#### `cart`

| Test Name                                        | Purpose                                   | Area   | Result   |
| ------------------------------------------------ | ----------------------------------------- | ------ | -------- |
| `test_cart_item_str_method`                      | Cart item str method                      | Models | ✅ Passed |
| `test_cart_item_total_price`                     | Cart item total price                     | Models | ✅ Passed |
| `test_cart_item_product_relation`                | Cart item product relation                | Models | ✅ Passed |
| `test_cart_item_user_relation`                   | Cart item user relation                   | Models | ✅ Passed |
| `test_view_cart_url_resolves`                    | View cart url resolves                    | URLs   | ✅ Passed |
| `test_remove_from_cart_url_resolves`             | Remove from cart url resolves             | URLs   | ✅ Passed |
| `test_update_cart_url_resolves`                  | Update cart url resolves                  | URLs   | ✅ Passed |
| `test_clear_cart_url_resolves`                   | Clear cart url resolves                   | URLs   | ✅ Passed |
| `test_update_cart_quantity_increases`            | Update cart quantity increases            | Views  | ✅ Passed |
| `test_update_cart_quantity_removes_item`         | Update cart quantity removes item         | Views  | ✅ Passed |
| `test_add_to_cart_initial`                       | Add to cart initial                       | Views  | ✅ Passed |
| `test_add_to_cart_duplicate`                     | Add to cart duplicate                     | Views  | ✅ Passed |
| `test_add_to_cart_redirect`                      | Add to cart redirect                      | Views  | ✅ Passed |
| `test_remove_product_from_cart`                  | Remove product from cart                  | Views  | ✅ Passed |
| `test_remove_nonexistent_product_does_not_error` | Remove nonexistent product does not error | Views  | ✅ Passed |
| `test_remove_from_cart_redirects`                | Remove from cart redirects                | Views  | ✅ Passed |
| `test_cart_view_context_totals`                  | Cart view context totals                  | Views  | ✅ Passed |

#### `checkout`

| Test Name                                                    | Purpose                                               | Area        | Result   |
| ------------------------------------------------------------ | ----------------------------------------------------- | ----------- | -------- |
| `test_order_str_method`                                      | Order str method                                      | Models      | ✅ Passed |
| `test_order_number_is_generated_on_save`                     | Order number is generated on save                     | Models      | ✅ Passed |
| `test_get_subtotal`                                          | Get subtotal                                          | Models      | ✅ Passed |
| `test_checkout_url_resolves`                                 | Checkout url resolves                                 | URLs        | ✅ Passed |
| `test_checkout_url_redirect_empty_cart`                      | Checkout url redirect empty cart                      | Views       | ✅ Passed |
| `test_create_checkout_session_url_resolves`                  | Create checkout session url resolves                  | URLs        | ✅ Passed |
| `test_order_success_url_resolves`                            | Order success url resolves                            | URLs        | ✅ Passed |
| `test_order_confirmation_url_resolves`                       | Order confirmation url resolves                       | URLs        | ✅ Passed |
| `test_stripe_webhook_url_resolves`                           | Stripe webhook url resolves                           | URLs        | ✅ Passed |
| `test_order_confirmation_missing_id_raises_error`            | Order confirmation missing id raises error            | Views       | ✅ Passed |
| `test_checkout_namespace_reverse`                            | Checkout namespace reverse                            | URLs        | ✅ Passed |
| `test_create_checkout_session_disallows_get`                 | Create checkout session disallows get                 | Views       | ✅ Passed |
| `test_order_confirmation_url_weird_id`                       | Order confirmation url weird id                       | URLs        | ✅ Passed |
| `test_checkout_view_get`                                     | Checkout view get                                     | Views       | ✅ Passed |
| `test_checkout_view_redirects_if_cart_empty`                 | Checkout view redirects if cart empty                 | Views       | ✅ Passed |
| `test_create_checkout_session_as_user_returns_200`           | Create checkout session as user returns 200           | Integration | ✅ Passed |
| `test_webhook_creates_order`                                 | Webhook creates order                                 | Integration | ✅ Passed |
| `test_order_success_view`                                    | Order success view                                    | Views       | ✅ Passed |
| `test_order_confirmation_view`                               | Order confirmation view                               | Views       | ✅ Passed |
| `test_order_confirmation_view_returns_404_for_invalid_order` | Order confirmation view returns 404 for invalid order | Views       | ✅ Passed |
| `test_stripe_webhook_invalid_signature_returns_400`          | Stripe webhook invalid signature returns 400          | Integration | ✅ Passed |
| `test_checkout_session_creation_exception_returns_500`       | Checkout session creation exception returns 500       | Integration | ✅ Passed |

#### `core`

| Test Name                     | Purpose                | Area  | Result   |
| ----------------------------- | ---------------------- | ----- | -------- |
| `test_home_page_url_resolves` | Home page url resolves | URLs  | ✅ Passed |
| `test_home_view_context_data` | Home view context data | Views | ✅ Passed |

#### `orders`

| Test Name               | Purpose          | Area   | Result   |
| ----------------------- | ---------------- | ------ | -------- |
| `test_order_str_method` | Order str method | Models | ✅ Passed |
| `test_get_subtotal`     | Get subtotal     | Models | ✅ Passed |

#### `products`

| Test Name                                         | Purpose                                    | Area   | Result   |
| ------------------------------------------------- | ------------------------------------------ | ------ | -------- |
| `test_product_str_method`                         | Product str method                         | Models | ✅ Passed |
| `test_product_category_relation`                  | Product category relation                  | Models | ✅ Passed |
| `test_stock_quantity`                             | Stock quantity                             | Models | ✅ Passed |
| `test_product_price_decimal`                      | Product price decimal                      | Models | ✅ Passed |
| `test_product_list_url_resolves`                  | Product list url resolves                  | URLs   | ✅ Passed |
| `test_product_detail_url_resolves`                | Product detail url resolves                | URLs   | ✅ Passed |
| `test_add_to_cart_url_resolves`                   | Add to cart url resolves                   | URLs   | ✅ Passed |
| `test_product_list_view_status_code`              | Product list view status code              | Views  | ✅ Passed |
| `test_product_detail_view_status_code`            | Product detail view status code            | Views  | ✅ Passed |
| `test_product_detail_view_content`                | Product detail view content                | Views  | ✅ Passed |
| `test_product_detail_404_for_invalid_product`     | Product detail 404 for invalid product     | Views  | ✅ Passed |
| `test_product_excess_stock_add_to_cart_redirects` | Product excess stock add to cart redirects | Views  | ✅ Passed |

## Coverage Summary

Commands used:

```bash
coverage run manage.py test
coverage report -m
```

> **Note:** `accounts` coverage was raised substantially by adding view tests for `login_view`, `order_history_view`, `order_detail_view`, `change_password_view`, and `account_detail_view`.


| App       | Files | Statements | Miss | Coverage |
| --------- | ----: | ---------: | ---: | -------: |
| accounts  |     — |          — |    — |        — |
| cart      |     — |          — |    — |        — |
| checkout  |     — |          — |    — |        — |
| core      |     — |          — |    — |        — |
| orders    |     — |          — |    — |        — |
| products  |     — |          — |    — |        — |
| **TOTAL** |     — |          — |    — |        — |

## Bug Tracking & Resolutions

| Issue                                                          | Root Cause                                                | Fix                                                                                | Status     |
| -------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------- |
| Checkout POST returning 200 instead of redirect                | Form errors re‑rendered page; test expected redirect      | Ensured valid path triggers redirect to Stripe; tests assert 302 where appropriate | ✅ Resolved |
| Failing test only under coverage for `create_checkout_session` | Auth/session handling differed in coverage run            | Used `force_login` and asserted correct status/redirect chain                      | ✅ Resolved |
| Filter state lost on pagination                                | Pagination template used `products` instead of `page_obj` | Switched to `page_obj` in template and view context                                | ✅ Resolved |
| Renamed `order_number` → `order_session` broke lookups         | Code and tests referenced old field                       | Renamed everywhere; updated fixtures/tests                                         | ✅ Resolved |
| Guest email field inconsistency                                | `guest_email` vs `email`                                  | Unified to `email` on `CheckoutOrder`; updated email tests                         | ✅ Resolved |
| Accounts coverage initially 38%                                | Missing tests for several views                           | Added tests for login, order history/detail, change password, account detail       | ✅ Resolved |

## Deployment & Environment Testing

* **Environments:** Local dev & production (Django). Static files collected with `collectstatic` and served from the configured storage.
* **Environment Variables:**

  * `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
  * `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
  * Email backend settings for order confirmations
* **Stripe Flow:**

  1. Create Checkout Session → redirect to Stripe.
  2. On success, Stripe sends webhook (`checkout.session.completed`).
  3. Webhook handler verifies signature and creates the order from the session.
* **Tests executed against deployment:**

  * Placed a test order in Stripe test mode and verified webhook → order creation → confirmation email → order history visibility.

## Conclusion

The project meets testing goals through a combination of automated unit/integration tests and comprehensive manual verification of core user journeys.

**Future improvements**

* Factory‑based test data (e.g., `factory_boy`) and `pytest` fixtures.
* Playwright smoke tests for end‑to‑end cart → Stripe → webhook flow.
* Automated accessibility checks (axe‑core) in CI.
