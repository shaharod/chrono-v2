# Patient Action & Status Mapping

## 1. Automation Logic (The "Calculator")
These statuses are calculated based on the `last_picked_up_date`.

| Days Overdue | Status | System Action |
| :--- | :--- | :--- |
| 0 - 30 days | **Active** | None |
| 31 - 60 days | **Warning** | Generate "Warning Email" |
| 61 - 90 days | **Probation** | Generate "Probation Email" |
| > 90 days | **Removal** | Flag for "Doctor Review" |

---

## 2. Communication Templates
*Drafting the actual messages here helps when we build the email service later.*

### Warning Email (Day 31)
"Hi [Name], we noticed you haven't picked up your prescription for [Drug Name] in over 30 days. Please visit the clinic soon."

### Probation Email (Day 61)
"URGENT: Your prescription for [Drug Name] is now in Probation status. Please contact the clinic immediately to avoid removal from the active list."

---

## 3. Physical Actions
* **Location Management**: If status is **Removal**, the physical location (e.g., Drawer 1) is marked as "Empty/Available" in the system.
* **Manual Override**: Doctors must click a "Confirm Removal" button before the patient is officially deleted from the dashboard.