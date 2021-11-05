# -*- coding: utf-8 -*-
'''----------------------------------------------------------------------------------
Source Name:    ngs_xml_writer.py
Version:        Python 3.7
Author:         Grant Haynes, National Geodetic Survey, National Oceanic and Atmospheric Administration

Updates:        2021/02/03 - VI complete
                2021/03/02 - Added numeric checks for arguments that should be numeric
                2021/04/15 - Added CVX and LVX writer classes as well as xml parent class

Description:    This module contains classes to create objects to write ngs xml documents including
                GVX - GNSS Vector Exchange
                CVX - Classical Vector Exchange
                LVX - Level Vector Exchange
----------------------------------------------------------------------------------'''
import xml.etree.ElementTree as ET
from validation_lookup_and_reformatting import String_Checker

# This is the Base XML parent class
# This parent class contains the common tags shared by all the xml formats
#---------------------------------------------------------------------------------------------------------------
class Base_XML:

    def __init__(self, filepath):
        self.filepath = filepath                    # Set the filepath attribute here, Added 6/21/2021 GH
        self.string_checker = String_Checker()      # Create a string checker object here, Added 6/21/2021 GH
        self.source_data_records = 0
        self.project_information_records = 0
        
    def initialize_for_file(self, file_type, version):
        self.root = ET.Element(file_type.upper())
        self.root.set("VERSION", str(version))      # Set the root version attribute here, Added 4/22/2021 GH

        # Add the SOURCE_DATA elements here
        # QC 2/23/2021 GH
        sourceData = ET.Element("SOURCE_DATA")
        self.root.append(sourceData)
        self.sd_NAME = ET.SubElement(sourceData, "NAME")
        self.sd_CREATED_DATE = ET.SubElement(sourceData, "CREATED_DATE")

        application = ET.SubElement(sourceData, "APPLICATION")
        self.sd_app_NAME = ET.SubElement(application, "NAME")
        self.sd_app_VERSION = ET.SubElement(application, "VERSION")
        self.sd_app_MANUFACTURER = ET.SubElement(application, "MANUFACTURER")
        self.sd_app_MANUFACTURER_URL = ET.SubElement(application, "MANUFACTURER_URL")

        # Add the CONVERTED_BY elements here
        # QC 2/23/2021 GH
        convertedBy = ET.SubElement(sourceData, "CONVERTED_BY")
        self.sd_convert_SOFTWARE_NAME = ET.SubElement(convertedBy, "SOFTWARE_NAME")
        self.sd_convert_VERSION = ET.SubElement(convertedBy, "VERSION")
        self.sd_convert_SOFTWARE_URL = ET.SubElement(convertedBy, "SOFTWARE_URL")
        self.sd_convert_CONVERTED_DATE = ET.SubElement(convertedBy, "CONVERTED_DATE")

        # Add the PROJECT_INFORMATION elements here
        # QC 2/23/2021 GH
        self.pi = ET.Element("PROJECT_INFORMATION")
        self.root.append(self.pi)
        self.pi_TITLE = ET.SubElement(self.pi, "TITLE")
        self.pi_EMAIL_ADDRESS = ET.SubElement(self.pi, "EMAIL_ADDRESS")
        self.pi_PARTY_CHIEF = ET.SubElement(self.pi, "PARTY_CHIEF")
        self.pi_AGENCY = ET.SubElement(self.pi, "AGENCY")
        self.pi_START_DATE = ET.SubElement(self.pi, "START_DATE")
        self.pi_END_DATE = ET.SubElement(self.pi, "END_DATE")
        self.pi_REMARK = ET.SubElement(self.pi, "REMARK")

        # Add the REFERENCE_SYSTEM elements here
        # QC 2/23/2021 GH
        self.rs = ET.Element("REFERENCE_SYSTEM")
        self.root.append(self.rs)
        self.rs_ID = ET.SubElement(self.rs, "ID")     
        self.rs_CODE = ET.SubElement(self.rs, "CODE")
        self.rs_NAME = ET.SubElement(self.rs, "NAME")
        self.rs_REMARK = ET.SubElement(self.rs, "REMARK")


# This is the GVX writer, this class contains a number of methods to construct a GVX xml file
#---------------------------------------------------------------------------------------------------------------
class GVX_XML_Writer(Base_XML):


    # add_source_data function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_source_data(self, 
    source_NAME, 
    application_NAME, 
    converted_by_SOFTWARE_NAME, 
    source_CREATED_DATE, 
    converted_by_CONVERTED_DATE, 
    application_VERSION, 
    application_MANUFACTURER = None, 
    application_MANUFACTURER_URL = None, 
    converted_by_VERSION = None, 
    converted_by_SOFTWARE_URL = None):

        if self.source_data_records == 0:

            self.initialize_for_file("GVX", "1.0")

            self.sd_NAME.text = str(source_NAME)

            if self.string_checker.is_valid_datetime(source_CREATED_DATE):
                self.sd_CREATED_DATE.text = str(source_CREATED_DATE)
            else:
                raise Exception("Source data created date must be in the proper format YYYY-MM-DDThh:mm:ss.ss")

            self.sd_app_NAME.text = str(application_NAME)

            self.sd_app_VERSION.text = str(application_VERSION)

            if application_MANUFACTURER:
                self.sd_app_MANUFACTURER.text = str(application_MANUFACTURER)

            if application_MANUFACTURER_URL:
                self.sd_app_MANUFACTURER_URL.text = str(application_MANUFACTURER_URL)

            self.sd_convert_SOFTWARE_NAME.text = str(converted_by_SOFTWARE_NAME)

            if converted_by_VERSION:
                self.sd_convert_VERSION.text = str(converted_by_VERSION)

            if converted_by_SOFTWARE_URL:
                self.sd_convert_SOFTWARE_URL.text = str(converted_by_SOFTWARE_URL)

            if self.string_checker.is_valid_datetime(converted_by_CONVERTED_DATE):
                self.sd_convert_CONVERTED_DATE.text = str(converted_by_CONVERTED_DATE)
            else:
                raise Exception("Converted by converted date must be in the proper format YYYY-MM-DDThh:mm:ss.ss")

        else:
            raise Exception("Source data record already assigned, only one allowed")

        self.source_data_records += 1

    # add_project_information function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_project_information(self, 
    TITLE, 
    PARTY_CHIEF, 
    AGENCY, 
    START_DATE, 
    END_DATE, 
    EMAIL_ADDRESS = None, 
    REMARK = None):

        if self.project_information_records == 0:

            self.pi_TITLE.text = str(TITLE)

            if EMAIL_ADDRESS:
                self.pi_EMAIL_ADDRESS.text = str(EMAIL_ADDRESS)

            self.pi_PARTY_CHIEF.text = str(PARTY_CHIEF)

            self.pi_AGENCY.text = str(AGENCY)

            if self.string_checker.is_valid_datetime(START_DATE):
                self.pi_START_DATE.text = str(START_DATE)
            else:
                raise Exception("Start date must be in the proper format YYYY-MM-DDThh:mm:ss.ss")

            if self.string_checker.is_valid_datetime(END_DATE):
                self.pi_END_DATE.text = str(END_DATE)
            else:
                raise Exception("End date must be in the proper format YYYY-MM-DDThh:mm:ss.ss")

            if REMARK:
                self.pi_REMARK.text = str(REMARK)
        else:
            raise Exception("Project information record already assigned, only one allowed")
        self.project_information_records += 1

    # add_reference_system function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_reference_system(self, 
    ID, 
    NAME, 
    angular_unit_NAME, 
    linear_unit_NAME, 
    CODE = None, 
    angular_unit_SIGNIFICANT_DIGITS = None, 
    angular_unit_CONVERSION_FACTOR = None, 
    linear_unit_SIGNIFICANT_DIGITS = None, 
    linear_unit_CONVERSION_FACTOR = None, 
    REMARK = None):
        
        # Add the REFERENCE_SYSTEM elements here
        # QC 2/23/2021 GH
        linearUnit = ET.SubElement(self.rs, "LINEAR_UNIT")
        rs_lu_NAME = ET.SubElement(linearUnit, "NAME")
        rs_lu_SIGNIFICANT_DIGITS = ET.SubElement(linearUnit, "SIGNIFICANT_DIGITS")
        rs_lu_CONVERSION_FACTOR = ET.SubElement(linearUnit, "CONVERSION_FACTOR")
        angularUnit = ET.SubElement(self.rs, "ANGULAR_UNIT")
        rs_au_NAME = ET.SubElement(angularUnit, "NAME")
        rs_au_SIGNIFICANT_DIGITS = ET.SubElement(angularUnit, "SIGNIFICANT_DIGITS")
        rs_au_CONVERSION_FACTOR = ET.SubElement(angularUnit, "CONVERSION_FACTOR")

        # Assign arguments here
        #------------------------------------------------------------------------------------------------------------

        self.rs_ID.text = str(ID)

        self.rs_CODE.text = str(CODE)

        self.rs_NAME.text = str(NAME)

        rs_lu_NAME.text = str(linear_unit_NAME)

        if linear_unit_SIGNIFICANT_DIGITS:
            if self.string_checker.is_int(linear_unit_SIGNIFICANT_DIGITS):
                rs_lu_SIGNIFICANT_DIGITS.text = str(linear_unit_SIGNIFICANT_DIGITS)
            else:
                raise Exception("Linear unit SIGNIFICANT DIGITS must be an integer")

        if linear_unit_CONVERSION_FACTOR:
            if self.string_checker.is_float(linear_unit_CONVERSION_FACTOR):
                rs_lu_CONVERSION_FACTOR.text = str(linear_unit_CONVERSION_FACTOR)
            else:
                raise Exception("Linear unit CONVERSION FACTOR must be a double")

        rs_au_NAME.text = str(angular_unit_NAME)

        if angular_unit_SIGNIFICANT_DIGITS:
            if self.string_checker.is_int(angular_unit_SIGNIFICANT_DIGITS):
                rs_au_SIGNIFICANT_DIGITS.text = str(angular_unit_SIGNIFICANT_DIGITS)
            else:
                raise Exception("Angular unit SIGNIFICANT DIGITS must be an integer")

        if angular_unit_CONVERSION_FACTOR: 
            if self.string_checker.is_float(angular_unit_CONVERSION_FACTOR):
                rs_au_CONVERSION_FACTOR.text = str(angular_unit_CONVERSION_FACTOR)
            else:
                raise Exception("Angular unit CONVERSION FACTOR must be a double")

        if REMARK:
            self.rs_REMARK.text = str(REMARK)

    # add_equipment function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_equipment(self, 
    ID, 
    receiver_TYPE, 
    receiver_SERIAL_NUMBER, 
    receiver_FIRMWARE_VERSION, 
    antenna_TYPE, 
    antenna_SERIAL_NUMBER, 
    antenna_CALIBRATION_TYPE = None, 
    antenna_CALIBRATION_SOURCE = None):
        
        # Add the EQUIPMENT elements here
        # QC 2/23/2021 GH
        equipment = ET.Element("EQUIPMENT")
        self.root.append(equipment)
        eqse1 = ET.SubElement(equipment, "ID") 
        receiver = ET.SubElement(equipment, "RECEIVER")
        eqse2 = ET.SubElement(receiver, "TYPE")
        eqse3 = ET.SubElement(receiver, "SERIAL_NUMBER")
        eqse4 = ET.SubElement(receiver, "FIRMWARE_VERSION")
        antenna = ET.SubElement(equipment, "ANTENNA")
        eqse5 = ET.SubElement(antenna, "TYPE")
        eqse6 = ET.SubElement(antenna, "CALIBRATION_TYPE")
        eqse7 = ET.SubElement(antenna, "CALIBRATION_SOURCE")
        eqse8 = ET.SubElement(antenna, "SERIAL_NUMBER")

        # Assign arguments here
        #------------------------------------------------------------------------------------------------------------ 
        eqse1.text = str(ID)    

        eqse2.text = str(receiver_TYPE)

        eqse3.text = str(receiver_SERIAL_NUMBER)

        eqse4.text = str(receiver_FIRMWARE_VERSION)

        eqse5.text = str(antenna_TYPE)

        if antenna_CALIBRATION_TYPE:
            eqse6.text = str(antenna_CALIBRATION_TYPE)

        if antenna_CALIBRATION_SOURCE:
            eqse7.text = str(antenna_CALIBRATION_SOURCE)

        eqse8.text = str(antenna_SERIAL_NUMBER)

    # add_survey_setup function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_survey_setup(self, 
    ID, 
    SOLUTION_TYPE, 
    OPERATOR, 
    software_NAME, 
    software_VERSION, 
    software_URL = None, 
    CORRECTOR_FORMAT = None, 
    rtk_NAME = None, 
    rtk_MOUNT_POINT = None, 
    rtk_TYPE = None, 
    rtk_IP_ADDRESS = None, 
    rtk_IP_PORT = None, 
    REMARK = None):
        
        # Add the SURVEY_SETUP elements here
        # QC 2/23/2021 GH
        surveySetup = ET.Element("SURVEY_SETUP")
        self.root.append(surveySetup)
        ssse1 = ET.SubElement(surveySetup, "ID")
        ssse2 = ET.SubElement(surveySetup, "SOLUTION_TYPE")
        ssse3 = ET.SubElement(surveySetup, "OPERATOR")
        processingSoftware = ET.SubElement(surveySetup, "PROCESSING_SOFTWARE")
        ssse4 = ET.SubElement(processingSoftware, "NAME")
        ssse5 = ET.SubElement(processingSoftware, "VERSION")
        ssse6 = ET.SubElement(processingSoftware, "SOFTWARE_URL")
        ssse7 = ET.SubElement(surveySetup, "CORRECTOR_FORMAT")
        networkRTK = ET.SubElement(surveySetup, "NETWORKRTK")
        ssse8 = ET.SubElement(networkRTK, "NAME")
        ssse9 = ET.SubElement(networkRTK, "MOUNT_POINT")
        ssse10 = ET.SubElement(networkRTK, "TYPE")
        ssse11 = ET.SubElement(networkRTK, "IP_ADDRESS")
        ssse12 = ET.SubElement(networkRTK, "IP_PORT")
        ssse13 = ET.SubElement(surveySetup, "REMARK")
        
        # Assign arguments here
        #------------------------------------------------------------------------------------------------------------
        ssse1.text = str(ID)

        ssse2.text = str(SOLUTION_TYPE)

        ssse3.text = str(OPERATOR)

        ssse4.text = str(software_NAME)

        ssse5.text = str(software_VERSION)

        if software_URL:
            ssse6.text = str(software_URL)

        if CORRECTOR_FORMAT:
            ssse7.text = str(CORRECTOR_FORMAT)

        if rtk_NAME:
            ssse8.text = str(rtk_NAME)

        if rtk_MOUNT_POINT:
            ssse9.text = str(rtk_MOUNT_POINT)

        if rtk_TYPE:
            ssse10.text = str(rtk_TYPE)

        if rtk_IP_ADDRESS:
            ssse11.text = str(rtk_IP_ADDRESS)

        if rtk_IP_PORT:
            if self.string_checker.is_int(rtk_IP_PORT):
                ssse12.text = str(rtk_IP_PORT)
            else:
                raise Exception("RTK IP PORT must be an integer")

        if REMARK:
            ssse13.text = str(REMARK)

    # add_source_data function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_point(self, 
    ID, 
    NAME, 
    EQUIPMENT_ID, 
    ARP_HEIGHT, 
    POINT_TYPE, 
    REFERENCE_SYSTEM_ID, 
    EPOCH, 
    LATITUDE, 
    LONGITUDE, 
    ELLIPSOIDAL_HEIGHT, 
    CODE = None, 
    NETWORK_LOCATION = None, 
    TILT_COMPENSATOR = None, 
    X = None, 
    Y = None, 
    Z = None, 
    SDN = None, 
    SDE = None, 
    SDU = None, 
    PNE = None, 
    PNU = None, 
    PEU = None, 
    SDX = None, 
    SDY = None, 
    SDZ = None, 
    PXY = None, 
    PXZ = None,
    PYZ = None):

        # Add the POINT elements here
        # QC 2/23/2021 GH
        point = ET.Element("POINT")
        self.root.append(point)
        point_ID = ET.SubElement(point, "ID")
        point_NAME = ET.SubElement(point, "NAME")
        point_CODE = ET.SubElement(point, "CODE")
        point_EQUIPMENT_ID = ET.SubElement(point, "EQUIPMENT_ID")
        point_ARP_HEIGHT = ET.SubElement(point, "ARP_HEIGHT")
        point_POINT_TYPE = ET.SubElement(point, "POINT_TYPE")
        point_NETWORK_LOCATION = ET.SubElement(point, "NETWORK_LOCATION")
        point_TILT_COMPENSATOR = ET.SubElement(point, "TILT_COMPENSATOR")
        coordinates = ET.SubElement(point, "COORDINATES")
        point_REFERENCE_SYSTEM_ID = ET.SubElement(coordinates, "REFERENCE_SYSTEM_ID")               
        point_EPOCH = ET.SubElement(coordinates, "EPOCH")

        geodeticCoords = ET.SubElement(coordinates, "GEODETIC_COORDINATES")
        point_LATITUDE = ET.SubElement(geodeticCoords, "LATITUDE")
        point_LONGITUDE= ET.SubElement(geodeticCoords, "LONGITUDE")
        point_ELLIPSOIDAL_HEIGHT = ET.SubElement(geodeticCoords, "ELLIPSOIDAL_HEIGHT")

        geocentricCoords = ET.SubElement(coordinates, "GEOCENTRIC_COORDINATES")
        point_X = ET.SubElement(geocentricCoords, "X")
        point_Y = ET.SubElement(geocentricCoords, "Y")
        point_Z = ET.SubElement(geocentricCoords, "Z")

        cml = ET.SubElement(coordinates, "CORRELATION_MATRIX_LOCAL")
        point_cml_SDN = ET.SubElement(cml, "SDN")
        point_cml_SDE = ET.SubElement(cml, "SDE")
        point_cml_SDU = ET.SubElement(cml, "SDU")
        point_cml_PNE = ET.SubElement(cml, "PNE")
        point_cml_PNU = ET.SubElement(cml, "PNU")
        point_cml_PEU = ET.SubElement(cml, "PEU")

        cm = ET.SubElement(coordinates, "CORRELATION_MATRIX")
        point_cm_SDX = ET.SubElement(cm, "SDX")
        point_cm_SDY = ET.SubElement(cm, "SDY")
        point_cm_SDZ = ET.SubElement(cm, "SDZ")
        point_cm_PXY = ET.SubElement(cm, "PXY")
        point_cm_PXZ = ET.SubElement(cm, "PXZ")
        point_cm_PYZ = ET.SubElement(cm, "PYZ")

        # Assign arguments here
        #------------------------------------------------------------------------------------------------------------
        point_ID.text = str(ID)
        point_NAME.text = str(NAME)
        if CODE:
            point_CODE.text = str(CODE)
        point_EQUIPMENT_ID.text = str(EQUIPMENT_ID)
        if self.string_checker.is_float(ARP_HEIGHT):
            point_ARP_HEIGHT.text = str(ARP_HEIGHT)
        else:
            raise Exception("ARP HEIGHT must be a double")
        point_POINT_TYPE.text = str(POINT_TYPE)
        if NETWORK_LOCATION:
            point_NETWORK_LOCATION.text = str(NETWORK_LOCATION)

        if TILT_COMPENSATOR:
            # TILT COMPENSATOR is a bit different than the others, it expects a 1 or a 0 to indicate
            # a true/false so we'll use the __is_int() to test it
            if self.string_checker.is_int(TILT_COMPENSATOR):
                point_TILT_COMPENSATOR.text = str(TILT_COMPENSATOR)   
            else:
                raise Exception("TILT COMPENSATOR must be an int of either 1 or 0")

        point_REFERENCE_SYSTEM_ID.text = str(REFERENCE_SYSTEM_ID)

        if self.string_checker.is_float(EPOCH):
            point_EPOCH.text = str(EPOCH)
        else:
            raise Exception("EPOCH must be a double")

        if self.string_checker.is_float(LATITUDE):
            point_LATITUDE.text = str(LATITUDE)
        else:
            raise Exception("LATITUDE must be a double")

        if self.string_checker.is_float(LONGITUDE):
            point_LONGITUDE.text = str(LONGITUDE)
        else:
            raise Exception("LONGITUDE must be a double")

        if self.string_checker.is_float(ELLIPSOIDAL_HEIGHT):
            point_ELLIPSOIDAL_HEIGHT.text = str(ELLIPSOIDAL_HEIGHT)
        else:
            raise Exception("ELLIPSOIDAL_HEIGHT must be a double")

        if X:
            if self.string_checker.is_float(X):
                point_X.text = str(X)
            else:
                raise Exception("X must be a double")
        if Y:
            if self.string_checker.is_float(Y):
                point_Y.text = str(Y)
            else:
                raise Exception("Y must be a double")

        if Z:
            if self.string_checker.is_float(Z):
                point_Z.text = str(Z)
            else:
                raise Exception("Z must be a double")

        if SDN:
            if self.string_checker.is_float(SDN):
                point_cml_SDN.text = str(SDN)
            else:
                raise Exception("SDN must be a double")

        if SDE:
            if self.string_checker.is_float(SDE):
                point_cml_SDE.text = str(SDE)
            else:
                raise Exception("SDE must be a double")

        if SDU:
            if self.string_checker.is_float(SDU):
                point_cml_SDU.text = str(SDU)
            else:
                raise Exception("SDU must be a double")

        if PNE:
            if self.string_checker.is_float(PNE):
                point_cml_PNE.text = str(PNE)
            else:
                raise Exception("PNE must be a double")

        if PNU:
            if self.string_checker.is_float(PNU):
                point_cml_PNU.text = str(PNU)
            else:
                raise Exception("PNU must be a double")

        if PEU:
            if self.string_checker.is_float(PEU):
                point_cml_PEU.text = str(PEU)
            else:
                raise Exception("PEU must be a double")

        if SDX:
            if self.string_checker.is_float(SDX):
                point_cm_SDX.text = str(SDX)
            else:
                raise Exception("SDX must be a double")

        if SDY:
            if self.string_checker.is_float(SDY):
                point_cm_SDY.text = str(SDY)
            else:
                raise Exception("SDY must be a double")

        if SDZ:
            if self.string_checker.is_float(SDZ):
                point_cm_SDZ.text = str(SDZ)
            else:
                raise Exception("SDZ must be a double")

        if PXY:
            if self.string_checker.is_float(PXY):
                point_cm_PXY.text = str(PXY)
            else:
                raise Exception("PXY must be a double")

        if PXZ:
            if self.string_checker.is_float(PXZ):
                point_cm_PXZ.text = str(PXZ)
            else:
                raise Exception("PXZ must be a double")

        if PYZ:
            if self.string_checker.is_float(PYZ):
                point_cm_PYZ.text = str(PYZ)
            else:
                raise Exception("PYZ must be a double")

    # add_gnss_vector function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_gnss_vector(self, 
    ID, 
    INITIAL_POINT_ID, 
    TERMINAL_POINT_ID, 
    SURVEY_SETUP_ID, 
    START, 
    END, 
    orbit_TYPE, 
    orbit_SOURCE, 
    DX, 
    DY, 
    DZ, 
    SDX, 
    SDY, 
    SDZ, 
    PXY, 
    PXZ,
    PYZ, 
    UTC_OFFSET = None, 
    LEAP_SECONDS = None, 
    EPOCHS_USED = None, 
    RMS = None, 
    ELEVATION = None, 
    PDOP_MASK = None, 
    GDOP = None, 
    HDOP = None, 
    PDOP = None, 
    TDOP = None, 
    VDOP = None, 
    satellite_TOTAL = None, 
    GPS = None, 
    GLONASS = None, 
    GALILEO = None, 
    QZSS = None, 
    BEIDOU = None, 
    REFERENCE_SYSTEM_ID = None, 
    DOWNLOAD_DATE = None, 
    CORRECTOR_AGE = None):
        
        # Add the GNSS_VECTOR vector elements here
        # QC 2/23/2021 GH
        gnssVector = ET.Element("GNSS_VECTOR")
        self.root.append(gnssVector)  
        gvse1 = ET.SubElement(gnssVector, "ID")
        gvse2 = ET.SubElement(gnssVector, "INITIAL_POINT_ID")
        gvse3 = ET.SubElement(gnssVector, "TERMINAL_POINT_ID")
        gvse4 = ET.SubElement(gnssVector, "SURVEY_SETUP_ID")
        observationTime = ET.SubElement(gnssVector, "OBSERVATION_TIME")
        gvse5 = ET.SubElement(observationTime, "START")
        gvse6 = ET.SubElement(observationTime, "END")
        gvse7 = ET.SubElement(observationTime, "UTC_OFFSET")
        gvse8 = ET.SubElement(observationTime, "LEAP_SECONDS")
        qualityControl = ET.SubElement(gnssVector, "QUALITY_CONTROL")
        gvse9 = ET.SubElement(qualityControl, "EPOCHS_USED")
        mask = ET.SubElement(qualityControl, "MASK")
        gvse10 = ET.SubElement(mask, "ELEVATION")       
        gvse11 = ET.SubElement(mask, "PDOP_MASK")
        gvse12 = ET.SubElement(qualityControl, "RMS")
        dilutionPrecision = ET.SubElement(qualityControl, "DILUTION_PRECISION")
        gvse13 = ET.SubElement(dilutionPrecision, "GDOP")
        gvse14 = ET.SubElement(dilutionPrecision, "HDOP")
        gvse15 = ET.SubElement(dilutionPrecision, "PDOP")
        gvse16 = ET.SubElement(dilutionPrecision, "TDOP")
        gvse17 = ET.SubElement(dilutionPrecision, "VDOP")
        satelliteUsed = ET.SubElement(qualityControl, "SATELLITE_USED")
        gvse18 = ET.SubElement(satelliteUsed, "TOTAL")
        gvse19 = ET.SubElement(satelliteUsed, "GPS")
        gvse20 = ET.SubElement(satelliteUsed, "GLONASS")
        gvse21 = ET.SubElement(satelliteUsed, "GALILEO")
        gvse22 = ET.SubElement(satelliteUsed, "QZSS")
        gvse23 = ET.SubElement(satelliteUsed, "BEIDOU")
        orbit = ET.SubElement(qualityControl, "ORBIT")
        gvse24 = ET.SubElement(orbit, "TYPE")
        gvse25 = ET.SubElement(orbit, "SOURCE")     
        gvse26 = ET.SubElement(orbit, "REFERENCE_SYSTEM_ID")
        gvse27 = ET.SubElement(orbit, "DOWNLOAD_DATE")
        gvce = ET.SubElement(qualityControl, "CORRECTOR_AGE") # Named gvce for gnss vector corrector age since its at the second sub element level with no subelements
        ecefDetails = ET.SubElement(qualityControl, "ECEF_DELTAS")
        gvse28 = ET.SubElement(ecefDetails, "DX")
        gvse29 = ET.SubElement(ecefDetails, "DY")
        gvse30 = ET.SubElement(ecefDetails, "DZ")
        cm = ET.SubElement(qualityControl, "CORRELATION_MATRIX")
        gvse31 = ET.SubElement(cm, "SDX")
        gvse32 = ET.SubElement(cm, "SDY")
        gvse33 = ET.SubElement(cm, "SDZ")
        gvse34 = ET.SubElement(cm, "PXY")
        gvse35 = ET.SubElement(cm, "PXZ")
        gvse36 = ET.SubElement(cm, "PYZ")

        # Assign arguments here
        #------------------------------------------------------------------------------------------------------------
        gvse1.text = str(ID)

        gvse2.text = str(INITIAL_POINT_ID)

        gvse3.text = str(TERMINAL_POINT_ID)

        gvse4.text = str(SURVEY_SETUP_ID)

        gvse5.text = str(START)

        gvse6.text = str(END)

        if UTC_OFFSET:
            if self.string_checker.is_float(UTC_OFFSET):
                gvse7.text = str(UTC_OFFSET)
            else:
                raise Exception("UTC OFFSET must be a double")

        if LEAP_SECONDS:
            if self.string_checker.is_int(LEAP_SECONDS):
                gvse8.text = str(LEAP_SECONDS)
            else:
                raise Exception("LEAP SECONDS must be an integer")

        if EPOCHS_USED:
            if self.string_checker.is_int(EPOCHS_USED):
                gvse9.text = str(EPOCHS_USED)
            else:
                raise Exception("EPOCHS USED must be an integer")

        if ELEVATION:
            if self.string_checker.is_float(ELEVATION):
                gvse10.text = str(ELEVATION)  
            else:
                raise Exception("ELEVATION must be a double")

        if PDOP_MASK:
            if self.string_checker.is_float(PDOP_MASK):
                gvse11.text = str(PDOP_MASK)
            else:
                raise Exception("PDOP MASK must be a double")

        if RMS:
            if self.string_checker.is_float(RMS):
                gvse12.text = str(RMS)
            else:
                raise Exception("RMS must be a double")

        if GDOP:
            if self.string_checker.is_float(GDOP):
                gvse13.text = str(GDOP)
            else:
                raise Exception("GDOP must be a double")

        if HDOP:
            if self.string_checker.is_float(HDOP):
                gvse14.text = str(HDOP)
            else:
                raise Exception("HDOP must be a double")

        if PDOP:
            if self.string_checker.is_float(PDOP):
                gvse15.text = str(PDOP)
            else:
                raise Exception("PDOP must be a double")

        if TDOP:
            if self.string_checker.is_float(TDOP):
                gvse16.text = str(TDOP)
            else:
                raise Exception("TDOP must be a double")

        if VDOP:
            if self.string_checker.is_float(VDOP):
                gvse17.text = str(VDOP)
            else:
                raise Exception("VDOP must be a double")

        if satellite_TOTAL:
            if self.string_checker.is_int(satellite_TOTAL):
                gvse18.text = str(satellite_TOTAL)
            else:
                raise Exception("satellite TOTAL must be an integer")

        if GPS:
            if self.string_checker.is_int(GPS):
                gvse19.text = str(GPS)
            else:
                raise Exception("GPS must be an integer")

        if GLONASS:
            if self.string_checker.is_int(GLONASS):
                gvse20.text = str(GLONASS)
            else:
                raise Exception("GLONASS must be an integer")

        if GALILEO:
            if self.string_checker.is_int(GALILEO):
                gvse21.text = str(GALILEO)
            else:
                raise Exception("GALILEO must be an integer")

        if QZSS:
            if self.string_checker.is_int(QZSS):
                gvse22.text = str(QZSS)
            else:
                raise Exception("QZSS must be an integer")

        if BEIDOU:
            if self.string_checker.is_int(BEIDOU):
                gvse23.text = str(BEIDOU)
            else:
                raise Exception("BEIDOU must be an integer")

        gvse24.text = str(orbit_TYPE)

        gvse25.text = str(orbit_SOURCE)

        if REFERENCE_SYSTEM_ID:
            gvse26.text = str(REFERENCE_SYSTEM_ID) 

        if DOWNLOAD_DATE:
            if self.string_checker.is_valid_datetime(DOWNLOAD_DATE):
                gvse27.text = str(DOWNLOAD_DATE)
            else:
                raise Exception("Download date must be in the proper format YYYY-MM-DDThh:mm:ss.ss")

        if self.string_checker.is_float(DX):
            gvse28.text = str(DX)
        else:
            raise Exception("DX must be a double")

        if self.string_checker.is_float(DY):
            gvse29.text = str(DY)
        else:
            raise Exception("DY must be a double")

        if self.string_checker.is_float(DZ):
            gvse30.text = str(DZ)
        else:
            raise Exception("DZ must be a double")

        if CORRECTOR_AGE:
            if self.string_checker.is_int(CORRECTOR_AGE):
                gvce.text = str(CORRECTOR_AGE)
            else:
                raise Exception("CORRECTOR AGE must be an integer")

        if self.string_checker.is_float(SDX):
            gvse31.text = str(SDX)
        else:
            raise Exception("SDX must be a double")

        if self.string_checker.is_float(SDY):
            gvse32.text = str(SDY)
        else:
            raise Exception("SDY must be a double")

        if self.string_checker.is_float(SDZ):
            gvse33.text = str(SDZ)
        else:
            raise Exception("SDZ must be a double")

        if self.string_checker.is_float(PXY):
            gvse34.text = str(PXY)
        else:
            raise Exception("PXY must be a double")

        if self.string_checker.is_float(PXZ):
            gvse35.text = str(PXZ)
        else:
            raise Exception("PXZ must be a double")

        if self.string_checker.is_float(PYZ):
            gvse36.text = str(PYZ)
        else:
            raise Exception("PYZ must be a double")

    # add_session function
    # QC GH 3/2/2021
    # ---------------------------------------------------------------------------------------------------------------------------
    def add_session(self, 
    ID, 
    TOTAL_VECTORS, 
    START, 
    END, 
    ORDER,
    CCM_BLOCK, 
    UTC_OFFSET = None, 
    LEAP_SECONDS = None):
        
        # Add the SESSION elements here
        # QC 2/23/2021 GH
        session = ET.Element("SESSION")
        self.root.append(session)       
        sessionTime = ET.SubElement(session, "SESSION_TIME")
        sse1 = ET.SubElement(sessionTime, "START")
        sse2 = ET.SubElement(sessionTime, "END")
        sse3 = ET.SubElement(sessionTime, "UTC_OFFSET")
        sse4 = ET.SubElement(sessionTime, "LEAP_SECONDS")
        ccm = ET.SubElement(session, "CROSS_CORRELATION_MATRIX")

        # Assign arguments here
        #------------------------------------------------------------------------------------------------------------        
        # For whatever reason SESSION is the only element that contains attribute in it and in its subelements
        session.set("ID", str(ID))

        if self.string_checker.is_int(TOTAL_VECTORS):
            session.set("TOTAL_VECTORS", str(TOTAL_VECTORS))
        else:
            raise Exception("TOTAL VECTORS must be an integer")

        sse1.text = str(START)

        sse2.text = str(END)

        if UTC_OFFSET:
            if self.string_checker.is_float(UTC_OFFSET):
                sse3.text = str(UTC_OFFSET)
            else:
                raise Exception("UTC OFFSET must be a double")

        if LEAP_SECONDS:
            if self.string_checker.is_int(LEAP_SECONDS):
                sse4.text = str(LEAP_SECONDS)
            else:
                raise Exception("LEAP SECONDS must be an int")
        
        ccm.set("ORDER", str(ORDER))

        # Go through and write the list of ccm blocks here
        # TODO make this more generic?

        for block in CCM_BLOCK:
            ccmBlock = ET.SubElement(ccm, "CCM_BLOCK")
            ccmBlock.set("VECTOR_ID_COL", str(block['vec_id_row']))
            ccmBlock.set("VECTOR_ID_ROW", str(block['vec_id_col']))

            correlations = ET.SubElement(ccmBlock, "CORRELATIONS")
            converted_list = []
            for item in block['correlations']:
                converted_list.append(str(item))
            correlations.text = ",".join(converted_list)

    def write_file(self):
        tree = ET.ElementTree(self.root)
        with open (self.filepath, "wb") as gvxFile:
            tree.write(gvxFile)