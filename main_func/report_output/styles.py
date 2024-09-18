# styles.py
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_ALIGN_PARAGRAPH, WD_LINE_SPACING


def modify_styles(doc):
    """修改内置的样式"""
    # 修改内置的 Heading 1 样式
    heading1 = doc.styles['Heading 1']
    heading1.font.name = 'Times New Roman'
    heading1._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    heading1.font.size = Pt(18)
    heading1.font.bold = True
    heading1.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    heading1.paragraph_format.space_before = Pt(12)
    heading1.paragraph_format.space_after = Pt(12)
    heading1.paragraph_format.line_spacing = 1.0

    # 修改内置的 Heading 2 样式
    heading2 = doc.styles['Heading 2']
    heading2.font.name = 'Times New Roman'
    heading2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    heading2.font.size = Pt(14)
    heading2.font.bold = True
    heading2.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    heading2.paragraph_format.space_before = Pt(6)
    heading2.paragraph_format.space_after = Pt(6)
    heading2.paragraph_format.line_spacing = 1.0

    # 修改内置的 Heading 3 样式
    heading3 = doc.styles['Heading 3']
    heading3.font.name = 'Times New Roman'
    heading3._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    heading3.font.size = Pt(12)
    heading3.font.bold = True
    heading3.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    heading3.paragraph_format.space_before = Pt(6)
    heading3.paragraph_format.space_after = Pt(6)
    heading3.paragraph_format.line_spacing = 1.0

    # 修改内置的 Header 样式
    header = doc.styles['Header']
    header.base_style = None
    header.font.name = 'Times New Roman'
    header._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    header.font.size = Pt(12)
    header.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header.paragraph_format.line_spacing = 1.0

    # 修改内置的 Footer 样式
    footer = doc.styles['Footer']
    footer.base_style = None
    footer.font.name = 'Times New Roman'
    footer._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    footer.font.size = Pt(10)
    footer.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.paragraph_format.line_spacing = 1.0


def create_custom_styles(doc):
    """创建自定义样式"""
    # 封面标题样式
    title_style = doc.styles.add_style('Title-1', 1)
    title_font = title_style.font
    title_font.name = 'Times New Roman'  # 设置字体
    title_font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    title_font.size = Pt(26)  # 字体大小
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 居中
    title_style.paragraph_format.line_spacing = 1  # 单倍行距

    # 封面表格样式
    cover_table_style = doc.styles.add_style('Cover_Table', 1)
    cover_table_font = cover_table_style.font
    cover_table_font.name = 'Times New Roman'
    cover_table_font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    cover_table_font.size = Pt(18)
    cover_table_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    cover_table_style.paragraph_format.line_spacing = 1
    cover_table_style.font.underline = True

    # 封面时间样式
    cover_time_style = doc.styles.add_style('Cover_Time', 1)
    cover_time_font = cover_time_style.font
    cover_time_font.name = 'Times New Roman'
    cover_time_font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    cover_time_font.size = Pt(18)
    cover_time_font.bold = True
    cover_time_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_time_style.paragraph_format.line_spacing = 1
    cover_time_style.paragraph_format.space_before = Pt(3.1)
    cover_time_style.paragraph_format.space_after = Pt(3.1)

    # 图片样式
    picture_style = doc.styles.add_style('Picture', 1)
    picture_font = picture_style.font
    picture_font.name = 'Times New Roman'  # 设置字体
    picture_font.size = Pt(12)  # 字体大小
    picture_paragraph_format = picture_style.paragraph_format
    picture_paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    picture_paragraph_format.line_spacing = 1  # 单倍行距

    # 图名样式
    pic_name_style = doc.styles.add_style('PictureName', 1)
    pic_name_font = pic_name_style.font
    pic_name_font.name = 'Times New Roman'
    title_font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    pic_name_font.size = Pt(10)
    pic_name_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic_name_style.paragraph_format.line_spacing = 1

    # 表格样式
    table_para_style = doc.styles.add_style('TableParagraph', 1)
    table_para_font = table_para_style.font
    table_para_font.name = 'Times New Roman'
    title_font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    table_para_font.size = Pt(12)
    table_para_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table_para_style.paragraph_format.line_spacing = 1






