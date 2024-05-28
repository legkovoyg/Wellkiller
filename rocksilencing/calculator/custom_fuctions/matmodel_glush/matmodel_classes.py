from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_pressures as mfP
from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_heights as mfH
from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_commons as mfCom
from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_constructions as mfCon
from scipy.interpolate import interp1d
import math


class Construction:
    def __init__(self, type, length, area, volume, inner_diameter=None, external_diameter=None):
        self.type = type
        self.length = length
        self.area = area
        self.volume = volume
        if self.type != "KP":
            self.inner_diameter = inner_diameter
            self.external_diameter = external_diameter
            self.inner_radius = inner_diameter / 2
            self.external_radius = external_diameter / 2


class Operations:
    def __init__(self):
        pass

    def save_params(self, params, type):
        if type == "post":
            for attr_name, param in params.items():
                setattr(self, f"{attr_name}_post", param)
        if type == "post_post":
            for attr_name, param in params.items():
                setattr(self, f"{attr_name}_post_post", param)

    # Замена параметров "по змейке от пост-пост на пост, пост на текущее, текущее на посчитаное"
    def update_values(self, attr_name, attr_calculated):
        setattr(self, f"{attr_name}_post_post", float(getattr(self, f"{attr_name}_post")))
        setattr(self, f"{attr_name}_post", float(getattr(self, f"{attr_name}")))
        setattr(self, f"{attr_name}", float(attr_calculated))


class WellSpace(Operations):
    def __init__(self, name, t, dt, oil_volume, oil_height, jgs_volume, jgs_height, pressure, construction):
        # Текущие значения
        self.t = t
        self.dt = dt
        self.name = name
        self.oil_volume = oil_volume
        self.oil_height = oil_height
        self.jgs_volume = jgs_volume
        self.jgs_height = jgs_height
        self.construction = construction
        self.pressure = pressure

    def calculate_level_oil_NKT(self, common):
        if self.oil_height is None:
            self.oil_height = mfH.calculate_NKT_oil_height(common.h_yr, common.Hjg_reduced_post)
            return self.oil_height
        else:
            calculated_oil_height = mfH.calculate_NKT_oil_height(common.h_yr, common.Hjg_reduced_post)
            self.update_values('oil_height', calculated_oil_height)
            return self.oil_height

    def calculate_level_oil_KP(self, common, ):
        if self.oil_height is None:
            self.oil_height = mfH.calculate_KP_oil_height(common.h_yr, self.jgs_height)
            return self.oil_height
        else:
            calculated_oil_height = mfH.calculate_KP_oil_height(common.h_yr, self.jgs_height)
            self.update_values('oil_height', calculated_oil_height)
            return self.oil_height

    def calculate_level_oil_EXP(self, NKT_params, EXP_params):
        if self.oil_height is None:
            self.oil_height = mfH.calculate_EXP_oil_height(NKT_params.oil_height, self.construction.length,
                                                           EXP_params.jgs_height)
            return self.oil_height
        else:
            calculated_oil_height = mfH.calculate_EXP_oil_height(NKT_params.oil_height, self.construction.length,
                                                                 EXP_params.jgs_height)
            self.update_values("oil_height", calculated_oil_height)
            return self.oil_height

    def calculate_level_jgs_NKT(self, Hjg, NKT_params, EXP, dh_jg, V_pogl, NKT, KP):
        if self.jgs_height is None:
            self.jgs_height = mfH.calculate_NKT_jg_height(NKT_params.oil_height, Hjg, dh_jg, V_pogl, EXP, NKT, KP, self.jgs_height_post)
            return self.jgs_height
        else:
            calculated_value = mfH.calculate_NKT_jg_height(NKT_params, Hjg, dh_jg, V_pogl, EXP, NKT, KP,
                                                          self.jgs_height)
            self.update_values('jgs_height', calculated_value)
            return self.jgs_height

    def calculate_level_jgs_KP(self, NKT_params, All_common_calculations, tech_params, NKT_construction,
                               EXP_construction, KP_construction):
        if self.jgs_height is None:
            self.jgs_height = mfH.calculate_KP_jg_height(NKT_oil_height=NKT_params.oil_height,
                                                         KP_jg_height_pred=self.jgs_height_post,
                                                         dh_jg=All_common_calculations.dh_jg,
                                                         V_pogl=tech_params.V_pogl,
                                                         EXP_area=EXP_construction.area,
                                                         NKT_area=NKT_construction.area,
                                                         NKT_length=NKT_construction.length,
                                                         KP_area=KP_construction.area)

            return self.jgs_height
        else:
            calculated_jgs_height = mfH.calculate_KP_jg_height(NKT_oil_height=NKT_params.oil_height,
                                                               KP_jg_height_pred=self.jgs_height,
                                                               dh_jg=All_common_calculations.dh_jg,
                                                               V_pogl=tech_params.V_pogl,
                                                               EXP_area=EXP_construction.area,
                                                               NKT_area=NKT_construction.area,
                                                               NKT_length=NKT_construction.length,
                                                               KP_area=KP_construction.area)
            self.update_values("jgs_height", calculated_jgs_height)
            return self.jgs_height

    def calculate_level_jgs_EXP(self, NKT_params, tech_params):
        if self.jgs_height is None:
            self.jgs_height = mfH.calculate_EXP_jgs_height(NKT_params.oil_height, self.jgs_height_post,
                                                           tech_params.V_pogl, self.construction.area,
                                                           self.construction.length)
            return self.jgs_height
        else:
            calculated_jgs_height = mfH.calculate_EXP_jgs_height(NKT_params.oil_height, self.jgs_height,
                                                                 tech_params.V_pogl, self.construction.area,
                                                                 self.construction.length)
            self.update_values("jgs_height", calculated_jgs_height)
            return self.jgs_height

    def calculate_pressure(self, Fluid_oil, Fluid_jgs, ):
        if self.pressure is None:
            self.pressure = mfP.calculate_Pressure_at_Wellspace(self.oil_height, Fluid_oil.density, self.jgs_height,
                                                                Fluid_jgs.density)
            return self.pressure
        else:
            calculated_pressure = mfP.calculate_Pressure_at_Wellspace(self.oil_height, Fluid_oil.density,
                                                                      self.jgs_height, Fluid_jgs.density)
            self.update_values('pressure', calculated_pressure)
            return self.pressure

    def calculate_volume_NKT_oil(self, NKT_construction):
        if self.oil_volume is None:
            self.oil_volume = self.oil_height * NKT_construction.area
            return self.oil_volume
        else:
            calculated_oil_volume = self.oil_height * NKT_construction.area
            self.update_values('oil_volume', calculated_oil_volume)
            return self.oil_volume

    def calculate_volume_NKT_jgs(self, NKT_construction):
        if self.jgs_volume is None:
            self.jgs_volume = self.jgs_height * NKT_construction.area
            return self.jgs_volume
        else:
            calculated_jgs_volume = self.jgs_height * NKT_construction.area
            self.update_values('jgs_volume', calculated_jgs_volume)
            return self.jgs_volume

    def calculate_volume_KP_oil(self, KP_construction):
        if self.oil_volume is None:
            self.oil_volume = self.oil_height * KP_construction.area
            return self.oil_volume
        else:
            calculated_oil_volume = self.oil_height * KP_construction.area
            self.update_values('oil_volume', calculated_oil_volume)
            return self.oil_volume

    def calculate_volume_KP_jgs(self, KP_construction):
        if self.jgs_volume is None:
            self.jgs_volume = self.jgs_height * KP_construction.area
            return self.jgs_volume
        else:
            calculated_jgs_volume = self.jgs_height * KP_construction.area
            self.update_values('jgs_volume', calculated_jgs_volume)
            return self.jgs_volume

    def calculate_volume_EXP_oil(self, EXP_construction):
        if self.oil_volume is None:
            self.oil_volume = self.oil_height * EXP_construction.area
            return self.oil_volume
        else:
            calculated_oil_volume = self.oil_height * EXP_construction.area
            self.update_values('oil_volume', calculated_oil_volume)
            return self.oil_volume

    def calculate_volume_EXP_jgs(self, EXP_construction):
        if self.jgs_volume is None:
            self.jgs_volume = self.jgs_height * EXP_construction.area
            return self.jgs_volume
        else:
            calculated_jgs_volume = self.jgs_height * EXP_construction.area
            self.update_values('jgs_volume', calculated_jgs_volume)
            return self.jgs_volume


class Reservoir:
    def __init__(self, porosity, permeability_oil, permeability_jgs, height, pressure):
        self.porosity = porosity
        self.permeability_oil = permeability_oil
        self.permeability_jgs = permeability_jgs
        self.height = height
        self.pressure = pressure


class CommonCalculations(Operations):
    def __init__(self, Vjg, Vjg_reduced, Hjg, Hjg_reduced, dh_jg, dh_jg_reduced, speed, h_yr, dV_pogl):
        # Текущие значения
        self.Vjg = Vjg
        self.Vjg_reduced = Vjg_reduced
        self.Hjg = Hjg
        self.Hjg_reduced = Hjg_reduced
        self.dh_jg = dh_jg
        self.dh_jg_reduced = dh_jg_reduced
        self.speed = speed
        self.h_yr = h_yr

    def calculateVjgs(self, debit, density_of_oil, density_of_jgs, time):
        if self.Vjg is None:
            self.Vjg, self.Vjg_reduced = mfCom.calculate_com_volume_of_jgs(debit=debit, time=time, case='reduced',

                                                                           density_of_oil=density_of_oil,
                                                                           density_of_jgs=density_of_jgs)
            return self.Vjg, self.Vjg_reduced
        else:
            Vjg_calculated, Vjg_reduced_calculated = mfCom.calculate_com_volume_of_jgs(debit=debit, time=time,
                                                                                       case='reduced',
                                                                                       density_of_oil=density_of_oil,
                                                                                       density_of_jgs=density_of_jgs)
            self.update_values("Vjg", Vjg_calculated)
            self.update_values("Vjg_reduced", Vjg_reduced_calculated)
            return self.Vjg, self.Vjg_reduced

    def calculateHjg(self, NKT_area):
        if self.Hjg is None:
            self.Hjg = self.Vjg / NKT_area
            self.Hjg_reduced = self.Vjg_reduced / NKT_area
            return self.Hjg, self.Hjg_reduced
        else:
            Hjg_calculated = self.Vjg / NKT_area
            Hjg_reduced_calculated = self.Vjg_reduced / NKT_area
            self.update_values("Hjg", Hjg_calculated)
            self.update_values("Hjg_reduced", Hjg_reduced_calculated)
            return self.Hjg, self.Hjg_reduced

    def calculatedh(self):
        if self.dh_jg or self.dh_jg_reduced is None:
            self.dh_jg = self.Hjg - self.Hjg_post
            self.dh_jg_reduced = self.Hjg_reduced - self.Hjg_reduced_post
            return self.dh_jg, self.dh_jg_reduced
        else:
            dh_jg_calculated = self.Hjg - self.Hjg_post
            dh_jg_reduced_calculated = self.Hjg_reduced - self.Hjg_reduced_post
            self.update_values("dh_jg", dh_jg_calculated)
            self.update_values("dh_jg_reduced", dh_jg_reduced_calculated)
            return self.dh_jg, self.dh_jg_reduced

    def calculatespeed(self):
        if self.speed is None:
            self.speed = math.sqrt(self.dh_jg_reduced * 9.81 * 2)
            return self.speed
        else:
            speed_calculated = math.sqrt(self.dh_jg_reduced * 9.81 * 2)
            self.update_values("speed", speed_calculated)
            return self.speed

    def calculate_h_yr(self, NKT_params, KP_params, NKT, KP, tech_params):

        if self.h_yr is None:
            self.h_yr = mfH.calculate_h_yr(self.Vjg_reduced_post, NKT_params.oil_volume_post, KP_params.oil_volume_post,
                                           tech_params.V_pogl_post, NKT.area, KP.area, NKT.length)
            # print(f"Я ТАМ ГДЕ NONE\n"
            #     f"self.VJG_reduced_post = {self.Vjg_reduced_post}\n"
            #       f"NKT OIL VOLUME_POST  = {NKT_params.oil_volume_post}\n"
            #       f"KP OIL VOLUME POST = {KP_params.oil_volume_post}\n"
            #       f"TECH dV_pogl_post = {tech_params.dV_pogl_post}\n"
            #       f"TECH V_pogl_post = {tech_params.V_pogl_post}\n"
            #       f"NKT AREa = {NKT.area}\n"
            #       f"KP Area = {KP.area}\n"
            #       f"NKT length = {NKT.length}\n")
            return self.h_yr
        else:
            h_yr_calculated = mfH.calculate_h_yr(self.Vjg_reduced_post, NKT_params.oil_volume,
                                                 KP_params.oil_volume, tech_params.V_pogl_post, NKT.area, KP.area,
                                                 NKT.length)
            # print(f"Я ТАМ ГДЕ NE NONE\n"
            #     f"self.VJG_reduced_post = {self.Vjg_reduced_post}\n"
            #       f"NKT OIL VOLUME_POST  = {NKT_params.oil_volume}\n"
            #       f"KP OIL VOLUME POST = {KP_params.oil_volume}\n"
            #       f"TECH dV_pogl_post = {tech_params.dV_pogl}\n"
            #       f"TECH V_pogl_post = {tech_params.V_pogl_post}\n"
            #       f"NKT AREa = {NKT.area}\n"
            #       f"KP Area = {KP.area}\n"
            #       f"NKT length = {NKT.length}\n")
            self.update_values("h_yr", h_yr_calculated)
            return self.h_yr


class Fluid:
    def __init__(self, name, viscosity, density, phase_permeability):
        self.name = name
        self.viscosity = viscosity
        self.density = density
        self.phase_permeability = phase_permeability


class TechnicalCalculations(Operations):
    def __init__(self, Q_pogl, V_pogl, dV_pogl, Rn, pressure_friction, pressure_wellhead, pressure_downhole,
                 pressure_overall, Rk, dt, Q):
        self.Q_pogl = Q_pogl
        self.V_pogl = V_pogl
        self.dV_pogl = dV_pogl
        self.Rn = Rn
        self.dt = dt
        self.pressure_friction = pressure_friction
        self.pressure_wellhead = pressure_wellhead
        self.pressure_downhole = pressure_downhole
        self.pressure_overall = pressure_overall
        self.Rk = Rk
        self.Q = Q

    def calculate_Q_pogl(self, plast_thickness, Fluid_oil, Fluid_jgs, EXP_construction):
        # print(f" plast_thickness : {plast_thickness}\n"
        #       f"FLUID OIL.phase_permeability : {Fluid_oil.phase_permeability}\n"
        #       f"Fluid JGS.phase_permeability {Fluid_jgs.phase_permeability}\n"
        #       f"FLUID OIL.viscosity : {Fluid_oil.viscosity}\n"
        #       f"Fluid JGS.viscosity {Fluid_jgs.viscosity}\n"
        #       f"EXP_CONSTRUCTION : {EXP_construction.inner_radius}\n"
        #       f"self.pressure_overall_post {self.pressure_overall_post}\n"
        #       f"self.pressure_overall_post_post {self.pressure_overall_post_post}\n"
        #       f"self.RN_POST {self.Rn_post}\n")
        if self.Q_pogl is None:
            self.Q_pogl = mfCom.Q(plast_thickness, self.pressure_overall_post, self.pressure_overall_post_post,
                                  self.Rn_post,
                                  self.Rk,
                                  EXP_construction.inner_radius, Fluid_oil.viscosity, Fluid_jgs.viscosity,
                                  Fluid_oil.phase_permeability,
                                  Fluid_jgs.phase_permeability)
            return self.Q_pogl
        else:
            Q_calculated = mfCom.Q(plast_thickness, self.pressure_overall, self.pressure_overall_post,
                                   self.Rn, self.Rk,
                                   EXP_construction.inner_radius, Fluid_oil.viscosity, Fluid_jgs.viscosity,
                                   Fluid_oil.phase_permeability,
                                   Fluid_jgs.phase_permeability)
            self.update_values("Q_pogl", Q_calculated)
            return self.Q_pogl

    def calculate_V_pogl(self):
        if self.V_pogl is None:
            self.V_pogl = mfCom.Vpogl(self.Q_pogl, self.dt)
            return self.V_pogl
        else:
            calculated_V_pogl = mfCom.Vpogl(self.Q_pogl, self.dt)
            self.update_values("V_pogl", calculated_V_pogl)
            return self.V_pogl

    def calculate_Rn(self, Reservoir):
        if self.Rn is None:
            self.Rn = mfCom.calculate_Rn(self.Rn_post, self.Q_pogl, Reservoir.height, Reservoir.porosity, self.dt)
            return self.Rn
        else:
            calculated_Rn = mfCom.calculate_Rn(self.Rn, self.Q_pogl, Reservoir.height, Reservoir.porosity, self.dt)
            self.update_values("Rn", calculated_Rn)
            return self.Rn

    def calculate_dV_pogl(self):
        if self.dV_pogl is None:
            self.dV_pogl = self.dV_pogl_post - self.V_pogl
            return self.dV_pogl
        else:
            calculated_dV_pogl = self.dV_pogl - self.V_pogl
            self.update_values('dV_pogl', calculated_dV_pogl)
            return self.dV_pogl

    def calculate_pressure_friction(self, NKT_params, KP_params, NKT_construction, EXP_construction, Fluid_oil,
                                    Fluid_jgs, NKT_speed, KP_speed):
        if self.pressure_friction is None:
            self.pressure_friction = mfP.calculate_Pressure_friction(NKT_params.oil_height, NKT_params.jgs_height,
                                                                     KP_params.oil_height,
                                                                     KP_params.jgs_height, NKT_construction.length,
                                                                     NKT_construction.inner_diameter,
                                                                     NKT_construction.external_diameter,
                                                                     EXP_construction.inner_diameter, NKT_speed,
                                                                     KP_speed, Fluid_oil.viscosity, Fluid_jgs.viscosity)
            return self.pressure_friction
        else:
            calculated_pressure_friction = mfP.calculate_Pressure_friction(NKT_params.oil_height, NKT_params.jgs_height,
                                                                           KP_params.oil_height,
                                                                           KP_params.jgs_height,
                                                                           NKT_construction.length,
                                                                           NKT_construction.inner_diameter,
                                                                           NKT_construction.external_diameter,
                                                                           EXP_construction.inner_diameter, NKT_speed,
                                                                           KP_speed, Fluid_oil.viscosity,
                                                                           Fluid_jgs.viscosity)
            self.update_values('pressure_friction', calculated_pressure_friction)
            return self.pressure_friction

    def calculate_pressure_wellhead(self, Reservoir):
        if self.pressure_wellhead is None:
            self.pressure_wellhead = mfP.calculate_Pressure_wellhead(Reservoir.pressure, self.pressure_friction)
            return self.pressure_wellhead
        else:
            calculated_pressure_wellhead = mfP.calculate_Pressure_wellhead(Reservoir.pressure, self.pressure_friction)
            self.update_values("pressure_wellhead", calculated_pressure_wellhead)
            return self.pressure_wellhead

    def calculate_pressure_overall(self, NKT_params, EXP_params):
        if self.pressure_overall is None:
            self.pressure_overall = mfP.calculate_Pressure_downhole(101325, NKT_params.pressure, EXP_params.pressure)
            return self.pressure_overall
        else:
            calculated_pressure_overall = mfP.calculate_Pressure_downhole(self.pressure_wellhead, NKT_params.pressure,
                                                                          EXP_params.pressure)
            self.update_values("pressure_overall", calculated_pressure_overall)
            return self.pressure_overall


class DesignGlush():
    def __init__(self, volume_car, YV_density, YV_dole, emul_density, emul_dole, zapas, chosen_salt):
        self.stage_1_EMUL_volume = None
        self.stage_4_SOLE_RAST = None
        self.stage_4_BP_volume = None
        self.stage_4_YV_volume = None
        self.stage_4_EMUL_volume = None
        self.stage_3_SOLE_RAST = None
        self.stage_3_BP_volume = None
        self.stage_2_BP_volume = None
        self.stage_3_YV_volume = None
        self.stage_3_EMUL_volume = None
        self.stage_2_EMUL_volume = None
        self.stage_2_SOLE_RAST = None
        self.stage_2_YV_volume = None
        self.stage_1_SOLE_RAST = None
        self.stage_1_YV_volume = None
        self.stage_1_BP_volume = None
        self.salt_mass = None
        self.water_mass = None
        self.chosen_salt_debit = None
        self.chosen_water_debit = None
        self.recommended_water_debit = None
        self.recommended_salt_debit = None
        self.recommended_salt_name = None
        self.volume_of_rast = None
        self.true_jgs_density = None
        self.volume_car = volume_car
        self.YV_density = YV_density
        self.YV_dole = YV_dole
        self.emul_density = emul_density
        self.emul_dole = emul_dole
        self.zapas = zapas

        self.rash_glush_volume = None
        self.rash_glush_volume_zapas = None
        self.rash_glush_volume_with_zapas = None
        self.volume_oil = None
        self.volume_emul = None
        self.theory_jgs_density = None
        self.pressure_zapas = None
        self.safe_jgs_density = None
        self.chosen_salt = chosen_salt
        # def calculate_glush_volume(self, NKT, EXP, KP, one_cycle = True):

    #     if one_cycle is True:
    #         self.rash_glush_volume = NKT.volume + KP.volume
    #         self.rash_glush_volume_zapas = self.rash_glush_volume * self.zapas
    #         self.rash_glush_volume_with_zapas = self.rash_glush_volume + self.rash_glush_volume_zapas
    #         return self.rash_glush_volume
    #     else:
    #         self.rash_glush_volume = NKT.volume + KP.volume + KP.volume
    #         self.rash_glush_volume_zapas = self.rash_glush_volume * self.zapas
    #         self.rash_glush_volume_with_zapas = self.rash_glush_volume + self.rash_glush_volume_zapas
    #         return self.rash_glush_volume

    def calculate_glush_volume(self, NKT, EXP, KP, one_cycle=True):
        self.rash_glush_volume = NKT.volume + KP.volume + (EXP.volume if one_cycle else 0)
        self.rash_glush_volume_zapas = self.rash_glush_volume * self.zapas
        self.rash_glush_volume_with_zapas = self.rash_glush_volume + self.rash_glush_volume_zapas
        return self.rash_glush_volume_with_zapas

    def calculate_volume_oil(self):
        self.volume_oil = self.rash_glush_volume_with_zapas * self.YV_dole
        return self.volume_oil

    def calculate_volume_emul(self):
        self.volume_emul = self.rash_glush_volume_with_zapas * self.emul_dole
        return self.volume_emul

    def calculate_volume_of_rast(self):
        self.volume_of_rast = self.rash_glush_volume_with_zapas - self.volume_emul - self.volume_oil
        return self.volume_of_rast

    def calculate_theory_jgs_density(self, plast_pressure, from_yst_to_plast):
        self.theory_jgs_density = plast_pressure * 100 / (9.81 * from_yst_to_plast)
        return self.theory_jgs_density

    def calculate_pressure_zapas(self, plast_pressure, from_yst_to_plast):
        plast_pressure = plast_pressure
        if from_yst_to_plast >= 1200:
            if plast_pressure * 0.5 > 25:
                self.pressure_zapas = 25
                return self.pressure_zapas
            else:
                self.pressure_zapas = plast_pressure * 0.5
                return self.pressure_zapas
        else:
            if plast_pressure * 0.1 > 15:
                self.pressure_zapas = 15
                return self.pressure_zapas
            else:
                self.pressure_zapas = plast_pressure * 0.1
                return self.pressure_zapas

    def calculate_safe_jgs_density(self, plast_pressure, from_yst_to_plast):
        self.safe_jgs_density = (plast_pressure + self.pressure_zapas) * 100 / (9.81 * from_yst_to_plast)
        return self.safe_jgs_density

    def calculate_true_jgs_density(self):
        if self.safe_jgs_density <= 1:
            self.true_jgs_density = 1
            return self.true_jgs_density
        else:
            self.true_jgs_density = (
                                            self.safe_jgs_density * self.rash_glush_volume_with_zapas - self.YV_density * self.volume_oil - self.emul_density * self.volume_emul) / self.volume_of_rast
            return self.true_jgs_density

    def recommended_choose_salt(self, bdCaCl, bdCaJG, Q):
        x, y, z = [], [], []
        if self.true_jgs_density == 1:
            self.recommended_salt_name = "без соли"
            self.recommended_salt_debit = 0
            self.recommended_water_debit = Q
            return self.recommended_salt_name, self.recommended_salt_debit, self.recommended_water_debit
        else:
            if self.true_jgs_density <= 1.31:
                self.recommended_salt_name = "CaCl"
                for i in bdCaCl:
                    x.append(i.density)
                    y.append(i.salt_consumption)
                    z.append(i.water_consumption)
                interpolation_fuction_for_salt_consump = interp1d(x, y, kind='cubic', fill_value='extrapolate')
                interpolation_function_for_water_consumption = interp1d(x, z, kind='cubic', fill_value='extrapolate')
                x_new = self.true_jgs_density
                y_new = interpolation_fuction_for_salt_consump(x_new)
                z_new = interpolation_function_for_water_consumption(x_new)
                self.recommended_water_debit = z_new
                self.recommended_salt_debit = y_new
                return self.recommended_salt_name, self.recommended_salt_debit, self.recommended_water_debit

            else:
                self.recommended_salt_name = 'CaЖГ'
                for i in bdCaJG:
                    x.append(i.density)
                    y.append(i.salt_consumption)
                    z.append(i.water_consumption)
                interpolation_fuction_for_salt_consump = interp1d(x, y, kind='cubic', fill_value='extrapolate')
                interpolation_function_for_water_consumption = interp1d(x, z, kind='cubic', fill_value='extrapolate')
                x_new = self.true_jgs_density
                y_new = interpolation_fuction_for_salt_consump(x_new)
                z_new = interpolation_function_for_water_consumption(x_new)
                self.recommended_water_debit = z_new
                self.recommended_salt_debit = y_new
                return self.recommended_salt_name, self.recommended_salt_debit, self.recommended_water_debit

    def choose_salt(self, bdCaCl, bdCaJG, Q, ):
        x, y, z = [], [], []
        if self.true_jgs_density == 1:
            self.chosen_salt_name = "без соли"
            self.chosen_salt_debit = 0
            self.chosen_water_debit = Q
            return self.chosen_salt_name, self.chosen_salt_debit, self.chosen_water_debit
        else:
            if self.true_jgs_density <= 1.31:
                self.chosen_salt_name = "CaCl"
                for i in bdCaCl:
                    x.append(i.density)
                    y.append(i.salt_consumption)
                    z.append(i.water_consumption)
                interpolation_fuction_for_salt_consump = interp1d(x, y, kind='cubic', fill_value='extrapolate')
                interpolation_function_for_water_consumption = interp1d(x, z, kind='cubic', fill_value='extrapolate')
                x_new = self.true_jgs_density
                y_new = interpolation_fuction_for_salt_consump(x_new)
                z_new = interpolation_function_for_water_consumption(x_new)
                self.chosen_water_debit = z_new
                self.chosen_salt_debit = y_new
                return self.chosen_salt_name, self.chosen_salt_debit, self.chosen_water_debit

            else:
                self.chosen_salt_name = 'CaЖГ'
                for i in bdCaJG:
                    x.append(i.density)
                    y.append(i.salt_consumption)
                    z.append(i.water_consumption)
                interpolation_fuction_for_salt_consump = interp1d(x, y, kind='cubic', fill_value='extrapolate')
                interpolation_function_for_water_consumption = interp1d(x, z, kind='cubic', fill_value='extrapolate')
                x_new = self.true_jgs_density
                y_new = interpolation_fuction_for_salt_consump(x_new)
                z_new = interpolation_function_for_water_consumption(x_new)
                self.chosen_water_debit = z_new
                self.chosen_salt_debit = y_new
                return self.chosen_salt_name, self.chosen_salt_debit, self.chosen_water_debit

    def calculate_water_volume(self):
        if self.chosen_salt_name == 'без соли':
            return self.rash_glush_volume_with_zapas - self.volume_oil - self.volume_emul
        else:
            return self.volume_of_rast * self.chosen_water_debit / 1000

    def calculate_mass(self):
        self.water_mass = self.volume_of_rast * self.chosen_water_debit
        self.salt_mass = self.volume_of_rast * self.chosen_salt_debit
        return self.water_mass, self.salt_mass

    def RECIPE_YV(self, stage):
        if stage == 1:
            if self.rash_glush_volume_with_zapas >= self.volume_car:
                self.stage_1_YV_volume = self.volume_car / self.rash_glush_volume_with_zapas * self.volume_oil
                return self.stage_1_YV_volume
            else:
                self.stage_1_YV_volume = self.volume_oil
                return self.stage_1_YV_volume
        elif stage == 2:
            if (self.rash_glush_volume_with_zapas - self.stage_1_BP_volume) >= self.volume_car:
                self.stage_2_YV_volume = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume) * (
                                                 self.volume_oil - self.stage_1_YV_volume)
                return self.stage_2_YV_volume
            else:
                self.stage_2_YV_volume = self.volume_oil - self.stage_1_YV_volume
                return self.stage_2_YV_volume
        elif stage == 3:
            if (self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume) >= self.volume_car:
                self.stage_3_YV_volume = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume) * (
                                                 self.volume_oil - self.stage_1_YV_volume - self.stage_2_YV_volume)
                return self.stage_3_YV_volume
            else:
                self.stage_3_YV_volume = self.volume_oil - self.stage_1_YV_volume - self.stage_2_YV_volume
                return self.stage_3_YV_volume
        elif stage == 4:
            if (
                    self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume - self.stage_3_BP_volume) >= self.volume_car:
                self.stage_4_YV_volume = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume - self.stage_3_BP_volume) * (
                                                 self.volume_oil - self.stage_1_YV_volume - self.stage_2_YV_volume - self.stage_3_YV_volume)
                return self.stage_4_YV_volume
            else:
                self.stage_4_YV_volume = self.volume_oil - self.stage_1_YV_volume - self.stage_2_YV_volume - self.stage_3_YV_volume
                return self.stage_4_YV_volume

    def RECIPE_EMUL(self, stage):
        if stage == 1:
            if self.rash_glush_volume_with_zapas >= self.volume_car:
                self.stage_1_EMUL_volume = self.volume_car / self.rash_glush_volume_with_zapas * self.volume_emul
                return self.stage_1_EMUL_volume
            else:
                self.stage_1_EMUL_volume = self.volume_emul
                return self.stage_1_EMUL_volume
        elif stage == 2:
            if (self.rash_glush_volume_with_zapas - self.stage_1_BP_volume) >= self.volume_car:
                self.stage_2_EMUL_volume = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume) * (
                                                   self.volume_emul - self.stage_1_EMUL_volume)
                return self.stage_2_EMUL_volume
            else:
                self.stage_2_EMUL_volume = self.volume_emul - self.stage_1_EMUL_volume
                return self.stage_2_EMUL_volume
        elif stage == 3:
            if (self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume) >= self.volume_car:
                self.stage_3_EMUL_volume = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume) * (
                                                   self.volume_emul - self.stage_1_EMUL_volume - self.stage_2_EMUL_volume)
                return self.stage_3_EMUL_volume
            else:
                self.stage_3_EMUL_volume = self.volume_emul - self.stage_1_EMUL_volume - self.stage_2_EMUL_volume
                return self.stage_3_EMUL_volume
        elif stage == 4:
            if (
                    self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume - self.stage_3_BP_volume) >= self.volume_car:
                self.stage_4_EMUL_volume = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume - self.stage_3_BP_volume) * (
                                                   self.volume_emul - self.stage_1_EMUL_volume - self.stage_2_EMUL_volume - self.stage_3_EMUL_volume)
                return self.stage_4_EMUL_volume
            else:
                self.stage_4_EMUL_volume = self.volume_emul - self.stage_1_EMUL_volume - self.stage_2_EMUL_volume - self.stage_3_EMUL_volume
                return self.stage_4_EMUL_volume

    def RECIPE_SOLE_RAST(self, stage):
        if stage == 1:
            if self.rash_glush_volume_with_zapas >= self.volume_car:
                self.stage_1_SOLE_RAST = self.volume_car / self.rash_glush_volume_with_zapas * self.volume_of_rast
                return self.stage_1_SOLE_RAST
            else:
                self.stage_1_SOLE_RAST = self.volume_of_rast
                return self.stage_1_SOLE_RAST
        elif stage == 2:
            if (self.rash_glush_volume_with_zapas - self.stage_1_BP_volume) >= self.volume_car:
                self.stage_2_SOLE_RAST = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume) * (
                                                 self.volume_of_rast - self.stage_1_SOLE_RAST)
                return self.stage_2_SOLE_RAST
            else:
                self.stage_2_SOLE_RAST = self.volume_of_rast - self.stage_1_SOLE_RAST
                return self.stage_2_SOLE_RAST
        elif stage == 3:
            if (self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume) >= self.volume_car:
                self.stage_3_SOLE_RAST = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume) * (
                                                 self.volume_of_rast - self.stage_1_SOLE_RAST - self.stage_2_SOLE_RAST)
                return self.stage_3_SOLE_RAST
            else:
                self.stage_3_SOLE_RAST = self.volume_of_rast - self.stage_1_SOLE_RAST - self.stage_2_SOLE_RAST
                return self.stage_3_SOLE_RAST
        elif stage == 4:
            if (
                    self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume - self.stage_3_BP_volume) >= self.volume_car:
                self.stage_4_SOLE_RAST = self.volume_car / (
                        self.rash_glush_volume_with_zapas - self.stage_1_BP_volume - self.stage_2_BP_volume - self.stage_3_BP_volume) * (
                                                 self.volume_of_rast - self.stage_1_SOLE_RAST - self.stage_2_SOLE_RAST - self.stage_3_SOLE_RAST)
                return self.stage_4_SOLE_RAST
            else:
                self.stage_4_SOLE_RAST = self.volume_of_rast - self.stage_1_SOLE_RAST - self.stage_2_SOLE_RAST - self.stage_3_SOLE_RAST
                return self.stage_4_SOLE_RAST

    def RECIPE_BP(self, stage):
        if stage == 1:
            self.stage_1_BP_volume = self.stage_1_YV_volume + self.stage_1_EMUL_volume + self.stage_1_SOLE_RAST
            return self.stage_1_BP_volume
        elif stage == 2:
            self.stage_2_BP_volume = self.stage_2_YV_volume + self.stage_2_EMUL_volume + self.stage_2_SOLE_RAST
            return self.stage_2_BP_volume
        elif stage == 3:
            self.stage_3_BP_volume = self.stage_3_YV_volume + self.stage_3_EMUL_volume + self.stage_3_SOLE_RAST
            return self.stage_3_BP_volume
        elif stage == 4:
            self.stage_4_BP_volume = self.stage_4_YV_volume + self.stage_4_EMUL_volume + self.stage_4_SOLE_RAST
            return self.stage_4_BP_volume
