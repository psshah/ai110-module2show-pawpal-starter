# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    At a high level, this system will support these core actions.
    1. Add a owner and a pet.
    2. Add task and frequency for pet.
    3. Add constraints (daily availability and priority).
    4. Generate a plan for the pet with given inputs, and provide explanation.

    Here is the detailed requirement.

    1. Owner should be able to add themselves and a pet. 
        Constraint: For initial version, we will keep multiple pets per owner out of scope.  
        Constraint: For initial version, we will not handle if there are multiple owners for same pet (eg. two people in a household). For now, they can share the same account.
    2. Once added, owner can specify task and frequency to generate a plan. 
        Task is free-form string to begin with, and frequency can be between 1-5 times a day.
        Example: Add feedings for pet, twice a day.
        Example: Grooming once a week.
        Example: Vet appointment once every 3 months.
    3. Owner can add Schedule around their availability and priority of tasks.
        Example: Eg vet appt high priority, walks medium priority.
        Example: Available for walks between 8-9 am. 
    Out of scope for initial version:
        - Removing a pet
        - Deleting a task.
        - Updating frequency and hence updating the plan.
        - Advance scheduling eg. business travel next week so no vet appt next week.

- What classes did you include, and what responsibilities did you assign to each?
    Class: Owner
        Attributes: 
            First name: string, 
            Last name: string, 
            Email: string, 
            Scheduler: Scheduler
        Methods: 
            addPet(Pet pet): void
            addScheduler(Scheduler scheduler): void
            generatePlan(): Plan

    Class: Pet
        Attributes: 
            Name: string, 
            Type: string, 
        Method:
            addTask(Task task): void

    Class: Task
        Attributes: 
            Type: string (walk, feed, meds), 
            Frequency: enum (daily, weekly), 
            Duration: int,
            Priority: enum (low, medium, high), 
        Methods:
    
    Class: Scheduler
        Attributes: 
            AvailableStartTime: datetime
            AvailableEndTime: datetime
    
    Class: Plan
        Attributes: 
            Id: int, 
            PetId: int, 
            taskList: List[Task, time],
            Explanation: string 

    Relationship:
        - Owner --> pet (association). Owner has a pet (1:n)
        - Pet can have multiple Tasks (1:n)
        - Each owner has a Scheduler (1:n)
        - Each Task has a Scheduler
        - Each owner-pet has one plan (1:1)
        - Each plan has multiple tasks associated with it.

    Mermaid class diagram:

    ```mermaid
    classDiagram
        class Owner {
            +string firstName
            +string lastName
            +string email
            +Scheduler scheduler
            +List~Pet~ pets
            +addPet(pet: Pet): void
            +addScheduler(scheduler: Scheduler): void
            +generatePlan(): Plan
        }

        class Pet {
            +string name
            +string type
            +List~Task~ tasks
            +addTask(task: Task): void
        }

        class Task {
            +TaskType type
            +int frequency
            +int durationMinutes
            +Priority priority
        }

        class Priority {
            <<enumeration>>
            LOW
            MEDIUM
            HIGH
        }

        class TaskType {
            <<enumeration>>
            WALKS
            FEEDING
            BATHROOM_BREAKS
            MENTAL_PLAY
            GROOMING
            MEDICATIONS
            VET_APPOINTMENT
        }

        class TimeSlot {
            +datetime startTime
            +datetime endTime
        }

        class Scheduler {
            +List~TimeSlot~ timeSlots
            +buildPlan(pets: List~Pet~): Plan
        }

        class Plan {
            +int id
            +Map~string_List~Task~~ taskListByPet
            +string explanation
        }

        Owner "1" --> "*" Pet : owns
        Pet --> Task : has
        Owner --> Scheduler : has
        Scheduler --> TimeSlot : uses
        Owner --> Plan : generates
        Plan --> Task : contains
    ```

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
1. Added duration to Task. Without it, scheduler/plan can't decide if task will fit in available window.
2. Added a build_plan method to Scheduler to move the responsibility of building the plan outside of Owner. Reasoning - Owner is not responsible for all logic.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Schedudler considers owner's availability as a constraint. Also priority, shortest task first as another constraint (greedy algorithm).
- How did you decide which constraints mattered most?
Priority matters most since tasks with high priority (like medication) need to be on the schedule.  

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It picks the shortest task first at same priority level. For example, a 10-min task with frequency=2 (cost=20) will always beat a 25-min task with frequency=1 (cost=25), even though both are MEDIUM priority.
- Why is that tradeoff reasonable for this scenario?
The algorithm trades fairness between same-priority tasks for optimal utilization of a slot - this is a reasonable first-cut strategy for a scheduling assistant. Making it even fairer would involve more complexity - like weighted approach to give all same-priority tasks an equal shot regardless of duration.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
* I used AI at every step - to ensure my class / UML designs were accurate and understand design trade-offs. eg. do I use object reference (Pet in Owner class) or do I use ids (like traditional database eg. owner.pet_id = pet_id). 
* I used it to brainstorm algorithms for scheduling and taking a step-by-step approach to that algorithm. 
* I also used it to code unit tests, add complex python lambda code to the scheduling build_plan() function.
* Not being familiar with UI, I used it to debug streamlit session state issues (eg. task being appended directly to session state instead of owner object). 

- What kinds of prompts or questions were most helpful?
* Giving it context - eg. line numbers, and  being specific - eg. make this readable, focus on being brief were useful. eg. tests used fixtures which I am not familiar with, so I used AI to refactor them to simpler readable code.

* Another example - when building scheduler, I gave it detailed sample input and sample output to design the algorithm and how the explanation should look like.

* Or providing information about why I would make a certain decision or code and what else would AI suggest (and why) was most helpful. eg. when adding time on UI, being specific that add text boxes, for starttime and endtime. No need for date. Data should be readable as python datetime object. 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
* Scheduling algorithm - the first draft suggested by AI was not doing round-robin eg. task with frequency=2 would be scheduled in the same time slot if time available (walk dog 6:10-6:20 am, walk dog 6:20-6:30 am). I updated the algorithm to schedule it across different slots (eg. walk 6:10-6:20 am, then walk 7-7:10 pm)

- How did you evaluate or verify what the AI suggested?
* Asked AI itself to provide an explanation.
* Cross-verified by reading code and design myself to understand. 
* In some cases where I did not have sufficient knowledge, I asked another AI (ChatGPT).

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Basic tests for each feature - add owner, add pets, add tasks, add scheduler, generate plan. And regenerate plan after adding new task.

- Why were these tests important?
These are the most common workflows (happy path) and wanted to ensure these are functional.

**b. Confidence**

- How confident are you that your scheduler works correctly?
3-4 on a scale of 5. I have not tested edge cases or carefully reviewed code for it - although have added the checks and balances. I have also not tested all scenarios where tasks don't fit, different priority tasks etc.

- What edge cases would you test next if you had more time?
* Task time = exact same as available time slot.
* Owner has pets, no tasks or no scheduler added.
* Task frequency > number of slots. eg. feed 3 times, available time slots=2. Should get skipped once.
* Task duration > available time slot. Should be skipped.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Building a working system from scratch, including translating requirements to design.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Get clarity requirements better upfront - it caused a lot of churn in the design and implementation. 
* I did not realize until later system needed to support multiple pets per owner.
* I did not build it initially to regenerate plan as I did not see that requirement until later.
* I built it for daily schedule use but did not anticipate it to be used for higher frequency (weekly). Did not see that requirement till Phase-4.
* I have not built it for mark_completion() as I do not understand that requirement fully. Did not see that requirement till Phase-4.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
That AI can make a system really complex uncessarily if left to completely write code or design itself. It sometimes designs or writes code which is unreadable and hard to follow through. It is much more productive to guide it step-by-step with clear instructions than just give a generic prompt like 'implement build_plan()'.

Same thing with explanations, comments or tests - it can be too verbose or unncessarily complex. Need to keep a check and ask it to keep it simple.

- Which AI coding assistant features were most effective for building your scheduler?
- Add context.
- /compact
- Agent Mode

- Give one example of an AI suggestion you rejected or modified to keep your system design clean.
Adding extra attributes like age, gender, or DOB of owner.

- How did using separate chat sessions for different phases help you stay organized?
Used one for UML design, one for core implementation, one for brainstorming on plan generation alternatives. Separate chat sessions kept the context crisp and allowed to focus on task at hand (as opposed to using /clear or /compact).