"""Run a lab with your own OpenAI key; no credentials are persisted."""
import argparse
import os
from pathlib import Path
import runpy
import sys
from dotenv import dotenv_values

parser = argparse.ArgumentParser()
parser.add_argument("--env", type=Path, required=True, help="Private .env containing LLM_API_KEY or OPENAI_API_KEY")
parser.add_argument("script", help="Lab script, or pytest")
parser.add_argument("args", nargs=argparse.REMAINDER)
args = parser.parse_args()
values = dotenv_values(args.env)
key = values.get("LLM_API_KEY") or values.get("OPENAI_API_KEY")
if not key:
    parser.error("No LLM_API_KEY or OPENAI_API_KEY in the specified private file")
os.environ.update(OPENAI_API_KEY=key, OPENROUTER_API_KEY=key,
                  OPENAI_BASE_URL="https://api.openai.com/v1",
                  HELICONE_BASE_URL="https://api.openai.com/v1",
                  HELICONE_API_KEY="direct-openai-no-helicone",
                  OTEL_SDK_DISABLED="true", CREWAI_TELEMETRY_ENABLED="false")
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]
sys.argv = [args.script] + args.args
if args.script == "pytest":
    import pytest
    raise SystemExit(pytest.main(args.args))
runpy.run_path(args.script, run_name="__main__")
