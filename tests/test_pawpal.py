"""Tests for PawPal+ scheduling system."""

from datetime import datetime
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType, TimeSlot, Priority

# --- Shared time slots used in tests ---
# Morning: 8am - 10am (2 hours)
# Evening: 6pm - 8pm (2 hours)
MORNING_SLOT = TimeSlot(
    start_time=datetime(2026, 7, 4, 8, 0),
    end_time=datetime(2026, 7, 4, 10, 0),
)
EVENING_SLOT = TimeSlot(
    start_time=datetime(2026, 7, 4, 18, 0),
    end_time=datetime(2026, 7, 4, 20, 0),
)


def test_create_owner():
    # Create an owner and check their info is saved correctly
    owner = Owner(first_name="Alex", last_name="Smith", email="alex@example.com")

    assert owner.first_name == "Alex"
    assert owner.last_name == "Smith"
    assert owner.email == "alex@example.com"
    assert owner.pets == []          # no pets yet
    assert owner.scheduler is None   # no schedule yet


def test_create_two_pets():
    # Create an owner, then add two pets
    owner = Owner(first_name="Alex", last_name="Smith", email="alex@example.com")

    pet1 = Pet(name="Buddy", type="dog")
    pet2 = Pet(name="Whiskers", type="cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    assert len(owner.pets) == 2
    assert owner.pets[0].name == "Buddy"
    assert owner.pets[1].name == "Whiskers"


def test_add_owner_availability():
    # Give the owner a morning and evening time slot (2 hours each)
    owner = Owner(first_name="Alex", last_name="Smith", email="alex@example.com")

    scheduler = Scheduler(time_slots=[MORNING_SLOT, EVENING_SLOT])
    owner.add_scheduler(scheduler)

    assert owner.scheduler is not None
    assert len(owner.scheduler.time_slots) == 2
    assert MORNING_SLOT.available_minutes == 120   # 2 hours = 120 minutes
    assert EVENING_SLOT.available_minutes == 120


def test_generate_plan():
    # Set up owner, two pets, one task each, then generate a plan
    owner = Owner(first_name="Alex", last_name="Smith", email="alex@example.com")

    pet1 = Pet(name="Buddy", type="dog")
    pet2 = Pet(name="Whiskers", type="cat")

    # Task 1: a 10-minute walk for Buddy
    task1 = Task(type=TaskType.WALKS, frequency=1, duration_minutes=10, priority=Priority.MEDIUM)
    pet1.add_task(task1)

    # Task 2: a 30-minute feeding for Whiskers
    task2 = Task(type=TaskType.FEEDING, frequency=1, duration_minutes=30, priority=Priority.MEDIUM)
    pet2.add_task(task2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)
    owner.add_scheduler(Scheduler(time_slots=[MORNING_SLOT, EVENING_SLOT]))

    plan = owner.generate_plan()

    # Check that both tasks ended up in the plan
    buddy_tasks = plan.task_list_by_pet["Buddy"]
    whiskers_tasks = plan.task_list_by_pet["Whiskers"]

    assert len(buddy_tasks) == 1
    assert len(whiskers_tasks) == 1
    assert buddy_tasks[0].task.type == TaskType.WALKS
    assert whiskers_tasks[0].task.type == TaskType.FEEDING


def test_add_high_priority_task_and_regenerate_plan():
    # Tests whether build_plan sorts correctly when a high-priority task is added and regenerates the plan.
    # Start with the same setup as above
    owner = Owner(first_name="Alex", last_name="Smith", email="alex@example.com")

    pet1 = Pet(name="Buddy", type="dog")
    pet2 = Pet(name="Whiskers", type="cat")

    pet1.add_task(Task(type=TaskType.WALKS, frequency=1, duration_minutes=10, priority=Priority.MEDIUM))
    pet2.add_task(Task(type=TaskType.FEEDING, frequency=1, duration_minutes=30, priority=Priority.MEDIUM))

    owner.add_pet(pet1)
    owner.add_pet(pet2)
    owner.add_scheduler(Scheduler(time_slots=[MORNING_SLOT, EVENING_SLOT]))

    # Generate first plan — Buddy should have 1 task
    first_plan = owner.generate_plan()
    assert len(first_plan.task_list_by_pet["Buddy"]) == 1

    # Now add a new HIGH priority medication task (10 min) to Buddy
    high_priority_task = Task(
        type=TaskType.MEDICATIONS,
        frequency=1,
        duration_minutes=10,
        priority=Priority.HIGH,
    )
    pet1.add_task(high_priority_task)

    # Regenerate the plan — Buddy should now have 2 tasks
    second_plan = owner.generate_plan()
    buddy_tasks = second_plan.task_list_by_pet["Buddy"]
    buddy_task_types = [scheduled.task.type for scheduled in buddy_tasks]

    assert len(buddy_tasks) == 2
    assert TaskType.MEDICATIONS in buddy_task_types   # new high-priority task is in the plan
    assert TaskType.WALKS in buddy_task_types          # original task is still there
