import time
from datetime import datetime
import signal, os, subprocess
from pprint import pprint
import lcd

class Camera:
    def __init__(self, Model, Usb):
        self.model = Model
        self.usb = Usb
        self.usbid = "usb:{}".format(",".join(Usb))

    def __repr__(self):
        return "Camera[model={} usb={}]".format(self.model, self.usbid)

class CameraController:
    def __init__(self):
        #Intialise LCD and kill gphoto2
        self.LCD = lcd.lcd()
        self.killGphoto2Process()

        self.status = 0
        

    def getControl(self, camera_index=0):
        try:
            self.cameras = self.getCameras()
            if len(self.cameras) < camera_index:
                raise ValueError
                

            #Get cameras and config data
            self.active_camera = self.cameras[camera_index]
            self.getConfig()

            self.displayLCD(self.active_camera.model)

            self.status = 1
            
        except ValueError:
            self.displayLCD("Failed to get camera '{}'".format(camera_index))

        except Exception as e:
            self.displayLCD("Unexpected Error", str(e))

    def getStatus(self):
        return self.status
        
    def displayLCD(self, line1, line2="", scrollingEnabled=True):
        self.LCD.lcd_clear()
        self.LCD.backlight(0)
        self.LCD.lcd_display_string(self.active_camera.model)


    def killGphoto2Process(self):
        #Get and kill all gphoto instances
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE); out, err = p.communicate()
        for line in out.splitlines():
            if b'gphoto2' in line: os.kill(int(line.split(None, 1)[0]), signal.SIGKILL)

    def sphoto(self, args):
        start = time.time()
        os.system("gphoto2 {}".format(args))
        print("executed '{}' in {:.2f} secs".format(args, time.time()-start))
        
                    
    def gphoto(self, args):
        out, err = subprocess.Popen(['gphoto2', args], stdout=subprocess.PIPE).communicate()
        if err != None: print(err)
        return str(out.decode()).split("\r")[-1]


    def getCameras(self):
        #Return a list of cameras from gphoto
        camera_list = [Camera(camera.split("usb:")[0], tuple(camera.split("usb:")[1].replace(" ", "").split(","))) for camera in self.gphoto("--auto-detect").replace("  ", "").split("\n")[2:-1]]
        return camera_list


    def getConfig(self):
        start = time.time()
        config = {}
        #rint(self.gphoto("--list-all-config"))
        for setting in self.gphoto("--list-all-config")[1:].split("\n/"):
            setting = "".join(setting).split("\n")

            group, option = setting[0].replace("main/", "").split("/")
            
            try: config[group]
            except: config[group] = {}
                
            config[group][option] = {}
            config[group][option]["options"] = []
            for attribute in setting:
                attribute = attribute.split(":")
                if len(attribute) != 1:
                    if attribute[0] == "Choice":
                        config[group][option]["options"] += [[attribute[1].split(" ")[1], " ".join(attribute[1].split(" ")[2:])]]
                    else:
                        config[group][option][attribute[0].lower()] = attribute[1][1:]

            if len(config[group][option]["options"]) == 0:
                del config[group][option]["options"]
    
        print("fetched config in {:.2f} secs".format(time.time()-start))
        return config

    def takePhoto(self):

        """
        self.sphoto("--set-config shutterspeed=1/20")
        self.sphoto("--set-config aperture=4")
        self.sphoto("--set-config iso=400")
        self.sphoto("--set-config imageformat=0")
        """


        taken = False
        while taken == False:
            self.sphoto("--capture-image-and-download")

            for filename in os.listdir("."):
                if filename.split(".")[-1].lower() in ["jpg", "cr2", "crw"]:
                    new_filename = "images/{}.{}".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), filename.split(".")[-1])
                    os.rename(filename, (new_filename))
                    print("successfully saved", new_filename)
                    
                    taken = True

            if not taken:
                print("Capture failed, retrying...")

                    

                
        
  
  
	
app = CameraController()
#app.root.mainloop()

"""
{'actions': {'autofocusdrive': {'current': '0',
                                'label': 'Drive Canon DSLR Autofocus',
                                'type': 'TOGGLE'},
             'cancelautofocus': {'current': '0',
                                 'label': 'Cancel Canon DSLR Autofocus',
                                 'type': 'TOGGLE'},
             'eosremoterelease': {'current': 'None',
                                  'label': 'Canon EOS Remote Release',
                                  'options': [['0', 'None'],
                                              ['1', 'Press Half'],
                                              ['2', 'Press Full'],
                                              ['3', 'Release Half'],
                                              ['4', 'Release Full'],
                                              ['5', 'Immediate'],
                                              ['6', 'Press 1'],
                                              ['7', 'Press 2'],
                                              ['8', 'Press 3'],
                                              ['9', 'Release 1'],
                                              ['10', 'Release 2'],
                                              ['11', 'Release 3']],
                                  'type': 'RADIO'},
             'eoszoom': {'current': '0',
                         'label': 'Canon EOS Zoom',
                         'type': 'TEXT'},
             'eoszoomposition': {'current': '0,0',
                                 'label': 'Canon EOS Zoom Position',
                                 'type': 'TEXT'},
             'manualfocusdrive': {'current': 'None',
                                  'label': 'Drive Canon DSLR Manual focus',
                                  'options': [['0', 'Near 1'],
                                              ['1', 'Near 2'],
                                              ['2', 'Near 3'],
                                              ['3', 'None'],
                                              ['4', 'Far 1'],
                                              ['5', 'Far 2'],
                                              ['6', 'Far 3']],
                                  'type': 'RADIO'},
             'opcode': {'current': '0x1001,0xparam1,0xparam2',
                        'label': 'PTP Opcode',
                        'type': 'TEXT'},
             'syncdatetime': {'current': '0',
                              'label': 'Synchronize camera date and time with '
                                       'PC',
                              'type': 'TOGGLE'},
             'syncdatetimeutc': {'current': '0',
                                 'label': 'Synchronize camera date and time '
                                          'with PC',
                                 'type': 'TOGGLE'},
             'uilock': {'current': '2', 'label': 'UI Lock', 'type': 'TOGGLE'},
             'viewfinder': {'current': '2',
                            'label': 'Canon EOS Viewfinder',
                            'type': 'TOGGLE'}},
 'capturesettings': {'aeb': {'current': 'off',
                             'label': 'Auto Exposure Bracketing',
                             'options': [['0', 'off'],
                                         ['1', '+/- 1/3'],
                                         ['2', '+/- 2/3'],
                                         ['3', '+/- 1'],
                                         ['4', '+/- 1 1/3'],
                                         ['5', '+/- 1 2/3'],
                                         ['6', '+/- 2']],
                             'type': 'RADIO'},
                     'aperture': {'current': '4',
                                  'label': 'Aperture',
                                  'options': [['0', '2.8'],
                                              ['1', '3.2'],
                                              ['2', '3.5'],
                                              ['3', '4'],
                                              ['4', '4.5'],
                                              ['5', '5'],
                                              ['6', '5.6'],
                                              ['7', '6.3'],
                                              ['8', '7.1'],
                                              ['9', '8'],
                                              ['10', '9'],
                                              ['11', '10'],
                                              ['12', '11'],
                                              ['13', '13'],
                                              ['14', '14'],
                                              ['15', '16'],
                                              ['16', '18'],
                                              ['17', '20'],
                                              ['18', '22']],
                                  'type': 'RADIO'},
                     'autoexposuremode': {'current': 'Manual',
                                          'label': 'Canon Auto Exposure Mode',
                                          'options': [['0', 'P'],
                                                      ['1', 'TV'],
                                                      ['2', 'AV'],
                                                      ['3', 'Manual'],
                                                      ['4', 'Bulb'],
                                                      ['5', 'A_DEP'],
                                                      ['6', 'DEP'],
                                                      ['7', 'Custom'],
                                                      ['8', 'Lock'],
                                                      ['9', 'Green'],
                                                      ['10', 'Night Portrait'],
                                                      ['11', 'Sports'],
                                                      ['12', 'Portrait'],
                                                      ['13', 'Landscape'],
                                                      ['14', 'Closeup'],
                                                      ['15', 'Flash Off']],
                                          'type': 'RADIO'},
                     'bracketmode': {'current': '0',
                                     'label': 'Bracket Mode',
                                     'type': 'TEXT'},
                     'drivemode': {'current': 'Continuous',
                                   'label': 'Drive Mode',
                                   'options': [['0', 'Single'],
                                               ['1', 'Continuous'],
                                               ['2', 'Timer 10 sec'],
                                               ['3', 'Timer 2 sec'],
                                               ['4', 'Unknown value 0007']],
                                   'type': 'RADIO'},
                     'focusmode': {'current': 'AI Focus',
                                   'label': 'Focus Mode',
                                   'options': [['0', 'One Shot'],
                                               ['1', 'AI Focus'],
                                               ['2', 'AI Servo']],
                                   'type': 'RADIO'},
                     'meteringmode': {'current': 'Evaluative',
                                      'label': 'Metering Mode',
                                      'options': [['0', 'Evaluative'],
                                                  ['1', 'Partial'],
                                                  ['2',
                                                   'Center-weighted average']],
                                      'type': 'RADIO'},
                     'picturestyle': {'current': 'Standard',
                                      'label': 'Picture Style',
                                      'options': [['0', 'Auto'],
                                                  ['1', 'Standard'],
                                                  ['2', 'Portrait'],
                                                  ['3', 'Landscape'],
                                                  ['4', 'Neutral'],
                                                  ['5', 'Faithful'],
                                                  ['6', 'Monochrome'],
                                                  ['7', 'User defined 1'],
                                                  ['8', 'User defined 2'],
                                                  ['9', 'User defined 3']],
                                      'type': 'RADIO'},
                     'shutterspeed': {'current': '1/20',
                                      'label': 'Shutter Speed',
                                      'options': [['0', 'bulb'],
                                                  ['1', '30'],
                                                  ['2', '25'],
                                                  ['3', '20'],
                                                  ['4', '15'],
                                                  ['5', '13'],
                                                  ['6', '10'],
                                                  ['7', '8'],
                                                  ['8', '6'],
                                                  ['9', '5'],
                                                  ['10', '4'],
                                                  ['11', '3.2'],
                                                  ['12', '2.5'],
                                                  ['13', '2'],
                                                  ['14', '1.6'],
                                                  ['15', '1.3'],
                                                  ['16', '1'],
                                                  ['17', '0.8'],
                                                  ['18', '0.6'],
                                                  ['19', '0.5'],
                                                  ['20', '0.4'],
                                                  ['21', '0.3'],
                                                  ['22', '1/4'],
                                                  ['23', '1/5'],
                                                  ['24', '1/6'],
                                                  ['25', '1/8'],
                                                  ['26', '1/10'],
                                                  ['27', '1/13'],
                                                  ['28', '1/15'],
                                                  ['29', '1/20'],
                                                  ['30', '1/25'],
                                                  ['31', '1/30'],
                                                  ['32', '1/40'],
                                                  ['33', '1/50'],
                                                  ['34', '1/60'],
                                                  ['35', '1/80'],
                                                  ['36', '1/100'],
                                                  ['37', '1/125'],
                                                  ['38', '1/160'],
                                                  ['39', '1/200'],
                                                  ['40', '1/250'],
                                                  ['41', '1/320'],
                                                  ['42', '1/400'],
                                                  ['43', '1/500'],
                                                  ['44', '1/640'],
                                                  ['45', '1/800'],
                                                  ['46', '1/1000'],
                                                  ['47', '1/1250'],
                                                  ['48', '1/1600'],
                                                  ['49', '1/2000'],
                                                  ['50', '1/2500'],
                                                  ['51', '1/3200'],
                                                  ['52', '1/4000']],
                                      'type': 'RADIO'}},
 'imgsettings': {'colorspace': {'current': 'sRGB',
                                'label': 'Color Space',
                                'options': [['0', 'sRGB'], ['1', 'AdobeRGB']],
                                'type': 'RADIO'},
                 'imageformat': {'current': 'Large Fine JPEG',
                                 'label': 'Image Format',
                                 'options': [['0', 'Large Fine JPEG'],
                                             ['1', 'Large Normal JPEG'],
                                             ['2', 'Medium Fine JPEG'],
                                             ['3', 'Medium Normal JPEG'],
                                             ['4', 'Small Fine JPEG'],
                                             ['5', 'Small Normal JPEG'],
                                             ['6', 'Smaller JPEG'],
                                             ['7', 'Tiny JPEG'],
                                             ['8', 'RAW + Large Fine JPEG'],
                                             ['9', 'RAW']],
                                 'type': 'RADIO'},
                 'imageformatsd': {'current': 'Large Fine JPEG',
                                   'label': 'Image Format SD',
                                   'options': [['0', 'Large Fine JPEG'],
                                               ['1', 'Large Normal JPEG'],
                                               ['2', 'Medium Fine JPEG'],
                                               ['3', 'Medium Normal JPEG'],
                                               ['4', 'Small Fine JPEG'],
                                               ['5', 'Small Normal JPEG'],
                                               ['6', 'Smaller JPEG'],
                                               ['7', 'Tiny JPEG'],
                                               ['8', 'RAW + Large Fine JPEG'],
                                               ['9', 'RAW']],
                                   'type': 'RADIO'},
                 'iso': {'current': '400',
                         'label': 'ISO Speed',
                         'options': [['0', 'Auto'],
                                     ['1', '100'],
                                     ['2', '200'],
                                     ['3', '400'],
                                     ['4', '800'],
                                     ['5', '1600'],
                                     ['6', '3200'],
                                     ['7', '6400'],
                                     ['8', '12800']],
                         'type': 'RADIO'},
                 'whitebalance': {'current': 'Auto',
                                  'label': 'WhiteBalance',
                                  'options': [['0', 'Auto'],
                                              ['1', 'Daylight'],
                                              ['2', 'Shadow'],
                                              ['3', 'Cloudy'],
                                              ['4', 'Tungsten'],
                                              ['5', 'Fluorescent'],
                                              ['6', 'Flash'],
                                              ['7', 'Manual']],
                                  'type': 'RADIO'},
                 'whitebalanceadjusta': {'current': '0',
                                         'label': 'WhiteBalance Adjust A',
                                         'options': [['0', '-9'],
                                                     ['1', '-8'],
                                                     ['2', '-7'],
                                                     ['3', '-6'],
                                                     ['4', '-5'],
                                                     ['5', '-4'],
                                                     ['6', '-3'],
                                                     ['7', '-2'],
                                                     ['8', '-1'],
                                                     ['9', '0'],
                                                     ['10', '1'],
                                                     ['11', '2'],
                                                     ['12', '3'],
                                                     ['13', '4'],
                                                     ['14', '5'],
                                                     ['15', '6'],
                                                     ['16', '7'],
                                                     ['17', '8'],
                                                     ['18', '9']],
                                         'type': 'RADIO'},
                 'whitebalanceadjustb': {'current': '0',
                                         'label': 'WhiteBalance Adjust B',
                                         'options': [['0', '-9'],
                                                     ['1', '-8'],
                                                     ['2', '-7'],
                                                     ['3', '-6'],
                                                     ['4', '-5'],
                                                     ['5', '-4'],
                                                     ['6', '-3'],
                                                     ['7', '-2'],
                                                     ['8', '-1'],
                                                     ['9', '0'],
                                                     ['10', '1'],
                                                     ['11', '2'],
                                                     ['12', '3'],
                                                     ['13', '4'],
                                                     ['14', '5'],
                                                     ['15', '6'],
                                                     ['16', '7'],
                                                     ['17', '8'],
                                                     ['18', '9']],
                                         'type': 'RADIO'},
                 'whitebalancexa': {'current': '0',
                                    'label': 'WhiteBalance X A',
                                    'type': 'TEXT'},
                 'whitebalancexb': {'current': '0',
                                    'label': 'WhiteBalance X B',
                                    'type': 'TEXT'}},
 'other': {'5001': {'current': '100',
                    'label': 'Battery Level',
                    'options': [['0', '100'],
                                ['1', '0'],
                                ['2', '75'],
                                ['3', '0'],
                                ['4', '50']],
                    'type': 'MENU'},
           'd303': {'current': '1',
                    'label': 'PTP Property 0xd303',
                    'type': 'TEXT'},
           'd402': {'current': 'Canon EOS 1200D',
                    'label': 'PTP Property 0xd402',
                    'type': 'TEXT'},
           'd406': {'current': 'Unknown Initiator',
                    'label': 'PTP Property 0xd406',
                    'type': 'TEXT'},
           'd407': {'current': '1',
                    'label': 'PTP Property 0xd407',
                    'type': 'TEXT'}},
 'settings': {'artist': {'current': 'Tom Cupis',
                         'label': 'Artist',
                         'type': 'TEXT'},
              'autopoweroff': {'current': '0',
                               'label': 'Auto Power Off',
                               'type': 'TEXT'},
              'capture': {'current': '0', 'label': 'Capture', 'type': 'TOGGLE'},
              'capturetarget': {'current': 'Internal RAM',
                                'label': 'Capture Target',
                                'options': [['0', 'Internal RAM'],
                                            ['1', 'Memory card']],
                                'type': 'RADIO'},
              'copyright': {'current': '',
                            'label': 'Copyright',
                            'type': 'TEXT'},
              'customfuncex': {'current': 'bc,4,1,2c,3,101,1,0,103,1,1,10f,1,0,2,2c,3,201,1,0,202,1,3,203,1,0,3,14,1,50e,1,0,4,38,4,701,1,0,704,1,0,70e,1,0,811,1,0,',
                               'label': 'Custom Functions Ex',
                               'type': 'TEXT'},
              'datetime': {'current': '1576452049',
                           'help': "Use 'now' as the current time when "
                                   'setting.',
                           'label': 'Camera Date and Time',
                           'printable': 'Sun 15 Dec 2019 23',
                           'type': 'DATE'},
              'datetimeutc': {'current': '1576448449',
                              'help': "Use 'now' as the current time when "
                                      'setting.',
                              'label': 'Camera Date and Time',
                              'printable': 'Sun 15 Dec 2019 22',
                              'type': 'DATE'},
              'depthoffield': {'current': '0',
                               'label': 'Depth of Field',
                               'type': 'TEXT'},
              'evfmode': {'current': '1',
                          'label': 'EVF Mode',
                          'options': [['0', '1'], ['1', '0']],
                          'type': 'RADIO'},
              'focusinfo': {'current': 'eosversion=2,size=5184x3456,size2=5184x3456,points={{0,743,117,181},{-839,393,172,129},{839,393,172,129},{-1394,0,172,129},{0,0,224,222},{1394,0,172,129},{-839,-393,172,129},{839,-393,172,129},{0,-743,117,181}},select={},unknown={10000000ffff}',
                            'label': 'Focus Info',
                            'type': 'TEXT'},
              'movierecordtarget': {'current': 'None',
                                    'label': 'Recording Destination',
                                    'options': [['0', 'None']],
                                    'type': 'RADIO'},
              'output': {'current': 'Off',
                         'label': 'Camera Output',
                         'options': [['0', 'TFT'],
                                     ['1', 'PC'],
                                     ['2', 'TFT + PC'],
                                     ['3', 'Setting 4'],
                                     ['4', 'Setting 5'],
                                     ['5', 'Setting 6'],
                                     ['6', 'Setting 7'],
                                     ['7', 'Off']],
                         'type': 'RADIO'},
              'ownername': {'current': 'Tom Cupis',
                            'label': 'Owner Name',
                            'type': 'TEXT'},
              'reviewtime': {'current': '8 seconds',
                             'label': 'Quick Review Time',
                             'options': [['0', 'None'],
                                         ['1', '2 seconds'],
                                         ['2', '4 seconds'],
                                         ['3', '8 seconds'],
                                         ['4', 'Hold']],
                             'type': 'RADIO'}},
 'status': {'Battery Level': {'current': '100%',
                              'label': 'Battery Level',
                              'type': 'TEXT'},
            'availableshots': {'current': '43779',
                               'label': 'Available Shots',
                               'type': 'TEXT'},
            'batterylevel': {'current': '100%',
                             'label': 'Battery Level',
                             'type': 'TEXT'},
            'cameramodel': {'current': 'Canon EOS 1200D',
                            'label': 'Camera Model',
                            'type': 'TEXT'},
            'deviceversion': {'current': '3-1.0.2',
                              'label': 'Device Version',
                              'type': 'TEXT'},
            'eosserialnumber': {'current': '043072084383',
                                'label': 'Serial Number',
                                'type': 'TEXT'},
            'lensname': {'current': '17-50mm',
                         'label': 'Lens Name',
                         'type': 'TEXT'},
            'manufacturer': {'current': 'Canon Inc.',
                             'label': 'Camera Manufacturer',
                             'type': 'TEXT'},
            'model': {'current': '2147484455',
                      'label': 'Camera Model',
                      'type': 'TEXT'},
            'ptpversion': {'current': '256',
                           'label': 'PTP Version',
                           'type': 'TEXT'},
            'serialnumber': {'current': '1456bcf27e9c45418bf20da74c902ea5',
                             'label': 'Serial Number',
                             'type': 'TEXT'},
            'shuttercounter': {'current': '16682',
                               'label': 'Shutter Counter',
                               'type': 'TEXT'},
            'vendorextension': {'current': 'None',
                                'label': 'Vendor Extension',
                                'type': 'TEXT'}}}


                                
Common options
  -?, --help                                                                      Print complete help
										  message on program usage
	--usage                                                                     Print short message on
										  program usage
	--debug                                                                     Turn on debugging
	--debug-loglevel=STRING                                                     Set debug level
										  [error|debug|data|all]
	--debug-logfile=FILENAME                                                    Name of file to write
										  debug info to
  -q, --quiet                                                                     Quiet output
										  (default=verbose)
	--hook-script=FILENAME                                                      Hook script to call after
										  downloads, captures, etc.

Miscellaneous options (unsorted)
	--stdout                                                                    Send file to stdout
	--stdout-size                                                               Print filesize before data
	--auto-detect                                                               List auto-detected cameras
	--show-exif=STRING                                                          Show EXIF information of
										  JPEG images
	--show-info=STRING                                                          Show image information,
										  like width, height, and
										  capture time
	--summary                                                                   Show camera summary
	--manual                                                                    Show camera driver manual
	--about                                                                     About the camera driver
										  manual
	--storage-info                                                              Show storage information
	--shell                                                                     gPhoto shell

Get information on software and host system (not from the camera)
  -v, --version                                                                   Display version and exit
	--list-cameras                                                              List supported camera
										  models
	--list-ports                                                                List supported port
										  devices
  -a, --abilities                                                                 Display the camera/driver
										  abilities in the
										  libgphoto2 database

Specify the camera to use
	--port=FILENAME                                                             Specify device port
	--speed=SPEED                                                               Specify serial transfer
										  speed
	--camera=MODEL                                                              Specify camera model
	--usbid=USBIDs                                                              (expert only) Override
										  USB IDs

Camera and software configuration
	--config                                                                    Configure
	--list-config                                                               List configuration tree
	--list-all-config                                                           Dump full configuration
										  tree
	--get-config=STRING                                                         Get configuration value
	--set-config=STRING                                                         Set configuration value
										  or index in choices
	--set-config-index=STRING                                                   Set configuration value
										  index in choices
	--set-config-value=STRING                                                   Set configuration value
	--reset                                                                     Reset device port

Capture an image from or on the camera
	--keep                                                                      Keep images on camera
										  after capturing
	--keep-raw                                                                  Keep RAW images on camera
										  after capturing
	--no-keep                                                                   Remove images from camera
										  after capturing
	--wait-event[=COUNT, SECONDS, MILLISECONDS or MATCHSTRING]                  Wait for event(s) from
										  camera
	--wait-event-and-download[=COUNT, SECONDS, MILLISECONDS or MATCHSTRING]     Wait for event(s) from
										  the camera and download
										  new images
	--capture-preview                                                           Capture a quick preview
	--show-preview                                                              Show a quick preview as
										  Ascii Art
  -B, --bulb=SECONDS                                                              Set bulb exposure time in
										  seconds
  -F, --frames=COUNT                                                              Set number of frames to
										  capture (default=infinite)
  -I, --interval=SECONDS                                                          Set capture interval in
										  seconds
	--reset-interval                                                            Reset capture interval on
										  signal (default=no)
	--capture-image                                                             Capture an image
	--trigger-capture                                                           Trigger capture of an
										  image
	--capture-image-and-download                                                Capture an image and
										  download it
	--capture-movie[=COUNT or SECONDS]                                          Capture a movie
	--capture-sound                                                             Capture an audio clip
	--capture-tethered[=COUNT, SECONDS, MILLISECONDS or MATCHSTRING]            Wait for shutter release
										  on the camera and download
	--trigger-capture                                                           Trigger image capture

Downloading, uploading and manipulating files
  -l, --list-folders                                                              List folders in folder
  -L, --list-files                                                                List files in folder
  -m, --mkdir=DIRNAME                                                             Create a directory
  -r, --rmdir=DIRNAME                                                             Remove a directory
  -n, --num-files                                                                 Display number of files
  -p, --get-file=RANGE                                                            Get files given in range
  -P, --get-all-files                                                             Get all files from folder
  -t, --get-thumbnail=RANGE                                                       Get thumbnails given in
										  range
  -T, --get-all-thumbnails                                                        Get all thumbnails from
										  folder
	--get-metadata=RANGE                                                        Get metadata given in
										  range
	--get-all-metadata                                                          Get all metadata from
										  folder
	--upload-metadata=STRING                                                    Upload metadata for file
	--get-raw-data=RANGE                                                        Get raw data given in
										  range
	--get-all-raw-data                                                          Get all raw data from
										  folder
	--get-audio-data=RANGE                                                      Get audio data given in
										  range
	--get-all-audio-data                                                        Get all audio data from
										  folder
  -d, --delete-file=RANGE                                                         Delete files given in
										  range
  -D, --delete-all-files                                                          Delete all files in
										  folder (--no-recurse by
										  default)
  -u, --upload-file=FILENAME                                                      Upload a file to camera
	--filename=FILENAME_PATTERN                                                 Specify a filename or
										  filename pattern
  -f, --folder=FOLDER                                                             Specify camera folder
										  (default="/")
  -R, --recurse                                                                   Recursion (default for
										  download)
	--no-recurse                                                                No recursion (default for
										  deletion)
	--new                                                                       Process new files only
	--force-overwrite                                                           Overwrite files without
										  asking
	--skip-existing                                                             Skip existing files
"""
