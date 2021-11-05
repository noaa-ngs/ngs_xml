NGS xml Writer

Description:
    In an effort to standardize and improve survey instrument data storage and transportation
    the National Geodetic Survey has developed a number of standardized xml formats for various
    instrument types and setups. These python scripts were developed as a complement to that project to 
    be able to write data to flat xml files.

Python Version:
    3 and greater

Script outline:
    ngs_xml_writer - Contains classes with class level methods for writing xml flat files, methods group together
    common subelements.
        Classes: 
            BASE_XML - Contains methods and properties used by all the xml writers.
            GVX_XML_Writer - Creates an object to write a GVX (gravity vector exchange) file, is a child class of BASE_XML.

    validation_lookup_and_reformatting - Provides classes and class level methods for the validation and reformatting of data passed into the writer.
        Classes:
            String_Checker - Checks to make sure strings represent what they need to represent, e.g a float, a datetime string format as dictated by the schema.
            ISO_Lookup - Looks up old NGS codes and returns the corresponding ISO codes.
            String_Reformatter - Reformats strings, e.g date time strings.

General use directions:
    Import and instantiate a writer object to be able to write a GVX file. 
    Call each writer object method and pass in variables needed for each method.
    Call Write file when the file is ready to be written.

Version naming convention
    The version numbers for this python package follow the following convention, the first number
    indicates a major revision from the previous version and is incremented by 1, the second number
    indicates a minor revision from the previous version and is incremented by 1.

Known issues
    None as of 8/30/2021

Author, contacts, and additional information:
    Author: 
        Grant Haynes, grant.haynes@noaa.gov
    Other contacts: 
        Dan Gillins, daniel.gillins@noaa.gov 
    GVX information page:
        https://geodesy.noaa.gov/data/formats/GVX/index.shtml

License:
    Software code created by U.S. Government employees is not subject to copyright in the United States (17 U.S.C.
    §105). The United States/Department of Commerce reserve all rights to seek and obtain copyright protection in
    countries other than the United States for Software authored in its entirety by the Department of Commerce. To
    this end, the Department of Commerce hereby grants to Recipient a royalty-free, nonexclusive license to use,
    copy, and create derivative works of the Software outside of the United States.

Disclaimer:
    This repository is a scientific product and is not official communication of the National Oceanic and
    Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is
    provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of
    Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed
    by all applicable Federal law. Any reference to specific commercial products, processes, or services by service
    mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or
    favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a
    DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by
    DOC or the United States Government.