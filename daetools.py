
import xml.etree.ElementTree as xml
import xml.dom.minidom as minidom
import re

#xml.register_namespace("", "")

def deslash(nodes):
	if type(nodes) == str:
		return nodes.split("/")
	else:
		return nodes

def stripns(node, level):
	if node.tag[0] == "{":
		node.tag = node.tag.split("}")[1]

append = xml.SubElement

class Dae:
	def __init__(self, file):
		self.tree = xml.parse(file)
		self.root = self.tree.getroot()
		self.recurse(stripns)

	def save(self, file):
		#self.tree.write(file, encoding='utf-8', xml_declaration=True)
		ugly = xml.tostring(self.root, encoding='utf8', method='xml').decode("utf-8")
		ugly = re.sub(r"\r?\n\t* *", "", ugly)
		nice = minidom.parseString(ugly).toprettyxml()
		with open(file, "w") as fid:
			fid.write(nice)

	def path(self, nodes):
		elem = self.root
		for n in deslash(nodes):
			elem = elem.find(n)
			if elem == None:
				break
		return elem

	def remove(self, nodes):
		nodes = deslash(nodes)
		try:
			self.path(nodes[:-1]).remove(self.path(nodes))
		except:
			pass

	def append(self, nodes):
		nodes = deslash(nodes)
		elem = xml.SubElement(self.path(nodes[:-1]), nodes[-1])
		return elem

	def insertAfter(self, nodes, node):
		nodes = deslash(nodes)
		parent = self.path(nodes[:-1])
		index = parent.getchildren().index(self.path(nodes))
		elem = xml.Element(node)
		parent.insert(index+1, elem)
		return elem

	def insertBefore(self, nodes, node):
		nodes = deslash(nodes)
		parent = self.path(nodes[:-1])
		index = parent.getchildren().index(self.path(nodes))
		elem = xml.Element(node)
		parent.insert(index, elem)

	def recurse(self, callback, elem = None, level = 0):
		if level == 0:
			elem = self.root
		callback(elem, level)
		for child in elem:
			self.recurse(callback, child, level+1)
