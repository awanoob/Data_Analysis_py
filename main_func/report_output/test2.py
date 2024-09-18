from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
from docx import Document

def set_cell_margins(cell, **kwargs):
    '''设置某单元格间距

    :param cell: 某单元格
    :param top: 上边距 (cm)
    :param start: 左边距 (cm) (Word)
    :param bottom: 下边距 (cm)
    :param end: 右边距 (cm) (Word)
    :param left: 左边距 (cm) (WPS)
    :param right: 右边距 (cm) (WPS)
    '''
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')

    for m in ['top', 'start', 'bottom', 'end', 'left', 'right']:
        if m in kwargs:
            node = OxmlElement(f'w:{m}')
            try:
                # 将厘米转换为 Twips
                cm_value = float(kwargs[m])
                twips = int(Cm(cm_value).twips)

                node.set(qn('w:w'), str(twips))
                node.set(qn('w:type'), 'dxa')
                existing = tcMar.find(qn(f'w:{m}'))
                if existing is not None:
                    tcMar.remove(existing)
                tcMar.append(node)
            except ValueError:
                print(f"Invalid value for {m}: {kwargs[m]}. Skipping.")

    # 处理 left/right 和 start/end 的兼容性
    if 'left' in kwargs and 'start' not in kwargs:
        set_cell_margins(cell, start=kwargs['left'])
    if 'right' in kwargs and 'end' not in kwargs:
        set_cell_margins(cell, end=kwargs['right'])



doc = Document()
table = doc.add_table(rows=3, cols=3)

# 设置第一个单元格的边距
cell = table.cell(0, 0)
set_cell_margins(cell, top=0.5, start=0.5, bottom=0.5, end=0.5)

# 设置第二个单元格的边距（使用WPS样式的参数）
cell = table.cell(0, 1)
set_cell_margins(cell, top=0.3, left=0.3, bottom=0.3, right=0.3)

doc.save('table_with_custom_margins_cm.docx')