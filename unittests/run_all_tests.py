import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()

    tests = loader.discover(start_dir="unittests", pattern="test*.py")

    runner = unittest.TextTestRunner()

    runner.run(tests)
