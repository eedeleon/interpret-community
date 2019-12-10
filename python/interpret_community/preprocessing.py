PREPROCESSOR_KEY = "preprocessors"


def add_preprocessing(base_class):
    base_class_init = base_class.__init__

    def new_init(self, func, data, *args, **kwargs):
        if PREPROCESSOR_KEY in kwargs:
            for preprocessor in kwargs.get(PREPROCESSOR_KEY):
                data = preprocessor(data)
        base_class_init(self, func, data, *args, **kwargs)
    base_class.__init__ = new_init
    return base_class
