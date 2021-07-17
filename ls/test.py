import os
import shutil
import unittest
import tempfile

import ls as ls_md


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.root_dir = tempfile.mkdtemp(prefix="test_ls_cmd_dir_")
        print(self.root_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.root_dir)

    def create_file(self, filename, dirpath=None):
        if dirpath is None:
            dirpath = self.root_dir
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'w') as f:
            f.write('')
        return filepath

    def create_dir(self, dirname):
        dirpath = os.path.join(self.root_dir, dirname)
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    def test_case_01(self):
        filenames = ['test1', 'test2', 'test3']
        for fname in filenames:
            self.create_file(fname)

        expect = ['test1', 'test2', 'test3']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir)])
        self.assertEqual(ls_result, expect)

    def test_case_02(self):
        filenames = ['test1', 'test2', '.test3']
        for fname in filenames:
            self.create_file(fname)

        expect = ['test1', 'test2']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir)])
        self.assertEqual(ls_result, expect)


    def test_case_03(self):
        filenames = ['test1', 'test2', '.test3']
        for fname in filenames:
            self.create_file(fname)

        expect = {'test1', 'test2', '.test3'}
        ls_result = [item.name for item in ls_md._in_dir(self.root_dir, include_hidden=True)]
        self.assertEqual(len(ls_result), 3)
        self.assertEqual(set(ls_result), expect)

    def test_case_04(self):
        filenames = ['test1', 'test2', 'test3']
        dirnames = ['test4', 'test5', '.test6']
        for fname in filenames:
            self.create_file(fname)

        for dname in dirnames:
            self.create_dir(dname)

        expect = ['test1', 'test2', 'test3', 'test4', 'test5']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir)])
        self.assertEqual(ls_result, expect)

    def test_case_05(self):
        filenames = ['.test1', 'test2', 'test3']
        dirnames = ['test4', 'test5', 'test6']
        for fname in filenames:
            self.create_file(fname)

        for dname in dirnames:
            self.create_dir(dname)

        expect = ['.test1', 'test2', 'test3', 'test4', 'test5', 'test6']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir, include_hidden=True)])
        self.assertEqual(ls_result, expect)

    def test_case_06(self):
        filenames = ['file1', 'file2', 'file3']
        dirnames = ['dir1', 'dir2',]
        for fname in filenames:
            self.create_file(fname)

        for dname in dirnames:
            self.create_dir(dname)

        dir3 = self.create_dir('dir3')
        for fname in ['file4', 'file5', 'file6']:
            self.create_file(fname, dirpath=dir3)

        expect = ['dir1', 'dir2', 'dir3', 'file1', 'file2', 'file3', 'file4', 'file5', 'file6']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir, recursive=True)])
        self.assertEqual(ls_result, expect)

    def test_case_07(self):
        filenames = ['file1', 'file2', 'file3']
        dirnames = ['dir1', 'dir2',]
        for fname in filenames:
            self.create_file(fname)

        for dname in dirnames:
            self.create_dir(dname)

        dir3 = self.create_dir('dir3')
        for fname in ['file4', 'file5', 'file6']:
            self.create_file(fname, dirpath=dir3)

        expect = ['dir1', 'dir2', 'dir3', 'file1', 'file2', 'file3']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir, recursive=False)])
        self.assertEqual(ls_result, expect)

    def test_case_08(self):
        self.create_dir('dir1/dir2/dir3')
        expect = ['dir1', 'dir2', 'dir3']
        ls_result = sorted([item.name for item in ls_md._in_dir(self.root_dir, recursive=True)])
        self.assertEqual(ls_result, expect)


if __name__ == '__main__':
    unittest.main()
