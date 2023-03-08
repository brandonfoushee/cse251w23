![](../../banner.png)

# 10 Prove: Dining philosophers

## Overview

### Problem Statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can only eat spaghetti when they have both left and right forks. Each fork can be held by only one philosopher and so a philosopher can use the fork only if it is not being used by another philosopher. After an individual philosopher finishes eating, they need to put down both forks so that the forks become available to others. A philosopher can only take the fork on their right or the one on their left as they become available and they cannot start eating before getting both forks.

In order to pick up a fork, a philosopher must ask the waiter. The waiter controls the forks and tells the philosopher if they can eat.

Eating is not limited by the remaining amounts of spaghetti or stomach space; an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm) such that no philosopher will starve; i.e., each can forever continue to alternate between eating and thinking, assuming that no philosopher can know when others may want to eat or think.

![](dining_philosophers_problem.png)

## Assignment

You will be implementing this above problem statement.  Refer to the header of the Python file for requirements for this assignment.

The file used for this assignment is [assignment10.py](assignment10.py)

## Rubric

Item | Proficient | Emerging | Beginning | Missing
--- | --- | --- | --- | ---
Runs without errors | 20 | 0 | 0 | 0
[Style](../../style.md) | 15 | 10 | 5 | 0
Program not hard coded to 5 philosophers | 10 | 0 | 0 | 0
Waiter class used to control forks | 15 | 0 | 0 | 0
Program is concurrent (philosophers take turns) | 30 | 20 | 10 | 0
Program provides evidence that philosophers eat and think approx. same number of times | 10 | 7 | 3 | 0

Assignments are not accepted late. Instead, you should submit what you have completed by the due date for partial credit. 

Assignments are individual and not team based.  Any assignments found to be  plagiarized will be graded according to the `ACADEMIC HONESTY` section in the syllabus. The Assignment will be graded in broad categories as outlined in the syllabus.

## Submission

Submit your assignment Python file in Canvas.
