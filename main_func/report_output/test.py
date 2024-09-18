from docx import Document

#打开word文档
document = Document('test1.docx')

#获取所有段落
all_paragraphs = document.paragraphs
count = 1
for paragraph in all_paragraphs:
    # 打印每一个段落的文字
    print(paragraph.text + str(count))
    count += 1
    # 循环读取每个段落里的run内容
    # for run in paragraph.runs:
    #     print(run.text) #打印run内容
