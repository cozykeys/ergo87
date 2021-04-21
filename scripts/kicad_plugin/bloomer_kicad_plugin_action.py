import enum
import inspect
import json
import os
import pcbnew
import wx

import sys

scripts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.append(scripts_dir)
from lib import SwitchData, Logger, get_bloomer_repo_dir, Corner

# Useful documentation:
# - https://docs.kicad-pcb.org/doxygen/classMODULE.html
# - https://docs.kicad-pcb.org/doxygen/classBOARD.html

POSITION_SCALE = 1000000.0
ROTATION_SCALE = 10

MID_X = 96.45

# TODO: These shouldn't need to be hard-coded but this needs to be resolved:
# https://gitlab.com/kicad/code/kicad/-/issues/4308
COZY_FOOTPRINT_LIBRARY_PATH = "/home/pewing/kicad/cozy-parts.pretty"


class Position:
    def __init__(self, x=0.0, y=0.0, r=0.0):
        self.x = x
        self.y = y
        self.r = r


class TextSize:
    def __init__(self, h=1.0, w=1.0, t=0.15):
        self.h = h
        self.w = w
        self.t = t


class Text:
    def __init__(
        self,
        text="",
        position=Position(),
        layer=pcbnew.F_SilkS,
        size=TextSize(),
        justify=pcbnew.GR_TEXT_HJUSTIFY_CENTER,
    ):
        self.text = text
        self.position = position
        self.layer = layer
        self.size = size
        self.justify = justify


class Graphic:
    def __init__(
        self,
        reference="",
        footprint="",
        library="",
        position=Position(),
        layer=pcbnew.F_SilkS,
    ):
        self.reference = reference
        self.footprint = footprint
        self.library = library
        self.position = position
        self.layer = layer


class LogLevel(enum.IntEnum):
    ERROR = 0
    WARN = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4


class BloomerKicadPluginDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Bloomer Dialog", style=wx.RESIZE_BORDER)

        self.panel = wx.Panel(self)

        title = wx.StaticText(self.panel, wx.ID_ANY, "Bloomer Plugin Log")
        self.log = wx.TextCtrl(
            self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH
        )
        button = wx.Button(self.panel, wx.ID_OK, label="OK")

        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        logSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(title, 0, wx.ALL, 5)
        logSizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        buttonSizer.Add(button, 0, wx.ALL | wx.EXPAND, 5)

        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(logSizer, 1, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(buttonSizer, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizerAndFit(topSizer)

    def LogClear(self, text):
        self.log.Clear()

    def LogAppend(self, level, text):
        lookup = {
            LogLevel.ERROR: ("ERROR", wx.RED),
            LogLevel.WARN: ("WARN", wx.YELLOW),
            LogLevel.INFO: ("INFO", wx.BLUE),
            LogLevel.DEBUG: ("DEBUG", wx.GREEN),
            LogLevel.TRACE: ("TRACE", wx.LIGHT_GREY),
        }

        (label, color) = lookup[level]

        self.log.SetDefaultStyle(wx.TextAttr(color))
        self.log.AppendText("[{}] {}\n".format(label, text))
        self.log.SetDefaultStyle(wx.TextAttr(wx.BLACK))


class BloomerKicadPluginAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Bloomer Plugin"
        self.category = "Modify PCB"
        self.description = "Place Bloomer components"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            get_bloomer_repo_dir(), "icon", "bloomer_32x32.png"
        )
        self.version = "0.0.11"
        self.wx_version = wx.version()
        self.dialog = None
        self.footprints = None
        self.log_level = LogLevel.INFO
        self.local_build = False

    def Run(self):
        self.logger = Logger()
        self.initialize_dialog()
        self.log_info("Running version {}".format(self.version))
        self.log_info("Running wxPython version {}".format(self.wx_version))
        self.log_info("Logging to directory {}".format(self.logger.path))

        if self.local_build:
            self.initialize_footprint_cache()
        pcb = pcbnew.GetBoard()

        self.log_info("Running Bloomer Kicad plugin")

        self.switch_data = SwitchData()

        # TODO: NYI
        # Set switch and diode positions
        key_count = 87
        for i in range(0, key_count):
            # TODO: Don't zfill
            key_id = "K{}".format(str(i).zfill(2))
            key = pcb.FindModuleByReference(key_id)
            if key == None:
                raise Exception("No key with id {} found".format(key_id))
            self.set_key_position(key)

            diode_id = "D{}".format(str(i).zfill(2))
            # diode_id = 'D{}'.format(i)
            diode = pcb.FindModuleByReference(diode_id)
            if diode == None:
                raise Exception("No diode with id {} found".format(diode_id))
            self.set_diode_position(diode)

        # TODO: NYI
        # Setup M2 spacer holes
        for i in range(0, 4):
            hole_id = "H{}".format(i + 1)
            hole = pcb.FindModuleByReference(hole_id)
            if hole == None:
                self.log_info("No hole {} found, creating it".format(hole_id))
                hole = pcbnew.FootprintLoad(
                    COZY_FOOTPRINT_LIBRARY_PATH, "HOLE_M2_SPACER"
                )
                hole.SetParent(pcb)
                hole.SetReference(hole_id)
                pcb.Add(hole)
            else:
                self.log_info("Found hole {}".format(hole_id))
            self.set_hole_position(hole)

        # TODO: NYI
        # Elite-C
        mcu_id = "U1"
        mcu = pcb.FindModuleByReference(mcu_id)
        if mcu == None:
            self.log_warn("No mcu with id {} found".format(mcu_id))
        else:
            self.log_info("Found MCU {}".format(mcu_id))
            self.set_mcu_position(mcu)

        # TODO: NYI
        # Reset switch
        reset_switch_id = "SW1"
        reset_switch = pcb.FindModuleByReference(reset_switch_id)
        if reset_switch == None:
            self.log_warn("No reset_switch with id {} found".format(reset_switch_id))
        self.set_reset_switch_position(reset_switch)

        # TODO: NYI
        # Remove all existing drawings on the Edge.Cuts line, then add the
        # desired edge cut segments
        for d in pcb.GetDrawings():
            if d.GetLayerName() == "Edge.Cuts":
                self.log_info("Found a drawing on Edge.Cuts layer")
                pcb.Remove(d)
        self.draw_edge_cuts(pcb)

        self.setup_text(pcb)
        self.setup_graphics(pcb)

    def log_error(self, message):
        self.log(LogLevel.ERROR, message)

    def log_warn(self, message):
        self.log(LogLevel.WARN, message)

    def log_info(self, message):
        self.log(LogLevel.INFO, message)

    def log_debug(self, message):
        self.log(LogLevel.DEBUG, message)

    def log_trace(self, message):
        self.log(LogLevel.TRACE, message)

    def log(self, level, message):
        if int(level) > int(self.log_level):
            return
        if self.logger != None:
            self.logger.log(message)
        if self.dialog != None:
            self.dialog.LogAppend(level, message)

    def initialize_dialog(self):
        pcbnew_window = None
        for w in wx.GetTopLevelWindows():
            if w.GetTitle().startswith("Pcbnew"):
                pcbnew_window = w
                self.log_info("Pcbnew window found!")
                break

        self.dialog = None
        for child in w.GetChildren():
            if type(child) == BloomerKicadPluginDialog:
                self.dialog = child
                self.log_info("Bloomer window found!")
                break

        if self.dialog == None:
            self.dialog = BloomerKicadPluginDialog(pcbnew_window)

        self.dialog.Show()
        self.dialog.SetSize(800, 600)

    def initialize_footprint_cache(self):
        self.footprints = {}
        libraryNames = pcbnew.GetFootprintLibraries()
        self.log_info("Initializing footprint cache:")
        self.log_debug("Footprints:")
        count = 0
        for l in libraryNames:
            self.log_debug("    {}".format(l))
            if not l in self.footprints:
                self.footprints[l] = []
            for f in pcbnew.GetFootprints(l):
                self.log_debug("        {}".format(f))
                self.footprints[l].append(f)
                count += 1
        self.log_info("Footprint cache initialized; {} footprints found".format(count))

    def set_key_position(self, key):
        ref = key.GetReference()
        pos = key.GetPosition()
        s = self.switch_data.get_switch_by_ref(ref)
        pos.x = int(s["x"] * POSITION_SCALE)
        pos.y = int(s["y"] * POSITION_SCALE)
        key.SetPosition(pos)
        key.SetOrientation(180 * ROTATION_SCALE)

    def set_diode_position(self, diode):
        ref = diode.GetReference()
        pos = diode.GetPosition()
        s = self.switch_data.get_switch_by_ref(ref)
        rot = None
        if s["diode_position"] == "left":
            pos.x = int((s["x"] - 8.2625) * POSITION_SCALE)
            pos.y = int(s["y"] * POSITION_SCALE)
            rot = 270
        elif s["diode_position"] == "right":
            pos.x = int((s["x"] + 8.2625) * POSITION_SCALE)
            pos.y = int(s["y"] * POSITION_SCALE)
            rot = 270
        elif s["diode_position"] == "top":
            pos.x = int(s["x"] * POSITION_SCALE)
            pos.y = int((s["y"] - 8.2625) * POSITION_SCALE)
            rot = 180
        elif s["diode_position"] == "bottom":
            pos.x = int(s["x"] * POSITION_SCALE)
            pos.y = int((s["y"] + 8.2625) * POSITION_SCALE)
            rot = 180
        else:
            raise Exception("Unsupported diode position {}".format(s["diode_position"]))
        diode.SetPosition(pos)
        if diode.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping diode {} because layer name {} is not B.Cu".format(
                    ref, diode.GetLayerName()
                )
            )
            diode.Flip(pos)
        diode.SetOrientation(rot * ROTATION_SCALE)

    def set_hole_position(self, hole):
        ref = hole.GetReference()
        pos = hole.GetPosition()

        lookup_tables = {
            "H1": self.switch_data.get_corner((0, 0), Corner.BOTTOM_RIGHT),
            "H2": self.switch_data.get_corner((0, 4), Corner.BOTTOM_RIGHT),
            "H3": self.switch_data.get_corner((5, 0), Corner.TOP_RIGHT),
            "H4": self.switch_data.get_corner((5, 4), Corner.TOP_RIGHT),
        }

        x = lookup_table[ref][0]
        y = lookup_table[ref][1]

        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        hole.SetPosition(pos)

    def set_mcu_position(self, mcu):
        ref = mcu.GetReference()
        pos = mcu.GetPosition()
        (x, y, r) = (48.35, 101.6, 90)
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        mcu.SetPosition(pos)
        mcu.SetOrientation(r * ROTATION_SCALE)
        if mcu.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping mcu {} because layer name {} is not B.Cu".format(
                    ref, mcu.GetLayerName()
                )
            )
            mcu.Flip(pos)

    def set_capacitor_position(self, capacitor):
        lookup_table = {
            "C1": (48.35 - 11, 107, 0),
            "C2": (48.35 - 11, 97, 0),
            "C3": (43.325, 93.2, 180),
            "C4": (56.75, 96.575, 90),
            "C5": (35.5, 113, 270),
            "C6": (38, 113, 270),
            "C7": (52.575, 110, 0),
            "C8": (40.5, 113, 270),
        }

        ref = capacitor.GetReference()
        pos = capacitor.GetPosition()
        (x, y, r) = lookup_table[ref]
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        capacitor.SetPosition(pos)
        capacitor.SetOrientation(r * ROTATION_SCALE)
        if capacitor.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping capacitor {} because layer name {} is not B.Cu".format(
                    ref, capacitor.GetLayerName()
                )
            )
            capacitor.Flip(pos)

    def set_resistor_position(self, resistor):
        lookup_table = {
            "R1": (42, 50.938, 270.0),
            "R2": (53.375, 93.2, 180.0),
            "R3": (47.08, 27, 90.0),
            "R4": (49.62, 27, 90.0),
            "R5": (44.54, 27, 90.0),
            "R6": (52.16, 27, 90.0),
        }

        ref = resistor.GetReference()
        pos = resistor.GetPosition()
        (x, y, r) = lookup_table[ref]
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        resistor.SetPosition(pos)
        resistor.SetOrientation(r * ROTATION_SCALE)
        if resistor.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping resistor {} because layer name {} is not B.Cu".format(
                    ref, resistor.GetLayerName()
                )
            )
            resistor.Flip(pos)

    def set_crystal_position(self, crystal):
        ref = crystal.GetReference()
        pos = crystal.GetPosition()
        (x, y, r) = (48.35 - 11, 101.6 + 0.4, 135)
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        crystal.SetPosition(pos)
        crystal.SetOrientation(r * ROTATION_SCALE)
        if crystal.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping crystal {} because layer name {} is not B.Cu".format(
                    ref, crystal.GetLayerName()
                )
            )
            crystal.Flip(pos)

    def set_reset_switch_position(self, reset_switch):
        ref = reset_switch.GetReference()
        pos = reset_switch.GetPosition()
        (x, y) = self.switch_data.get_midpoint((0, 7), (1, 7))
        x = x - 3.25
        y = y + 2.25
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        reset_switch.SetPosition(pos)
        if reset_switch.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping reset_switch {} because layer name {} is not B.Cu".format(
                    ref, reset_switch.GetLayerName()
                )
            )
            reset_switch.Flip(pos)

    def set_usb_port_position(self, usb_port):
        ref = usb_port.GetReference()
        pos = usb_port.GetPosition()
        (x, y, r) = (48.35, 18, 0)
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        usb_port.SetPosition(pos)
        usb_port.SetOrientation(r * ROTATION_SCALE)
        if usb_port.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping usb_port {} because layer name {} is not B.Cu".format(
                    ref, usb_port.GetLayerName()
                )
            )
            usb_port.Flip(pos)

    def set_oled_position(self, oled):
        ref = oled.GetReference()
        pos = oled.GetPosition()
        (x, y, r) = (48.35, 21.635, 0)
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        oled.SetPosition(pos)
        oled.SetOrientation(r * ROTATION_SCALE)
        if oled.GetLayerName() != "F.Cu":
            self.log_info(
                "Flipping oled {} because layer name {} is not F.Cu".format(
                    ref, oled.GetLayerName()
                )
            )
            oled.Flip(pos)

    def draw_edge_cuts(self, pcb):
        vertices = [
            self.switch_data.get_corner((0, 0), Corner.TOP_LEFT),
            self.switch_data.get_corner((0, 3), Corner.TOP_LEFT),
            self.switch_data.get_corner((0, 3), Corner.TOP_RIGHT),
            # self.switch_data.get_corner((0,5), Corner.TOP_RIGHT),
            (146.451, 29.036),
            self.switch_data.get_corner((4, 6), Corner.TOP_RIGHT),
            # (163.125, 123.6),
            self.switch_data.get_corner((4, 6), Corner.BOTTOM_RIGHT),
            self.switch_data.get_corner((5, 5), Corner.BOTTOM_LEFT),
            self.switch_data.get_corner((5, 1), Corner.BOTTOM_RIGHT),
            self.switch_data.get_corner((5, 0), Corner.BOTTOM_LEFT),
        ]

        l = len(vertices)
        for i in range(0, l):
            start = vertices[i]
            end = vertices[(i + 1) % l]
            segment = pcbnew.DRAWSEGMENT()
            segment.SetStartX(int(start[0] * POSITION_SCALE))
            segment.SetStartY(int(start[1] * POSITION_SCALE))
            segment.SetEndX(int(end[0] * POSITION_SCALE))
            segment.SetEndY(int(end[1] * POSITION_SCALE))
            segment.SetAngle(int(90 * ROTATION_SCALE))
            segment.SetWidth(int(0.3 * POSITION_SCALE))
            segment.SetLayer(pcbnew.Edge_Cuts)
            pcb.Add(segment)

    def setup_text(self, pcb):
        texts = (
            [
                Text(
                    text="Left",
                    position=Position(130.9875, 28.702, 0),
                    size=TextSize(2.0, 2.0, 0.3),
                )
            ],
        )

        for d in pcb.GetDrawings():
            if type(d) == pcbnew.TEXTE_PCB:
                pcb.Remove(d)

        for text in texts:
            # The ordering of these operations is very important. Properties
            # like angle/justifcation affect the behavhior of the flip
            # operation. Always set position and flip before adjusting text.
            t = pcbnew.TEXTE_PCB(pcb)
            pos = t.GetPosition()
            pos.x = int(text.position.x * POSITION_SCALE)
            pos.y = int(text.position.y * POSITION_SCALE)
            t.SetPosition(pos)
            t.SetLayer(pcbnew.F_SilkS)
            if text.layer == pcbnew.B_SilkS:
                if self.local_build:
                    t.Flip(pos, False)
                else:
                    t.Flip(pos)
            t.SetText(text.text)
            t.SetTextAngle(text.position.r * ROTATION_SCALE)
            if self.local_build:
                t.SetTextThickness(int(text.size.t * POSITION_SCALE))
            else:
                t.SetThickness(int(text.size.t * POSITION_SCALE))
            t.SetTextWidth(int(text.size.w * POSITION_SCALE))
            t.SetTextHeight(int(text.size.h * POSITION_SCALE))
            t.SetHorizJustify(text.justify)
            pcb.Add(t)

    def setup_graphics(self, pcb):
        graphics = (
            [
                Graphic(
                    reference="G1",
                    footprint="oshw-logo-small",
                    library=COZY_FOOTPRINT_LIBRARY_PATH,
                    position=Position(MID_X + 55.05, 95, 0),
                    layer=pcbnew.F_SilkS,
                ),
                Graphic(
                    reference="G2",
                    footprint="oshw-logo-small",
                    library=COZY_FOOTPRINT_LIBRARY_PATH,
                    position=Position(MID_X + 55.05, 95, 180),
                    layer=pcbnew.B_SilkS,
                ),
                Graphic(
                    reference="G3",
                    footprint="qmk-badge",
                    library=COZY_FOOTPRINT_LIBRARY_PATH,
                    position=Position(MID_X - 38.0935, 25.654, 0),
                    layer=pcbnew.F_SilkS,
                ),
                Graphic(
                    reference="G4",
                    footprint="qmk-badge",
                    library=COZY_FOOTPRINT_LIBRARY_PATH,
                    position=Position(MID_X - 38.0935, 25.654, 180),
                    layer=pcbnew.B_SilkS,
                ),
                Graphic(
                    reference="G5",
                    footprint="bloomer-attribution-small",
                    library=COZY_FOOTPRINT_LIBRARY_PATH,
                    position=Position(MID_X, 136, 0),
                    layer=pcbnew.F_SilkS,
                ),
                Graphic(
                    reference="G6",
                    footprint="bloomer-attribution-small",
                    library=COZY_FOOTPRINT_LIBRARY_PATH,
                    position=Position(MID_X, 136, 180),
                    layer=pcbnew.B_SilkS,
                ),
            ],
        )

        for g in graphics:
            module = pcb.FindModuleByReference(g.reference)
            if module != None:
                self.log_info("Found existing graphic {}, removing".format(g.reference))
                pcb.Remove(module)
            module = pcbnew.FootprintLoad(g.library, g.footprint)
            module.SetParent(pcb)
            module.SetReference(g.reference)
            pcb.Add(module)
            pos = module.GetPosition()
            pos.x = int(g.position.x * POSITION_SCALE)
            pos.y = int(g.position.y * POSITION_SCALE)
            module.SetPosition(pos)
            module.SetOrientation(g.position.r * ROTATION_SCALE)
            module.SetLayer(pcbnew.F_SilkS)
            if g.layer == pcbnew.B_SilkS:
                module.Flip(pos)


BloomerKicadPluginAction().register()
