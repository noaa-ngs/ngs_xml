# -*- coding: utf-8 -*-
'''----------------------------------------------------------------------------------
Source Name:    validation_lookup_and_reformatting.py
Version:        Python 3.7
Author:         Grant Haynes, National Geodetic Survey, National Oceanic and Atmospheric Administration

Updates:        2021/04/30 - V.I complete
                2021/05/27 - changed the default hour from 1 to 0, added max hour argument
                which results in a default dt string with the maximum hour, consolidated all validation
                lookup and related code to this script

Description:    This script contains a class with class level functions to reformat strings
                into those required by the xmls
----------------------------------------------------------------------------------'''
import re, datetime

class String_Checker():
    def __init__(self):
        pass
    
    # Checks to see if the string is a float. If not returns false.
    def is_float(self, n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    # Checks if the string is a number. If not it returns false
    def is_int(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    def is_valid_datetime(self, dt_string):
        try:
            datetime.datetime.strptime(dt_string,'%Y-%m-%dT%H:%M:%S.%f')
            return True
        except ValueError:
            return False

class ISO_Lookup():
    def __init__(self):
        self.bluebook_ref_id_iso_ref_id ={
            "02":["156","World Geodetic System 1984 TRANSIT"],
            "05":["192","ITRF1989"],
            "08":["143","ITRF1991"],
            "11":["103","ITRF1992"],
            "12":["122","ITRF1993"],
            "13":["116", "World Geodetic System 1984 (G730)"],
            "15":["197","ITRF1994"],
            "16":["135", "World Geodetic System 1984 (G873)"],
            "18":["146","ITRF1996"],
            "19":["145","ITRF1997"],
            "20":["142","IGS97"],
            "21":["165","ITRF2000"],
            "22":["194","IGS00"],
            "23":["114","World Geodetic System 1984 (G1150)"],
            "24":["115","IGb00"],
            "25":["105","ITRF2005"],
            "26":["202","IGS05"],
            "29":["179","ITRF2008"],
            "27":["106","IGS08"],
            "28":["159","IGb08"],
            "30":["196", "World Geodetic System 1984 (G1674)"],
            "31":["131", "World Geodetic System 1984 (G1762)"],
            "32":["175","ITRF2014"],
            "33":["153","IGS14"],
            "37":["724","IGb14"],
        }

    def bluebook_ref_id_to_iso_id(self, bluebook_ref_id):
        if bluebook_ref_id in self.bluebook_ref_id_iso_ref_id:
            return self.bluebook_ref_id_iso_ref_id[bluebook_ref_id]
        else:
            print("WARNING! No iso id found that corresponds to {}".format(bluebook_ref_id))
            return["unknown", "unknown"]
            #raise Exception("Unable to find iso id that corresponds to {}".format(bluebook_ref_id))

    # Takes in a datum name and returns the corresponding iso ID and epoch
    # added 3/17/2021 by Grant Haynes, Happy St Patty's day!
    # edited 4/9/2021 by Grant Haynes to use of a regex to strip all non alphanumeric characters 
    # edited 5/27/2021 by Grant Haynes, moved to a different script and class
    def ref_alias_to_iso_id_and_epoch(self, alias):
        found = False
        alias = alias.upper()
        alias = alias.strip()
        alias = alias.replace(" ", "")
        alias = re.sub('[^0-9a-zA-Z]+', "", alias)
        lookup = [(["NAD832011","NAD1983"],["126","2010.00"]), 
        (["NAD83PA11"],["188","2010.00"]), 
        (["NAD83MA11"],["101","2010.00"]), 
        (["NAD831986","NAD83ORIGINAL"], ["161","1986.00"]), 
        (["NAD83HARN", "NAD83HPGN", "NAD831989TONAD831997"], ["119", "1989-1997"]), 
        (["NAD83FBN", "NAD831996TONAD832001"],["176", "1996-2001"]),
        (["NAD83CORS96"],["112", "2002.00-2003.00"]),
        (["NAD832007NAD"],["134", "2007.00"]),
        (["NAD83PACP00"],["113", "1993.62"]),
        (["NAD83MARP00"],["162", "1993.62"]),
        (["WGS84","WGS-84","WORLDGEODETICSYS.-84"],["131", "2005.00"])]

        i = 0
        while i < len(lookup):
            for name in lookup[i][0]:
                if alias == name:
                    found = True
                    return lookup[i][1]
            i += 1
        if found == False:
            raise Exception("Unable to find iso ID and epoch for {}".format(alias))

class String_Reformatter():
    def __init__(self):
        self.ngs_xml_dt_format_string = '%Y-%m-%dT%H:%M:%S.00'

    # Formats an incoming string into an acceptable dt format for the xmls
    # 2021/06/25 - GH added statements to handle strings of 0s 
    def date_formatter(self, dt_string, maxhour):
        blank_dt_string = "{}-{}-{}T{}:{}:{}.{}"
        # Some date time strings will come in properly formatted but in an unacceptable arrangement, try to parse them here
        # and arrange them into an acceptable format
        # TODO incorporate max hour into this part?
        # Check here to see if the string already matches the xml format
        try:
            dt = datetime.datetime.strptime(dt_string, '%m-%d-%YT%H:%M:%S.00')
            return dt
        except Exception as ex:
            pass
        try:
            dt = datetime.datetime.strptime(dt_string, '%m-%d-%Y %H:%M:%S')
            return datetime.datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.00')
        except Exception as ex:
            pass       
        dt_string = re.sub('[^0-9a-zA-Z]+', "", dt_string)
        dt_string_len = len(dt_string) 
        if maxhour == False:
            if dt_string_len == 4:
                if dt_string == "0000":
                    return (blank_dt_string.format("0001", "01", "01", "00", "00", "00", "00"))
                else:
                    return (blank_dt_string.format(dt_string, "01", "01", "00", "00", "00", "00"))
            elif dt_string_len == 6:
                if dt_string == "000000":
                    return (blank_dt_string.format("0001", "01", "01", "00", "00", "00", "00"))
                else:   
                    return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], "01", "00", "00", "00", "00"))
            elif dt_string_len == 8:
                if dt_string == "00000000":
                    return (blank_dt_string.format("0001", "01", "01", "00", "00", "00", "00"))
                else:
                    return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], "00", "00", "00", "00"))
            elif dt_string_len == 10:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], "00", "00", "00"))
            elif dt_string_len == 12:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], dt_string[10:12], "00", "00"))
            elif dt_string_len == 14:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], dt_string[10:12], dt_string[12:13], "00"))
            elif dt_string_len == 16:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], dt_string[10:12], dt_string[12:13], dt_string[13:14]))
            else:
                return dt_string
        else:
            if dt_string_len == 4:
                return (blank_dt_string.format(dt_string, "01", "01", "23", "59", "59", "00"))
            elif dt_string_len == 6:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], "01", "23", "59", "59", "00"))
            elif dt_string_len == 8:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], "23", "59", "59", "00"))
            elif dt_string_len == 10:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], "59", "59", "00"))
            elif dt_string_len == 12:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], dt_string[10:12], "59", "00"))
            elif dt_string_len == 14:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], dt_string[10:12], dt_string[12:13]), "00")
            elif dt_string_len == 16:
                return (blank_dt_string.format(dt_string[0:4], dt_string[4:6], dt_string[6:8], dt_string[8:10], dt_string[10:12], dt_string[12:13]), dt_string[13:14])
            else:
                return dt_string