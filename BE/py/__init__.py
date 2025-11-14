"""Python implementations for CodeBase Genius agents"""

# Import only what exists
try:
    from .repo_mapper import RepoMapper
except ImportError:
    RepoMapper = None

try:
    from .code_analyzer import CodeAnalyzer
except ImportError:
    CodeAnalyzer = None

try:
    from .docgen import DocGenerator
except ImportError:
    DocGenerator = None

# Export what's available
__all__ = []
if RepoMapper:
    __all__.append('RepoMapper')
if CodeAnalyzer:
    __all__.append('CodeAnalyzer')
if DocGenerator:
    __all__.append('DocGenerator')