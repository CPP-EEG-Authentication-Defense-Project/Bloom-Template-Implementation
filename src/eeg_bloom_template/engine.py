from .backend import BaseBloomFilterHashBackend


class EEGBloomFilterTemplateEngine:
    def __init__(self, backend: BaseBloomFilterHashBackend):
        self._backend = backend

    # TODO: build bloom filters and implement serialization/deserialization
