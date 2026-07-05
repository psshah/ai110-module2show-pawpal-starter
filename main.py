from pawpal_system import *

owner = Owner("John", "Doe", "john.doe@example.com")
pet1 = Pet("Buddy", "Dog")
pet2 = Pet("Whiskers", "Cat")

owner.add_pet(pet1)
owner.add_pet(pet2)

task1 = Task(TaskType.FEEDING, 2, 15, Priority.MEDIUM)
task2 = Task(TaskType.WALKS, 2, 45, Priority.LOW)
task3 = Task(TaskType.FEEDING, 1, 10, Priority.MEDIUM)
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

today = datetime.today().date()
morning = TimeSlot(datetime.combine(today, datetime.min.time().replace(hour=7)), datetime.combine(today, datetime.min.time().replace(hour=10)))
evening = TimeSlot(datetime.combine(today, datetime.min.time().replace(hour=18)), datetime.combine(today, datetime.min.time().replace(hour=22)))
owner.add_scheduler(Scheduler([morning, evening]))

plan = owner.generate_plan()
print("Today's schedule:")
print(plan.explanation)

# Add a new task and generate an updated plan
new_task = Task(TaskType.MEDICATIONS, 1, 5, Priority.HIGH)
try:
    pet1.add_task(new_task)
except ValueError as e:
    print(f"Error adding task: {e}")

plan = owner.generate_plan()
print("\nUpdated schedule after adding a new task:")
print(plan.explanation)
