import streamlit as st
from pawpal_system import Owner, Pet, Task, TaskType, Priority, TimeSlot, Scheduler
from datetime import datetime, time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.subheader("Owner & Pets")
if "owner" not in st.session_state:
    st.session_state.owner = None

owner_firstname = st.text_input("Owner first name")
owner_lastname = st.text_input("Owner last name")
owner_email = st.text_input("Owner email")
if st.button("Add owner"):
    st.session_state.owner = Owner(owner_firstname, owner_lastname, owner_email)
    st.success(f"Owner {owner_firstname} {owner_lastname} saved!")

pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(name=pet_name, type=species)
    st.session_state.owner.add_pet(pet)
    st.success(f"Pet {pet_name} added!")

# Show owner info and all their pets
if st.session_state.owner:
    owner = st.session_state.owner
    st.markdown("**Current owner & pets**")
    st.write(f"Owner: {owner.first_name} {owner.last_name} ({owner.email})")
    if owner.pets:
        for pet in owner.pets:
            st.write(f"- {pet.name} ({pet.type})")
    else:
        st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    pet_options = [pet.name for pet in st.session_state.owner.pets] if st.session_state.owner and st.session_state.owner.pets else []
    task_pet_name = st.selectbox("Pet name", options=pet_options)
with col2:
    task_options = [t.value for t in TaskType]
    task_title = st.selectbox("Task title", options=task_options, index=1)
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority_options = [p.value for p in Priority]
    priority = st.selectbox("Priority", options=priority_options, index=1)
with col5:
    frequency = st.number_input("Frequency", min_value=1, max_value=9, value=1, step=1,
                                help="How many times this task will occur per day")

if st.button("Add task"):
    try:
        pet = next(p for p in st.session_state.owner.pets if p.name == task_pet_name)
        task = Task(
            type=TaskType(task_title),
            frequency=int(frequency),
            duration_minutes=int(duration),
            priority=Priority(priority),
        )
        pet.add_task(task)
        st.success(f"Task '{task_title}' added to {task_pet_name}!")
    except StopIteration:
        st.error(f"Pet '{task_pet_name}' not found.")
    except ValueError as e:
        st.error(f"Could not add task: {e}")

if st.session_state.owner and any(pet.tasks for pet in st.session_state.owner.pets):
    st.write("Current tasks:")
    rows = [
        {"pet": pet.name, "task": t.type.value, "duration_minutes": t.duration_minutes, "priority": t.priority.value, "frequency": t.frequency}
        for pet in st.session_state.owner.pets
        for t in pet.tasks
    ]
    st.table(rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Owner Schedule")
slot_date = datetime.today().date()
start_time = st.time_input("Start time", value=time(8, 0), step=900)
end_time = st.time_input("End time", value=time(10, 0), step=900)

if st.button("Add time slot"):
    try:
        start = datetime.combine(slot_date, start_time)
        end = datetime.combine(slot_date, end_time)
        new_slot = TimeSlot(start_time=start, end_time=end)
        if st.session_state.owner.scheduler is None:
            st.session_state.owner.scheduler = Scheduler(time_slots=[new_slot])
        else:
            st.session_state.owner.scheduler.time_slots.append(new_slot)
        st.success(f"Time slot added: {start_time} → {end_time}")
    except ValueError as e:
        st.error(f"Invalid input: {e}")

if st.session_state.owner and st.session_state.owner.scheduler:
    st.write("Current time slots:")
    for slot in st.session_state.owner.scheduler.time_slots:
        st.write(f"- {slot.start_time.strftime('%Y-%m-%d %H:%M')} → {slot.end_time.strftime('%Y-%m-%d %H:%M')} ({slot.available_minutes:.0f} min)")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner:
        try:
            plan = st.session_state.owner.generate_plan()
            st.success("Schedule generated!")
            st.markdown("**Plan explanation:**")
            st.text(plan.explanation)
        except Exception as e:
            st.error(f"Error generating schedule: {e}")
    else:
        st.warning("Please add an owner first.")