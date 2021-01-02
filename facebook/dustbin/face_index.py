from xml.dom import minidom
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
import lxml.etree as LET
import xml
import os

path_name = 'log.xml'
ss = ['label_len', 'sample_used', 'result', 'labels']
label_len = ss[0]
sample_used = ss[1]
result = ss[2]
labels = ss[3]


def path_reslove(path_name):
    currnet_path = os.path.abspath(__file__)
    if not os.path.exists(path_name):
        path_name = r'.//facebook//'+ path_name
    if not os.path.exists(path_name):
        raise FileNotFoundError
    return path_name

def creat_log(atts=None, samples=None):
    doc = xml.dom.minidom.Document()
    # 创建一个根节点companys对象
    root = doc.createElement('train_log')
    print('添加的xml标签为：', root.tagName)

    # 给根节点添加属性
    if atts is None:
        root.setAttribute('version', '0')
    else:
        for att in atts:
            root.setAttribute(att[0], att[1])
    # 将根节点添加到文档对象中
    doc.appendChild(root)
    if samples is None:
        # 给根节点添加一个叶子节点
        company = doc.createElement('sample')
        new_sample = company
        new_sample.setAttribute('id', str(0))
        new_sample.setAttribute('label_length', str(1))
        new_sample.setAttribute('sample_used', str(0))
        new_sample.setAttribute('result', 'trainner.xml')
        new_sample.appendChild(doc.createTextNode('0,1'))
        # 将company节点添加到根节点companys中
        root.appendChild(company)
    else:
        for sample in samples:
            root.appendChild(sample)
    # 此处需要用codecs.open可以指定编码方式
    path_name2 = path_reslove(path_name)
    fp = open(path_name2, 'w')

    # fp=open(r'company.xml','w','utf-8')
    # 将内存中的xml写入到文件
    doc.writexml(fp, indent='', addindent='\t', newl='\n', encoding='utf-8')
    fp.close()


def add_item_to_log(info) -> None:
    '''
    :param info: dictionary containing 'label_len'，'sample_used'，'result'，'labels' all are string
    :return:
    '''
    path_name2 = path_reslove(path_name)
    DOMTree = parse(path_name)
    # 获取xml文档对象，就是拿到树的根
    root = DOMTree.documentElement
    samples = root.getElementsByTagName('sample')
    length = len(samples)
    root_version = int(root.getAttribute('version')) + 1
    root.setAttribute('version', str(root_version))

    print('sample length:', length)
    sample = samples[length - 1]
    print(sample.nodeName)
    att = sample.getAttribute('id')
    id_now = int(att) + 1

    new_sample = DOMTree.createElement('sample')
    root.appendChild(new_sample)

    # 给根节点添加属性
    new_sample.setAttribute('id', str(id_now))
    new_sample.setAttribute('label_length', info['label_len'])
    new_sample.setAttribute('sample_used', info['sample_used'])
    new_sample.setAttribute('result', info['result'])

    new_sample.appendChild(DOMTree.createTextNode(info['labels']))

    samples = root.getElementsByTagName('sample')
    creat_log([('version', str(root_version))], samples)


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
info_path = 'info.xml'
''' <face photo="photo1.png" name="PM" label="0"/>'''


def find_label(name):
    '''
    :param name: face name
    :return: label[int], -1 for not found
    '''
    info_path2 = path_reslove(info_path)
    tree = ET.parse(info_path2)
    root = tree.getroot()
    for item in root:
        if item.attrib['name'] == name:
            return int(item.attrib['label'])
    return -1


def find_name(label):
    """
    find a face name by a label
    :param label: [int],[string]
    :return: [OK, face_name]
    """
    label = str(label)
    info_path2=path_reslove(info_path)
    tree = ET.parse(info_path2)
    root = tree.getroot()
    length = len(root)
    print(length)
    for item in root:
        if item.attrib['label'] == label:
            return [True, (item.attrib['name'])]
    return [False, None]


def add_label_name(label, name):
    label = str(label)
    info_path2= path_reslove(info_path)
    tree = LET.parse(info_path2)
    root = tree.getroot()
    for item in root:
        if item.attrib['label'] == label:
            raise Exception('label already exist')
    length = len(root) + 1
    new_sample = LET.Element('face')
    new_sample.attrib['label'] = label
    new_sample.attrib['name'] = name
    root.append(new_sample)
    root.attrib['size']=str(length)
    LET.indent(root)
    tree.write(info_path)
    # doc = minidom.parseString(LET.tostring(tree)).toprettyxml()
    # print(doc)
    # fp = open(info_path, 'w')
    # fp.write(doc)
    # # fp=open(r'company.xml','w','utf-8')
    # # 将内存中的xml写入到文件
    # # doc.writexml(fp, indent='', addindent='\t', newl='\n', encoding='utf-8')
    # fp.close()


if __name__ == '__main__':
    add_label_name(2,'pm2')
    # add_item_to_log({label_len: '0', sample_used: '12', result: 'train.xml', labels: 'xxx'})
