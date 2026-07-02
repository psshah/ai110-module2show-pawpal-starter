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
            Id: int, 
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
            Id: int, 
            Name: string, 
            Type: string, 
            Age: int, 
            OwnerId: int
        Method:
            addTask(Task task): void

    Class: Task
        Attributes: 
            Type: string (walk, feed, meds), 
            Frequency: enum (daily, weekly), 
            PetId: int, 
            Scheduler: Scheduler
        Methods:
            addScheduler(Scheduler scheduler): void
    
    Class: Scheduler
        Attributes: 
            Priority: enum (low, medium, high), 
            AvailableStartTime: datetime
            AvailableEndTime: datetime
    
    Class: Plan
        Attributes: 
            Id: int, 
            PetId: int, 
            PlanId: int, 
            taskList: List[Task, time],
            Explanation: string 

    Relationship:
        - Owner --> pet (association). Owner has a pet (1:1)
        - Pet can have multiple Tasks (1:n)
        - Each owner has a Scheduler (1:n)
        - Each Task has a Scheduler
        - Each owner-pet has one plan (1:1)
        - Each plan has multiple tasks associated with it.

    Mermaid class diagram:

    ```mermaid
    classDiagram
        class Owner {
            +int id
            +string firstName
            +string lastName
            +string email
            +Scheduler scheduler
            +addPet(pet: Pet): void
            +addScheduler(scheduler: Scheduler): void
            +generatePlan(): Plan
        }

        class Pet {
            +int id
            +string name
            +string type
            +int age
            +int ownerId
            +addTask(task: Task): void
        }

        class Task {
            +string type
            +string frequency
            +int petId
            +Scheduler scheduler
            +addScheduler(scheduler: Scheduler): void
        }

        class Scheduler {
            +string priority
            +datetime availableStartTime
            +datetime availableEndTime
        }

        class Plan {
            +int id
            +int petId
            +int planId
            +List~Task~ taskList
            +string explanation
        }

        Owner --> Pet : owns
        Pet --> Task : has
        Owner --> Scheduler : has
        Task --> Scheduler : uses
        Owner --> Plan : generates
        Plan --> Task : contains
    ```

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
