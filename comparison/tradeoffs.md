# Cross-framework observations

Measured with gpt-4.1-mini through direct OpenAI, using the same task, tools,
and a fresh workspace per run. These are one observed run per framework,
not statistically general rankings. See results.json and artifacts/.

## 1. Control flow
LangGraph makes the agent/tool transitions and step guard explicit. It used
4 model calls in the comparison. AutoGen expressed the task as a conversation
between an assistant and a noninteractive tool proxy, using 6 calls. CrewAI
used a role, task, and crew configuration and completed in 3 calls.

## 2. Tool integration
LangGraph bound the supplied schemas directly. AutoGen required separate
registration for model selection and proxy execution. Its custom tracking
client had to be registered after the tools because tool registration rebuilt
the client. CrewAI required decorated wrappers with clear docstrings.

## 3. Token usage
LangGraph used 2,642 prompt + 427 completion = 3,069 tokens. AutoGen used
4,559 + 523 = 5,082. CrewAI used 2,049 + 850 = 2,899. In this run AutoGen had
the highest total and CrewAI the lowest. All figures come from actual API
response usage; counters record each response, not a single aggregate step.

## 4. Debugging and reliability
The supplied write tools target a temporary workspace, but execution originally
ran in the repository directory. The first LangGraph attempt needed 13 calls.
Giving every framework a fresh workspace and executing from that directory
removed the mismatch; the recorded comparison used 4 LangGraph calls.
An AutoGen-only model_client_cls field also had to be removed before forwarding
a request to OpenAI. These were integration failures, not model quality claims.

## 5. Latency and overhead
Observed elapsed times were 5.42 seconds for LangGraph, 9.98 for AutoGen, and
16.07 for CrewAI. CrewAI used fewer calls but took longer in this single run.
Network timing and initialization affect this metric. Repeat trials would be
necessary before making a performance recommendation.

## 6. Framework choice
For this small coder, I would choose LangGraph because state, routing, and
termination are directly inspectable. AutoGen is useful when conversations
between multiple roles are central. CrewAI is convenient for role/task-oriented
workflows, but its abstractions and version changes require integration checks.
All three completed the same task; the choice depends on control and workflow
needs, not this one token table alone.
