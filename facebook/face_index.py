from xml.dom.minidom import parse
from xml.dom.minidom import getDOMImplementation
import xml.etree.ElementTree as ET

import xml
path_name = "log.xml"
ss = ['label_len','sample_used','result','labels']
label_len = ss[0]
sample_used = ss[1]
result = ss[2]
labels = ss[3]

def creat_log(atts=None,samples=None):
    doc= xml.dom.minidom.Document()
    #创建一个根节点companys对象
    root=doc.createElement('train_log')
    print('添加的xml标签为：',root.tagName)

    #给根节点添加属性
    if atts is None:
        root.setAttribute('version','0')
    else:
        for att in atts:
            root.setAttribute(att[0],att[1])
    #将根节点添加到文档对象中
    doc.appendChild(root)
    if samples is None:
    #给根节点添加一个叶子节点
        company=doc.createElement('sample')
        new_sample = company
        new_sample.setAttribute('id',str(0))
        new_sample.setAttribute('label_length',str(1))
        new_sample.setAttribute('sample_used',str(0))
        new_sample.setAttribute('result','trainner.xml')
        new_sample.appendChild(doc.createTextNode('0,1'))
        #将company节点添加到根节点companys中
        root.appendChild(company)
    else:
        for sample in samples:
            root.appendChild(sample)
    #此处需要用codecs.open可以指定编码方式
    fp = open(path_name,'w')

    # fp=open(r'company.xml','w','utf-8')
    #将内存中的xml写入到文件
    doc.writexml(fp,indent='',addindent='\t',newl='\n',encoding='utf-8')
    fp.close()

def add_item_to_log(info):
    '''
    :param info: dictionary containing 'label_len'，'sample_used'，'result'，'labels' all are string
    :return:
    '''
    DOMTree=parse(path_name)
    #获取xml文档对象，就是拿到树的根
    root=DOMTree.documentElement
    samples = root.getElementsByTagName('sample')
    length = len(samples)
    root_version = int(root.getAttribute('version'))+1
    root.setAttribute('version',str(root_version))

    print('sample length:',length)
    sample = samples[length - 1]
    print(sample.nodeName)
    att = sample.getAttribute('id')
    id_now = int(att) + 1

    new_sample = DOMTree.createElement('sample')
    root.appendChild(new_sample)

    #给根节点添加属性
    new_sample.setAttribute('id',str(id_now))
    new_sample.setAttribute('label_length',info['label_len'])
    new_sample.setAttribute('sample_used',info['sample_used'])
    new_sample.setAttribute('result',info['result'])

    new_sample.appendChild(DOMTree.createTextNode(info['labels']))

    samples = root.getElementsByTagName('sample')
    creat_log([('version',str(root_version))],samples)
    # fp = open(file=path_name,mode = 'w',encoding='utf-8')
    # DOMTree.writexml(fp,newl='\n',encoding='utf-8')
    # fp.close()


'''
tree = ET.parse(path_name)
root = tree.getroot()
length = len(root)
print(length)
sample = root[length -1]
id_now = int(sample.attrib['id']) + 1
new_sample = ET.Element(sample.tag)
new_sample.attrib = sample.attrib
new_sample.attrib['id'] = str(id_now)
sub_node = ET.Element(sample[0].tag)
sub_node.text = '1,2,3'
new_sample.append(sub_node)
root.append(new_sample)
tree.write(path_name,pretty_print=True)

'''

if __name__=='__main__':
    add_item_to_log({label_len :'0',sample_used:'12',result:'train.xml',labels:'xxx'})