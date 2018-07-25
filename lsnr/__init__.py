from comm.LLog import Logger
log = Logger("lsnr_package_init__").getLogger()
log.print ("lsnr__INIT__start")
from .fa import Lsnrctl
appContext = Lsnrctl()
appContext.start()
import traceback
log.print (traceback.print_exc())
log.print ("lsnr__INIT__end")