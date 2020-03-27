# SkinCollada
Apply materials to Collada files so they can be used with three.js.

## Usage
Create all your meshes in Blender, assign names to them (in the mesh browser) and export them as a Collada (.dae) file. Then create a json file specifying the material for each mesh:

```json
{
	"myMesh":{
		"diffuse":{"color":[1, 0, 0, 1], "map":"myDiffuseMap.png", "repeat":[3, 3], "wrap":[1, 1], "offset":[0.5, 0.5]},
		"normal":{"map":"myNormalMap.png", "repeat":[3, 3], "wrap":[1, 1], "offset":[0.5, 0.5]},
		"specular":{"color":[1, 1, 1, 1], "map":"mySpecularMap.png"},
		"emissive":{"color":[0, 1, 0, 1], "map":"myEmissiveMap.png", "repeat":[3, 3], "wrap":[1, 1], "offset":[0.5, 0.5]},
	},
	"myOtherMesh":{
		"diffuse":{"color":[1, 0, 0, 1], "map":"myOtherDiffuseMap.png", "repeat":[3, 3], "wrap":[1, 1], "offset":[0.5, 0.5]},
		"normal":{"map":"myOtherNormalMap.png", "repeat":[3, 3], "wrap":[1, 1], "offset":[0.5, 0.5]},
		"specular":{"color":[1, 1, 1, 1], "map":"myOtherSpecularMap.png"},
		"emissive":{"color":[0, 1, 0, 1], "map":"myOtherEmissiveMap.png", "repeat":[3, 3], "wrap":[1, 1], "offset":[0.5, 0.5]},
	}
}
```

Notes:

* You can omit any of the fields and three.js will use the default.
* If you use the same texture for different meshes, it will be referenced only once in the <library_images> section of the collada file.
* For a material, three.js only allows one set of repeat/offset values and ignores the rest.
* If you copy a mesh in blender, it will be automatically be named like "myMesh.001", "myMesh.002" and so on. This project ignores the ".###" suffix completely and will regard all of them as "myMesh" so if you want to assign a different material to the copies, you have to rename them.

Then run

```
python skincollada.py myBlenderMesh.dae myMaterials.json myResult.dae
```

or if you want to try the example:

```
python skincollada.py exampe/blender.dae example/materials.json example/result.dae
```

The (somewhat ugly because I didn't put any effort into it) result can be seen here: https://mqnc.github.io/skincollada/example/view.html

Now you can use the resulting beautifully skinned collada file in your three.js (or other) projects.

### Enjoy!
