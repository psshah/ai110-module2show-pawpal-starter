# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Owner & pet management** — Create an owner with name and email, add multiple pets (by name and species), and associate them all under one profile
- **Flexible task definition** — Each task has a type (walk, feeding, grooming, etc.), duration in minutes, priority level (HIGH / MEDIUM / LOW), and a daily frequency
- **Priority-aware scheduling** — Tasks are scheduled HIGH → MEDIUM → LOW; within the same priority, shorter tasks (by total cost = frequency × duration) are placed first to maximize slot utilization
- **Recurring task distribution** — Tasks that repeat during the day are automatically spread across available time slots rather than being packed into the earliest window
- **Greedy slot filling** — The scheduler tracks remaining minutes per slot and places each task occurrence in the first slot with enough time; overflow moves to the next slot automatically
- **Graceful skipping** — If a task occurrence doesn't fit in any slot, it is skipped and recorded in the plan explanation with the reason
- **Human-readable plan explanation** — Each generated plan includes a timestamped schedule per pet, a summary of minutes used vs. available, and notes on any skipped tasks
- **Time slot flexibility** — Owners can define multiple availability windows per day (e.g. a morning block and an evening block)
- **Input validation** — Task frequency, priority, and type are validated at creation time; time slots enforce start < end

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
```

## 📐 Scheduling Algorithm

The core scheduling logic lives in `Scheduler.build_plan()` in [pawpal_system.py](pawpal_system.py). See [build_plan](pawpal_system.py#L62) for the full implementation.

| Step | What happens | Details |
|------|-------------|---------|
| 1 — Gather tasks | All tasks from all pets are combined into one list | Every task competes for the same shared time slots |
| 2 — Sort | Tasks ordered HIGH → MEDIUM → LOW priority | Ties broken by shortest total cost (`frequency × duration`) first |
| 3 — Spread recurring tasks | Repeated tasks are distributed across slots | Occurrence 0 starts at slot 0, occurrence 1 at slot 1, and so on |
| 4 — Fill slots greedily | Each occurrence is placed in the first slot with enough time left | If no slot fits, the occurrence is skipped gracefully — no crash, a note is added to the plan explanation with the reason |
| 5 — Return plan | Scheduled items sorted by start time and grouped by pet | Returned as a `Plan` with a full written explanation |

## 📸 Demo Walkthrough

The app has four sections — Owner & Pets, Tasks, Owner Schedule, and Build Schedule — each building on the previous one. 

User can add owner, assigns pets to owner, add tasks for the pets and their availability. User can then generate a schedule for the owner based on provided constraints and information.

### Sample workflow.
1. Add an owner by adding first name, last name and email.
2. Add pet to owner using their name and species.
3. Repeat step 2 as needed to add more pets to owner.
4. Once you add a pet, add task using dropdown menu for pet name, task type, frequency (how many times a day), duration (in minutes) and priority.
5. Add owner's available time slot using start time and end time for current day (eg. morning slot of 8 am-10 am and evening slot of 6 pm-8 pm).
6. Click 'Generate plan' to see the plan for the day.
7. Add new tasks as needed and retrieve updated plan by clicking 'Generate plan' button again.

Scheduler performs Priority-aware scheduling, Recurring task spread across different timeslots instead of one, Greedy slot filling and Graceful skipping if task does not fit into any slot. See Scheduling Algorithm section for more details.


### Sample output 
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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
<video src="diagrams/screen_recording.mov" width="100%" controls>