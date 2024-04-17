from Build.TerrainWebots import WebotsBuilder
import time
import numpy as np

seed = 10
builder = WebotsBuilder()
print("hello, ", builder)

path = "E:\\webots_projects\\TerrainBuilder\\worlds"
terrainName = "randomBox"
absloutePath = path + "\\" + terrainName


builder.setArena(40.0, 40.0)
builder.getArena()
builder.setWorld()
# buildBox, buildSlope, buildStair, buildDitch, buildRough, buildHilly, buildPit,buildTerrainFrom3DModel
choose = "buildDitch"


if choose == "buildBox":
    print("buildBox")
    box_list = [
        "Box1",
        "Box2",
        "Box3",
        "Box4",
        "Box5",
        "Box6",
        "Box7",
        "Box8",
        "Box9",
        "Box10",
    ]

    for i in range(200):
        builder.reset()
        builder.buildBox(box_list)
        builder.master.step(builder.timestep * 2)
        time.sleep(0.5)

elif choose == "buildSlope":
    print("buildSlope")
    for seed in range(200):
        builder.reset()
        xyz = [2.0, 0.05, 2.0]
        print(xyz)
        rad1 = 0.2
        rad2 = 0.2
        high_slope = 0.5
        x_decay = 2.0
        h_decay = 0.990
        high = high_slope
        builder.buildSlope(
            xyz,
            rad1,
            rad2,
            high,
            x_decay,
            h_decay,
            texture_image_path="",
            roughness=0.2,
            metalness=0.8,
        )
        builder.master.step(builder.timestep * 2)
        time.sleep(0.5)
elif choose == "buildStair":
    print("buildStair")
    for seed in range(200):
        builder.reset()
        width_stair = np.random.uniform(1, 4, 1)
        high_stair = np.random.uniform(0.01, 1, 1)
        lenth_stair = np.random.uniform(1, 10, 1)
        pattern_stair = np.random.randint(0, 2, 1)
        high = high_stair
        width = width_stair
        lenth = lenth_stair
        pattern = pattern_stair
        builder.buildStair(
            high,
            width,
            lenth,
            pattern,
            texture_image_path="",
            roughness=0.2,
            metalness=0.8,
        )
        builder.master.step(builder.timestep * 2)
        time.sleep(0.5)

elif choose == "buildDitch":
    print("buildDitch")
    for seed in range(200):
        builder.reset()
        width_ditch = np.random.uniform(0.5, 1, 1)
        high_ditch = np.random.uniform(0.01, 0.5, 1)
        lenth_ditch = np.random.uniform(5, 10, 1)
        distance_ditch = np.random.uniform(0.5, 1, 1)
        builder.buildDitch(
            high_ditch,
            width_ditch,
            lenth_ditch,
            distance_ditch,
            texture_image_path="",
            roughness=0.2,
            metalness=0.8,
        )
        builder.master.step(builder.timestep * 2)
        time.sleep(0.5)
elif choose == "buildRough":
    print("buildRough")
    for seed in range(200):
        builder.reset()
        print(seed)
        a = 0.10
        b = 0.05
        c = 0.01
        size = 24
        builder.buildRough(
            size,
            a,
            b,
            c,
            0,
            texture_image_path="",
            roughness=0.2,
            metalness=0.8,
        )
        builder.master.step(builder.timestep * 2)
        time.sleep(1)
elif choose == "buildHilly":
    print("buildHilly")
    for seed in range(200):
        builder.reset()
        print(seed)
        bianchang = 24
        montainNum = 0
        minHeight = 0.01
        maxHeight = 1.0
        builder.buildHilly(
            bianchang,
            montainNum,
            minHeight,
            maxHeight,
            texture_image_path="",
            roughness=0.2,
            metalness=0.8,
        )
        builder.master.step(builder.timestep * 2)
        time.sleep(0.5)

elif choose == "buildPit":
    print("buildPit")
    for seed in range(200):
        builder.reset()
        print(seed)
        xx = np.random.randint(10, 20)
        yy = np.random.randint(3, 7)
        zz = np.random.randint(10, 20)
        xDimension = np.random.randint(10, 40)
        zDimension = np.random.randint(10, 40)
        builder.buildPit(
            xx,
            yy,
            zz,
            xDimension,
            zDimension,
            randomSeed=3,
            texture_image_path="",
            roughness=0.2,
            metalness=0.8,
        )
        builder.master.step(builder.timestep * 2)
        time.sleep(0.5)

elif choose == "buildTerrainFrom3DModel":
    print("buildTerrainFrom3DModel")
    builder.buildFrom3DModel("D:/sunjieqiang/sucai/test/2.obj","D:/sunjieqiang/sucai/test/er.jpg",0.00,0.00)
