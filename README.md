# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Pets: Buddy, Whiskers

  [Whiskers] feeding | 7:00 AM – 7:10 AM
  [Buddy] feeding | 7:10 AM – 7:25 AM
  [Buddy] walks | 7:25 AM – 8:10 AM
  [Buddy] feeding | 6:00 PM – 6:15 PM
  [Buddy] walks | 6:15 PM – 7:00 PM

```
priyankashah@Priyankas-MacBook-Air ai110-module2show-pawpal-starter % python3 main.py
Today's schedule:
Owner plan | 420 min available across 2 slot(s)
Pets: Buddy, Whiskers

  [Whiskers] feeding | 7:00 AM – 7:10 AM
  [Buddy] feeding | 7:10 AM – 7:25 AM
  [Buddy] walks | 7:25 AM – 8:10 AM
  [Buddy] feeding | 6:00 PM – 6:15 PM
  [Buddy] walks | 6:15 PM – 7:00 PM

Summary: 130/420 min used.
Conflict resolution: tasks ordered by priority (HIGH→MEDIUM→LOW), ties broken by shortest total duration first.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
(.venv) priyankashah@Priyankas-MacBook-Air ai110-module2show-pawpal-starter % pytest --cov=pawpal_system tests/

================================================================ test session starts ================================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/priyankashah/Documents/Development/codepath/ai110-module2show-pawpal-starter
plugins: cov-7.1.0
collected 5 items                                                                                                                                   

tests/test_pawpal.py .....                                                                                                                    [100%]

================================================================== tests coverage ===================================================================
__________________________________________________ coverage: platform darwin, python 3.9.6-final-0 __________________________________________________

Name               Stmts   Miss  Cover
--------------------------------------
pawpal_system.py     123     11    91%
--------------------------------------
TOTAL                123     11    91%
================================================================= 5 passed in 0.04s =================================================================
```

Sample test output:

```
% pytest tests/test_pawpal.py      
================================================================ test session starts ================================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/priyankashah/Documents/Development/codepath/ai110-module2show-pawpal-starter
collected 5 items                                                                                                                                   

tests/test_pawpal.py .....                                                                                                                    [100%]

================================================================= 5 passed in 0.02s =================================================================```

## 📐 Scheduling Algorithm — `Scheduler.build_plan`

The core scheduling logic lives in `Scheduler.build_plan()` in [pawpal_system.py](pawpal_system.py).

**Step 1 — Gather all tasks**
All tasks from all pets are combined into one list so they compete for the same time slots.

**Step 2 — Sort by priority, then cost**
Tasks run in order: HIGH first, then MEDIUM, then LOW. If two tasks have the same priority, the shorter one (`frequency × duration`) goes first.

**Step 3 — Spread recurring tasks across slots**
If a task repeats (e.g. feeding twice a day), it doesn't get scheduled back-to-back in the same slot. The first occurrence is placed starting from slot 0, the second starting from slot 1, and so on — so the task is spread throughout the day.

**Step 4 — Fill each slot greedily**
For each task occurrence, the algorithm checks slots in order and places it in the first one with enough time left. If nothing fits, the occurrence is skipped and a note is added to the plan explanation.

**Step 5 — Return the plan**
Scheduled items are sorted by start time, grouped by pet, and returned as a `Plan` with a written explanation.

| Feature | How it's handled |
|---------|-----------------|
| Priority ordering | `HIGH → MEDIUM → LOW`; ties broken by shortest total cost first |
| Recurring tasks | Occurrences spread across slots — round N starts from slot N |
| Time conflicts | Greedy fill — each slot tracks remaining minutes; overflow moves to next slot |
| Unschedulable tasks | Skipped occurrences listed in the plan explanation with a reason |
| Output grouping | Scheduled tasks grouped by pet name in the returned `Plan` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Add an owner by adding first name, last name and email.
2. Add pet to owner using their name and species.
3. Repeat step 2 as needed to add more pets to owner.
4. Once you add a pet, add task using dropdown menu for pet name, task type, frequency (how many times a day), duration (in minutes) and priority.
5. Add owner's available time slot using start time and end time for current day (eg. morning slot of 8 am-10 am and evening slot of 6 pm-8 pm).
6. Click 'Generate plan' to see the plan for the day.
7. Add new tasks as needed and retrieve updated plan by clicking 'Generate plan' button again.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
<video src="diagrams/screen_recording.mov" width="100%" controls>