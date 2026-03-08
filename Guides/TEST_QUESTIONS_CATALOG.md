# 📋 Test Questions Catalog

Generic test scenarios for **Web, API, and Android** testing.
Most of these can be run without knowing the specific URL — you just fill in the blanks.

---

## 🌐 Web Testing — Common Test Scenarios

### 🔐 Authentication / Login Page
| # | Test Question | What to check |
|---|---|---|
| 1 | Does the login page load? | Page title contains expected text |
| 2 | Can a valid user log in? | After login → redirected to dashboard/home |
| 3 | Does wrong password show an error? | Error message appears on screen |
| 4 | Does empty email show validation? | "Email is required" or similar message |
| 5 | Does empty password show validation? | "Password is required" message |
| 6 | Does "Forgot Password" link work? | Link navigates to reset password page |
| 7 | Does logout work? | After logout → redirected to login page |
| 8 | Can a logged-out user access protected pages? | Redirected back to login |

### 🏠 Home / Dashboard Page
| # | Test Question | What to check |
|---|---|---|
| 9 | Does the page load after login? | No errors, content visible |
| 10 | Is the correct username/email shown? | User's name appears in header/nav |
| 11 | Do all navigation menu items work? | Each link leads to the right page |
| 12 | Are all buttons clickable? | No disabled or hidden buttons unexpectedly |

### 📝 Forms (Registration, Profile, Checkout, etc.)
| # | Test Question | What to check |
|---|---|---|
| 13 | Can a user submit a valid form? | Success message appears |
| 14 | Does the form reject empty required fields? | Error shown for each empty field |
| 15 | Does an invalid email format get rejected? | "Invalid email" message |
| 16 | Does a too-short password get rejected? | "Password too short" or min-length error |
| 17 | Does a duplicate email get rejected? | "Email already in use" error |
| 18 | Does the form keep filled data after an error? | Fields don't clear on validation fail |

### 🔍 Search
| # | Test Question | What to check |
|---|---|---|
| 19 | Does searching a known term return results? | Results list is not empty |
| 20 | Does searching a nonsense term show "no results"? | "No results found" message |
| 21 | Does search work with special characters? | No crash or server error |

### 🛒 E-commerce Specific
| # | Test Question | What to check |
|---|---|---|
| 22 | Can a user add an item to the cart? | Cart count increases |
| 23 | Can a user remove an item from the cart? | Item disappears from cart |
| 24 | Does the cart total update correctly? | Price math is correct |
| 25 | Can a user complete checkout? | Order confirmation page shown |

---

## 🔌 API Testing — Common Test Scenarios

### ✅ Status Code Tests (works with ANY API)
| # | Test Question | Expected |
|---|---|---|
| 1 | GET valid resource → correct status? | `200 OK` |
| 2 | GET non-existent resource → correct status? | `404 Not Found` |
| 3 | POST valid data → correct status? | `201 Created` |
| 4 | POST with missing required fields? | `400 Bad Request` |
| 5 | DELETE existing resource? | `200` or `204 No Content` |
| 6 | Access without auth token? | `401 Unauthorized` |
| 7 | Access with wrong permissions? | `403 Forbidden` |

### ⚡ Performance Tests
| # | Test Question | Expected |
|---|---|---|
| 8 | Does GET /[resource] respond in < 2 seconds? | Response time < 2000ms |
| 9 | Does POST respond in < 3 seconds? | Response time < 3000ms |

### 📦 Data / Schema Tests
| # | Test Question | What to check |
|---|---|---|
| 10 | Does the response contain expected fields? | `id`, `name`, `email` etc. present |
| 11 | Are field types correct? | `id` is integer, `email` is string |
| 12 | Does the GET list return an array? | Response is `[...]` not `{...}` |
| 13 | Does pagination work? | `page=2` returns different results |
| 14 | Does the created object match what was sent? | POST body matches response body |

### 🔒 Authentication Tests
| # | Test Question | What to check |
|---|---|---|
| 15 | Valid token → access granted? | `200 OK` |
| 16 | Expired token → rejected? | `401 Unauthorized` |
| 17 | Malformed token → rejected? | `401 Unauthorized` |
| 18 | No token → rejected? | `401 Unauthorized` |

---

## 📱 Android Testing — Common Test Scenarios

### 🚀 App Launch & Stability
| # | Test Question | What to check |
|---|---|---|
| 1 | Does the app install and launch? | Home/splash screen appears |
| 2 | Does the app launch in < 5 seconds? | Timing check |
| 3 | Does the app survive rotating the screen? | No crash on orientation change |
| 4 | Does the app survive going to background and back? | All data/state preserved |
| 5 | Does the app work with no internet? | Shows offline message, doesn't crash |

### 🔐 Login / Onboarding
| # | Test Question | What to check |
|---|---|---|
| 6 | Does the login screen appear on first launch? | Login / welcome screen visible |
| 7 | Can a valid user log in? | Home screen appears after login |
| 8 | Does wrong password show an error? | Error toast or dialog appears |
| 9 | Does empty email/password show validation? | Validation message below field |
| 10 | Does "Remember Me" persist the session? | Re-open app → still logged in |
| 11 | Does logout clear the session? | Login screen shown after logout |

### 🏠 Home Screen / Dashboard
| # | Test Question | What to check |
|---|---|---|
| 12 | Do all menu items / tabs open the right screen? | Correct screen title shown |
| 13 | Does the back button go to the previous screen? | Correct screen navigation |
| 14 | Does pressing back on home exit/minimize app? | App minimizes gracefully |
| 15 | Does scrolling work on long lists? | Can swipe to bottom without crash |

### 📝 Forms / Input
| # | Test Question | What to check |
|---|---|---|
| 16 | Does tapping a text field open the keyboard? | Keyboard slides up |
| 17 | Does tapping outside a field dismiss keyboard? | Keyboard slides down |
| 18 | Does submitting empty required fields show error? | Error message shown |
| 19 | Does the form submit successfully with valid data? | Success screen or message |

### 🔔 Notifications (if applicable)
| # | Test Question | What to check |
|---|---|---|
| 20 | Do push notifications appear? | Notification in status bar |
| 21 | Tapping a notification opens the right screen? | Deep link works correctly |

---

## 📌 Do You Need the URL / App Details?

| Scenario | Web | Android | API |
|---|---|---|---|
| **Generic checks** (loads, status codes, navigation) | URL only | App installed | Base URL only |
| **Specific element interaction** (click button, fill form) | URL + **inspect element** for locators | **Appium Inspector** for element IDs | Endpoint path + request schema |
| **Data validation** | URL + expected page content | Element text values | API response schema (from docs or Postman) |

### How to get Web locators (right-click → Inspect)
```
1. Open your website in Chrome
2. Right-click on button/field → Inspect
3. Look for: id="submit-btn" → use By.ID, "submit-btn"
              class="login-form" → use By.CLASS_NAME, "login-form"
              data-testid="email" → use By.CSS_SELECTOR, "[data-testid='email']"
```

### How to get Android locators (Appium Inspector)
```
1. Start Appium: npx appium
2. Open: https://github.com/appium/appium-inspector/releases
3. Connect to http://127.0.0.1:4723
4. Start session with your device
5. Click any element → copy its accessibility-id or resource-id
```
