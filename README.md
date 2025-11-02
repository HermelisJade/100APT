## 100APT — Apartment Builder Simulator

**COMP9001 Python Final Project**

---

### 1. How to Run

This project uses **only Python standard libraries (`random`, `sys`, `os`, `datetime`)** , so no installation is required.

Run the program with:

python 100APT.py

### 2. Overview

You are a real-estate developer building a skyscraper one floor at a time.

Manage capital, choose apartment themes, and assign fantasy tenants wisely to maximise income.

| Mechanic         | Description                         |
| ---------------- | ----------------------------------- |
| Starting Capital | $500                                |
| Duration         | 52 in-game weeks                    |
| Weekly Actions   | 7 actions per week                  |
| Max Floors       | 100 floors                          |
| Bonus System     | Match tenant preference = +10% rent |
| Maintenance Cost | Grows with floors + floor height    |
| Bankruptcy       | Capital ≤ -50 resets capital        |

### 3. Files Included

100APT.py # main program file
README.md # (this document)
game_log.txt # auto-generated gameplay log after running

### 4. Program Structure

#### 4.1 Main Game Loop

```text
Initialize game
│
├─ For each year:
│   ├─ For each week (52):
│   │   ├─ Display tower
│   │   ├─ Player takes 7 actions
│   │   └─ Settle weekly finances
│   └─ End-of-year summary + capital carry-over
│
└─ Repeat or exit
```

#### 4.2 Notes

- Gameplay log auto-saves to `game_log.txt`
- You may quit anytime using `q`



