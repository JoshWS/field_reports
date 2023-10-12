import jpype
import asposecells

jpype.startJVM()
from asposecells.api import Workbook

workbook = Workbook("input.json")
workbook.save("Output.pdf")
jpype.shutdownJVM()
