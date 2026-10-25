"""Check the actual generated modules, beyond the starter's syntax checks."""
import importlib.util
from pathlib import Path
import pytest


@pytest.fixture(params=['agent_langgraph', 'agent_autogen', 'agent_crewai'])
def generated(request):
    path = Path('comparison/artifacts') / request.param / 'word_freq.py'
    assert path.exists(), 'Run compare.py before validating generated artifacts'
    spec = importlib.util.spec_from_file_location('generated_' + request.param, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.word_frequency


def test_case_punctuation_counts_and_descending_order(generated, tmp_path):
    text = tmp_path / 'input.txt'
    text.write_text('Cat, DOG! cat. bird dog dog')
    result = generated(str(text))
    assert result == {'dog': 3, 'cat': 2, 'bird': 1}
    assert list(result.values()) == [3, 2, 1]


def test_empty_input(generated, tmp_path):
    text = tmp_path / 'empty.txt'
    text.write_text('')
    assert generated(str(text)) == {}


def test_missing_file(generated, tmp_path):
    with pytest.raises(FileNotFoundError, match='.+'):
        generated(str(tmp_path / 'missing.txt'))
