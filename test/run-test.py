#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
sys.path.insert(0, os.path.abspath(os.path.split(os.path.dirname(__file__))[0]))

import unittest
import negi

class NegiTest(unittest.TestCase):
    basepath = os.path.dirname(__file__)

    def _path(self,path):
        return os.path.join(self.basepath,path)
    def setUp(self):
        pass
    def tearDown(self):
        pass
    #test load json file
    def test_json(self):
        n = negi.Negi(self._path('datas/test_json'),'','')
        #bad json format file
        self.assertRaises(ValueError,n._read_json, n.data_root, 'bad.json')
        #json not found
        self.assertRaises(IOError,n._read_json, n.data_root, 'notfound.json')
    #test params from json
    def test_params(self):
        n = negi.Negi(self._path('datas/test_params'),'','')
        n.load_params()
        #root param
        self.assertEqual(n.params['/']['root'],'hello')
        #param at _contents
        self.assertEqual(n.params['/']['_pages']['index']['param1'],'index')
        #json file as page definition
        self.assertEqual(n.params['/']['_pages']['page']['param1'],'page')
        #params written in underscored file
        self.assertEqual(n.params['/']['param2'],[1,2,"3"])
        self.assertEqual(n.params['/']['param3'],"hello,world\n")
        self.assertEqual(n.params['/']['_pages']['index']['param2'],{'test':1})
        self.assertEqual(n.params['/']['_pages']['index']['param3'],'Domo!\n')
        self.assertEqual(n.params['/']['_pages']['page']['param2'],[2,5])
        #deep directory
        self.assertEqual(n.params['/foo/bar']['_pages']['index']['param1'],'foo/bar/index')
        #parent
        self.assertEqual(n.params['/foo/bar']['_parent']['_parent']['param3'],"hello,world\n")

        #builded parameters=========
        params = n._build_params('/foo/bar','index')
        #self
        self.assertEqual(params['param4'],'self')
        #inherited
        self.assertEqual(params['param3'],"hello,world\n")
        #override
        self.assertEqual(params['param1'],"foo/bar/index")
        #utility params
        self.assertEqual(params['_rel_root'],'../..')
        self.assertEqual(params['_ext'],'.html')

        #check output path
        pass
    #test find template
    def test_template(self):
        tmpl_path = self._path('datas/test_template')
        n = negi.Negi('',tmpl_path,'')
        #same name
        self.assertEqual(n._find_template('spam/egg/ham1/samename.html'),'spam/egg/ham1/samename.html')
        #different extension but same filename
        self.assertEqual(n._find_template('spam/egg/ham1/samename.php'),'spam/egg/ham1/samename.html')
        #same directory's __base__.html
        self.assertEqual(n._find_template('spam/egg/ham1/notfound.html'),'spam/egg/ham1/__base__.html')
        #parent directory's __base__.html
        self.assertEqual(n._find_template('spam/egg/ham2/notfound.html'),'spam/egg/__base__.html')
        #underscored
        self.assertEqual(n._find_template('foo/bar/baz.php'),'foo_bar_baz.php')
        #underscored parent
        self.assertEqual(n._find_template('hoge/fuga/piyo.php'),'hoge.php')
        #not found
        self.assertRaises(negi.TemplateNotFound,n._find_template,'/not/found.html')
    #test output
    def test_output(self):
        pass








def main():
    unittest.main()


if __name__ == '__main__':
    main()
