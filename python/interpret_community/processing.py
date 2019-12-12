
PREPROCESSOR_KEY = "preprocessors"
POSTPROCESSOR_KEY = "postprocessors"


def add_preprocessing(base_class):
    base_class_init = base_class.__init__

    def new_init(self, func, data, *args, **kwargs):
        if PREPROCESSOR_KEY in kwargs and kwargs.get(PREPROCESSOR_KEY):
            for preprocessor in kwargs.get(PREPROCESSOR_KEY):
                data = preprocessor(data)
            base_class_init(self, func, data, *args, **kwargs)
        base_class.__init__ = new_init
    return base_class


def add_postprocessing(base_class):
    base_class_init = base_class.__init__

    def new_init(self, *args, **kwargs):
        if POSTPROCESSOR_KEY in kwargs and kwargs.get(POSTPROCESSOR_KEY):
            self._internal_postprocessor = kwargs.get(POSTPROCESSOR_KEY)
            base_class_init(self, *args, **kwargs)
    base_class.__init__ = new_init

    if hasattr(base_class, "explain_local"):
        base_class._original_explain_local = base_class.explain_local

        def new_explain_local(self, *args, **kwargs):
            explanation = base_class._original_explain_local(self, *args, **kwargs)
            if hasattr(self, "_internal_postprocessor"):
                for postprocessor in self._internal_postprocessors:
                    explanation = postprocessor(explanation)
            return explanation
    base_class.explain_local = new_explain_local

    if hasattr(base_class, "explain_global"):
        def new_explain_global(self, *args, **kwargs):
            explanation = base_class._original_explain_global(self, *args, **kwargs)
            if hasattr(self, "_internal_postprocessor"):
                for postprocessor in self._internal_postprocessors:
                    explanation = postprocessor(explanation)
            return explanation
    base_class.explain_global = new_explain_global

    return base_class
