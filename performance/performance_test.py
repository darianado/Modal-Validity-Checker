import time
import tracemalloc
import random
from parse import Parser
from tableau_procedure import check_validity_of
import csv

def get_long_formula(times):
    unary={"!","◻","◇"}
    binary={"^","|","→"}
    s={"p","q","r"}
    longest = ""
    while times>0:
        arity = random.randint(1, 2)
        arity = random.choices([1,2],weights=[1,1])[0]
        if arity==1:
            conective= random.choice(list(unary))
            new=conective+random.choice(list(s))
            s.add(new)
        elif arity==2:
            conective= random.choice(list(binary))
            new="("+random.choice(list(s))+conective+random.choice(list(s))+")"
            s.add(new)
        if len(new) > len(longest):
            longest = new
        times=times -1
    return longest

# Generate 10 formulas of varying complexity for each number
formulas = []
for num in [10, 100, 500, 1000, 5000, 10000]:
    for _ in range(5):
        formula = get_long_formula(num)
        formulas.append(formula)

# Measure execution time and memory usage for each formula
for formula in formulas:
    parser= Parser()
    pf = parser.parse_text(formula)

    # Start the timer
    start_time = time.time()

    # Start tracking memory usage
    tracemalloc.start()

    # Evaluate the formula
    check_validity_of(pf)

    # Stop tracking memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Calculate execution time and memory usage
    elapsed_time = time.time() - start_time
    memory_used = peak / 10**6  # Convert from bytes to megabytes
    
    # Print results in cvs
    with open('results.cvs', 'a',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([f"{len(formula)} characters",f"{elapsed_time:.6f} seconds",f"{memory_used:.6f} MB"])
   