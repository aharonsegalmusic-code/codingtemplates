"""
gets from 3 topics
            raw
            clean
            analytics
stores them as one image id with 3 versions of it
"""

from indexOrchestrator import orchestrator, _config

orchestrator.poll_and_index(_config.es_index)
