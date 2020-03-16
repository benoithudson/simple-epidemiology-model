# simple-epidemiology-model

Flatten-the-curve is a simple model to explore the idea that the goal of social
distancing etc is to have the same overall case load in the end, but just
spread out over a longer period to avoid overloading health services.
This is a pretty common message during the COVID-19 epidemic.

Run it with for example:
```
python flatten-the-curve.py 2.3
```
to see what happens if R0 (the number of people you'd infect on average if
nobody around you had immunity to it) is at 2.3.

That's the only variable you easily control, to model the main tool public
health authorities have, which is ordering social distancing measures and
quarantines, and establishing a cordon sanitaire. All actions that reduce R0.

## The upshot

What the model indicates is that you can't avoid going into health system
overload unless you manage to get R0 to be below 1.02.

If you get R0 below 1, you've achieved containment. So in other words, for a
disease like COVID-19, ***a successful "flatten the curve" effort is basically
the same as containment.***

## The model

Obviously, this is a very simplified model on account of I'm not an actual
epidemiologist and I only spent an hour developing this thing.

The model includes:
- There's one daily visitor with the disease. That's the only source of new infections.
- It takes exactly 5 days to become infectious. (COVID-19 generally takes 3 to 10 days)
- On that day, and never again, the patient spreads disease to R0 others. Any
    of them who isn't immune is now at day 0 of their illness.
- The disease takes exactly 28 days to clear for a patient who lives, or
    exactly 14 days to death for a patient who dies. (These are drawn from
    memory of reading papers about Hubei province.)
- People who've had the disease are immune to it (or dead), so the effective R0
    falls over time as herd immunity builds up.
- Nobody ever changes their behaviour, so R0 always stays the same (obviously, not the case!)
- The case fatality rate is low if the case load is low.
- If the case load is high, the case fatality rate is instantly high. We want to avoid this.
- Case load being high means 0.1% of the population actively sick. That's about when Italy
    and Hubei each started having their hospitals be overwhelmed.

## Extensions

To get to a better model you'd want to use a network model. Here I'm assuming
everyone is equally likely to bump into everyone else, but real life has
super-spreaders versus people who can't even infect anyone with the measles.

It would also have a model of who's at home, who's in a hospital bed, who's on
a ventilator. It wouldn't assume that the instant you run out of ventilators,
nobody gets a ventilator anymore. It would have people spreading throughout
their illness. It would model that restrictions get added bit by bit. Etc.
