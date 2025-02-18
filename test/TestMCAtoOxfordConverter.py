import sys
import os
import glob
import unittest

# Insert the absolute path to the src folder so that we can import the converter module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from converter import MCAtoOxfordConverter

class TestMCAtoOxfordConverter(unittest.TestCase):
    def setUp(self):
        # Use the provided test data folder.
        self.test_folder = os.path.join(os.path.dirname(__file__), "testData")
        # Remove any leftover .dat files from previous runs.
        for dat_file in glob.glob(os.path.join(self.test_folder, "*.dat")):
            try:
                os.remove(dat_file)
            except Exception as e:
                print(f"Error removing {dat_file}: {e}")

    def tearDown(self):
        # Optionally clean up .dat files after tests.
        for dat_file in glob.glob(os.path.join(self.test_folder, "*.dat")):
            try:
                os.remove(dat_file)
            except Exception as e:
                print(f"Error removing {dat_file}: {e}")

    def test_conversion_creates_dat_files(self):
        # Create the converter and run the conversion on the testData folder.
        converter = MCAtoOxfordConverter(self.test_folder)
        converter.convert_folder()
        
        # For each .mca file, check that a corresponding .dat file exists.
        mca_files = glob.glob(os.path.join(self.test_folder, "*.mca"))
        for mca_file in mca_files:
            expected_dat_file = os.path.splitext(mca_file)[0] + ".dat"
            self.assertTrue(os.path.exists(expected_dat_file),
                            f"{expected_dat_file} not found after conversion.")

    def test_find_dat_files_creates_list(self):
        # Run conversion to ensure .dat files exist.
        converter = MCAtoOxfordConverter(self.test_folder)
        converter.convert_folder()
        # Then create the file listing.
        converter.find_dat_files(self.test_folder)
        
        # Check that the "00_nameList.txt" file exists.
        name_list_path = os.path.join(self.test_folder, "00_nameList.txt")
        self.assertTrue(os.path.exists(name_list_path),
                        "00_nameList.txt was not created by find_dat_files")
        
        # Verify that every .dat file is listed in the text file.
        dat_files = glob.glob(os.path.join(self.test_folder, "*.dat"))
        with open(name_list_path, "r", encoding="utf-8") as f:
            content = f.read()
            for dat_file in dat_files:
                self.assertIn(dat_file, content,
                              f"{dat_file} is not listed in 00_nameList.txt")

if __name__ == '__main__':
    unittest.main()
