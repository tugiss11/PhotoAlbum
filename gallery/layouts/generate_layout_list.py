import glob
import os
import inspect

NAME_DB_MAX_LENGTH = 20

my_path = os.path.dirname(inspect.getfile(inspect.currentframe()))
layout_path = os.path.join(my_path, "..", "..", "static", "page_layouts")
css_files = glob.glob(os.path.join(layout_path, "*.css"))
css_files = [os.path.basename(name) for name in css_files]
out_filename = os.path.join(my_path, 'layout_info.py')
f = open(out_filename, 'w')

f.write("#Generated file, DON'T EDIT! Run generate_layout_list.py instead!\n")
f.write("NAME_DB_MAX_LENGTH = " + str(NAME_DB_MAX_LENGTH) + "\n")
f.write("PAGE_LAYOUTS = (\n")
for file_name in css_files:
    f.write("   ('" + file_name.split('.')[0][0:NAME_DB_MAX_LENGTH] + "', '" + file_name + "'),\n")
f.write(")")
f.close()