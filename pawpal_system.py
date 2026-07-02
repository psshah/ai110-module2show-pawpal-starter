"""PawPal+ system classes for pet care task scheduling."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Scheduler:
    """Holds scheduling constraints: priority level and available time window."""

    priority: str
    available_start_time: datetime
    available_end_time: datetime


@dataclass
class Task:
    """A care task assigned to a pet (e.g. walk, feeding, grooming)."""

    type: str
    frequency: str
    pet_id: int
    scheduler: Optional[Scheduler] = None

    def add_scheduler(self, scheduler: Scheduler) -> None:
        """Attach a scheduler to this task."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet belonging to an owner."""

    id: int
    name: str
    type: str
    age: int
    owner_id: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        raise NotImplementedError


@dataclass
class Plan:
    """A generated daily care plan for a pet."""

    id: int
    pet_id: int
    plan_id: int
    task_list: list[Task] = field(default_factory=list)
    explanation: str = ""


class Owner:
    """A pet owner who can manage pets, a scheduler, and generate care plans."""

    def __init__(
        self,
        id: int,
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
        self.pet: Optional[Pet] = None

    def add_pet(self, pet: Pet) -> None:
        """Associate a pet with this owner."""
        raise NotImplementedError

    def add_scheduler(self, scheduler: Scheduler) -> None:
        """Attach a scheduler to this owner."""
        raise NotImplementedError

    def generate_plan(self) -> Plan:
        """Generate a daily care plan based on pets, tasks, and scheduler constraints."""
        raise NotImplementedError
