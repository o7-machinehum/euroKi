import shutil
import pdb
from operator import add

x = 0 ; y = 1
# Class for making eurorack parts
class euroRack:
    # Don't change these please
    Line = 103
    Datum = [150, 150] # Everthing is referenced off the datum point
    pcbDatum = [0, 0] # This is the PCB that's mounting to the back

    def __init__(self, fout):
        self.fout = fout;
        shutil.copytree('default', fout) # Make a copy of the default stuff
        with open(fout + '/default.kicad_pcb', 'r') as f :
            self.data = f.readlines()
    
    def fin(self):
        with open(self.fout + '/default.kicad_pcb', 'w') as f :
             f.writelines(self.data)

    def insertText(self, line):
        self.data.insert(self.Line, line)
        self.Line += 1

    def drawLine(self, start, end, layer):
        self.insertText('(gr_line (start %d %d) (end %d %d) (layer %s) (width 0.15))' % (self.Datum[x] + start[x], self.Datum[y] - start[y], self.Datum[x] + end[x], self.Datum[y] - end[y], layer))

    def drawRails(self):
        self.drawLine(list(map(add,self.topLeft,[0, -9.25])), list(map(add,self.topRight,[0, -9.25])), 'Dwgs.User')
        self.drawLine(list(map(add,self.bottomLeft,[0, 9.25])), list(map(add,self.bottomRight,[0, 9.25])), 'Dwgs.User')

    def drawHole(self, loc, size):
        self.insertText('(via (at %d %d) (size %f) (drill %f) (layers F.Cu B.Cu) (net 0))' % (self.Datum[x] + loc[x], self.Datum[y] - loc[y], size+0.1, size))

    def drawOutline(self, numHp):
        self.HP = numHp

        self.bottomLeft = [0,0]
        self.topLeft = [0,128.5]
        self.topRight = [numHp*5,128.5]
        self.bottomRight = [numHp*5,0]
        self.center = (numHp * 5) / 2;

        self.drawLine(self.bottomLeft, self.topLeft,'Edge.Cuts')
        self.drawLine(self.topLeft, self.topRight, 'Edge.Cuts')
        self.drawLine(self.topRight, self.bottomRight, 'Edge.Cuts')
        self.drawLine(self.bottomRight, self.bottomLeft, 'Edge.Cuts')

    def drawMountingHoles(self):
        if(self.HP > 10): # Four holes are required
           self.drawHole(list(map(add,self.bottomLeft,[7.5,3])), 3.2)
           self.drawHole(list(map(add,self.bottomRight,[-7.5, 3])), 3.2)
           self.drawHole(list(map(add,self.topLeft,[7.5, -3])), 3.2)
           self.drawHole(list(map(add,self.topRight,[-7.5, -3])), 3.2)
        else:
           self.drawHole(list(map(add,self.topLeft,[7.5, -3])), 3.2)
           self.drawHole(list(map(add,self.bottomRight,[-7.5, 3])), 3.2)

    def initPCB(self, size):
        self.pcbSize = size
        self.pcbDatum = [(self.bottomRight[x] - size[x]) / 2, (128.5 - size[y])/2]

    def drawPCB(self):
        self.drawLine(self.pcbDatum, [self.pcbDatum[x], self.pcbDatum[y] + self.pcbSize[y]], 'Dwgs.User')
        self.drawLine([self.pcbDatum[x], self.pcbDatum[y] + self.pcbSize[y]], [self.pcbDatum[x] + self.pcbSize[x], self.pcbDatum[y] + self.pcbSize[y]], 'Dwgs.User')
        self.drawLine([self.pcbDatum[x] + self.pcbSize[x], self.pcbDatum[y] + self.pcbSize[y]], [self.pcbDatum[x] + self.pcbSize[x], self.pcbDatum[y] ], 'Dwgs.User')
        self.drawLine(self.pcbDatum, [self.pcbDatum[x] + self.pcbSize[x], self.pcbDatum[y]], 'Dwgs.User')
    
    def drawPot(self, loc):
        self.drawHole(list(map(add,self.pcbDatum, loc)), self.pot)

    def drawJack(self, loc):
        self.drawHole(list(map(add,self.pcbDatum, loc)), self.jack)

# Example Front module
# ---------------------------------------------------------------------
er = euroRack('NewModule')
er.drawOutline(8)
er.drawMountingHoles()
er.drawRails()

er.pot = 7.1 # Alpha 9mm pots
er.jack = 6.1 # Thonk 3.5mm jack
er.initPCB([33, 90]) # This is the PCB that will go behind the panel
er.drawPCB()

er.drawPot([7, 33])
er.drawPot([26, 33])
er.drawPot([7, 53])
er.drawPot([26, 53])
er.drawJack([7, 76])
er.drawJack([26, 76])

er.fin() # Cleanup
# ---------------------------------------------------------------------
