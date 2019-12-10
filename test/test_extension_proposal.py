import pytest

from interpret_community.preprocessing import add_preprocessing
from interpret.blackbox import ShapKernel


class CustomException(Exception):
    pass


def test_add_preprocessing():
    with pytest.raises(CustomException):
        def raise_exception():
            raise CustomException("ran preprocess")

        add_preprocessing(ShapKernel)(lambda x: 1, "a", preprocessors=[lambda a: raise_exception()])
