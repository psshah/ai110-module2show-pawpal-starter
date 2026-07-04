"""PawPal+ system classes for pet care task scheduling."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Priority levels for a care task."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskType(Enum):
    """Supported pet care task types."""

    WALKS = "walks"
    FEEDING = "feeding"
    BATHROOM_BREAKS = "bathroom_breaks"
    MENTAL_PLAY = "mental_play"
    GROOMING = "grooming"
    MEDICATIONS = "medications"
    VET_APPOINTMENT = "vet_appointment"


@dataclass
class TimeSlot:
    """A single block of time the owner is available for pet care."""

    start_time: datetime
    end_time: datetime

    def __post_init__(self) -> None:
        if self.start_time >= self.end_time:
            raise ValueError(
                f"start_time must be before end_time, got {self.start_time} >= {self.end_time}"
            )

    @property
    def available_minutes(self) -> float:
        return (self.end_time - self.start_time).total_seconds() / 60


@dataclass
class Scheduler:
    """Holds owner availability slots and builds the daily care plan."""

    time_slots: list[TimeSlot]

    def __post_init__(self) -> None:
        if not self.time_slots:
            raise ValueError("Scheduler must have at least one time slot.")

    def build_plan(self, pets: list[Pet]) -> Plan:
        """Build one plan for all pets, scheduling their tasks against shared time slots.

        All tasks across all pets compete for the same slots.
        Tasks sorted HIGH→MEDIUM→LOW priority; ties broken by shortest total cost first.
        Occurrences are interleaved across slots (one round per slot) so tasks spread
        throughout the day rather than being packed into the earliest slot.
        Results grouped by pet name in the plan. Skipped occurrences noted in explanation.
        """
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

        all_tasks: list[tuple[Task, str]] = [
            (task, pet.name)
            for pet in pets
            for task in pet.tasks
        ]

        sorted_tasks = sorted(
            all_tasks,
            key=lambda tp: (priority_order[tp[0].priority], tp[0].frequency * tp[0].duration_minutes),
        )

        max_freq = max((t.frequency for t, _ in all_tasks), default=0)
        total_available = sum(slot.available_minutes for slot in self.time_slots)

        # Track the current fill position (time) and remaining minutes for each slot
        slot_cursor: list[datetime] = [slot.start_time for slot in self.time_slots]
        slot_remaining: list[float] = [slot.available_minutes for slot in self.time_slots]

        scheduled_items: list[ScheduledTask] = []
        skipped_lines: list[str] = []

        # Each occurrence round starts at the next slot so tasks spread across the day.
        # Round 0 → slot 0, round 1 → slot 1, etc. Overflow to later slots if a task
        # doesn't fit in the round's preferred slot.
        for occurrence_idx in range(max_freq):
            start_slot = min(occurrence_idx, len(self.time_slots) - 1)
            for task, pet_name in sorted_tasks:
                if task.frequency <= occurrence_idx:
                    continue
                placed = False
                for i in range(start_slot, len(self.time_slots)):
                    if slot_remaining[i] >= task.duration_minutes:
                        start = slot_cursor[i]
                        end = start + timedelta(minutes=task.duration_minutes)
                        scheduled_items.append(
                            ScheduledTask(task=task, pet_name=pet_name, start_time=start, end_time=end)
                        )
                        slot_cursor[i] = end
                        slot_remaining[i] -= task.duration_minutes
                        placed = True
                        break
                if not placed:
                    skipped_lines.append(
                        f"  ✗ [{pet_name}] {task.type.value} occurrence {occurrence_idx + 1} skipped — "
                        f"no slot had {task.duration_minutes} min remaining"
                    )

        scheduled_items.sort(key=lambda x: x.start_time)

        scheduled_by_pet: dict[str, list[ScheduledTask]] = {pet.name: [] for pet in pets}
        for si in scheduled_items:
            scheduled_by_pet[si.pet_name].append(si)

        total_used = total_available - sum(slot_remaining)

        explanation_lines: list[str] = [
            f"Owner plan | {total_available:.0f} min available across {len(self.time_slots)} slot(s)",
            f"Pets: {', '.join(pet.name for pet in pets)}",
            "",
        ]
        for si in scheduled_items:
            explanation_lines.append(
                f"  [{si.pet_name}] {si.task.type.value} | "
                f"{si.start_time.strftime('%-I:%M %p')} – {si.end_time.strftime('%-I:%M %p')}"
            )
        explanation_lines += skipped_lines
        explanation_lines += [
            "",
            f"Summary: {total_used:.0f}/{total_available:.0f} min used.",
            "Conflict resolution: tasks ordered by priority (HIGH→MEDIUM→LOW), "
            "ties broken by shortest total duration first.",
        ]

        return Plan(id=1, task_list_by_pet=scheduled_by_pet, explanation="\n".join(explanation_lines))


@dataclass
class Task:
    """A care task assigned to a pet (e.g. walk, feeding, grooming)."""

    type: TaskType
    frequency: int
    duration_minutes: int
    priority: Priority

    def __post_init__(self) -> None:
        if not (0 < self.frequency < 10):
            raise ValueError(f"frequency must be between 1 and 9, got {self.frequency}")
        if not isinstance(self.priority, Priority):
            raise ValueError(f"priority must be a Priority enum value, got {self.priority!r}")
        if not isinstance(self.type, TaskType):
            raise ValueError(f"type must be a TaskType enum value, got {self.type!r}")


@dataclass
class Pet:
    """A pet belonging to an owner."""

    #id: int
    name: str
    type: str
    #age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task. Raises ValueError if a task of the same type already exists."""
        if any(t.type == task.type for t in self.tasks):
            raise ValueError(f"Task of type '{task.type.value}' already exists for {self.name}")
        self.tasks.append(task)


@dataclass
class ScheduledTask:
    """A single task occurrence assigned to a concrete time window."""

    task: Task
    pet_name: str
    start_time: datetime
    end_time: datetime


@dataclass
class Plan:
    """A generated daily care plan for an owner, grouping scheduled tasks by pet."""

    id: int
    task_list_by_pet: dict[str, list[ScheduledTask]] = field(default_factory=dict)
    explanation: str = ""


class Owner:
    """A pet owner who can manage pets, a scheduler, and generate care plans."""

    def __init__(
        self,
        #id: int,
        first_name: str,
        last_name: str,
        email: str,
        scheduler: Optional[Scheduler] = None,
    ) -> None:
        self.id: int = id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.scheduler: Optional[Scheduler] = scheduler
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner. Raises ValueError if a pet with the same name already exists."""
        if any(p.name == pet.name for p in self.pets):
            raise ValueError(f"Owner already has a pet named '{pet.name}'")
        self.pets.append(pet)

    def add_scheduler(self, scheduler: Scheduler) -> None:
        """Attach a scheduler to this owner."""
        self.scheduler = scheduler

    def generate_plan(self) -> Plan:
        """Generate one plan for all pets. Raises ValueError if no pets or no scheduler."""
        if not self.pets:
            raise ValueError("No pets associated with this owner.")
        if self.scheduler is None:
            raise ValueError("No scheduler set for this owner.")
        return self.scheduler.build_plan(self.pets)
