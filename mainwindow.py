from PyQt4 import Qt, QtCore, QtGui, uic, Qwt5 as Qwt
#from collector import Precollector
import pcienetclient as pcie
import  pciedevsettings
import plots

Base, Form = uic.loadUiType("window.ui")
class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(Base, self).__init__(parent)
        self.setupUi(self)
        self.pcieWidget = DragonWidget()
        self.settings.addWidget(self.pcieWidget, 0, 0, 1, 1)
        
        self.dragonplot = plots.Plot(QtCore.QRectF(0, plots.SIGNAL_BOT, 8*6144, plots.SIGNAL_TOP - plots.SIGNAL_BOT), self)
        self.plots.addWidget(self.dragonplot, 1, 1)
        
        #self.precollector = Precollector(self)
                
        self.pcieClient = pcie.PCIENetWorker()
        self.pcieClient.setPCIESettings(self.pcieWidget.value())
        
        #self.pcieClient.measured.connect(self.precollector.appendDragonResponse)
        #self.precollector.reflectogrammChanged.connect(self.dragonplot.myplot)
        
        self.pcieClient.start()
        self.pcieClient.measured.connect(lambda x: self.dragonplot.myplot(x.data))
        

        self.pcieWidget.valueChanged.connect(self.pcieClient.setPCIESettings)        

        self.showMaximized()
        self.plotsOnly = False
        self.plotsFreezed = False

        
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F1:
            print "F1 pressed"
            self.freezeGraphs()
        super(Base, self).keyPressEvent(event)
    
    def freezeGraphs(self):
        if self.plotsFreezed:
            self.precollector.reflectogrammChanged.connect(self.dragonplot.myplot)
        else:
            self.precollector.reflectogrammChanged.disconnect(self.dragonplot.myplot)
        
        self.plotsFreezed = not self.plotsFreezed

        
import pickle
DragomBase, DragonForm = uic.loadUiType("dragon.ui")
class DragonWidget(DragomBase, DragonForm):
    valueChanged = QtCore.pyqtSignal(pciedevsettings.PCIESettings)
    def __init__(self, parent=None):
        super(DragomBase, self).__init__(parent)
        self.setupUi(self)
        try:
            self._value = pickle.load(open("pciesettings.ini", "r"))
        except IOError:
            self._value = self.value()
        else:
            for name in ["ch1amp", "ch1shift", "ch1count", "ch2amp",
                         "ch2count", "ch2shift", "framelength", "framecount"]:
                self.__dict__[name].setValue(self._value.__dict__[name])
            
        for widget in [ self.ch1amp, self.ch1shift, self.ch1count,
                        self.ch2amp, self.ch2count, self.ch2shift,
                        self.framelength, self.framecount]:
            widget.valueChanged.connect(self.rereadValue)
        self.framelength.editingFinished.connect(self.selfCorrect)
    
    def selfCorrect(self):
        val = self.framelength.value()
        if val % 6 != 0:
            self.framelength.setValue(val // 6 * 6)
        
    def value(self):
        return pciedevsettings.PCIESettings(
            ch1amp = self.ch1amp.value(),
            ch1count = self.ch1count.value(),
            ch1shift = self.ch1shift.value(),
            ch2amp = self.ch2amp.value(),
            ch2count = self.ch2count.value(),
            ch2shift = self.ch2shift.value(),
            framelength = self.framelength.value(),
            framecount = self.framecount.value())
    
    def rereadValue(self):
        val = self.value()
        if val != self._value:
            pickle.dump(val, open("pciesettings.ini", "w"))
            self._value = val
            self.valueChanged.emit(val)

            
