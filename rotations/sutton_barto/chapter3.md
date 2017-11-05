# Chapter 3: Finite Markov Decision Processes
## 3.1: The Agent-Environment Interface 
The **reinforcement learning framework** describes the problem of learning from interaction in pursuit of some goal. Broadly, it requires 3 components:
1. **Agent:** the learner and decision-maker
2. **Environment:** the surroundings of the agent, what it interacts with, containing rewards
3. **Task:** the complete specification of an environment, including how rewards are determined

A reinforcement learning problem is segmented into discrete time steps, *t = 0, 1, 2, 3, ...*, where each step is associated with some environmental **state** (of a set of possible states, *S*) and a corresponding **action** (of a set of possible actions, *A*,  available in a given state, *S*). In a subsequent step, the agent receives a numerical **reward** (*R*) and enters a new state. Each step is associated with a **policy** which maps states to probabilities of selecting particular actions, *p(a|s)*. In brief, reinforcement learning methods specify how an agent changes its policy as a result of experience in order to maximize the total amount of reward it receives over the long run. 

It should be noted that the reinforcement learning framework is a considerable abstraction of decision-making and learning. It proposes that all of the pertinent details to a goal-directed agent can be reduced down to three signals: actions (choices made by the agent), states (basis on which choices are made), and rewards (the goal). 

## 3.2: Goals and Rewards
The explicit aim of a reinforcement learning problem, i.e. its goal, is the maximzation of the expected value of the cumulative sum of a received scalar signal (reward). The reward signal connotes *what* an agent is to achieve, but does not specify *how*.

## 3.3: Returns
The aim of reinforcement learning is to maximize the **expected return**, *G*, where G is defined as some specific function of the reward sequence. For example,

> G = R(1) + R(2) + R(3) + ... + R(t)

where *t* is a final time step of a series of agent-environment interactions (**episodes**). Each episode begins with a *starting state* and ends with a *terminal state*. Any task that can be described by a series of episodes is said to be *episodic*. In contrast, *continuing tasks* cannot be broken naturally into identifiable episodes, but instead go on continually without limit. 

**Discounting** is an important feature in calculating expected returns in that it weighs more heavily more immediate rewards over future rewards. 

## 3.4: Unified Notation for Episodic and Continuing Tasks
**Absorbing state:** occurring at an episode termination, a special state that transitions only to itself and generates only rewards of zero. 

## 3.5: The Markov Property
Up until now, a *state* has remained ill-defined. Formally, a state is comprised of whatever information is available to an agent (regardless of how it is constructed, modified, or learned). State representations may include immediate sensory information, or complex structures of accumulated sense information. Importantly, the available information of a state may not represent all possible information pertinent to a decision. Often there is **hidden state information** in the environment. 

Ideally, a state signal should succinctly summarize past sensations. The **Markov property** describes state signals that retain all *relevant* information. Note that relevant information may not include all past sequences of events. For example, the current positions of pieces on a chess board have the Markov property without needing the past history of moves that resulted in such a configuration. 

If a state signal has the Markov property, then the consequence of an action (i.e. the environment's response) at time *t+1* is dependent only on the state and action representations at time *t*. If a state maintains the Markov property, then the environment and task as a whole are said to also obey the Markov property. If an environment has the Markov property, it can be shown that one can predict all future states and expected rewards from knowledge only of the current state as well as would be possible given the complete history up to the current time. As a corollary, the best policy for choosing action as a function of a Markov state is just as good as the best policy for choosing actions as a function of complete histories. 

## 3.6: Markov Decision Process
A **Markov decision process (MDP)** is a reinforcement learning task that satisfies the Markov property. If the time increments are finite, then the task is a *finite MDP*. A particular finite MDP is specified by its state and action sets and by the one-step dynamics of the environment. 

## 3.7: Value Functions
Reinforcement learning problems typically involve estimating **value functions**, such as how good it is to be in a particular state or how good it is to perform a given action in a particular state. Note this distinction: separate value functions can be calculated for state (*state-value function for policy*, v) and action (*action-value function for policy*, q). Such functions can be calculated from experience. *Monte Carlo* methods describe estimation methods involving averaging over many random samples of actual returns. 

Importantly, the **Bellman equation** describes teh relationship between the value of a state and the values of its successor states. The equation averages over all the possibilities, weighting each by its probability of occurring. It states that the value of the start state must equal the (discounted) value of the next state, plus the reward expected along the way. 

## 3.8 Optimal Value Functions
Value functions define a partial ordering over policies: a policy is better than or equal to another if its expected return is greater than or equal to that of a second policy for all states. An optimal policy is one that is better than or equal to all other policies. The **Bellman optimality equation** expresses the fact that the value of a state udner an optimal policy must equal the expected return for the best action from that state.

## 3.9: Optimality and Approximation
It should be noted that optimality is rare in practice. Optimality is typically computationally constant, requiring a large amount of memory. Fortunately, the online nature of reinforcement learning makes it possible to approximate optimal policies in ways that put more effort into learning to make good decisions for frequently encountered states, at the expense of less effort for infrequently encountered states. 
