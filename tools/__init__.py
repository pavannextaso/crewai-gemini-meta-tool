from .meta_fetcher import fetch_meta
from .content_analyzer import analyze_content
from .plagiarism import plagiarism_detector
from .title_meta_extractor import extract_title_description

__all__ = [
    'fetch_meta',
    'analyze_content', 
    'plagiarism_detector',
    'extract_title_description'
]

tool_map = {
    "fetch_meta": fetch_meta,
    "analyze_content": analyze_content,
    "plagiarism_detector": plagiarism_detector,
    "extract_title_description": extract_title_description
}


"""
import os
import importlib
import inspect

__all__ = ["analyze_content","fetch_meta"]
tool_map = {
    "analyze_content":"analyze_content",
    "fetch_meta":"fetch_meta"
}


tool_dir = os.path.dirname(__file__)
tool_files = [f for f in os.listdir(tool_dir) if f.endswith('.py') and f != '__init__.py']

for file in tool_files:
    module_name = file[:-3]
    full_module_name = f"tools.{module_name}"
    module = importlib.import_module(full_module_name)

    print(f"🔍 Inspecting module: {full_module_name}")

    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isfunction(obj):
            print(f"✅ Found function: {name}")
            __all__.append(name)
            tool_map[name] = obj

"""