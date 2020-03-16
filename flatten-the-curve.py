#! /usr/bin/python
import sys

## assumptions

# Imported cases daily.
num_imported = 1

# Average infectiousness assuming an average person with all naive contacts and
# no reactive measures.
R0 = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5

# Time (days) from getting infected until you can infect someone else.
# That day you'll attack R0 people, and never again.
serial_time = 5

# Time (days) from getting infected until release from hospital.
recovery_time = 28

# Patients who die, die this many days after infection.
death_day = 14

# Maximum fraction of population that can afford to be simultaneously sick.
capacity = 0.001

# Case fatality rate below that fraction.
cfr_below_capacity = 0.009

# Case fatality rate above that fraction.
cfr_above_capacity = 0.05

# Model:
#   - number naive
#   - number infected but not yet infectious
# Each day:
#       shift the buckets of infected people
#       people infected exactly `serial_time` days attack R0 people among the
#               total population, who might be new infections or existing ones.
#       those newly infected are added to the head of the array.
total_pop = int(10e6)

num_infected = [ 0 for _ in range(recovery_time) ]
num_recovered = 0
num_dead = 0
deaths_today = 0

def total_infected():
    return sum(num_infected) + num_recovered + num_dead

def fraction_naive():
    return 1 - total_infected() / total_pop

def fraction_active():
    return sum(num_infected) / total_pop

def step():
    global num_infected
    global num_recovered
    global num_dead
    global deaths_today
    global total_pop
    total_pop += num_imported
    new_infections = int(round(num_infected[serial_time] * R0 * fraction_naive() + num_imported))
    new_infections = min(new_infections, total_pop - sum(num_infected) - num_recovered)
    num_infected = [ num_infected[i - 1] if i != 0 else new_infections for i in range(recovery_time) ]
    num_recovered += num_infected.pop()

    if fraction_active() > capacity:
        deaths_today = int(round(cfr_above_capacity * num_infected[death_day]))
    else:
        deaths_today = int(round(cfr_below_capacity * num_infected[death_day]))

    num_dead += deaths_today
    num_infected[death_day] -= deaths_today


def header():
    print("{:3s} {:8s} {:8s} {:8s} {:8s} {:s}%".format(
                "day", "cases", "new", "deaths", "new", "treatment"
                ))

def log(day):
    print("{:3d} {:8d} {:8d} {:8d} {:8d} {:.4f}%".format(
                day,
                sum(num_infected) + num_recovered,
                num_infected[0],
                num_dead,
                deaths_today,
                100 * fraction_active()
                ))
    
def iterate_to_time(numsteps):
    numdead = 0

    header()
    for i in range (numsteps):
        step()
        log(i)

def iterate_to_crash():
    header()
    i = 0
    yesterday = 0
    while fraction_active() >= yesterday:
        yesterday = fraction_active()
        i = i + 1
        step()
        log(i)
        if fraction_active() > capacity:
            print("Health system crash with R0 = {}".format(R0))
            return
    print("Peak infected reached at {} days with R0 = {}".format(i, R0))

if __name__ == '__main__':
    # iterate_to_time(800)
    iterate_to_crash()
