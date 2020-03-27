
import sys
import json
from daetools import *

self, infile, matfile, outfile = sys.argv

with open(matfile) as fid:
	materials = json.load(fid)

def file2name(file):
	return ''.join([c if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" else "_" for c in file])

three2dae = {
	"diffuse":"diffuse",
	"normal":"bump",
	"specular":"specular",
	"emissive":"emission",
	"shininess":"shininess"
}

dae = Dae(infile)

dae.remove("asset/up_axis")
dae.remove("library_images")
dae.remove("library_effects")
dae.remove("library_materials")

dae.insertAfter("asset", "library_images")
dae.insertAfter("library_images", "library_effects")
dae.insertAfter("library_effects", "library_materials")

def cb(node, level):
	if node.tag == "geometry":
		name = node.get("name").split(".")[0]
		if name in materials:
			node.find("mesh").find("triangles").set("material", "MESH_MATERIAL_0")

	if node.tag == "instance_geometry":
		name = node.get("name").split(".")[0]
		if name in materials:
			bind = append(node, "bind_material")
			tech = append(bind, "technique_common")
			inst = append(bind, "instance_material")
			inst.set("symbol", "MESH_MATERIAL_0")
			inst.set("target", "#" + name + "_material")

	if node.tag == "library_images":
		imgs = set()
		for m in materials:
			mat = materials[m]
			for p in mat:
				prop = mat[p]
				if type(prop) == dict and "map" in prop:
					imgs.add(prop["map"])

		for img in imgs:
			imgnode = append(node, "image")
			name = file2name(img)
			imgnode.set("id", name)
			imgnode.set("name", name)
			initfrom = append(imgnode, "init_from")
			initfrom.text = img

	if node.tag == "library_effects":
		for m in materials:
			mat = materials[m]

			effect = append(node, "effect")
			effect.set("id", m + "_effect")
			profile = append(effect, "profile_COMMON")

			for p in mat:
				prop = mat[p]
				if type(prop) == dict and "map" in prop:
					img = prop["map"]
					name = file2name(img)

					newparam = append(profile, "newparam")
					newparam.set("sid", name + "_surface")
					surface = append(newparam, "surface")
					surface.set("type", "2D")
					init_from = append(surface, "init_from")
					init_from.text = name

					newparam = append(profile, "newparam")
					newparam.set("sid", name + "_sampler")
					sampler2d = append(newparam, "sampler2D")
					source = append(sampler2d, "source")
					source.text = name + "_surface"

			technique = append(profile, "technique")
			technique.set("sid", "common")
			phong = append(technique, "phong")
			for p in mat:
				prop = mat[p]
				proptag = append(phong, three2dae[p])
				if type(prop) == int or type(prop) == float:
					append(proptag, "float").text = str(prop)
				if type(prop) == dict:
					if "color" in prop:
						color = append(proptag, "color")
						color.set("sid", p)
						color.text = ' '.join([str(v) for v in prop["color"]])
					if "map" in prop:
						texture = append(proptag, "texture")
						texture.set("texture", file2name(prop["map"] + "_sampler"))
						texture.set("texcoord", "UVMap")
						if "wrap" in prop or "repeat" in prop or "offset" in prop:
							extra = append(texture, "extra")
							subtech = append(extra, "technique")
							if "wrap" in prop:
								append(subtech, "wrapU").text = str(prop["wrap"][0])
								append(subtech, "wrapV").text = str(prop["wrap"][1])
							if "repeat" in prop:
								append(subtech, "repeatU").text = str(prop["repeat"][0])
								append(subtech, "repeatV").text = str(prop["repeat"][1])
							if "offset" in prop:
								append(subtech, "offsetU").text = str(prop["offset"][0])
								append(subtech, "offsetV").text = str(prop["offset"][1])

	if node.tag == "library_materials":
		for m in materials:
			material = append(node, "material")
			material.set("id", m + "_material")
			append(material, "instance_effect").set("url", "#" + m + "_effect")

dae.recurse(cb)

dae.save(outfile)
