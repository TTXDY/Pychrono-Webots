import numpy as np
from TerrainChrono import Terrain_Pychrono, get_obj_dimensions



Obj_file_path = "D:/sunjieqiang/sucai/test/nihao.obj"
Texture_file_path = "D:/sunjieqiang/sucai/test/1.jpg"
Noise_file_path = "D:/sunjieqiang/sucai/test/3.jpg"
Terrain_Pychrono(
    IsCarSystem=True,
    dimensions= get_obj_dimensions(Obj_file_path),
    noise_path=Noise_file_path,
    texture_path=Texture_file_path,
    obj_path=Obj_file_path,
    terrain_para=[[1724.69e3, 16.43e3, 0.2, 68.95e3, 20, 0.6e-2, 4e8, 3e4],[66.08e3, 10.55e3, 1.44, 6e3, 20.7, 3e-2, 4e8, 3e4],
    ],
).Run()
