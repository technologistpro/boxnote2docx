#!/usr/bin/env python

# Importing the Yattag library
from yattag import Doc
import json

# filename = "its-operations - 1-10-2023.boxnote"
filename = "Newsletter1.boxnote"

# Open boxfile for reading
with open(filename, "r") as boxnote:
    data = json.load(boxnote)

# object -> doc -> content
content_list = data['doc']['content']

d21 = content_list[21]

def print_content(el,html_style=''):
    # Recursive procedure to go through nested structure
    if 'content' in el.keys():
        if el['type'] == 'bullet_list':
            with tag('ul'):
                for item in el['content']:
                    print_content(item)
        elif el['type'] == 'list_item':
            with tag('li'):
                for item in el['content']:
                    print_content(item)
        elif el['type'] == 'paragraph':
            with tag('p'):
                if 'marks' in el.keys():
                    for mark in el['marks']:
                        if 'attrs' in mark.keys():
                            if 'alignment' in mark['attrs']:
                                # doc.attr(style = "text-align:{};".format(mark['attrs']['alignment']))
                                html_style += "text-align:{};".format(mark['attrs']['alignment'])
                                 
                for item in el['content']:
                    print_content(item, html_style)

        else: print("*** Unsupported type (in-content): {}".format(el['type']))
    
    # HTML convertible line(s)
    elif 'text' in el.keys():
        # Additional attributes 
        # html_style = ''
        html_strong = False
        if 'marks' in el.keys():
            for mark in el['marks']:                
                if mark['type'] == 'font_color':
                    html_style+="color:{};".format(mark['attrs']['color'])
                elif mark['type'] == 'font_size':
                    html_style+="font-size:{};".format(mark['attrs']['size'])
                elif mark['type'] == 'underline':
                    html_style+="text decoration:underline;"
                elif mark['type'] == 'strong':
                    html_strong = True
                else:
                    print("MARK: Unsupported type: {} - {}".format(el['type'],mark['type']))

            if html_style:
                doc.attr(style = html_style)
               
        if html_strong:
            with tag('strong'):  
                text(el['text'])
        else:
            text(el['text'])
            #  doc.asis("".format())
                
    elif el['type'] == 'paragraph' and len(el.keys()) > 1:
        if 'marks' not in el.keys(): 
            print("*** Unsupported type: {}".format(el['type']))
            print(el)

    

doc, tag, text = Doc().tagtext()

with tag('html'):
    with tag('body'):
        # print_content(content_list[21])
        for elm in content_list:
            print_content(elm)

        # with tag('p', id = 'main'):
        #     text('We can write any text here')
        # with tag('a', href = '/my-link'):
        #     text('We can insert any link here')
        

result = doc.getvalue()
print(result)


# data_sample = {'type': 'bullet_list',
#  'content': [{'type': 'list_item',
#    'content': [{'type': 'paragraph',
#      'content': [{'type': 'text',
#        'marks': [{'type': 'font_size', 'attrs': {'size': '0.8125em'}},
#         {'type': 'strong'},
#         {'type': 'underline'},
#         {'type': 'author_id', 'attrs': {'authorId': '180701212'}}],
#        'text': 'GC80 - 2022'}]}]},
#   {'type': 'list_item',
#    'content': [{'type': 'paragraph',
#      'content': [{'type': 'text',
#        'marks': [{'type': 'font_size', 'attrs': {'size': '0.8125em'}},
#         {'type': 'strong'},
#         {'type': 'underline'},
#         {'type': 'author_id', 'attrs': {'authorId': '180701212'}}],
#        'text': 'Software Asset Management'}]}]},
#   {'type': 'list_item',
#    'content': [{'type': 'paragraph',
#      'content': [{'type': 'text',
#        'marks': [{'type': 'font_size', 'attrs': {'size': '0.8125em'}},
#         {'type': 'strong'},
#         {'type': 'author_id', 'attrs': {'authorId': '180701212'}}],
#        'text': 'ITS - Ops – 2021 Applications Migration to the Cloud'}]}]},
#   {'type': 'bullet_list',
#    'content': [{'type': 'list_item',
#      'content': [{'type': 'paragraph',
#        'content': [{'type': 'text',
#          'marks': [{'type': 'font_size', 'attrs': {'size': '0.8125em'}},
#           {'type': 'strong'},
#           {'type': 'author_id', 'attrs': {'authorId': '180701212'}}],
#          'text': 'SecureTransport Migration'}]}]},
#     {'type': 'list_item',
#      'content': [{'type': 'paragraph',
#        'content': [{'type': 'text',
#          'marks': [{'type': 'font_size', 'attrs': {'size': '0.8125em'}},
#           {'type': 'strong'},
#           {'type': 'author_id', 'attrs': {'authorId': '180701212'}}],
#          'text': 'IR to containers | Axcelinno working on Gitlab upgrade\\'}]}]}]}]}
