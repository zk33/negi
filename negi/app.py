# -*- coding: utf-8 -*-

import os
import json
import codecs
import jinja2


class Negi(object):

    def __init__(self,data_dir,tmpl_dir,out_dir,verbose=False):
        self.params = {}
        self.data_root = os.path.normpath(data_dir)
        self.tmpl_root = os.path.normpath(tmpl_dir)
        self.output_root = os.path.normpath(out_dir)
        self.verbose = verbose
        self.jinja_env = jinja2.Environment(
            loader = jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(self.tmpl_root),
                jinja2.PackageLoader('negi','templates')
            ])
        )

    def build(self):
        self.load_params()
        self.render_all()

    def load_params(self):
        for current_dir, dirs, files in os.walk(self.data_root):
            self._process_params(current_dir, files, pages={})

    def _process_params(self,current_dir, files, pages={}):
        base_params = {}
        files.sort()

        #process __init__.json first (if exists)
        if '__init__.json' in files:
            base_params = self._read_json(current_dir,files.pop(files.index('__init__.json')))

        if '_contents' in base_params:
            pages.update( base_params['_contents'] )
            del base_params['_contents']

        for file_name in files:
            #skip dot file
            if file_name[0] is '.' or file_name.find('.') == -1:
                continue
            #check page or param
            name,ext = file_name.split('.')
            u_score_idx = name.find('_')

            #if has '_', this is param file. Otherwise, page definition file.
            if u_score_idx is not -1:
                page_name = name[0:u_score_idx]
                param_name = name[u_score_idx + 1:]

                if u_score_idx is 0:
                    #this is base param
                    base_params[param_name] = self._read_file(current_dir,file_name)
                else:
                    pages[page_name][param_name] = self._read_file(current_dir,file_name)
            else:
                pages[name] = self._read_json(current_dir,file_name)

        #save param
        path = current_dir.replace(self.data_root,'')
        if not path:
            path = '/'
        else:
            #if has parent, save parent params as _parent
            parent, now = os.path.split(path)
            if parent in self.params:
                base_params['_parent'] = self.params[parent]

        #save pages
        base_params['_pages'] = pages

        #save params as self.params['path/to/directory/from/root']
        self.params[path] = base_params

        #if pages[xxxx] has 'pages', call _process_params recursively
        for k,v in pages.items():
            if '_contents' in v:
                self._process_params( os.path.join(current_dir,k), [], v['_contents'])

    def render_all(self):
        for output_dir, base_params in self.params.items():
            if '_pages' in base_params:
                for page_name, page_params in base_params['_pages'].items():
                    #build params
                    params = self._build_params(output_dir,page_name)

                    #render
                    file_path = os.path.join(output_dir[1:], page_name + params['_ext'])
                    output,template_path = self._render(file_path,params)

                    #write file
                    self._save_page(file_path,output)

                    #output to console
                    if self.verbose:
                        print file_path + '\t <- ' + os.path.join(self.tmpl_root,template_path)

    def _render(self,file_path,params): 
        #find template
        tmpl_file = self._find_template(file_path)

        #render
        tmpl = self.jinja_env.get_template(tmpl_file)
        output = tmpl.render(params)

        return output, tmpl_file

    def _render_page(self,tmpl_file,params):
        return tmpl.render(params)

    def _save_page(self,save_path,content):
        output_path = os.path.join(self.output_root,save_path)
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self._write_file(output_path,content)

    def _build_params(self, output_dir, page_name):
        base_params = self.params[output_dir]
        page_params = base_params['_pages'][page_name]
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
        #add utility params
        result_params['_rel_root'] = os.path.relpath('/',output_dir)
        if '_ext' not in result_params:
            result_params['_ext'] = '.html'
        return result_params

    def _find_template(self,output_path):
        tmp_path,orig_ext = os.path.splitext(output_path)
        exam_ext = [orig_ext]
        if orig_ext != 'html':
            exam_ext.append('.html')
        while True:
            tmp_path_parent, deleted = os.path.split(tmp_path)
            exam_paths = (
                tmp_path,
                tmp_path.replace('/','_'),
                os.path.join(tmp_path_parent,'__base__'),
            )
            for exam_path in exam_paths:
                for ext in exam_ext:
                    path = exam_path + ext
                    if os.path.exists(os.path.join(self.tmpl_root,path)):
                        return path
            if not deleted:
                break
            tmp_path = tmp_path_parent
        raise TemplateNotFound(output_path)

    def _read_json(self,root,file_name):
        f  = open(os.path.join(root,file_name))
        return json.load(f)

    def _read_file(self,root,file_name):
        f = open(os.path.join(root,file_name))
        if file_name.find('.json') is not -1:
            return json.load(f)
        else:
            return f.read()
    def _write_file(self,path,content):
        f = codecs.open(path,'w','utf-8')
        f.write(content)
        f.close()


class TemplateNotFound(Exception):
    def __init__(self,path):
        self.path = path

    def __str__(self):
        return 'Template file for "%s" not found' % self.path
