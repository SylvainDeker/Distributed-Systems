import os
import pytest
import numpy as np
import cv2 as cv
# pytest test_fixture.py 

def test_needsfiles(tmpdir):
    # provide a temporary directory unique to the test invocation
    print(tmpdir)
    assert True

def test_create_file(tmp_path):
    # The tmp_path_factory is a session-scoped fixture which can be
    # used to create arbitrary temporary directories from any other
    # fixture or test.
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("CONTENT")
    assert p.read_text() == "CONTENT"
    assert len(list(tmp_path.iterdir())) == 1
    # assert False


@pytest.fixture(scope="session")
def image_file(tmpdir_factory):
    img = cv.imread("/home/bob/Documents/Distributed-Systems/data/NE1_50M_SR_W/NE1_50M_SR_W.tif")
    assert img.shape == (5400,10800,3)
    fn = tmpdir_factory.mktemp("data").join("img.png")
    # assert str(fn) == ""
    cv.imwrite(str(fn),img)
    return fn


# contents of test_image.py
def test_histogram(image_file):
    img = cv.imread(str(image_file))
    assert img.shape == (5400,10800,3)
    # compute and test histogram
