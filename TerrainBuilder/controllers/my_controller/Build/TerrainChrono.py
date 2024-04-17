import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as irr
import math
import random
import cv2
import numpy as np
from PIL import Image
import os

the_current_dir = os.path.dirname(os.path.abspath(__file__))
print(the_current_dir)


# from utils.util import Soil_Params
def ReImage(image_path):
    original_image = Image.open(image_path)
    # 创建一个新的镜像图像
    mirrored_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
    # 右旋转镜像图像
    rotated_image = mirrored_image.transpose(Image.ROTATE_270)
    result_path = the_current_dir + r"\image\texture.jpg"
    # 保存镜像并左旋转后的图像
    rotated_image.save(result_path)
    return result_path


# print(ReImage(r"c:\Users\Administrator\Downloads\v.jpg"))


# =============================================================================
class MySoilParams(veh.SoilParametersCallback):
    def __init__(self, noise_path, dim, terrain_para):
        veh.SoilParametersCallback.__init__(self)
        self.a = int(dim[0]) / 2
        self.b = int(dim[1]) / 2
        print(self.a)
        print(self.b)
        # terr_opt = [
        #     [1724.69e3, 16.43e3, 0.2, 68.95e3, 20, 0.6e-2, 4e8, 3e4],
        #     [66.08e3, 10.55e3, 1.44, 6e3, 20.7, 3e-2, 4e8, 3e4],
        # ]
        terr_opt = terrain_para
        print(terr_opt)
        xxx = 4096 * int(self.a / self.b)
        target_size = (xxx, 4096)
        image = Image.open(noise_path)
        resized_image = image.resize(target_size, Image.ADAPTIVE)
        noise_result_path = the_current_dir + r"\image\noise.jpg"
        resized_image.save(noise_result_path)

        src = cv2.imread(noise_result_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
        src /= 255.0
        h, w = src.shape
        self.terr = np.zeros([8, h, w])
        for k in range(8):
            self.terr[k] = src * terr_opt[0][k] + (1 - src) * terr_opt[1][k]

    def Set(self, loc, Kphi, Kc, n, coh, mu_angle, shear, K, R):
        Kphi_ = veh.doublep_value(Kphi)
        Kc_ = veh.doublep_value(Kc)
        n_ = veh.doublep_value(n)
        coh_ = veh.doublep_value(coh)
        mu_angle_ = veh.doublep_value(mu_angle)
        shear_ = veh.doublep_value(shear)
        K_ = veh.doublep_value(K)
        R_ = veh.doublep_value(R)

        the_x = int(loc.x + self.a) * int((4096 / (self.a * 2)) * int(self.a / self.b))
        the_y = int(loc.y + self.b) * int(4096 / (self.a * 2))
        Kphi_ = float(self.terr[0, the_x, the_y])
        Kc_ = float(self.terr[1, the_x, the_y])
        n_ = float(self.terr[2, the_x, the_y])
        # print(the_x, the_y, Kc_)

        coh_ = float(self.terr[3, the_x, the_y])
        mu_angle_ = float(self.terr[4, the_x, the_y])
        shear_ = float(self.terr[5, the_x, the_y])
        K_ = float(self.terr[6, the_x, the_y])
        R_ = float(self.terr[7, the_x, the_y])

        veh.doublep_assign(Kphi, Kphi_)
        veh.doublep_assign(Kc, Kc_)
        veh.doublep_assign(n, n_)
        veh.doublep_assign(coh, coh_)
        veh.doublep_assign(mu_angle, mu_angle_)
        veh.doublep_assign(shear, shear_)
        veh.doublep_assign(K, K_)
        veh.doublep_assign(R, R_)


class Terrain_Pychrono:
    def __init__(
        self,
        IsCarSystem=False,
        terrain_para=[1515.04e3, 5.27e3, 0.6, 1.72e3, 29, 2e-2, 4e8, 3e4],
        obj_path=r"c:\ProgramData\Anaconda3\envs\chrono2\Lib\site-packages\pychrono\demos\Ajay\blender12.obj",
        texture_path=r"d:\sunjieqiang\sucai\concatRGB2.jpg",
        noise_path=None,
        window_width=1024,
        window_height=1280,
        dimensions=None,
    ):
        self.IsCarSystem = IsCarSystem
        self.terrain_para = terrain_para
        self.obj_path = obj_path
        self.texture_path = texture_path
        self.delta = 0.2
        # Simulation step sizes
        self.step_size = 5e-3
        self.render_step_size = 1.0 / 50  # FPS = 50
        self.noise_path = noise_path
        self.window_width = window_width
        self.window_height = window_height
        self.dimensions = dimensions
        self.terrain_width = self.dimensions[0]
        self.terrain_height = self.dimensions[1]

    def Run(self):
        # 设置路径的
        veh.SetDataPath(chrono.GetChronoDataPath() + "vehicle/")
        # 不是车系统
        if not self.IsCarSystem:
            self.system = chrono.ChSystemSMC()
            terrain = veh.SCMDeformableTerrain(self.system)
            terrain.SetPlane(
                chrono.ChCoordsysD(
                    chrono.ChVectorD(0, 0.2, 0), chrono.Q_from_AngX(-math.pi / 2)
                )
            )
            terrain.Initialize(
                self.obj_path,
                self.delta,
            )
            terrain.SetTexture(ReImage(self.texture_path))
        else:
            my_hmmwv = veh.HMMWV_Reduced()
            my_hmmwv.SetContactMethod(chrono.ChContactMethod_SMC)
            my_hmmwv.SetInitPosition(
                chrono.ChCoordsysD(
                    chrono.ChVectorD(-3, -3, self.dimensions[2] + 0.3),
                    chrono.ChQuaternionD(0.707, 0, 0, 0.707),
                )
            )
            my_hmmwv.SetPowertrainType(veh.PowertrainModelType_SHAFTS)
            my_hmmwv.SetDriveType(veh.DrivelineTypeWV_AWD)
            my_hmmwv.SetTireType(veh.TireModelType_RIGID_MESH)
            my_hmmwv.Initialize()

            my_hmmwv.SetChassisVisualizationType(veh.VisualizationType_MESH)
            my_hmmwv.SetSuspensionVisualizationType(veh.VisualizationType_PRIMITIVES)
            my_hmmwv.SetSteeringVisualizationType(veh.VisualizationType_PRIMITIVES)
            my_hmmwv.SetWheelVisualizationType(veh.VisualizationType_PRIMITIVES)
            my_hmmwv.SetTireVisualizationType(veh.VisualizationType_MESH)
            self.system = my_hmmwv.GetSystem()
            terrain = veh.SCMDeformableTerrain(self.system)
            terrain.Initialize(
                self.obj_path,
                self.delta,
            )
            terrain.SetTexture(ReImage(self.texture_path))
        # my_params = MySoilParams(noise_path=self.noise_path, dim=self.dimensions)
        my_params = MySoilParams(noise_path=self.noise_path, dim=self.dimensions, terrain_para=self.terrain_para)
        terrain.RegisterSoilParametersCallback(my_params)
        terrain.SetPlotType(veh.SCMDeformableTerrain.PLOT_NONE, 0, 0.1)
        terrain.SetMeshWireframe(False)

        # vis
        if self.IsCarSystem:
            # Create the vehicle Irrlicht interface
            self.vis = veh.ChWheeledVehicleVisualSystemIrrlicht()
            self.vis.SetWindowTitle("HMMWV Deformable Soil Demo")
            self.vis.SetWindowSize(self.window_height, self.window_width)
            self.vis.SetChaseCamera(chrono.ChVectorD(0.0, 0.0, 1.75), 6.0, 0.5)
            self.vis.Initialize()
            self.vis.AddLogo(chrono.GetChronoDataFile("logo_pychrono_alpha.png"))
            self.vis.AddLightDirectional()
            self.vis.AddSkyBox()
            self.vis.AttachVehicle(my_hmmwv.GetVehicle())
            # 方案2 给轮车设置一个控制器
            driver = veh.ChIrrGuiDriver(self.vis)
            # driver.SetInputMode(driver.InputMode_JOYSTICK )
            # Set the time response for steering and throttle keyboard inputs.
            steering_time = 0.1  # time to go from 0 to +1 (or from 0 to -1)
            throttle_time = 0.10  # time to go from 0 to +1
            braking_time = 0.3  # time to go from 0 to +1
            driver.SetSteeringDelta(self.render_step_size / steering_time)
            driver.SetThrottleDelta(self.render_step_size / throttle_time)
            driver.SetBrakingDelta(self.render_step_size / braking_time)
            driver.Initialize()
        else:
            self.vis = irr.ChVisualSystemIrrlicht()
            self.vis.AttachSystem(self.system)
            self.vis.SetWindowSize(self.window_height, self.window_width)
            self.vis.SetWindowTitle("Deformable soil")
            self.vis.Initialize()
            self.vis.AddLogo(chrono.GetChronoDataFile("logo_pychrono_alpha.png"))
            self.vis.AddSkyBox()
            self.vis.AddCamera(
                chrono.ChVectorD(80, 14, -10.0), chrono.ChVectorD(-80, -14.0, 0)
            )
            self.vis.AddTypicalLights()

        if self.IsCarSystem:
            # Simulation loop
            while self.vis.Run():
                time = my_hmmwv.GetSystem().GetChTime()

                # Draw scene
                self.vis.BeginScene()
                self.vis.Render()
                self.vis.EndScene()

                # Get driver inputs
                driver_inputs = driver.GetInputs()

                # Update modules (process inputs from other modules)
                driver.Synchronize(time)
                terrain.Synchronize(time)
                my_hmmwv.Synchronize(time, driver_inputs, terrain)
                self.vis.Synchronize("", driver_inputs)

                # Advance simulation for one timestep for all modules
                driver.Advance(self.step_size)
                terrain.Advance(self.step_size)
                my_hmmwv.Advance(self.step_size)
                self.vis.Advance(self.step_size)

            return 0

        else:
            while self.vis.Run():
                self.vis.BeginScene()
                self.vis.Render()
                self.vis.EndScene()
                self.system.DoStepDynamics(0.002)


def get_obj_dimensions(obj_file_path):
    vertices = []

    with open(obj_file_path, "r") as file:
        for line in file.readlines():
            if line.startswith("v "):
                vertex = line.strip().split()[1:]
                vertex = [float(coord) for coord in vertex]
                vertices.append(vertex)

    vertices = np.array(vertices)
    min_vertex = np.min(vertices, axis=0)
    max_vertex = np.max(vertices, axis=0)
    dimensions = max_vertex - min_vertex

    return dimensions


def get_obj_dimensions(obj_file_path):
    vertices = []

    with open(obj_file_path, "r") as file:
        for line in file.readlines():
            if line.startswith("v "):
                vertex = line.strip().split()[1:]
                vertex = [float(coord) for coord in vertex]
                vertices.append(vertex)

    vertices = np.array(vertices)
    min_vertex = np.min(vertices, axis=0)
    max_vertex = np.max(vertices, axis=0)
    dimensions = max_vertex - min_vertex
    dimensions = [float(dimensions[0]), float(dimensions[1]), float(dimensions[2])]

    return dimensions

if __name__ == "__main__":
    Obj_file_path = "D:/sunjieqiang/sucai/test/nihao.obj"
    Texture_file_path = "D:/sunjieqiang/sucai/test/1.jpg"
    Noise_file_path = "D:/sunjieqiang/sucai/test/3.jpg"
    dimensions = get_obj_dimensions(Obj_file_path)
    Terrain_Pychrono(
        IsCarSystem=True,
        dimensions=dimensions,
        noise_path=Noise_file_path,
        texture_path=Texture_file_path,
        obj_path=Obj_file_path,
        terrain_para=[
            [1724.69e3, 16.43e3, 0.2, 68.95e3, 20, 0.6e-2, 4e8, 3e4],
            [66.08e3, 10.55e3, 1.44, 6e3, 20.7, 3e-2, 4e8, 3e4],
        ]
    ).Run()
