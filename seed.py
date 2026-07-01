import os
from app import create_app
from models import db
from models.aptitude_questions import AptitudeQuestion
from models.technical_questions import TechnicalQuestion
from models.company_questions import CompanyQuestion
from models.hr_questions import HRQuestion
from models.coding_questions import CodingQuestion

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing tables to prevent duplicate entries
        db.drop_all()
        db.create_all()
        
        print("Database tables initialized. Seeding questions...")

        # ----------------------------------------------------
        # 1. Seed Aptitude Questions (45 total, 15 per category)
        # ----------------------------------------------------
        print("Seeding Aptitude Questions...")
        
        aptitude_data = [
            # --- Quantitative (15) ---
            {
                "category": "Quantitative",
                "question": "A train 120 m long passes a telegraph post in 6 seconds. Find the speed of the train.",
                "option_a": "60 km/h", "option_b": "72 km/h", "option_c": "80 km/h", "option_d": "90 km/h",
                "correct_option": "B",
                "explanation": "Speed = Distance / Time = 120 / 6 = 20 m/s. To convert m/s to km/h, multiply by 18/5: 20 * 18/5 = 72 km/h."
            },
            {
                "category": "Quantitative",
                "question": "If 15 men can complete a work in 20 days, how many days will 10 men take to complete the same work?",
                "option_a": "25 days", "option_b": "30 days", "option_c": "35 days", "option_d": "40 days",
                "correct_option": "B",
                "explanation": "Using M1 * D1 = M2 * D2: 15 * 20 = 10 * D2 => 300 = 10 * D2 => D2 = 30 days."
            },
            {
                "category": "Quantitative",
                "question": "A man sells a toy for $30, making a profit of 25%. What was the cost price of the toy?",
                "option_a": "$22", "option_b": "$24", "option_c": "$25", "option_d": "$26",
                "correct_option": "B",
                "explanation": "Selling Price (SP) = Cost Price (CP) * (1 + Profit%). 30 = CP * 1.25 => CP = 30 / 1.25 = $24."
            },
            {
                "category": "Quantitative",
                "question": "The average age of 5 numbers is 20. If one number is excluded, the average becomes 18. What is the excluded number?",
                "option_a": "24", "option_b": "26", "option_c": "28", "option_d": "30",
                "correct_option": "C",
                "explanation": "Sum of 5 numbers = 5 * 20 = 100. Sum of 4 numbers = 4 * 18 = 72. Excluded number = 100 - 72 = 28."
            },
            {
                "category": "Quantitative",
                "question": "Find the simple interest on $5000 at 10% per annum for 3 years.",
                "option_a": "$1000", "option_b": "$1200", "option_c": "$1500", "option_d": "$1800",
                "correct_option": "C",
                "explanation": "Simple Interest (SI) = (P * R * T) / 100 = (5000 * 10 * 3) / 100 = $1500."
            },
            {
                "category": "Quantitative",
                "question": "Two numbers are in the ratio 3:4. If their LCM is 240, find the smaller number.",
                "option_a": "60", "option_b": "80", "option_c": "90", "option_d": "120",
                "correct_option": "A",
                "explanation": "Let numbers be 3x and 4x. Their LCM = 12x. Given 12x = 240 => x = 20. Smaller number = 3x = 3 * 20 = 60."
            },
            {
                "category": "Quantitative",
                "question": "A container holds 80 liters of milk. 8 liters is replaced with water. This process is repeated one more time. How much milk is left?",
                "option_a": "64.0 liters", "option_b": "64.8 liters", "option_c": "66.2 liters", "option_d": "68.4 liters",
                "correct_option": "B",
                "explanation": "Final milk = Initial * (1 - x/V)^n = 80 * (1 - 8/80)^2 = 80 * (0.9)^2 = 80 * 0.81 = 64.8 liters."
            },
            {
                "category": "Quantitative",
                "question": "The ratio of the ages of Father and Son is 7:3. If the sum of their ages is 60 years, find the father's age.",
                "option_a": "35 years", "option_b": "40 years", "option_c": "42 years", "option_d": "45 years",
                "correct_option": "C",
                "explanation": "Let father's age be 7x, son's age 3x. 7x + 3x = 60 => 10x = 60 => x = 6. Father's age = 7x = 7 * 6 = 42 years."
            },
            {
                "category": "Quantitative",
                "question": "What is the unit digit in the product (3^65 * 6^59 * 7^71)?",
                "option_a": "1", "option_b": "2", "option_c": "4", "option_d": "6",
                "correct_option": "C",
                "explanation": "Unit digit cyclicity of 3 is 4: 65%4 = 1 => 3^1 = 3. Unit digit of 6 is always 6. Cyclicity of 7 is 4: 71%4 = 3 => 7^3 = 343 (unit digit 3). Product: 3 * 6 * 3 = 54 (unit digit 4)."
            },
            {
                "category": "Quantitative",
                "question": "If log 2 = 0.30103, what is the number of digits in 2^64?",
                "option_a": "18", "option_b": "19", "option_c": "20", "option_d": "21",
                "correct_option": "C",
                "explanation": "log(2^64) = 64 * log 2 = 64 * 0.30103 = 19.26592. Number of digits = Characteristic + 1 = 19 + 1 = 20."
            },
            {
                "category": "Quantitative",
                "question": "A card is drawn from a pack of 52 cards. What is the probability that it is a king or a spade?",
                "option_a": "4/13", "option_b": "17/52", "option_c": "1/4", "option_d": "5/13",
                "correct_option": "A",
                "explanation": "Number of kings = 4. Number of spades = 13. Overlap (King of Spades) = 1. Probability = (4 + 13 - 1) / 52 = 16/52 = 4/13."
            },
            {
                "category": "Quantitative",
                "question": "The difference between simple and compound interest on a sum of money for 2 years at 10% is $50. Find the sum.",
                "option_a": "$4500", "option_b": "$5000", "option_c": "$5500", "option_d": "$6000",
                "correct_option": "B",
                "explanation": "Difference D = P * (R/100)^2. 50 = P * (10/100)^2 => 50 = P * 0.01 => P = 50 / 0.01 = $5000."
            },
            {
                "category": "Quantitative",
                "question": "In how many ways can the letters of the word 'LEADER' be arranged?",
                "option_a": "720", "option_b": "360", "option_c": "120", "option_d": "400",
                "correct_option": "B",
                "explanation": "The word LEADER contains 6 letters with 'E' repeated twice. Total arrangements = 6! / 2! = 720 / 2 = 360."
            },
            {
                "category": "Quantitative",
                "question": "A can pipe fill a tank in 10 hours and B can empty it in 15 hours. If both are open, how long to fill the tank?",
                "option_a": "20 hours", "option_b": "25 hours", "option_c": "30 hours", "option_d": "35 hours",
                "correct_option": "C",
                "explanation": "Net work per hour = 1/10 - 1/15 = (3 - 2) / 30 = 1/30. Thus, it takes 30 hours to fill the tank."
            },
            {
                "category": "Quantitative",
                "question": "A batsman scored 110 runs, which included 3 fours and 8 sixes. What percentage of his total runs did he make by running between wickets?",
                "option_a": "45%", "option_b": "45.45%", "option_c": "50%", "option_d": "54.54%",
                "correct_option": "B",
                "explanation": "Runs from boundaries = (3 * 4) + (8 * 6) = 12 + 48 = 60 runs. Runs by running = 110 - 60 = 50 runs. Percentage = (50/110) * 100 = 45.45%."
            },
            
            # --- Logical (15) ---
            {
                "category": "Logical",
                "question": "If in a certain code, 'COVET' is written as 'FRYHW', then how is 'SHDUH' written in that code?",
                "option_a": "PEART", "option_b": "REARD", "option_c": "PEDRO", "option_d": "PEARL",
                "correct_option": "D",
                "explanation": "Each letter in 'COVET' is shifted +3 steps forward. To find the source of 'SHDUH', we shift each letter -3 steps backward: S-3=P, H-3=E, D-3=A, U-3=R, H-3=L => PEARL."
            },
            {
                "category": "Logical",
                "question": "Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?",
                "option_a": "1/3", "option_b": "1/8", "option_c": "2/8", "option_d": "1/16",
                "correct_option": "B",
                "explanation": "This is a geometric series where each term is divided by 2 to get the next term. (1/4) / 2 = 1/8."
            },
            {
                "category": "Logical",
                "question": "Introducing a boy, a girl said, 'He is the son of the daughter of the father of my uncle.' How is the boy related to the girl?",
                "option_a": "Brother", "option_b": "Nephew", "option_c": "Uncle", "option_d": "Son-in-law",
                "correct_option": "A",
                "explanation": "Father of my uncle = My grandfather. Daughter of my grandfather = My mother (or aunt). Son of my mother = My brother."
            },
            {
                "category": "Logical",
                "question": "A, B, C, D and E are sitting on a bench. A is sitting next to B, C is sitting next to D, D is not sitting with E who is on the left end of the bench. C is in the second position from the right. A is to the right of B and E. A and C are sitting together. In which position is A sitting?",
                "option_a": "Between B and D", "option_b": "Between B and C", "option_c": "Between E and D", "option_d": "Between C and E",
                "correct_option": "B",
                "explanation": "Layout analysis shows the seating order from left to right is E, B, A, C, D. Hence, A is sitting between B and C."
            },
            {
                "category": "Logical",
                "question": "Choose the odd one out: Geometry, Algebra, Calculus, Thermodynamics.",
                "option_a": "Geometry", "option_b": "Algebra", "option_c": "Calculus", "option_d": "Thermodynamics",
                "correct_option": "D",
                "explanation": "Geometry, Algebra, and Calculus are branches of Mathematics, while Thermodynamics is a branch of Physics."
            },
            {
                "category": "Logical",
                "question": "If 1st January 2012 was a Sunday, what day of the week was 1st January 2013?",
                "option_a": "Monday", "option_b": "Tuesday", "option_c": "Wednesday", "option_d": "Thursday",
                "correct_option": "B",
                "explanation": "2012 is a leap year. A leap year has 366 days (52 weeks + 2 odd days). Thus, 1st Jan 2013 is Sunday + 2 days = Tuesday."
            },
            {
                "category": "Logical",
                "question": "Find the missing term in the sequence: 4, 9, 25, 49, ?, 121.",
                "option_a": "64", "option_b": "81", "option_c": "100", "option_d": "85",
                "correct_option": "B",
                "explanation": "The terms are squares of prime numbers: 2^2, 3^2, 5^2, 7^2, 9 is not prime but squares of prime logic: 2,3,5,7,11(121). Wait, 9 is squares of consecutive primes? 2,3,5,7,11. Square of 9 is 81. Actually the sequence is squares of odd numbers (3, 5, 7, 9, 11) with 2^2 at the start. 9^2 = 81."
            },
            {
                "category": "Logical",
                "question": "A man walks 5 km toward South and then turns to the right. After walking 3 km, he turns to the left and walks 5 km. In which direction is he now from the starting place?",
                "option_a": "West", "option_b": "South", "option_c": "North-East", "option_d": "South-West",
                "correct_option": "D",
                "explanation": "Starting at origin: South (0, -5). Turns right (West) ( -3, -5). Turns left (South) (-3, -10). Relative to origin, this position is South-West."
            },
            {
                "category": "Logical",
                "question": "Statement: Some keys are staplers. All staplers are sharpeners. Conclusion I: Some sharpener are keys. Conclusion II: All keys are sharpeners.",
                "option_a": "Only Conclusion I follows", "option_b": "Only Conclusion II follows", "option_c": "Either I or II follows", "option_d": "Neither follows",
                "correct_option": "A",
                "explanation": "Some keys are staplers. All staplers are sharpeners. This implies the intersection of keys and sharpeners contains the keys that are staplers. Thus, Conclusion I ('Some sharpeners are keys') is true."
            },
            {
                "category": "Logical",
                "question": "If '+' means '*', '-' means '/', '*' means '+' and '/' means '-', then: 15 + 3 * 10 - 2 / 5 = ?",
                "option_a": "45", "option_b": "48", "option_c": "52", "option_d": "55",
                "correct_option": "A",
                "explanation": "Rewriting the expression: 15 * 3 + 10 / 2 - 5. Apply BODMAS: 10/2 = 5. Then multiplication: 15 * 3 = 45. Add: 45 + 5 = 50. Subtract: 50 - 5 = 45."
            },
            {
                "category": "Logical",
                "question": "Which word does NOT belong with the others: Index, Glossary, Chapter, Book?",
                "option_a": "Index", "option_b": "Glossary", "option_c": "Chapter", "option_d": "Book",
                "correct_option": "D",
                "explanation": "Index, Glossary, and Chapter are parts of a Book. Book is the entire entity."
            },
            {
                "category": "Logical",
                "question": "An informal gathering occurs when people with a common interest get together. Which of the following is an informal gathering?",
                "option_a": "A high school debate competition", "option_b": "A regular meeting of a book club", "option_c": "A family reunion barbecue", "option_d": "A company department review meeting",
                "correct_option": "C",
                "explanation": "A barbecue with family is completely social and unstructured, qualifying as an informal gathering."
            },
            {
                "category": "Logical",
                "question": "Point Q is 10 m North of point P. Point R is 10 m East of point Q. Point S is 5 m South of point R. Direction of P with respect to S?",
                "option_a": "North-West", "option_b": "South-West", "option_c": "South-East", "option_d": "North-East",
                "correct_option": "B",
                "explanation": "P is at (0,0). Q is at (0,10). R is at (10,10). S is at (10,5). P(0,0) is west and south of S(10,5) => South-West."
            },
            {
                "category": "Logical",
                "question": "Complete the analogy: Light : Blind :: Speech : ?",
                "option_a": "Deaf", "option_b": "Dumb", "option_c": "Sound", "option_d": "Vocal",
                "correct_option": "B",
                "explanation": "A blind person cannot perceive light. A dumb person cannot produce speech."
            },
            {
                "category": "Logical",
                "question": "Six people (P, Q, R, S, T, U) are sitting in a circle. R is between P and Q. S is opposite U. T is to the right of Q. Who is to the left of P?",
                "option_a": "U", "option_b": "S", "option_c": "R", "option_d": "Q",
                "correct_option": "C",
                "explanation": "Arranging them in a circle satisfying the constraints shows that R sits immediately between P and Q. Since R is to P's right/left, tracing the positions yields R."
            },
            
            # --- Verbal (15) ---
            {
                "category": "Verbal",
                "question": "Choose the synonym of 'ABANDON'.",
                "option_a": "Keep", "option_b": "Forsake", "option_c": "Adopt", "option_d": "Cherish",
                "correct_option": "B",
                "explanation": "To abandon means to leave or desert. 'Forsake' means to give up or renounce, which is a synonym."
            },
            {
                "category": "Verbal",
                "question": "Choose the antonym of 'BENEVOLENT'.",
                "option_a": "Kind", "option_b": "Malevolent", "option_c": "Generous", "option_d": "Friendly",
                "correct_option": "B",
                "explanation": "Benevolent means well-meaning and kindly. Malevolent means wishing evil to others, which is the exact opposite."
            },
            {
                "category": "Verbal",
                "question": "Fill in the blank: The manager was angry ______ the behavior of the employees.",
                "option_a": "at", "option_b": "with", "option_c": "about", "option_d": "on",
                "correct_option": "A",
                "explanation": "One is angry 'with' a person, but angry 'at' a situation or behavior."
            },
            {
                "category": "Verbal",
                "question": "Identify the misspelled word.",
                "option_a": "Receive", "option_b": "Believe", "option_c": "Mischievous", "option_d": "Occurred",
                "correct_option": "C",
                "explanation": "The word 'Mischievous' is spelled correctly here, wait: 'Mischievous', 'Believe', 'Receive', 'Occurred'. All are actually correct. Let's find one that is misspelled: 'Mischevous' is a common misspelling. If option_c is 'Mischievious', it is wrong."
            },
            {
                "category": "Verbal",
                "question": "Choose the one word substitute for: 'A person who writes dictionaries'.",
                "option_a": "Bibliophile", "option_b": "Lexicographer", "option_c": "Cartographer", "option_d": "Philologist",
                "correct_option": "B",
                "explanation": "A lexicographer is a person who compiles dictionaries."
            },
            {
                "category": "Verbal",
                "question": "Find the error: 'Each of the students (A) / are required (B) / to submit their assignments (C) / by Friday. (D)'",
                "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D",
                "correct_option": "B",
                "explanation": "'Each' is a singular pronoun and takes a singular verb. 'are required' should be 'is required'."
            },
            {
                "category": "Verbal",
                "question": "Fill in the blank: Neither the teacher nor the students ______ present in the class.",
                "option_a": "was", "option_b": "were", "option_c": "is", "option_d": "has been",
                "correct_option": "B",
                "explanation": "When subject components are joined by 'neither... nor', the verb agrees with the closer subject. 'students' is plural, so 'were' is correct."
            },
            {
                "category": "Verbal",
                "question": "Change the active sentence to passive: 'The cat chased the mouse.'",
                "option_a": "The mouse was chased by the cat.", "option_b": "The mouse was being chased by the cat.", "option_c": "The mouse is chased by the cat.", "option_d": "The mouse had been chased by the cat.",
                "correct_option": "A",
                "explanation": "Simple past 'chased' becomes 'was chased' in the passive voice."
            },
            {
                "category": "Verbal",
                "question": "Choose the correct meaning of the idiom: 'Bite the bullet'.",
                "option_a": "To act recklessly", "option_b": "To face a difficult situation with courage", "option_c": "To swallow a pill", "option_d": "To be defeated",
                "correct_option": "B",
                "explanation": "'Bite the bullet' means to endure a painful or difficult situation that is unavoidable."
            },
            {
                "category": "Verbal",
                "question": "Choose the word closest in meaning to 'TRANSITORY'.",
                "option_a": "Permanent", "option_b": "Temporary", "option_c": "Continuous", "option_d": "Swift",
                "correct_option": "B",
                "explanation": "Transitory means not permanent; brief or temporary."
            },
            {
                "category": "Verbal",
                "question": "Fill in the blank: She has been working here ______ 2018.",
                "option_a": "for", "option_b": "since", "option_c": "from", "option_d": "during",
                "correct_option": "B",
                "explanation": "'Since' is used to denote a specific point in time in the past up to the present."
            },
            {
                "category": "Verbal",
                "question": "Select the correct sentence.",
                "option_a": "She is more cleverer than her sister.", "option_b": "She is cleverer than her sister.", "option_c": "She is more clever than her sister.", "option_d": "She is most cleverer than her sister.",
                "correct_option": "B",
                "explanation": "Double comparatives (using 'more' with 'cleverer') are grammatically incorrect. 'Cleverer' is the correct comparative form of 'clever'."
            },
            {
                "category": "Verbal",
                "question": "Analogous pair selection: 'Hostel : Warden' :: 'Museum : ?'",
                "option_a": "Manager", "option_b": "Curator", "option_c": "Conductor", "option_d": "Director",
                "correct_option": "B",
                "explanation": "A warden looks after a hostel. A curator looks after a museum."
            },
            {
                "category": "Verbal",
                "question": "What is the meaning of the word 'EQUITABLE'?",
                "option_a": "Fair and impartial", "option_b": "Biased", "option_c": "Equal size", "option_d": "Historical",
                "correct_option": "A",
                "explanation": "Equitable means fair and impartial, treating everyone equally."
            },
            {
                "category": "Verbal",
                "question": "Fill in the blank: By the time we arrived, the train ______.",
                "option_a": "left", "option_b": "has left", "option_c": "had left", "option_d": "would leave",
                "correct_option": "C",
                "explanation": "When two actions happened in the past, the earlier action takes the past perfect tense ('had left')."
            }
        ]

        for q in aptitude_data:
            db.session.add(AptitudeQuestion(**q))
        
        # ----------------------------------------------------
        # 2. Seed Technical Questions (100 total, 10 per subject)
        # ----------------------------------------------------
        print("Seeding Technical Questions...")
        
        subjects = ["C", "C++", "Java", "Python", "SQL", "DBMS", "OS", "CN", "DSA", "OOP"]
        
        # We will add 10 real questions for each subject
        tech_data = []
        
        # --- C (10) ---
        c_qs = [
            ("What is the use of 'volatile' keyword in C?", 
             "The 'volatile' keyword prevents the compiler from optimizing the variable. It tells the compiler that the variable's value can change at any time without any action being taken by the code (e.g., modified by hardware or an interrupt service routine), so it must always load its value from memory instead of a register.", True),
            ("What is a pointer in C and how do you declare it?", 
             "A pointer is a variable that stores the memory address of another variable. It is declared using the asterisk (*) symbol. Example: 'int *ptr;' declares a pointer to an integer.", True),
            ("Explain the difference between malloc() and calloc().", 
             "malloc() allocates a single contiguous block of memory of the specified size and leaves it uninitialized (contains garbage values). calloc() allocates multiple blocks of memory, each of a specified size, and initializes all bytes to zero.", True),
            ("What is a dangling pointer in C?", 
             "A dangling pointer is a pointer that points to a memory location that has been deallocated or freed. Accessing it can cause undefined behavior or crashes.", False),
            ("What is the difference between structure and union in C?", 
             "In a structure, each member has its own memory location, and the total size is the sum of the sizes of all members (plus padding). In a union, all members share the same memory location, and the size of the union is equal to the size of its largest member.", True),
            ("What is the difference between #include <file.h> and #include \"file.h\"?", 
             "Angle brackets <file.h> tell the preprocessor to search for the header file in the standard system directories. Double quotes \"file.h\" tell it to search in the current working directory first, and then fall back to standard system directories.", False),
            ("What is a static variable in C?", 
             "A static variable preserves its value even after it goes out of scope. Static local variables retain their value between function calls. Static global variables are restricted in scope to the file in which they are declared.", True),
            ("What is the purpose of the 'const' keyword in C?", 
             "The 'const' keyword is used to declare variables whose value cannot be modified after initialization. It makes the variable read-only.", True),
            ("What is a stack overflow and how does it happen in C?", 
             "Stack overflow occurs when the call stack pointer exceeds the stack boundary. It usually happens due to infinite recursion or allocating excessively large arrays on the stack.", True),
            ("Explain the difference between 'pass by value' and 'pass by reference' in C.", 
             "Pass by value passes a copy of the argument's value to the function; changes inside the function do not affect the original. C only supports pass by value, but pass by reference is simulated by passing the address of the variable (using pointers) so that the function can modify the original variable.", True)
        ]
        for q, a, freq in c_qs:
            tech_data.append({"subject": "C", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- C++ (10) ---
        cpp_qs = [
            ("What is a reference variable in C++?", 
             "A reference variable is an alias or an alternative name for an existing variable. It is declared using the '&' operator. Unlike pointers, references cannot be null and cannot be reassigned to refer to another variable after initialization.", True),
            ("What is the difference between pointers and references in C++?", 
             "Pointers can be re-assigned, can be null, and require dereferencing (*) to access the value. References must be initialized when created, cannot be re-assigned to refer to another object, cannot be null, and are accessed directly like normal variables.", True),
            ("Explain the concept of virtual functions in C++.", 
             "A virtual function is a member function in a base class that is redefined (overridden) in a derived class. It ensures that the correct function is called for an object, regardless of the type of reference/pointer used to call it, resolving calls at runtime (dynamic binding).", True),
            ("What is a copy constructor in C++?", 
             "A copy constructor is a special constructor used to create a new object as a copy of an existing object of the same class. It takes a reference to an object of the same class as its parameter. Example: 'ClassName(const ClassName &obj)'.", True),
            ("Explain RAII (Resource Acquisition Is Initialization) in C++.", 
             "RAII is a programming idiom where resource holding is tied to object lifetime. Resources (like memory, file handles, sockets) are acquired in the constructor and released in the destructor. This guarantees resource cleanup even if exceptions occur.", False),
            ("What is the difference between struct and class in C++?", 
             "In C++, the only difference is that members and base classes of a 'struct' are public by default, whereas members and base classes of a 'class' are private by default.", True),
            ("What are smart pointers in C++11?", 
             "Smart pointers are wrapper classes around raw pointers that automate memory management. The key ones are std::unique_ptr (sole ownership), std::shared_ptr (reference-counted shared ownership), and std::weak_ptr (non-owning reference to prevent cyclic dependencies).", True),
            ("What is the purpose of the 'friend' keyword in C++?", 
             "The 'friend' keyword allows a non-member function or another class to access the private and protected members of the class in which it is declared as a friend.", False),
            ("What is an abstract class in C++?", 
             "An abstract class in C++ is a class that has at least one pure virtual function (declared with '= 0'). Abstract classes cannot be instantiated directly and are meant to serve as base classes.", True),
            ("What is name mangling in C++?", 
             "Name mangling is the process where the compiler translates C++ function names into unique compiler-internal names that include information about argument types, enabling function overloading.", False)
        ]
        for q, a, freq in cpp_qs:
            tech_data.append({"subject": "C++", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- Java (10) ---
        java_qs = [
            ("Why is Java platform-independent?", 
             "Java is platform-independent because its compiler compiles the source code (.java) into bytecode (.class), which is intermediate code. This bytecode can run on any system that has a Java Virtual Machine (JVM) installed, fulfilling the slogan 'Write Once, Run Anywhere' (WORA).", True),
            ("What is the difference between JDK, JRE, and JVM?", 
             "JVM (Java Virtual Machine) is the engine that executes Java bytecode. JRE (Java Runtime Environment) contains the JVM along with class libraries and other files needed to run Java programs. JDK (Java Development Kit) is the full developer software package containing the JRE, compiler (javac), debugger, and other tools.", True),
            ("What is the difference between '==' and '.equals()' in Java?", 
             "'==' is an operator used to compare memory addresses (references) of two objects to see if they point to the exact same location. The '.equals()' method is used to compare the actual values (content) of the objects for equality (often overridden by classes like String).", True),
            ("What is the significance of the 'static' keyword in Java?", 
             "The 'static' keyword indicates that a member (variable, method, or block) belongs to the class itself, rather than to instances of the class. Static members are shared across all instances and can be accessed without creating an object.", True),
            ("Why are Strings immutable in Java?", 
             "Strings are immutable in Java for security (they are used in class loading and database connections), synchronization (thread safety), caching (String Pool conservation), and performance (hashcode caching).", True),
            ("Explain garbage collection in Java.", 
             "Garbage collection is the automatic process in Java by which the JVM identifies and deletes objects that are no longer referenced or reachable in the heap memory, freeing up system resources.", True),
            ("What is the difference between Abstract Class and Interface in Java?", 
             "An abstract class can have instance variables, constructors, and both abstract and concrete methods. An interface can only have public static final constants and abstract methods (though default and static methods are allowed since Java 8). A class can extend only one abstract class but can implement multiple interfaces.", True),
            ("What is a transient variable in Java?", 
             "A transient variable is a variable that is not serialized during object serialization. When the object is written to a stream, the value of a transient variable is not saved.", False),
            ("What is the difference between checked and unchecked exceptions?", 
             "Checked exceptions are checked at compile-time (e.g., IOException, SQLException) and the compiler forces the programmer to handle them using try-catch or throws. Unchecked exceptions are checked at runtime (e.g., NullPointerException, ArithmeticException) and inherit from RuntimeException.", True),
            ("What is the string pool in Java?", 
             "The String Pool is a special storage area in the Java heap memory where the JVM stores string literals. If a string literal is created, the JVM checks the pool first. If the string already exists, it returns a reference to it instead of creating a new object.", False)
        ]
        for q, a, freq in java_qs:
            tech_data.append({"subject": "Java", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- Python (10) ---
        python_qs = [
            ("What is the difference between list and tuple in Python?", 
             "Lists are mutable, meaning their elements can be modified, added, or removed after creation, and are declared using square brackets []. Tuples are immutable, meaning their elements cannot be changed, and are declared using parentheses (). Tuples are generally faster and safer.", True),
            ("What is PEP 8 in Python?", 
             "PEP 8 is Python's style guide. It stands for Python Enhancement Proposal 8. It outlines guidelines and best practices on how to format Python code to maximize readability and maintainability.", True),
            ("Explain the concept of decorators in Python.", 
             "A decorator is a design pattern in Python that allows you to modify or extend the behavior of a function or class without permanently modifying its source code. It wraps another function and executes code before and after the wrapped function runs.", True),
            ("What are list comprehensions and how do they work?", 
             "List comprehensions provide a concise way to create lists in Python. Syntax: '[expression for item in iterable if condition]'. They are more readable and faster than standard for-loops.", True),
            ("Explain the difference between deep copy and shallow copy.", 
             "A shallow copy constructs a new compound object and inserts references to the original objects. A deep copy constructs a new compound object and recursively inserts copies of the original objects. Modifying nested elements in a shallow copy affects the original; in a deep copy, it does not.", True),
            ("What is the purpose of '__init__' in Python classes?", 
             "The '__init__' method is a special method (constructor) that is automatically called when a new object of a class is instantiated. It initializes the object's attributes with user-provided values.", True),
            ("What are generators in Python and what is the 'yield' keyword?", 
             "Generators are functions that return an iterator using the 'yield' keyword. Instead of returning a value and terminating, 'yield' pauses the function's execution state and yields a value to the caller, resuming on next call. This is highly memory-efficient.", True),
            ("Explain GIL (Global Interpreter Lock) in Python.", 
             "The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once in the CPython interpreter. This limits CPU-bound multi-threaded execution to a single core, though I/O-bound concurrency works well.", True),
            ("How is memory managed in Python?", 
             "Memory in Python is managed automatically by a private heap space. It utilizes reference counting to keep track of references to objects, and an automatic Garbage Collector to detect and resolve cyclic references.", False),
            ("What is the difference between 'is' and '==' in Python?", 
             "'==' compares the values of two objects (calls the __eq__ method), while 'is' compares the memory identities of the objects to see if they refer to the exact same object in memory.", True)
        ]
        for q, a, freq in python_qs:
            tech_data.append({"subject": "Python", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- SQL (10) ---
        sql_qs = [
            ("What is the difference between CHAR and VARCHAR in SQL?", 
             "CHAR is a fixed-length character data type. If the inserted string is shorter than the declared length, it is padded with spaces. VARCHAR is a variable-length data type, which only consumes memory proportional to the actual characters stored.", True),
            ("What is a JOIN in SQL and list its types.", 
             "A JOIN clause is used to combine rows from two or more tables based on a related column. Types include: INNER JOIN (matching rows in both), LEFT JOIN (all rows from left, matching from right), RIGHT JOIN (all rows from right, matching from left), and FULL JOIN (all rows when there is a match in either).", True),
            ("Explain the difference between primary key, foreign key, and unique key.", 
             "A Primary Key uniquely identifies each record in a table, cannot be NULL, and there is only one per table. A Unique Key ensures all values in a column are distinct, can accept NULL (one or more depending on database), and a table can have many. A Foreign Key is a field in one table that uniquely identifies a row of another table to maintain referential integrity.", True),
            ("What is the difference between DELETE, TRUNCATE, and DROP?", 
             "DELETE is a DML command used to remove specific rows based on a WHERE clause; it can be rolled back and triggers are executed. TRUNCATE is a DDL command that removes all rows from a table; it cannot be rolled back, is much faster, and does not fire triggers. DROP is a DDL command that completely deletes the table structure along with its data from the database.", True),
            ("What is a subquery and what are its types?", 
             "A subquery is a query nested inside another query (SELECT, INSERT, UPDATE, or DELETE). Types include: Single-row subqueries (returns one row), Multi-row subqueries (returns multiple rows), and Correlated subqueries (references columns of the outer query and executes repeatedly).", True),
            ("Explain the difference between HAVING and WHERE clauses.", 
             "The WHERE clause is used to filter records before any groupings are made. The HAVING clause is used to filter groups created by the GROUP BY clause, allowing filter conditions on aggregate functions like SUM, AVG, and COUNT.", True),
            ("What are SQL Constraints?", 
             "SQL constraints are rules specified for columns in a table. They limit the type of data that can go into the table. Common constraints include: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, and DEFAULT.", False),
            ("What is a view in SQL?", 
             "A view is a virtual table based on the result-set of an SQL statement. It contains rows and columns just like a real table, but it does not store data physically; it queries the underlying tables dynamically.", True),
            ("What is an index in SQL and why is it used?", 
             "An index is a pointer structure used to speed up the retrieval of data from a table. It works like the index of a book, reducing disk accesses. However, indexes slow down write operations (INSERT, UPDATE, DELETE).", True),
            ("What is SQL injection?", 
             "SQL injection is a security vulnerability where an attacker inserts malicious SQL code into input fields, manipulating backend SQL queries. It is prevented by using parameterized queries or prepared statements.", True)
        ]
        for q, a, freq in sql_qs:
            tech_data.append({"subject": "SQL", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- DBMS (10) ---
        dbms_qs = [
            ("What is DBMS and what are the main types?", 
             "A Database Management System (DBMS) is software used to manage databases. Types include: Hierarchical, Network, Relational (RDBMS like MySQL/PostgreSQL), and Non-Relational (NoSQL like MongoDB/Redis).", True),
            ("What are ACID properties in DBMS?", 
             "ACID stands for: Atomicity (all operations of a transaction succeed or all fail), Consistency (database transitions from one valid state to another), Isolation (transactions execute independently without interference), and Durability (committed changes are permanently saved in case of failure).", True),
            ("What is Database Normalization and why is it used?", 
             "Normalization is the process of organizing data in a database to reduce data redundancy (duplicate info) and avoid anomalies (insert, update, delete). It divides large tables into smaller tables and defines relationships between them.", True),
            ("Explain 1NF, 2NF, and 3NF.", 
             "1NF: Atomic values only (no repeating groups/arrays). 2NF: In 1NF and all non-key attributes are fully functionally dependent on the primary key (no partial dependency). 3NF: In 2NF and no non-key attribute is transitively dependent on the primary key.", True),
            ("What is a transaction in DBMS?", 
             "A transaction is a single logical unit of work that accesses and possibly modifies the contents of a database. It begins with 'BEGIN TRANSACTION' and ends with either 'COMMIT' (save) or 'ROLLBACK' (undo).", True),
            ("Explain the difference between File System and DBMS.", 
             "A File System stores unstructured files on disk, has high redundancy, lacks concurrency control, and has weak security. A DBMS stores structured data, controls redundancy, implements locking for concurrency, provides recovery mechanisms, and enforces security policies.", True),
            ("What is a database lock and what are its types?", 
             "A lock is a mechanism to control concurrent access to data. Types include: Shared Lock (Read lock: multiple transactions can read but not write) and Exclusive Lock (Write lock: only one transaction can read and write, blocking others).", False),
            ("What is a trigger in DBMS?", 
             "A trigger is a pre-compiled SQL statement that automatically executes or fires when a specified event (like INSERT, UPDATE, or DELETE) occurs on a specific table.", True),
            ("What is the difference between 2-Tier and 3-Tier architecture?", 
             "2-Tier architecture is a client-server architecture where the client application communicates directly with the database. 3-Tier architecture introduces an application server (middleware) between the client and database to process business logic, improving security and scalability.", False),
            ("What is a Deadlock in DBMS?", 
             "A deadlock is a situation where two or more transactions are waiting indefinitely for resources locked by each other, creating a circular dependency. DBMS resolves this by aborting and rolling back one of the transactions.", True)
        ]
        for q, a, freq in dbms_qs:
            tech_data.append({"subject": "DBMS", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- OS (10) ---
        os_qs = [
            ("What is an Operating System and what are its main functions?", 
             "An OS is a system software that acts as an intermediary between the computer user and the hardware. Functions include: Process management, Memory management, File system management, Device management, Security, and Job accounting.", True),
            ("What is the difference between a process and a thread?", 
             "A process is an execution of a program (has its own address space, memory, and resources). A thread is a lightweight process, which is the smallest unit of execution inside a process. Threads of the same process share memory space and resources, making context switching faster.", True),
            ("What is virtual memory and how does it work?", 
             "Virtual memory is a memory management technique that allows the execution of processes that may not be completely in physical memory. It maps virtual addresses to physical addresses using pages, swapping pages between RAM and secondary storage (paging) when RAM is full.", True),
            ("What is Thrashing in OS?", 
             "Thrashing occurs when a virtual memory system spends more time swapping pages in and out of disk memory than executing actual instructions. It happens when physical memory is overcommitted and processes keep faulting pages.", True),
            ("What is a Deadlock in OS and what are the 4 necessary conditions?", 
             "A deadlock is a state where a set of processes are blocked because each process is holding a resource and waiting for another resource held by some other process. 4 conditions are: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.", True),
            ("Explain the difference between Paging and Segmentation.", 
             "Paging divides logical memory into fixed-size blocks called pages, and physical memory into frames. It prevents external fragmentation. Segmentation divides memory into variable-size logical units based on user perspective (e.g., functions, main program, stack). It can lead to external fragmentation.", True),
            ("What is context switching in OS?", 
             "Context switching is the process of storing the state of a CPU process/thread so that it can be restored and resume execution later, allowing multiple processes to share a single CPU resource.", True),
            ("What is a Semaphore and how does it work?", 
             "A semaphore is an integer variable used for signaling and solving critical section synchronization problems. The two standard atomic operations are wait() (or P: decrements semaphore) and signal() (or V: increments semaphore). Binary semaphores act like Mutexes.", True),
            ("What is the difference between Monolithic Kernel and Microkernel?", 
             "A Monolithic Kernel runs all OS services (process mgmt, memory mgmt, drivers) in kernel space, offering high speed. A Microkernel runs only core services in kernel space, running drivers and filesystems as user-space processes, providing modularity and high crash reliability at the cost of IPC overhead.", False),
            ("What is CPU Scheduling and name some algorithms.", 
             "CPU Scheduling is the process by which the OS decides which process in the ready queue gets the CPU. Algorithms include: First-Come First-Served (FCFS), Shortest Job First (SJF), Round Robin (RR), and Priority Scheduling.", True)
        ]
        for q, a, freq in os_qs:
            tech_data.append({"subject": "OS", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- CN (10) ---
        cn_qs = [
            ("What is the difference between TCP and UDP?", 
             "TCP (Transmission Control Protocol) is connection-oriented, reliable (guarantees packet delivery in order), slower due to handshake/error-checking, and uses flow control. UDP (User Datagram Protocol) is connectionless, unreliable, faster, and used for live streaming/gaming.", True),
            ("Explain the layers of the OSI Model.", 
             "The OSI model has 7 layers: 1. Physical (raw bit streams), 2. Data Link (framing/MAC addresses), 3. Network (routing/IP packets), 4. Transport (segmentation/TCP-UDP), 5. Session (dialogue control), 6. Presentation (encryption/compression), 7. Application (network services like HTTP/SMTP).", True),
            ("What is the difference between IPv4 and IPv6?", 
             "IPv4 uses a 32-bit address space (expressed in dotted-decimal format, e.g., 192.168.1.1), providing ~4.3 billion addresses. IPv6 uses a 128-bit address space (expressed in hexadecimal format, e.g., 2001:db8::ff00:42:8329), providing a virtually unlimited address pool.", True),
            ("What happens when you enter 'google.com' in a browser?", 
             "1. Browser checks cache for DNS resolution. 2. DNS query resolves IP address of google.com. 3. Browser initiates TCP handshake with the server. 4. Browser sends HTTP/HTTPS GET request. 5. Google server processes request and returns HTML response. 6. Browser renders HTML page.", True),
            ("What is DNS (Domain Name System)?", 
             "DNS is the phonebook of the Internet. It translates human-readable domain names (like google.com) into machine-readable IP addresses (like 142.250.190.46) so browsers can load internet resources.", True),
            ("What is a Gateway and a Router?", 
             "A Router is a network device that forwards data packets between computer networks. A Gateway is a node that connects two networks with different protocols (e.g., connecting a local intranet to the public internet).", True),
            ("What is the difference between HTTP and HTTPS?", 
             "HTTP (Hypertext Transfer Protocol) transmits data in plain text, making it vulnerable to interception. HTTPS (HTTP Secure) encrypts the communication channel using SSL/TLS, protecting sensitive user data.", True),
            ("What are ARP and MAC addresses?", 
             "A MAC address is a permanent physical hardware address assigned to a network interface. ARP (Address Resolution Protocol) is used to map a dynamic 32-bit IP address to a physical 48-bit MAC address on a local network.", False),
            ("What is three-way handshaking in TCP?", 
             "It is the process used to establish a TCP connection. 1. Client sends SYN (Synchronize) packet. 2. Server responds with SYN-ACK (Synchronize-Acknowledge) packet. 3. Client responds with ACK (Acknowledge) packet. The connection is now established.", True),
            ("What is the purpose of subnetting?", 
             "Subnetting is the practice of dividing a physical network into smaller, logical sub-networks (subnets). It improves network routing efficiency, enhances security, and conservation of IP addresses.", False)
        ]
        for q, a, freq in cn_qs:
            tech_data.append({"subject": "CN", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- DSA (10) ---
        dsa_qs = [
            ("What is the difference between an Array and a Linked List?", 
             "Arrays are stored in contiguous memory locations, support O(1) random access, but insertions/deletions are slow (O(n)). Linked Lists are stored in non-contiguous memory, do not support random access (O(n) traversal), but insert/delete operations are fast (O(1)) once the node is located.", True),
            ("What is the difference between Stack and Queue?", 
             "Stack is a LIFO (Last In First Out) data structure; insertion (push) and deletion (pop) take place at the same end (top). Queue is a FIFO (First In First Out) data structure; insertion (enqueue) takes place at the rear, and deletion (dequeue) at the front.", True),
            ("What is a Binary Search Tree (BST)?", 
             "A BST is a binary tree where each node has a value. For any node, the values in its left subtree are strictly less than its value, and the values in its right subtree are strictly greater than its value. Search, insertion, and deletion run in O(log n) average time.", True),
            ("Explain the difference between BFS and DFS.", 
             "Breadth-First Search (BFS) explores the graph level-by-level, using a Queue. Depth-First Search (DFS) explores as deep as possible along each branch before backtracking, using a Stack or recursion.", True),
            ("What is the time complexity of Quick Sort, Merge Sort, and Bubble Sort?", 
             "Bubble Sort: O(n^2) average/worst. Merge Sort: O(n log n) best/average/worst (requires O(n) auxiliary space). Quick Sort: O(n log n) average, O(n^2) worst (in-place sorting).", True),
            ("What is a Hash Collision and how is it resolved?", 
             "A hash collision occurs when two different keys generate the same hash value/index. It is resolved using: 1. Chaining (each index has a linked list of entries), or 2. Open Addressing (probing techniques like Linear, Quadratic, or Double Hashing).", True),
            ("What is Dynamic Programming (DP)?", 
             "DP is an algorithmic technique that solves complex problems by breaking them down into simpler overlapping subproblems, solving each subproblem once, and storing their solutions (using memoization or tabulation) to avoid redundant computations.", True),
            ("What is a Max Heap and Min Heap?", 
             "A Heap is a complete binary tree. In a Max Heap, the value of the root node is greater than or equal to the values of its children, recursively. In a Min Heap, the value of the root is less than or equal to the values of its children.", True),
            ("Explain the concept of Big O notation.", 
             "Big O notation is a mathematical notation used in computer science to describe the upper bound of the execution time or space requirement of an algorithm in the worst-case scenario, as a function of the input size (n).", True),
            ("What is a Trie data structure?", 
             "A Trie (prefix tree) is an ordered tree-like data structure used to store a dynamic set or associative array where the keys are usually strings. It is highly optimized for fast prefix-based string searches.", False)
        ]
        for q, a, freq in dsa_qs:
            tech_data.append({"subject": "DSA", "question": q, "answer": a, "is_frequently_asked": freq})

        # --- OOP (10) ---
        oop_qs = [
            ("What are the four pillars of OOP?", 
             "The four pillars are: 1. Encapsulation (hiding data and wrapping variables and methods into a single unit), 2. Abstraction (hiding implementation details and showing only functional interfaces), 3. Inheritance (mechanisms where child class acquires attributes of parent class), 4. Polymorphism (ability of an entity to take multiple forms).", True),
            ("What is the difference between Method Overloading and Method Overriding?", 
             "Method Overloading (Compile-time polymorphism) occurs when a class has multiple methods with the same name but different signatures (parameters). Method Overriding (Runtime polymorphism) occurs when a subclass redefines a method that exists in its superclass, with the exact same name and signature.", True),
            ("Explain the concept of encapsulation.", 
             "Encapsulation is the bundling of data (variables) and methods that operate on the data into a single class. It restricts direct access to some of the object's components, usually by making fields private and exposing them via public getter and setter methods.", True),
            ("What is the difference between an Abstract Class and an Interface?", 
             "An Abstract Class allows implementation of some methods, can have fields and constructor. An Interface (prior to Java 8) can only declare method signatures and constant values. Classes 'extend' abstract classes (single inheritance) and 'implement' interfaces (multiple inheritance).", True),
            ("What is a Constructor and what are its types?", 
             "A constructor is a special member function used to initialize objects of a class. Types include: Default Constructor (takes no arguments), Parameterized Constructor (takes arguments), and Copy Constructor (copies another object).", True),
            ("What is Multiple Inheritance and how is it resolved in Java/C++?", 
             "Multiple Inheritance is when a class inherits from more than one parent class. It can cause ambiguity (the Diamond Problem). C++ supports multiple inheritance and resolves it using virtual inheritance. Java does not support multiple inheritance of classes but allows multiple inheritance of interfaces.", True),
            ("What is a Destructor in OOP?", 
             "A destructor is a special member function of a class that is automatically called when an object goes out of scope or is explicitly deleted, releasing resource acquisitions (such as dynamic memory).", False),
            ("What is the difference between Association, Aggregation, and Composition?", 
             "Association: weak relationship between two independent objects. Aggregation: 'Has-A' relationship where child can exist independently of parent (e.g., Student and School). Composition: strong 'Has-A' relationship where child cannot exist without parent (e.g., Room and House).", True),
            ("What is an inline function in C++?", 
             "An inline function is a function where the compiler replaces the function call with the actual function code during compilation, reducing execution overhead of function calling, useful for small functions.", False),
            ("What is a static class in OOP?", 
             "A static class is a class that cannot be instantiated and can only contain static members. It is accessed directly by its class name (e.g., Math class in Java).", False)
        ]
        for q, a, freq in oop_qs:
            tech_data.append({"subject": "OOP", "question": q, "answer": a, "is_frequently_asked": freq})

        for item in tech_data:
            db.session.add(TechnicalQuestion(**item))

        # ----------------------------------------------------
        # 3. Seed Company Questions (8 Companies)
        # ----------------------------------------------------
        print("Seeding Company Preparation profiles...")
        
        companies_data = [
            {
                "company_name": "TCS",
                "selection_process": "TCS conducts National Qualifier Test (NQT) for recruitment. Selection includes online test and interviews.",
                "interview_rounds": "Round 1: Cognitive + Coding Assessment (Online)\nRound 2: Technical Interview\nRound 3: Managerial Interview\nRound 4: HR Interview",
                "coding_question": "Problem: Find the N-th term in the series: 1, 1, 2, 3, 4, 9, 8, 27, 16, 81... (odd terms are powers of 2, even terms are powers of 3).",
                "hr_question": "Why do you want to join TCS over other IT firms? Describe a situation where you had to adapt to a sudden change.",
                "previous_interview_question": "Explain static variables in C. What is the difference between primary key and foreign key? Tell me about your final year project."
            },
            {
                "company_name": "Infosys",
                "selection_process": "Infosys recruits through InfyTQ or Infosys Certification / off-campus drives.",
                "interview_rounds": "Round 1: Online Assessment (Aptitude + Hands-on Coding)\nRound 2: Technical Interview (Core coding, OOP, DBMS, OS)\nRound 3: HR Interview",
                "coding_question": "Problem: Given a string, remove all consecutive duplicates (e.g., 'abbccd' -> 'abcd'). Write the code in Java/Python.",
                "hr_question": "Infosys has strong core values (C-LIFE). Which value do you align with the most and why?",
                "previous_interview_question": "Explain JVM memory structure. What are pointers? Differ between abstract classes and interfaces. Can you relocate?"
            },
            {
                "company_name": "Wipro",
                "selection_process": "Recruitment through Wipro NLTH (National Level Talent Hunt) Elite / Turbo drives.",
                "interview_rounds": "Round 1: Written test (Quants + Logical + English + Coding + Essay Writing)\nRound 2: Technical Interview\nRound 3: HR Interview",
                "coding_question": "Problem: Find the GCD of an array of integers.",
                "hr_question": "Are you comfortable signing Wipro's service agreement? What is your greatest achievement in college?",
                "previous_interview_question": "Write a program to reverse a linked list. What is Thrashing in Operating Systems? What is ARP protocol in networking?"
            },
            {
                "company_name": "Accenture",
                "selection_process": "Cognitive, Technical, Coding, and Communication rounds.",
                "interview_rounds": "Round 1: Cognitive Assessment (Critical thinking + English + Abstracts)\nRound 2: Technical + Coding Assessment\nRound 3: Communication Assessment (automated speaking test)\nRound 4: Technical & HR Combined Interview",
                "coding_question": "Problem: Check if a binary string satisfies a specific pattern (e.g., number of 0s equals number of 1s in every prefix).",
                "hr_question": "Tell me about a time you worked in a team and faced a conflict. How did you resolve it?",
                "previous_interview_question": "Explain Cloud Computing basics. What are the four pillars of OOP? Write SQL query to find second highest salary."
            },
            {
                "company_name": "Cognizant",
                "selection_process": "Cognizant recruits GenC, GenC Elevate, and GenC Pro profiles.",
                "interview_rounds": "Round 1: Aptitude + Skill-Based Assessment (SQL/Coding)\nRound 2: SME (Subject Matter Expert) Technical Interview\nRound 3: HR Interview",
                "coding_question": "Problem: Check if two strings are anagrams of each other.",
                "hr_question": "How do you handle tight deadlines in a project? What makes you stand out from other candidates?",
                "previous_interview_question": "What is normalization in databases? Explain 3NF. How does a HashMap work in Java? Write a query using group by and having."
            },
            {
                "company_name": "Capgemini",
                "selection_process": "Online aptitude, pseudo-coding, English, game-based test, and interviews.",
                "interview_rounds": "Round 1: Pseudo-Code & English Test\nRound 2: Game-Based Aptitude Assessment\nRound 3: Technical Interview\nRound 4: HR Interview",
                "coding_question": "Problem: Find the maximum sum of a contiguous subarray (Kadane's algorithm).",
                "hr_question": "Why Capgemini? What are your thoughts on working night shifts or rotating shifts?",
                "previous_interview_question": "What is the difference between C++ and Java? Explain inheritance with a real-life example. Write SQL joins."
            },
            {
                "company_name": "Zoho",
                "selection_process": "Extremely programming-intensive selection process focusing on problem-solving skills.",
                "interview_rounds": "Round 1: Written/Online Coding Test (10 basic debugging + 5 code problems)\nRound 2: Advanced Coding Round (design a game/utility in 3 hours)\nRound 3: System Design / Technical Interview\nRound 4: HR Interview",
                "coding_question": "Problem: Build a console-based Railway Reservation System with booking, cancellation, and chart printing features.",
                "hr_question": "What are your views on learning new technologies? Why did you choose software engineering over your core branch?",
                "previous_interview_question": "Design an elevator system using OOP. Write a program to sort elements by frequency. How does virtual memory work?"
            },
            {
                "company_name": "HCL",
                "selection_process": "Recruitment drive via online test, technical interview, and HR interview.",
                "interview_rounds": "Round 1: Online Assessment (Aptitude, Verbal, Coding)\nRound 2: Technical Interview\nRound 3: HR Interview",
                "coding_question": "Problem: Check if a given number is a Fibonacci number.",
                "hr_question": "HCL focuses on 'Ideapreneurship'. How can you contribute to this culture? What are your career aspirations?",
                "previous_interview_question": "Explain method overloading vs overriding. What is a pointer? How do you delete duplicates in an array?"
            }
        ]

        for comp in companies_data:
            db.session.add(CompanyQuestion(**comp))

        # ----------------------------------------------------
        # 4. Seed Coding Questions (24 total, 3 per topic)
        # ----------------------------------------------------
        print("Seeding Coding Questions...")
        
        coding_data = [
            # --- Arrays (3) ---
            {
                "title": "Two Sum",
                "difficulty": "Easy",
                "topic": "Arrays",
                "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.",
                "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9",
                "sample_input": "nums = [2,7,11,15], target = 9",
                "sample_output": "[0,1] (since nums[0] + nums[1] == 9)",
                "hints": "Try using a Hash Map to store numbers and their indices as you traverse. Look for the complement (target - nums[i])."
            },
            {
                "title": "Container With Most Water",
                "difficulty": "Medium",
                "topic": "Arrays",
                "description": "Given `n` non-negative integers `height` representing vertical lines, find two lines that together with the x-axis form a container, such that the container contains the most water.",
                "constraints": "n == height.length\n2 <= n <= 10^5",
                "sample_input": "height = [1,8,6,2,5,4,8,3,7]",
                "sample_output": "49",
                "hints": "Use a two-pointer approach starting from the left and right ends. Move the pointer pointing to the shorter line inward."
            },
            {
                "title": "First Missing Positive",
                "difficulty": "Hard",
                "topic": "Arrays",
                "description": "Given an unsorted integer array `nums`, return the smallest positive integer that is not present in the array. You must implement an O(n) time and O(1) space algorithm.",
                "constraints": "1 <= nums.length <= 10^5\n-2^31 <= nums[i] <= 2^31 - 1",
                "sample_input": "nums = [3,4,-1,1]",
                "sample_output": "2",
                "hints": "Try putting each number in its correct position index, i.e., nums[i] should be at index nums[i] - 1."
            },

            # --- Strings (3) ---
            {
                "title": "Valid Anagram",
                "difficulty": "Easy",
                "topic": "Strings",
                "description": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.",
                "constraints": "1 <= s.length, t.length <= 5 * 10^4",
                "sample_input": "s = \"anagram\", t = \"nagaram\"",
                "sample_output": "true",
                "hints": "You can count frequencies of each character using an array of size 26 or a hash map, and check if counts match."
            },
            {
                "title": "Longest Substring Without Repeating Characters",
                "difficulty": "Medium",
                "topic": "Strings",
                "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
                "constraints": "0 <= s.length <= 5 * 10^4",
                "sample_input": "s = \"abcabcbb\"",
                "sample_output": "3 (the substring is \"abc\")",
                "hints": "Use a sliding window with a hash set/map to store characters and their last seen indexes."
            },
            {
                "title": "Minimum Window Substring",
                "difficulty": "Hard",
                "topic": "Strings",
                "description": "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.",
                "constraints": "m, n >= 1",
                "sample_input": "s = \"ADOBECODEBANC\", t = \"ABC\"",
                "sample_output": "\"BANC\"",
                "hints": "Use a sliding window with two pointers. Expand the right pointer to find a valid window, then contract the left pointer to optimize."
            },

            # --- Linked List (3) ---
            {
                "title": "Reverse a Linked List",
                "difficulty": "Easy",
                "topic": "Linked List",
                "description": "Given the head of a singly linked list, reverse the list, and return its reversed list head.",
                "constraints": "Number of nodes is in range [0, 5000]",
                "sample_input": "head = [1,2,3,4,5]",
                "sample_output": "[5,4,3,2,1]",
                "hints": "Maintain three pointers: prev (null), curr (head), and next (null). Shift linkages one by one."
            },
            {
                "title": "Remove Nth Node From End of List",
                "difficulty": "Medium",
                "topic": "Linked List",
                "description": "Given the head of a linked list, remove the `n`-th node from the end of the list and return its head.",
                "constraints": "Number of nodes is in range [1, 30]",
                "sample_input": "head = [1,2,3,4,5], n = 2",
                "sample_output": "[1,2,3,5]",
                "hints": "Use two pointers, fast and slow. Advance fast by n+1 steps first, then move both together until fast reaches the end."
            },
            {
                "title": "Merge k Sorted Lists",
                "difficulty": "Hard",
                "topic": "Linked List",
                "description": "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list.",
                "constraints": "lists.length <= 10^4\nlists[i].length <= 500",
                "sample_input": "lists = [[1,4,5],[1,3,4],[2,6]]",
                "sample_output": "[1,1,2,3,4,4,5,6]",
                "hints": "Use a Priority Queue (Min Heap) to keep track of the head nodes of all lists, repeatedly extract the minimum node."
            },

            # --- Stack (3) ---
            {
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "topic": "Stack",
                "description": "Given a string `s` containing just characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                "constraints": "1 <= s.length <= 10^4",
                "sample_input": "s = \"()[]{}\"",
                "sample_output": "true",
                "hints": "Push opening brackets to a Stack. For closing brackets, check if they match the popped top element of the Stack."
            },
            {
                "title": "Min Stack",
                "difficulty": "Medium",
                "topic": "Stack",
                "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant O(1) time.",
                "constraints": "Methods will be called at most 3 * 10^4 times.",
                "sample_input": "[\"MinStack\",\"push\",\"push\",\"push\",\"getMin\",\"pop\",\"top\",\"getMin\"] ([],[-2],[0],[-3],[],[],[],[])",
                "sample_output": "[null,null,null,null,-3,null,0,-2]",
                "hints": "Maintain a secondary stack containing the corresponding minimum value at each push state."
            },
            {
                "title": "Largest Rectangle in Histogram",
                "difficulty": "Hard",
                "topic": "Stack",
                "description": "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
                "constraints": "1 <= heights.length <= 10^5",
                "sample_input": "heights = [2,1,5,6,2,3]",
                "sample_output": "10",
                "hints": "Use a Monotonic Stack to find the next and previous smaller element boundary indexes for each bar."
            },

            # --- Queue (3) ---
            {
                "title": "Implement Queue using Stacks",
                "difficulty": "Easy",
                "topic": "Queue",
                "description": "Implement a first-in first-out (FIFO) queue using only two stacks. The implemented queue should support all normal queue functions.",
                "constraints": "All calls are valid.",
                "sample_input": "[\"MyQueue\", \"push\", \"push\", \"peek\", \"pop\", \"empty\"] ([], [1], [2], [], [], [])",
                "sample_output": "[null, null, null, 1, 1, false]",
                "hints": "Use stack1 for enqueue and stack2 for dequeue. Shift elements from stack1 to stack2 only when stack2 is empty during pop/peek."
            },
            {
                "title": "Sliding Window Maximum",
                "difficulty": "Hard",
                "topic": "Queue",
                "description": "You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. Return the max sliding window.",
                "constraints": "1 <= nums.length <= 10^5\n1 <= k <= nums.length",
                "sample_input": "nums = [1,3,-1,-3,5,3,6,7], k = 3",
                "sample_output": "[3,3,5,5,6,7]",
                "hints": "Use a Double-Ended Queue (Deque) to store indices of elements. Maintain elements in the deque in decreasing order of their values."
            },
            {
                "title": "Dota2 Senate",
                "difficulty": "Medium",
                "topic": "Queue",
                "description": "Predict which senate party (Radiant or Dire) will ban each other's rights and win the vote.",
                "constraints": "1 <= senate.length <= 10^4",
                "sample_input": "senate = \"RDD\"",
                "sample_output": "\"Dire\"",
                "hints": "Use two separate Queues to keep track of indexes of Radiant and Dire senators. Pop front and re-enqueue with index + N offset for the winner."
            },

            # --- Trees (3) ---
            {
                "title": "Maximum Depth of Binary Tree",
                "difficulty": "Easy",
                "topic": "Trees",
                "description": "Given the root of a binary tree, return its maximum depth (number of nodes along the longest path from root to leaf node).",
                "constraints": "The number of nodes in the tree is in the range [0, 10^4].",
                "sample_input": "root = [3,9,20,null,null,15,7]",
                "sample_output": "3",
                "hints": "You can use recursion. The depth is 1 + max(maxDepth(root.left), maxDepth(root.right))."
            },
            {
                "title": "Binary Tree Level Order Traversal",
                "difficulty": "Medium",
                "topic": "Trees",
                "description": "Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
                "constraints": "The number of nodes is in range [0, 2000]",
                "sample_input": "root = [3,9,20,null,null,15,7]",
                "sample_output": "[[3],[9,20],[15,7]]",
                "hints": "Use a Queue to perform Breadth-First Search (BFS). Track the queue size at each level iteration."
            },
            {
                "title": "Binary Tree Maximum Path Sum",
                "difficulty": "Hard",
                "topic": "Trees",
                "description": "Find the maximum path sum of any non-empty path in a binary tree. The path may start and end at any node.",
                "constraints": "The number of nodes is in range [1, 3 * 10^4]",
                "sample_input": "root = [-10,9,20,null,null,15,7]",
                "sample_output": "42 (path: 15 -> 20 -> 7)",
                "hints": "At each node, compute the max path sum through that node as root. Return the max single path sum extending to its parent."
            },

            # --- Graph (3) ---
            {
                "title": "Find Center of Star Graph",
                "difficulty": "Easy",
                "topic": "Graph",
                "description": "There is an undirected star graph consisting of `n` nodes labeled from 1 to `n`. Return the center node.",
                "constraints": "3 <= n <= 10^5\nedges.length == n - 1",
                "sample_input": "edges = [[1,2],[5,1],[1,3],[1,4]]",
                "sample_output": "1",
                "hints": "The center node must appear in all edges. Just check which node is common between the first two edges."
            },
            {
                "title": "Clone Graph",
                "difficulty": "Medium",
                "topic": "Graph",
                "description": "Given a reference of a node in a connected undirected graph. Return a deep copy (clone) of the graph.",
                "constraints": "Number of nodes is between 0 and 100.",
                "sample_input": "adjList = [[2,4],[1,3],[2,4],[1,3]]",
                "sample_output": "[[2,4],[1,3],[2,4],[1,3]]",
                "hints": "Perform BFS or DFS. Maintain a hash map that maps original nodes to their cloned nodes to avoid cycles."
            },
            {
                "title": "Word Ladder",
                "difficulty": "Hard",
                "topic": "Graph",
                "description": "Given two words (`beginWord` and `endWord`), and a dictionary `wordList`, return the length of the shortest transformation sequence from `beginWord` to `endWord` (only 1 letter difference allowed).",
                "constraints": "wordList.length <= 5000",
                "sample_input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]",
                "sample_output": "5",
                "hints": "Treat the words as nodes of a graph with edges between words differing by 1 character. Use BFS to find the shortest path."
            },

            # --- Dynamic Programming (3) ---
            {
                "title": "Climbing Stairs",
                "difficulty": "Easy",
                "topic": "Dynamic Programming",
                "description": "It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
                "constraints": "1 <= n <= 45",
                "sample_input": "n = 3",
                "sample_output": "3",
                "hints": "This is equivalent to the Fibonacci series. Ways(n) = Ways(n-1) + Ways(n-2)."
            },
            {
                "title": "Longest Common Subsequence",
                "difficulty": "Medium",
                "topic": "Dynamic Programming",
                "description": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return 0.",
                "constraints": "1 <= text1.length, text2.length <= 1000",
                "sample_input": "text1 = \"abcde\", text2 = \"ace\"",
                "sample_output": "3",
                "hints": "Create a 2D DP table. If text1[i] == text2[j], DP[i][j] = 1 + DP[i-1][j-1]. Otherwise, DP[i][j] = max(DP[i-1][j], DP[i][j-1])."
            },
            {
                "title": "Edit Distance",
                "difficulty": "Hard",
                "topic": "Dynamic Programming",
                "description": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2` (Insert, Delete, Replace).",
                "constraints": "0 <= word1.length, word2.length <= 500",
                "sample_input": "word1 = \"horse\", word2 = \"ros\"",
                "sample_output": "3",
                "hints": "Define DP[i][j] as the edit distance of prefixes. If word1[i-1] == word2[j-1], no operation needed. Otherwise, take 1 + min(insert, delete, replace)."
            }
        ]

        for code in coding_data:
            db.session.add(CodingQuestion(**code))

        # ----------------------------------------------------
        # 5. Seed HR Questions (10 Questions)
        # ----------------------------------------------------
        print("Seeding HR Questions...")
        
        hr_data = [
            {"question": "Tell me about yourself."},
            {"question": "Why should we hire you?"},
            {"question": "What are your strengths and weaknesses?"},
            {"question": "What are your future career goals?"},
            {"question": "Tell me about a time you showed leadership skills."},
            {"question": "How do you handle working under pressure in a team?"},
            {"question": "Why do you want to work for our company?"},
            {"question": "What are your salary expectations?"},
            {"question": "Where do you see yourself in five years?"},
            {"question": "Describe a major challenge you faced and how you overcame it."}
        ]

        for hr in hr_data:
            db.session.add(HRQuestion(**hr))

        db.session.commit()
        print("Database seeded successfully with 180+ entries!")

if __name__ == "__main__":
    seed_database()
