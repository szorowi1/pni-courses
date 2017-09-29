# Chapter 1: The Reinforcement Learning Problem
## 1.1: Reinforcement Learning
Reinforcement learning problems involve learning what to do (i.e. how to map situations to actions) so as to maximize a numerical reward signal. Essential to this framework is the interaction of a goal-directed agent with an uncertain environment. Maximazation of this reward signal is what separates reinforcement learning from other types of learning (e.g. unsupervised learning as a means to discover latent structure).

Three characteristics of reinforcement learning problems:
1. **Closed-loop:** the ouputs of learning (i.e. action) influence later inputs
2. **Discovery:** the learning agent must discover the highest-reward actions through sampling
3. **Future impact:** present actions impact the next-experienced situation and all future rewards

An agent capable of reinforcement learning must, at the minimum, possess the following three characteristics:
1. **Sensation:** a learning agent must be able to sense (i.e. experience) the world
2. **Action:** a learning agent must be able to impact/influence the world through action
3. **Goal:** a learning agent must have some goal with respect to the environment

## 1.2: Examples
The following are some general themes and topics relevant to and explored within the reinforcement learning framework:
* Exploration & exploitation 
* Planning & immediate, intuitive action
* Adaptation & optimization
* Trial & error
* Model-free vs. model-based

## 1.3: Elements of Reinforcement Learning
Beyond the agent and the environment, four important subelements of a reinforcement learning system are:
1. **Policy:** an agent's mode of behavior at a given time, or a mapping from perceived states of the environment to corresponding actions.
    * Analogous to *stimulus-response rules*
    * The core of an RL agent insofar that policies are sufficient to determine behavior
2. **Reward signal:** a scalar value, reward, returned to the agent from the environment at each time step
    * Maximization of the reward signal is the ultimate goal of an RL agent, it is the ultimate driver of changing *policies*
    * The process that generates the reward signal must be unalterable by the agent
3. **Value:** total amount of reward an agent can expect to accumulate over the future; indicates the long-term desirability of *states* after taking into account the states that are likely to follow, and the rewards available in those states
    * **Value function:** specifies the reward in the long run
    * Whereas rewards are immediate (e.g. pleasure/pain), values correspond to long-term predictions of reward; in this regard, rewards are primary whereas values are secondary
    * RL agents seek actions that bring about states of highest value, not highest reward, because the seactions obtain the greatest amount of reward over the long run
    * Importantly, values are substantially harder to estimate than rewards insofar that rewards are directly provided by the environment but values must be estimated and re-estimated with additional experience
4. **Model of the environment:** enables inferences to be made about how the environment will behavior
    * For a given state and action, an environmental model might predict the subsequent state and reward
    * **Planning:** a way of deciding on a course of action by considering possible future situations before they are actually experienced
