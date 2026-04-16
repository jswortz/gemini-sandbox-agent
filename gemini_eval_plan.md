# Skill Evaluation & LLM Raters

For this A2A Sandbox agent, we want to ensure any code it generated (like `tictactoe_ralph.py`) passes quality standards via an LLM Rater architecture.

## Strategy: ADK Eval Sets

The ADK includes support for `eval_sets` where we can track LLM-driven or code-execution-driven assessments:
1. **Creation**: We can create an `EvalSet` capturing the prompt: "Build a Tic Tac Toe CLI..." and an expected criteria (e.g. valid Python syntax, all edge cases handled).
2. **Execution**: Using the `google.adk.evaluation` module, we can run batch tests matching agent traces against an `LLMEvaluator` using Gemini 1.5 Pro to judge the solution and code quality.
3. **Tracking**: The evaluation runs are captured in the ADK pipeline and served via `/apps/{app_name}/eval_results`.

## Adding a Custom LLM Rater Skill

We should consider building an explicit Rater Subagent (`QA Rater Skill`) plugged into the ADK:
*   `AgentRater`: Reviews `/tmp/tictactoe_ralph.py` output.
*   *Prompt Signature*: `Analyze this python script. Does it correctly capture row/col/diag win conditions? Does the AI make a valid move? Rate 1-5 and pass/fail.`
*   The Agent uses a `LongRunningFunctionTool` or Subagent approach to wait for the LLM grading step to complete before returning success to the user over A2A.

## Conclusion

By mounting `eval_sets` dynamically and writing expected outcomes as LLM assertions, we can wrap the Sandbox agent logic in a rigorous test loop that automatically denies low-quality code deployments to production systems.
