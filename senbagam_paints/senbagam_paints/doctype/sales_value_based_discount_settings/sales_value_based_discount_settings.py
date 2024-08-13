# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class SalesValueBasedDiscountSettings(Document):
	pass

@frappe.whitelist()
def img_preview(image=None):      
    layout_height =  "Auto"
    image_width =  "250px"        
    image_height =  "Auto" 
    html=''
    html='''            
    <html>
        <head>            <style>
        div.gallery {            border: 1px solid #ccc;
        }
        div.gallery:hover {            border: 1px solid #777;
        box-shadow: 0 22px 26px 0 rgba(0,0,0,0.24),0 27px 60px 0 rgba(0,0,0,0.19);            }

        div.gallery img {            width:'''+image_width+''';
        height:'''+image_height+''';            }
        div.desc {
        padding: 5px;            width: '''+image_width+''';
        height: 50px;
        text-align: center;            overflow:scroll;
        }
        * {
        box-sizing: border-box;            }
        .responsive {
        padding: 0 6px 6px;            height:'''+layout_height+''';
        float: left;            }
        
        .clearfix:after {
        content: "";            display: table;
        clear: both;            }
        </style>            </head>
        <body>            <h5>Image Preview</h5>
        '''        
    
    html = html+ f'''                 
        <div class="responsive">
            <div class="gallery">                    <a target="_blank" href="{image}">
                <img src="{image}" alt="No Image" >                    </a>
        </div>
            </div>            '''
    html = html + '''            <div class="clearfix"></div>
        </body>            </html>
    '''            
    return html

@frappe.whitelist()
def table_data_validation(tabel_rows, enter_value, enter_idx):

    tabel_rows = json.loads(tabel_rows)

    for i in range(0, len(tabel_rows), 1):

        if int(enter_idx) != tabel_rows[i]["idx"]:

            try:

                if float(enter_value) >= tabel_rows[i]["start_amount"] and float(enter_value) <= tabel_rows[i]["upto"]:
                    
                    return tabel_rows[i]["idx"]
                
                if float(enter_value) <= tabel_rows[i]["start_amount"] and float(enter_value) >= tabel_rows[i]["upto"]:
                    
                    return tabel_rows[i]["idx"]

            except:

                pass

