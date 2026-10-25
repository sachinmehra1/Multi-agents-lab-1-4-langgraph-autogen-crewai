# Verification — 26 October 2026

- Supplied live framework suite: **29 passed, no skips**, 218.07 seconds.
- Generated-artifact checks: **9 passed**; see test_generated_artifacts.py (counts, punctuation,
  ordering, empty input, and missing files across all three generated modules).
- All three agents completed the common task and recorded positive actual token usage.
- comparison/results.json contains one successful timed comparison. The six
  tradeoff sections reference those observed measurements.
- comparison/artifacts contains the latest generated files from the behavioral
  suite; these are later runs than the timed comparison, not its exact outputs.

Runtime: Python 3.12; exact primary package versions in requirements-tested.txt.
Model: gpt-4.1-mini. Route: direct OpenAI using the owner's account; Helicone
logging was not verified. No credentials are included in current files.

## Starter integration repairs

- Supplied client, task, tools, and token-counter files remain unchanged.
- LangChain uses the supported client/root_client parameters instead of the
  starter's openai_client hint. CrewAI uses its native OpenAI completion class.
- AutoGen uses the classic 0.2.35 API. Its tracked client is registered after
  tools, and AutoGen-only configuration is removed before API calls.
- Usage tracking records each actual response for all three frameworks. The
  original aggregate helpers are not used to represent an entire run as one step.
- Each run has a fresh temporary workspace, and subprocess execution uses that
  directory so imports see the files written by the tools.
- Framework output is checked before reporting success; graph recursion budget
  accommodates the explicit 15-model-call limit.
- The missing comparison template was replaced with six completed sections.

The supplied suite produced deprecation warnings from Chroma/AutoGen/CrewAI
integrations. They did not cause test failures. Broad upstream dependency ranges
may select incompatible APIs; use the tested requirements file.
