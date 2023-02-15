#!/usr/bin/env python

'''
    @author: John Gallo

    Boxnotes Converter

    Usage: 

'''

from yattag import Doc
from htmldocx import HtmlToDocx
import json
import logging


''' Convert Boxnote to HTML '''
def content_to_html(el,html_style=''):
    # Recursively go through nested structure
    if 'content' in el.keys():
        if el['type'] == 'bullet_list':
            with tag('ul'):
                for item in el['content']:
                    content_to_html(item)

        elif el['type'] == 'list_item':
            with tag('li'):
                for item in el['content']:
                    content_to_html(item)

        elif el['type'] == 'paragraph':
            with tag('p'):
                if 'marks' in el.keys():
                    for mark in el['marks']:
                        if 'attrs' in mark.keys():
                            if 'alignment' in mark['attrs']:
                                # doc.attr(style = "text-align:{};".format(mark['attrs']['alignment']))
                                html_style += "text-align:{};".format(mark['attrs']['alignment'])             
                for item in el['content']:
                    content_to_html(item, html_style)

        elif el['type'] == 'code_block':
            with tag('code'):
                for item in el['content']:
                    content_to_html(item)

        elif el['type'] == 'blockquote':
            with tag('blockquote'):
                for item in el['content']:
                    content_to_html(item)

        elif el['type'] == 'call_out_box':
            with tag('blockquote'):
                # html_style += "padding: 5px; background-color: #E1E8F2; border: dotted 2px #00518A;"
                for item in el['content']:
                    content_to_html(item, html_style)
                    
        elif el['type'] == 'table':
            with tag('table', cellspacing="0", border="1"):
                for item in el['content']:
                    content_to_html(item)
        
        elif el['type'] == 'table_row':
            with tag('tr'):
                for item in el['content']:
                    content_to_html(item)
        
        elif el['type'] == 'table_cell':
        
            try:
                t_colspan = el['attrs']['colspan']
                t_rowspan = el['attrs']['rowspan']
                t_colwidth = el['attrs']['colwidth'][0]

                with tag('td', colspan="{}".format(t_colspan), rowspan="{}".format(t_rowspan), colwidth="{}".format(t_colwidth) ):
                    for item in el['content']:
                        content_to_html(item)

            except (KeyError, TypeError):
                with tag('td'):
                    for item in el['content']:
                        content_to_html(item)

        else: logging.warning("*** Unsupported type (in-content): {}".format(el['type']))
    
    # HTML convertible line(s)
    elif 'text' in el.keys():
        # Additional attributes 
        # html_style = ''
        html_strong = False
        html_em = False
        html_s = False
        if 'marks' in el.keys():
            for mark in el['marks']:                
                if mark['type'] == 'font_color':
                    html_style+="color:{};".format(mark['attrs']['color'])
                elif mark['type'] == 'font_size':
                    html_style+="font-size:{};".format(mark['attrs']['size'])
                elif mark['type'] == 'underline':
                    html_style+="text-decoration:underline;"
                elif mark['type'] == 'strong':
                    html_strong = True
                elif mark['type'] == 'em':
                    html_em = True
                elif mark['type'] == 'strikethrough':
                    html_s = True
                elif mark['type'] == 'author_id':
                    pass
                else:
                    logging.warning("*** Unsupported type (in-text): {} - {}".format(el['type'],mark['type']))

            if html_style:
                doc.attr(style = html_style)
               
        if html_strong:
            with tag('strong'):  
                text(el['text'])
        elif html_em:
            with tag('em'):  
                text(el['text'])
        elif html_s:
            with tag('s'):  
                text(el['text'])
        else:
            text(el['text'])
            #  doc.asis("".format())
                
    elif el['type'] == 'paragraph' and len(el.keys()) > 1:
        if 'marks' not in el.keys(): 
            logging.warning("*** Unsupported type: {}".format(el['type']))
            logging.warning(el)


if __name__ == '__main__':    
    
    # Set logging configuration
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    # filename = "its-operations - 1-10-2023.boxnote"
    filename = "Newsletter1.boxnote"
    # filename = "Airtable: Client Stories App Requirements.boxnote"

    # Open Boxnote for reading
    with open(filename, "r") as boxnote:
        data = json.load(boxnote)

    # Determine if object contains doc object or atext object
    

    # Get interesting Node: object -> doc -> content
    content_list = data['doc']['content']

    # Initiate HTML Objects
    doc, tag, text = Doc().tagtext()

    # Generate HTML
    with tag('html'):
        with tag('body'):
            # content_to_html(content_list[21])
            for elm in content_list:
                content_to_html(elm)

    html_result = doc.getvalue()
    
    # print(html_result)
    with open(filename.replace('boxnote', "html"), "w") as file:
        file.write(html_result)

    new_parser = HtmlToDocx()
    new_parser.table_style = 'TableGrid'
    docx = new_parser.parse_html_string(html_result)
    
    docx.save(filename.replace('boxnote', "docx"))




