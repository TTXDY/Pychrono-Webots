import numpy as np
import random
import math

from controller import Supervisor


class WebotsBuilder:
    def __init__(self):
        self.master = Supervisor()
        self.timestep = int(self.master.getBasicTimeStep()) * 10
        print(self.timestep)

        self.master.getBasicTimeStep()
        self.root = self.master.getRoot()  

        print("root: ", self.root)
        self.rootChildren = self.root.getField("children")
        print("rootChildren: ", self.rootChildren)

    # 保存世界
    def saveWorld(self, path):
        self.master.worldSave(path)

    # 加载世界
    def loadWord(self, path):
        self.master.worldLoad(path)

    # 获取世界大小
    def setArena(self, lenth, width):
        arena = self.rootChildren.getMFNode(4)
        arena_lenth = arena.getField("floorSize")
        arena_lenth.setSFVec2f([lenth, width])

    # 获取世界大小
    def getArena(self):
        arena = self.rootChildren.getMFNode(4)
        arena_lenth = arena.getField("floorSize")
        x_y = arena_lenth.getSFVec2f()
        print(x_y)
        return x_y[0], x_y[1]

    # 更改世界属性  (包括重力、基础仿真步长、帧率等）
    def setWorld(self, gravity=9.81, CFM=1e-5, ERP=0.2, basicTimeStep=16, FPS=60):
        worldInfo = self.rootChildren.getMFNode(0)
        print(worldInfo)
        gravity_field = worldInfo.getField("gravity")
        cfm_field = worldInfo.getField("CFM")
        erp_field = worldInfo.getField("ERP")
        basicTimeStep_field = worldInfo.getField("basicTimeStep")
        fps_field = worldInfo.getField("FPS")

        gravity_field.setSFFloat(gravity)
        cfm_field.setSFFloat(CFM)
        erp_field.setSFFloat(ERP)
        basicTimeStep_field.setSFFloat(basicTimeStep)
        fps_field.setSFFloat(FPS)

    # 输入障碍物列表，随机生成各个障碍物的位置，并返回每个障碍物的新坐标
    def buildBox(self, box_list):
        # 设置随机种子
        # random.seed(seed)
        # np.random.seed(seed)

        box_handles = []  # 障碍物句柄列表
        coordinate_list = []  # 障碍物坐标列表

        # 获取各个障碍物的句柄
        for defname in box_list:
            print(self.master.getFromDef(defname))
            box_handles.append(self.master.getFromDef(defname))
        # 获取世界大小
        x, z = self.getArena()

        random_x = np.random.uniform(-x / 2.1, 0, 9)
        random_z = np.random.uniform(-z / 2.1, 0, 9)
        random_x = random_x.tolist()
        random_z = random_z.tolist()
        random_x_ = np.random.uniform(0, x / 2.1, 9)
        random_z_ = np.random.uniform(0, z / 2.1, 9)

        for i in range(9):
            random_x.append(random_x_[i])
            random_z.append(random_z_[i])
        np.random.shuffle(random_x)
        np.random.shuffle(random_z)
        for i in range(len(box_handles)):
            translation = box_handles[i].getField("translation")
            solid_translation = []
            solid_translation.append(random_x[i])
            solid_translation.append(0.1)
            solid_translation.append(random_z[i])
            print(solid_translation)
            translation.setSFVec3f(solid_translation)
            coordinate_list.append([random_x[i], 0.1, random_z[i]])

    def buildSlope(
        self,
        xyz,
        rad1,
        rad2,
        high,
        x_decay=2.2,
        h_decay=1.0,
        texture_image_path="",
        roughness=0.5,
        metalness=0.8,
    ):
        # xyz分别表示平面的长度、厚度、宽度，rad1表示上坡坡度，rad2表示下坡坡度，high表示平面高度,x_decay和h_decay分别是调整系数,用于弥合因路面厚度产生的误差
        # 建议x_decay取2~3,h_decay取0.99~1.01

        # 设置随机种子
        # random.seed(seed)
        # np.random.seed(seed)

        # base node 及其坐标句柄获取,获取整体坐标，如果用户需要该坐标可以直接得到
        base = "Base"
        base_node = self.master.getFromDef(base)
        # print("base: ", base_node)
        base_node_translation = base_node.getField("translation")
        base_xyz = base_node_translation.getSFVec3f()
        # print(base_xyz)

        # 坡道各组分以及各组分的shape的命名集合
        slope_consist = ["On", "Plane", "Down"]
        # slope_consist_shape = ['on_box', 'plane_box', 'down_box']

        # 坡道各组分以及各组分的形状的控制句柄集合
        slope_consist_handles = []
        slope_consist_shape_handles = []

        # 获取坡道各个组分的句柄
        for defname in slope_consist:
            # print("group: ", defname, self.master.getFromDef(defname))
            transform = self.master.getFromDef(defname)
            slope_consist_handles.append(transform)
            children = transform.getField("children")
            shape = children.getMFNode(0)
            slope_consist_shape_handles.append(shape)
        # 获取坡道各组分shape的句柄
        # for defname in slope_consist_shape:
        #     # print("group shape: ", defname, self.master.getFromDef(defname))
        #     slope_consist_shape_handles.append(self.master.getFromDef(defname))

        # 由用户给定的上坡坡度（rad1）、下坡坡度（rad2）、高度（high）、路面长度（x）、路面厚度（y）、路面宽度（z）
        # 计算各个组分各自的形状大小以及对应的坐标

        x = xyz[0]
        y = xyz[1]
        z = xyz[2]

        delta_x = np.tan(rad1) * y / 2.0  # 一个偏移量，用于弥合平面与两个坡道间因路面厚度而产生的缝隙

        # 计算三个组分各自的形状
        on_xyz = [high / np.sin(rad1), y, z]
        plane_xyz = [x + delta_x * x_decay, y, z]
        down_xyz = [high / np.sin(rad2), y, z]

        # 计算三个组分各自的坐标
        on_x_len = high / np.tan(rad1)
        down_x_len = high / np.tan(rad2)
        on_translation = [on_x_len / 2.0, high / 2.0, 0]
        plane_translation = [on_x_len + x / 2 + delta_x / 2, high * h_decay, 0]
        down_translation = [on_x_len + x + delta_x + down_x_len / 2.0, high / 2.0, 0]

        # 形状集合和坐标集合
        box_size_list = [on_xyz, plane_xyz, down_xyz]
        translation_list = [on_translation, plane_translation, down_translation]

        # 按计算出的坐标设置各个组分的位置
        for i in range(len(translation_list)):
            translation = slope_consist_handles[i].getField("translation")
            print("translation: ", translation_list[i])
            translation.setSFVec3f(translation_list[i])

        # 按计算出的形状大小设置各个组分的形状大小
        for i in range(len(box_size_list)):
            geometry = slope_consist_shape_handles[i].getField("geometry").getSFNode()
            size = geometry.getField("size")
            print("size: ", box_size_list[i])
            size.setSFVec3f(box_size_list[i])

        # 对于on 和 down,还需要设置它俩的坡度
        on_rotation = slope_consist_handles[0].getField("rotation")
        on_rotation.setSFRotation([0, 0, 1, rad1])
        down_rotation = slope_consist_handles[2].getField("rotation")
        down_rotation.setSFRotation([0, 0, 1, -rad2])

        for i in range(len(slope_consist_shape_handles)):
            shape_appearance = (
                slope_consist_shape_handles[i].getField("appearance").getSFNode()
            )
            shape_apperance_texture = shape_appearance.getField(
                "baseColorMap"
            ).getSFNode()
            shape_apperance_texture_url = shape_apperance_texture.getField("url")
            shape_apperance_texture_url.setMFString(0, texture_image_path)
            shape_appearance_roughness = shape_appearance.getField("roughness")
            shape_appearance_metalness = shape_appearance.getField("metalness")
            shape_appearance_roughness.setSFFloat(roughness)
            shape_appearance_metalness.setSFFloat(metalness)

    def buildStair(
        self,
        high,
        width,
        lenth,
        pattern=0,
        texture_image_path="",
        roughness=0.5,
        metalness=0.8,
    ):
        # high:每一层的层高； width：每一台阶的宽度；lenth：每一台阶的长度，pattern：模式（0：中间高两边低，1：一端高一端低）
        # 设置随机种子
        # random.seed(seed)
        # np.random.seed(seed)

        # base node 及其坐标句柄获取,获取整体坐标，如果用户需要该坐标可以直接得到
        base = "Base"
        base_node = self.master.getFromDef(base)
        # print("base: ", base_node)
        base_node_translation = base_node.getField("translation")
        base_xyz = base_node_translation.getSFVec3f()
        # print(base_xyz)

        # 坡道各组分以及各组分的shape的命名集合
        stair_consist = [
            "Stair1",
            "Stair2",
            "Stair3",
            "Stair4",
            "Stair5",
            "Stair6",
            "Stair7",
        ]
        # stair_consist_shape = ['stair1_box', 'stair2_box', 'stair3_box', 'stair4_box', 'stair5_box', 'stair6_box', 'stair7_box']

        # 坡道各组分以及各组分的形状的控制句柄集合
        stair_consist_handles = []
        stair_consist_shape_handles = []

        # 获取坡道各个组分的句柄
        for defname in stair_consist:
            print("group: ", defname, self.master.getFromDef(defname))
            transform = self.master.getFromDef(defname)
            stair_consist_handles.append(transform)
            children = transform.getField("children")
            shape = children.getMFNode(0)
            stair_consist_shape_handles.append(shape)

        # 获取坡道各组分shape的句柄
        # for defname in stair_consist_shape:
        #     print("group shape: ", defname, self.master.getFromDef(defname))
        #     stair_consist_shape_handles.append(self.master.getFromDef(defname))
        x = width / 2.0
        y = high / 2.0

        if pattern == 0:  # 中间高，两端低
            translation_list = [
                [x, y, 0],
                [x + width, y + high / 2.0, 0],
                [x + 2 * width, y + high, 0],
                [x + 3 * width, y + high * 3 / 2.0, 0],
                [x + 4 * width, y + high, 0],
                [x + 5 * width, y + high / 2.0, 0],
                [x + 6 * width, y, 0],
            ]
            size_list = [
                [width, high, lenth],
                [width, high * 2, lenth],
                [width, high * 3, lenth],
                [width, high * 4, lenth],
                [width, high * 3, lenth],
                [width, high * 2, lenth],
                [width, high, lenth],
            ]

        else:  # 一端高，一端低
            translation_list = [
                [x, y, 0],
                [x + width, y + high / 2.0, 0],
                [x + 2 * width, y + high, 0],
                [x + 3 * width, y + high * 3 / 2.0, 0],
                [x + 4 * width, y + high * 2, 0],
                [x + 5 * width, y + high * 5 / 2.0, 0],
                [x + 6 * width, y + high * 3, 0],
            ]
            size_list = [
                [width, high, lenth],
                [width, high * 2, lenth],
                [width, high * 3, lenth],
                [width, high * 4, lenth],
                [width, high * 5, lenth],
                [width, high * 6, lenth],
                [width, high * 7, lenth],
            ]
        for i in range(len(stair_consist_handles)):
            translation = stair_consist_handles[i].getField("translation")
            print("translation: ", translation_list[i])
            translation.setSFVec3f(translation_list[i])
        for i in range(len(stair_consist_shape_handles)):
            geometry = stair_consist_shape_handles[i].getField("geometry").getSFNode()
            size = geometry.getField("size")
            print("size: ", size_list[i])
            size.setSFVec3f(size_list[i])

        for i in range(len(stair_consist_shape_handles)):
            shape_appearance = (
                stair_consist_shape_handles[i].getField("appearance").getSFNode()
            )
            shape_apperance_texture = shape_appearance.getField(
                "baseColorMap"
            ).getSFNode()
            shape_apperance_texture_url = shape_apperance_texture.getField("url")
            shape_apperance_texture_url.setMFString(0, texture_image_path)
            shape_appearance_roughness = shape_appearance.getField("roughness")
            shape_appearance_metalness = shape_appearance.getField("metalness")
            shape_appearance_roughness.setSFFloat(roughness)
            shape_appearance_metalness.setSFFloat(metalness)

    def buildDitch(
        self,
        high,
        width,
        lenth,
        separation_distance,
        texture_image_path="",
        roughness=0.5,
        metalness=0.8,
    ):
        # high:每一渠的深度； width：渠梁的宽度；lenth：每一渠的长度，separation_distance：每一渠间的间隔
        # 设置随机种子
        # random.seed(seed)
        # np.random.seed(seed)

        # base node 及其坐标句柄获取,获取整体坐标，如果用户需要该坐标可以直接得到
        base = "Base"
        base_node = self.master.getFromDef(base)
        # print("base: ", base_node)
        base_node_translation = base_node.getField("translation")
        base_xyz = base_node_translation.getSFVec3f()
        # print(base_xyz)

        # 坡道各组分以及各组分的shape的命名集合
        ditch_consist = [
            "Ditch1",
            "Ditch2",
            "Ditch3",
            "Ditch4",
            "Ditch5",
            "Ditch6",
            "Ditch7",
        ]
        # ditch_consist_shape = ['ditch1_box', 'ditch2_box', 'ditch3_box', 'ditch4_box', 'ditch5_box', 'ditch6_box', 'ditch7_box']

        # 坡道各组分以及各组分的形状的控制句柄集合
        ditch_consist_handles = []
        ditch_consist_shape_handles = []

        # 获取坡道各个组分的句柄
        for defname in ditch_consist:
            print("group: ", defname, self.master.getFromDef(defname))
            transform_node = self.master.getFromDef(defname)
            ditch_consist_handles.append(transform_node)
            children = transform_node.getField("children")
            shape = children.getMFNode(0)
            ditch_consist_shape_handles.append(shape)

        # 获取坡道各组分shape的句柄
        # for defname in ditch_consist_shape:
        #     print("group shape: ", defname, self.master.getFromDef(defname))
        #     ditch_consist_shape_handles.append(self.master.getFromDef(defname))

        x = width / 2.0
        y = high / 2.0

        translation_list = [
            [x, y, 0],
            [x + width + separation_distance, y, 0],
            [x + 2 * (width + separation_distance), y, 0],
            [x + 3 * (width + separation_distance), y, 0],
            [x + 4 * (width + separation_distance), y, 0],
            [x + 5 * (width + separation_distance), y, 0],
            [x + 6 * (width + separation_distance), y, 0],
        ]
        size_list = [
            [width, high, lenth],
            [width, high, lenth],
            [width, high, lenth],
            [width, high, lenth],
            [width, high, lenth],
            [width, high, lenth],
            [width, high, lenth],
        ]

        for i in range(len(ditch_consist_handles)):
            translation = ditch_consist_handles[i].getField("translation")
            print("translation: ", translation_list[i])
            translation.setSFVec3f(translation_list[i])

        for i in range(len(ditch_consist_shape_handles)):
            geometry = ditch_consist_shape_handles[i].getField("geometry").getSFNode()
            size = geometry.getField("size")
            print("size: ", size_list[i])
            size.setSFVec3f(size_list[i])

        for i in range(len(ditch_consist_shape_handles)):
            shape_appearance = (
                ditch_consist_shape_handles[i].getField("appearance").getSFNode()
            )
            shape_apperance_texture = shape_appearance.getField(
                "baseColorMap"
            ).getSFNode()
            shape_apperance_texture_url = shape_apperance_texture.getField("url")
            shape_apperance_texture_url.setMFString(0, texture_image_path)
            shape_appearance_roughness = shape_appearance.getField("roughness")
            shape_appearance_metalness = shape_appearance.getField("metalness")
            shape_appearance_roughness.setSFFloat(roughness)
            shape_appearance_metalness.setSFFloat(metalness)

    def buildRough(
        self,
        size=24,
        a_height=0.1,
        b_height=0.08,
        c_height=0.05,
        pattern=0,
        texture_image_path="",
        roughness=0.5,
        metalness=0.8,
    ):
        # seed:随机种子， size：方形区域的边长， a_height\b_height\c_height均为控制随机地形高度的参数，所占权重逐渐减少
        # pattern提供两种随机生成高度的模式，0代表普通模式，按顺序设置；1代表一种稳健的模式，节点个数为3的倍数可以使用，以九宫格的形式进行生成
        rough_shape = self.master.getFromDef("Rough")
        rough_shape_geometry_node = rough_shape.getField("geometry").getSFNode()
        rough_height_field = rough_shape_geometry_node.getField("height")

        # elevationGrid节点相关属性
        rough_xDimension_field = rough_shape_geometry_node.getField("xDimension")
        rough_xSpacing_field = rough_shape_geometry_node.getField("xSpacing")
        rough_zDimension_field = rough_shape_geometry_node.getField("zDimension")
        rough_zSpacing_field = rough_shape_geometry_node.getField("zSpacing")
        rough_thickness_field = rough_shape_geometry_node.getField("thickness")

        rough_size = size * size
        x = rough_xDimension_field.getSFInt32()
        y = rough_zDimension_field.getSFInt32()
        old_rough_size = x * y
        rough_xDimension_field.setSFInt32(size)
        rough_zDimension_field.setSFInt32(size)
        if x * y != rough_size:
            self.clearRough(rough_shape, old_rough_size)
            self.initRough(rough_shape, rough_size)

        # 设置各个节点的高度
        List = [[0 for i in range(size)] for j in range(size)]

        if pattern == 0:
            a = random.uniform(0, a_height)
            for i in range(size):
                for j in range(size):
                    b = random.uniform(0, b_height)
                    c = random.uniform(-c_height, c_height)
                    List[i][j] = a + b + c
        else:
            a = random.uniform(0, a_height)
            size_6 = int(size / 6)
            for i in range(6):
                for j in range(6):
                    b = random.uniform(0, b_height)
                    for k in range(size_6):
                        for l in range(size_6):
                            c = random.uniform(-c_height, c_height)
                            List[i * size_6 + k][j * size_6 + l] = a + b + c

        for i in range(size):
            for j in range(size):
                rough_height_field.setMFFloat(i * size + j, List[i][j])

        for i in range(rough_size):
            if (
                i <= size - 1
                or i % size == 0
                or (i + 1) % size == 0
                or i >= rough_size - size
            ):
                rough_height_field.setMFFloat(i, 0)

        rough_shape_appearance = rough_shape.getField("appearance").getSFNode()
        rough_shape_apperance_texture = rough_shape_appearance.getField(
            "baseColorMap"
        ).getSFNode()
        rough_shape_apperance_texture_url = rough_shape_apperance_texture.getField(
            "url"
        )
        rough_shape_apperance_texture_url.setMFString(0, texture_image_path)
        rough_shape_appearance_roughness = rough_shape_appearance.getField("roughness")
        rough_shape_appearance_metalness = rough_shape_appearance.getField("metalness")
        rough_shape_appearance_roughness.setSFFloat(roughness)
        rough_shape_appearance_metalness.setSFFloat(metalness)

    def clearRough(self, shape_node, rough_size):
        # size需要大于elevationGrid中的节点总数（一般最大为xD*zD）
        # rough_shape = self.master.getFromDef('Rough')
        rough_shape_geometry_node = shape_node.getField("geometry").getSFNode()
        rough_height_field = rough_shape_geometry_node.getField("height")
        for i in range(rough_size):
            rough_height_field.removeMF(0)

    def initRough(self, shape_node, rough_size):
        # rough_shape = self.master.getFromDef('Rough')
        rough_shape_geometry_node = shape_node.getField("geometry").getSFNode()
        rough_height_field = rough_shape_geometry_node.getField("height")
        # 初始化，设置elevationGrid对应节点数目
        for i in range(rough_size):
            rough_height_field.insertMFFloat(0, 0)

    def buildHilly(
        self,
        hilly_size,
        montain_num,
        average_height,
        hilly_height,
        texture_image_path="",
        roughness=0.5,
        metalness=0.8,
    ):
        # hilly_size:丘陵地形的边长，montain_num：区域中小山的数量，
        # average_height：基础高度，类比于崎岖地形， hilly_height：小山的最大高度
        hilly_shape = self.master.getFromDef("Hilly")
        hilly_shape_geometry_node = hilly_shape.getField("geometry").getSFNode()
        hilly_height_field = hilly_shape_geometry_node.getField("height")

        hilly_xDimension_field = hilly_shape_geometry_node.getField("xDimension")
        hilly_xSpacing_field = hilly_shape_geometry_node.getField("xSpacing")
        hilly_zDimension_field = hilly_shape_geometry_node.getField("zDimension")
        hilly_zSpacing_field = hilly_shape_geometry_node.getField("zSpacing")
        hilly_thickness_field = hilly_shape_geometry_node.getField("thickness")

        size = hilly_size * hilly_size
        x = hilly_xDimension_field.getSFInt32()
        y = hilly_zDimension_field.getSFInt32()
        old_size = x * y
        hilly_xDimension_field.setSFInt32(hilly_size)
        hilly_zDimension_field.setSFInt32(hilly_size)
        if x * y != size:
            self.clearRough(hilly_shape, old_size)
            self.initRough(hilly_shape, size)

        montain_list = []

        for i in range(montain_num):
            montain = random.randint(hilly_size * 4, hilly_size * (hilly_size - 4))
            montain_list.append(montain)

        t = 0
        montain_list.sort()

        for i in range(hilly_size * hilly_size):
            hilly_height_field.setMFFloat(i, 0)
            if (
                i > hilly_size - 1
                and i % hilly_size != 0
                and (i + 1) % hilly_size != 0
                and i < hilly_size * hilly_size - hilly_size
            ):
                ret = random.uniform(0, average_height)
                hilly_height_field.setMFFloat(i, ret)
                if t < len(montain_list) and i == montain_list[t]:
                    t += 1
                    hilly_height_field.setMFFloat(
                        i, random.uniform(hilly_height / 2.0, hilly_height)
                    )

        hilly_shape_appearance = hilly_shape.getField("appearance").getSFNode()
        hilly_shape_apperance_texture = hilly_shape_appearance.getField(
            "baseColorMap"
        ).getSFNode()
        hilly_shape_apperance_texture_url = hilly_shape_apperance_texture.getField(
            "url"
        )
        hilly_shape_apperance_texture_url.setMFString(0, texture_image_path)
        hilly_shape_appearance_roughness = hilly_shape_appearance.getField("roughness")
        hilly_shape_appearance_metalness = hilly_shape_appearance.getField("metalness")
        hilly_shape_appearance_roughness.setSFFloat(roughness)
        hilly_shape_appearance_metalness.setSFFloat(metalness)

    def buildPit(
        self,
        x,
        y,
        z,
        xDimension,
        zDimension,
        randomSeed=1,
        perlinNOctaves=3,
        noiseAmplitude=0.15,
        pitRadius=3,
        texture_image_path="",
        roughness=0.5,
        metalness=0.8,
    ):
        pit_shape_node = self.master.getFromDef("Pit")
        # pit_children_field = pit.getField('children')
        # pit_shape = pit_children_field.getMFNode(0)
        # pit_shape_geometry_node = pit_shape.getField('geometry').getSFNode()

        pit_size = pit_shape_node.getField("size")
        pit_x = pit_shape_node.getField("xDimension")
        pit_z = pit_shape_node.getField("zDimension")
        pit_randomSeed = pit_shape_node.getField("randomSeed")
        pit_perlinNOctaves = pit_shape_node.getField("perlinNOctaves")
        pit_noiseAmplitude = pit_shape_node.getField("noiseAmplitude")
        pit_pitRadius = pit_shape_node.getField("pitRadius")
        # pit_xSpace = pit_shape_geometry_node.getField('xSpacing')
        # pit_zSpace = pit_shape_geometry_node.getField('zSpacing')

        # xDimension = np.random.randint(37,43)
        # zDimension = np.random.randint(37,43)
        pit_size.setSFVec3f([x, y, z])
        pit_x.setSFInt32(xDimension)
        pit_z.setSFInt32(zDimension)
        pit_randomSeed.setSFInt32(randomSeed)
        pit_perlinNOctaves.setSFInt32(perlinNOctaves)
        pit_noiseAmplitude.setSFFloat(noiseAmplitude)
        pit_pitRadius.setSFFloat(pitRadius)
        # pit_xSpace.setSFFloat(10.0/x)
        # pit_zSpace.setSFFloat(10.0/z)

        pit_appearance = pit_shape_node.getField("appearance").getSFNode()
        pit_apperance_texture = pit_appearance.getField("baseColorMap").getSFNode()
        pit_apperance_texture_url = pit_apperance_texture.getField("url")
        pit_apperance_texture_url.setMFString(0, texture_image_path)
        pit_appearance_roughness = pit_appearance.getField("roughness")
        pit_appearance_metalness = pit_appearance.getField("metalness")
        pit_appearance_roughness.setSFFloat(roughness)
        pit_appearance_metalness.setSFFloat(metalness)

    def buildFrom3DModel(
        self, obj_path, texture_image_path, roughness=0.5, metalness=0
    ):
        terrain = self.master.getFromDef("terrain_3Dmodel")
        terrain_shape = self.master.getFromDef("terrain_shape")

        terrain_shape_appearance = terrain_shape.getField("appearance").getSFNode()
        # terrain_shape_appearance_texture = terrain_shape_appearance.getField('texture').getSFNode()
        terrain_shape_appearance_texture = terrain_shape_appearance.getField(
            "baseColorMap"
        ).getSFNode()
        terrain_shape_appearance_texture_url = (
            terrain_shape_appearance_texture.getField("url")
        )
        # print("1: ", terrain_shape_appearance_texture_url.getSFString())
        # print("2: ", terrain_shape_appearance_texture_url.getMFString(0))
        terrain_shape_appearance_texture_url.setMFString(0, texture_image_path)

        terrain_shape_geometry = terrain_shape.getField("geometry").getSFNode()
        terrain_shape_geometry_url = terrain_shape_geometry.getField("url")
        # print("3: ", terrain_shape_geometry_url.getSFString())
        # print("4: ", terrain_shape_geometry_url.getMFString(0))
        terrain_shape_geometry_url.setMFString(0, obj_path)

        terrain_shape_appearance_roughness = terrain_shape_appearance.getField(
            "roughness"
        )
        terrain_shape_appearance_metalness = terrain_shape_appearance.getField(
            "metalness"
        )
        print(terrain_shape_appearance_metalness)
        terrain_shape_appearance_roughness.setSFFloat(roughness)
        terrain_shape_appearance_metalness.setSFFloat(metalness)
        # print(terrain)
        # print(terrain.exportString())

    def reset(self):
        self.master.simulationReset()  # 重置环境
        self.master.step(self.timestep)
