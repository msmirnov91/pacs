import sys

from PyQt4.QtGui import QApplication

from Main.main import PACS


app = QApplication(sys.argv)
pacs = PACS()
pacs.main()
sys.exit(app.exec_())
