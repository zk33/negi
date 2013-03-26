# -*- coding: utf-8 -*-

import os
import json
import jinja2


class Negi(object):

    def __init__(self,data_dir,tmpl_dir,out_dir,verbose=False):
        self.params = {}
        self.data_root = data_dir
        self.tmpl_root = tmpl_dir
        self.output_root = out_dir
        self.verbose = verbose
        self.jinja_env = jinja2.Environment(
            loader = jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(self.tmpl_root),
                jinja2.PackageLoader('negi','templates')
            ])
        )

    def build(self):
        self.load_params()
        self.render()

    def load_params(self):
        for current_dir, dirs, files in os.walk(self.data_root):
            self._process_params(current_dir, files, pages={})

    def _process_params(self,current_dir, files, pages={}):
        base_params = {}
        files.sort()

        #process __init__.json first (if exists)
        if '__init__.json' in files:
            base_params = self._read_json(current_dir,files.pop(files.index('__init__.json')))

        if 'contents' in base_params:
            pages = base_params['contents']
            del base_params['contents']

        for file_name in files:
            #skip dot file
            if file_name[0] is '.':
                continue
            #check page or param
            name,ext = file_name.split('.')
            u_score_idx = name.find('_')

            #if has '_', this is param file. Otherwise, page definition file.
            if u_score_idx is not -1:
                page_name = name[0:u_score_idx]
                param_name = name[u_score_idx + 1:]
                pages[page_name][param_name] = self._read_file(current_dir,file_name)
            else:
                pages[name] = self._read_json(current_dir,file_name)

        #save param
        parent, now = os.path.split(current_dir)
        if parent in self.params:
            base_params['_parent'] = self.params[parent]

        base_params['_contents'] = pages

        path = current_dir.replace(self.data_root,'')
        if not path:
            path = '/'
        self.params[path] = base_params

        #if pages[xxxx] has 'contents', call _process_params recursively
        for k,v in pages.items():
            if 'contents' in v:
                self._process_params( os.path.join(current_dir,k), [], v['contents'])

    def render(self):
        for path, base_params in self.params.items():
            if '_contents' in base_params:
                for page_name, page_params in base_params['_contents'].items():
                    page_params = self._build_params(page_params,base_params)

                    if 'ext' in page_params:
                        page_name = page_name + '.' + page_params['ext']
                    else:
                        page_name = page_name + '.html'

                    self._render_page(path, page_name, page_params)

    def _build_params(self, page_params, base_params):
        result_params = base_params.copy()
        result_params.update(page_params)
        tmp_params = base_params.copy()
        while True:
            if '_parent' in tmp_params:
                update_params = tmp_params['_parent'].copy()
                update_params.update(result_params)
                result_params = update_params
                tmp_params = tmp_params['_parent'].copy()
            else:
                break
        return result_params

    def _render_page(self, path, page_name, page_params):
        # get template file
        tmpl_file = self._find_template(os.path.join(path[1:],page_name))
        tmpl = self.jinja_env.get_template(tmpl_file)
        # render
        output = tmpl.render(page_params)
        # write file
        output_path = os.path.join(self.output_root, path[1:], page_name)
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = open(output_path,'w')
        output_file.write(output)
        output_file.close()
        if self.verbose:
            print output_path + '\t <- ' + os.path.join(self.tmpl_root,tmpl_file)

    def _find_template(self,path):
        tmp_path = path
        #same position/ same filename
        if os.path.exists(os.path.join(self.tmpl_root,tmp_path)):
            return tmp_path
        #same position/ same filename but different extension(if not .html)
        if len(tmp_path) > 5 and tmp_path[-5:] != '.html':
            tmp_path_arr = os.path.splitext(tmp_path)
            tmp_path = tmp_path_arr[0] + '.html'
            if os.path.exists(os.path.join(self.tmpl_root,tmp_path)):
                return tmp_path
        #joined  by underscore
        tmp_path = os.path.splitext(path)[0]
        exam_path = tmp_path.replace('/','_') + '.html'
        if os.path.exists(os.path.join(self.tmpl_root,exam_path)):
            return exam_path
        #loop parent
        while True:
            tmp_path, deleted = os.path.split(tmp_path)
            if not deleted:
                break
            #same direcotry's '__base__.html'
            exam_paths = (
                os.path.join(tmp_path,'__base__.html'),
                tmp_path + '.html',
                tmp_path.replace('/','_') + '.html'
            )
            for exam_path in exam_paths:
                if os.path.exists(os.path.join(self.tmpl_root,exam_path)):
                    return exam_path
        return ''

    def _read_json(self,root,file_name):
        f  = open(os.path.join(root,file_name))
        return json.load(f)

    def _read_file(self,root,file_name):
        f = open(os.path.join(root,file_name))
        if file_name.find('.json') is not -1:
            return json.load(f)
        else:
            return f.read()
